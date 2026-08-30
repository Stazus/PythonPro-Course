import asyncio
import csv
from datetime import datetime
from pathlib import Path

import boto3
import requests
from botocore.exceptions import BotoCoreError, ClientError


REGION = "eu-central-1"
HEALTHCHECK_URL = "https://example.com"
CSV_FILE = Path("zadanie15/metrics.csv")


def check_ec2_instances():
    ec2 = boto3.client("ec2", region_name=REGION)
    results = []

    try:
        response = ec2.describe_instances()

        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                results.append(
                    {
                        "resource": instance["InstanceId"],
                        "type": "EC2",
                        "status": instance["State"]["Name"],
                    }
                )

    except (BotoCoreError, ClientError) as error:
        print(f"ALERT: błąd EC2: {error}")

    return results


def check_ebs_volumes():
    ec2 = boto3.client("ec2", region_name=REGION)
    results = []

    try:
        response = ec2.describe_volumes()

        for volume in response["Volumes"]:
            results.append(
                {
                    "resource": volume["VolumeId"],
                    "type": "EBS",
                    "status": volume["State"],
                }
            )

    except (BotoCoreError, ClientError) as error:
        print(f"ALERT: błąd EBS: {error}")

    return results


def check_application():
    try:
        response = requests.get(HEALTHCHECK_URL, timeout=10)

        status = "OK" if response.status_code == 200 else "ERROR"

        if status == "ERROR":
            print(
                f"ALERT: aplikacja zwróciła HTTP "
                f"{response.status_code}"
            )

        return {
            "resource": HEALTHCHECK_URL,
            "type": "HTTP",
            "status": status,
        }

    except requests.RequestException as error:
        print(f"ALERT: health check nieudany: {error}")

        return {
            "resource": HEALTHCHECK_URL,
            "type": "HTTP",
            "status": "ERROR",
        }


def save_metrics(metrics):
    file_exists = CSV_FILE.exists()

    with CSV_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "timestamp",
                "resource",
                "type",
                "status",
            ],
        )

        if not file_exists:
            writer.writeheader()

        timestamp = datetime.now().isoformat()

        for metric in metrics:
            writer.writerow(
                {
                    "timestamp": timestamp,
                    "resource": metric["resource"],
                    "type": metric["type"],
                    "status": metric["status"],
                }
            )


def run_monitoring():
    print("Uruchamiam monitoring infrastruktury...")

    metrics = []
    metrics.extend(check_ec2_instances())
    metrics.extend(check_ebs_volumes())
    metrics.append(check_application())

    save_metrics(metrics)

    print("Monitoring zakończony. Metryki zapisano do CSV.")


async def main():
    while True:
        run_monitoring()
        await asyncio.sleep(300)


if __name__ == "__main__":
    asyncio.run(main())
