import os
import time
from collections import Counter

import boto3
import requests
from botocore.exceptions import BotoCoreError, ClientError


REGION = "eu-central-1"

DOMAIN_NAME = os.environ.get(
    "ROUTE53_DOMAIN",
    "test.yourdomain.com",
)

HOSTED_ZONE_ID = os.environ.get(
    "ROUTE53_HOSTED_ZONE_ID",
)

PRIMARY_ENDPOINT = os.environ.get(
    "PRIMARY_ENDPOINT",
)

CANARY_ENDPOINT = os.environ.get(
    "CANARY_ENDPOINT",
)

REQUEST_COUNT = 100


def create_weighted_records():
    if not HOSTED_ZONE_ID:
        print(
            "Brak zmiennej ROUTE53_HOSTED_ZONE_ID."
        )
        return False

    if not PRIMARY_ENDPOINT or not CANARY_ENDPOINT:
        print(
            "Brak PRIMARY_ENDPOINT lub CANARY_ENDPOINT."
        )
        return False

    route53 = boto3.client(
        "route53",
        region_name=REGION,
    )

    try:
        response = route53.change_resource_record_sets(
            HostedZoneId=HOSTED_ZONE_ID,
            ChangeBatch={
                "Changes": [
                    {
                        "Action": "UPSERT",
                        "ResourceRecordSet": {
                            "Name": DOMAIN_NAME,
                            "Type": "A",
                            "SetIdentifier": "primary",
                            "Weight": 80,
                            "TTL": 30,
                            "ResourceRecords": [
                                {
                                    "Value": PRIMARY_ENDPOINT,
                                }
                            ],
                        },
                    },
                    {
                        "Action": "UPSERT",
                        "ResourceRecordSet": {
                            "Name": DOMAIN_NAME,
                            "Type": "A",
                            "SetIdentifier": "canary",
                            "Weight": 20,
                            "TTL": 30,
                            "ResourceRecords": [
                                {
                                    "Value": CANARY_ENDPOINT,
                                }
                            ],
                        },
                    },
                ]
            },
        )

        change_id = response["ChangeInfo"]["Id"]

        print("Utworzono weighted routing w Route53.")
        print(f"Domain: {DOMAIN_NAME}")
        print("Primary weight: 80")
        print("Canary weight: 20")
        print(f"Change ID: {change_id}")

        return True

    except (BotoCoreError, ClientError) as error:
        print(
            f"Błąd podczas tworzenia rekordów Route53: {error}"
        )
        return False


def test_weighted_routing():
    if not DOMAIN_NAME:
        print("Brak nazwy domeny.")
        return

    print()
    print(
        f"Wysyłanie {REQUEST_COUNT} requestów "
        f"do https://{DOMAIN_NAME}"
    )
    print()

    results = Counter()

    for number in range(1, REQUEST_COUNT + 1):
        try:
            response = requests.get(
                f"https://{DOMAIN_NAME}",
                timeout=5,
            )

            server = response.headers.get(
                "X-Endpoint",
                response.text.strip(),
            )

            if "canary" in server.lower():
                results["canary"] += 1
            else:
                results["primary"] += 1

            print(
                f"Request {number:3}: "
                f"{response.status_code} -> {server}"
            )

        except requests.RequestException as error:
            results["error"] += 1

            print(
                f"Request {number:3}: ERROR -> {error}"
            )

        time.sleep(0.1)

    print()
    print("=== WYNIK ===")

    primary = results["primary"]
    canary = results["canary"]
    errors = results["error"]

    print(f"Primary: {primary}")
    print(f"Canary:  {canary}")
    print(f"Błędy:   {errors}")

    successful = primary + canary

    if successful:
        primary_percent = primary / successful * 100
        canary_percent = canary / successful * 100

        print()
        print(
            f"Primary: {primary_percent:.1f}%"
        )
        print(
            f"Canary:  {canary_percent:.1f}%"
        )

        print()
        print(
            "Oczekiwany wynik: około 80% / 20%"
        )


def main():
    if not HOSTED_ZONE_ID:
        print(
            "Nie można utworzyć weighted routing."
        )
        print(
            "Brak ROUTE53_HOSTED_ZONE_ID."
        )
        print(
            "Skrypt zakończył działanie bez "
            "tworzenia zasobów AWS."
        )
        return

    if not PRIMARY_ENDPOINT or not CANARY_ENDPOINT:
        print(
            "Brak endpointów primary/canary."
        )
        return

    if create_weighted_records():
        test_weighted_routing()


if __name__ == "__main__":
    main()
