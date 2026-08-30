import os

import boto3
from botocore.exceptions import ClientError


REGION = "eu-central-1"
RECORD_NAME = "test.yourdomain.com"
RECORD_TYPE = "A"
IP_ADDRESS = "1.2.3.4"
TTL = 300


def create_a_record():
    hosted_zone_id = os.environ.get("ROUTE53_HOSTED_ZONE_ID")

    if not hosted_zone_id:
        print(
            "Nie utworzono rekordu: brak zmiennej "
            "ROUTE53_HOSTED_ZONE_ID."
        )
        print(
            "Konto nie posiada Hosted Zone dla yourdomain.com, "
            "więc rekord nie może zostać utworzony."
        )
        return

    route53 = boto3.client("route53", region_name=REGION)

    try:
        response = route53.change_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            ChangeBatch={
                "Changes": [
                    {
                        "Action": "UPSERT",
                        "ResourceRecordSet": {
                            "Name": RECORD_NAME,
                            "Type": RECORD_TYPE,
                            "TTL": TTL,
                            "ResourceRecords": [
                                {
                                    "Value": IP_ADDRESS
                                }
                            ],
                        },
                    }
                ]
            },
        )

        print("Utworzono rekord Route53:")
        print(f"Nazwa: {RECORD_NAME}")
        print(f"Typ: {RECORD_TYPE}")
        print(f"Adres IP: {IP_ADDRESS}")
        print(f"TTL: {TTL}")
        print(f"Status: {response['ChangeInfo']['Status']}")

    except ClientError as error:
        print(f"Błąd podczas tworzenia rekordu Route53: {error}")


if __name__ == "__main__":
    create_a_record()
