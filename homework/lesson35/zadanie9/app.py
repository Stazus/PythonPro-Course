import logging

import boto3
from botocore.exceptions import BotoCoreError, ClientError


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def auto_stop_ec2_instances(region):
    ec2 = boto3.client("ec2", region_name=region)

    try:
        response = ec2.describe_instances(
            Filters=[
                {
                    "Name": "instance-state-name",
                    "Values": ["running"],
                }
            ]
        )

        running_instances = []

        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                running_instances.append(instance)

        if not running_instances:
            logging.info("Brak uruchomionych instancji EC2.")
            return

        for instance in running_instances:
            instance_id = instance["InstanceId"]
            tags = instance.get("Tags", [])

            auto_stop = False

            for tag in tags:
                if tag["Key"] == "AutoStop" and tag["Value"].lower() == "true":
                    auto_stop = True
                    break

            if auto_stop:
                logging.info(
                    "Zatrzymywanie instancji %s z tagiem AutoStop=true.",
                    instance_id,
                )

                ec2.stop_instances(InstanceIds=[instance_id])

                logging.info("Instancja %s została zatrzymana.", instance_id)
            else:
                logging.info(
                    "Instancja %s pozostaje uruchomiona - brak AutoStop=true.",
                    instance_id,
                )

    except (BotoCoreError, ClientError) as error:
        logging.error("Błąd AWS: %s", error)


if __name__ == "__main__":
    auto_stop_ec2_instances("eu-central-1")
