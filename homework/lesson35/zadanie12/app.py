from datetime import datetime, timezone

import boto3
from botocore.exceptions import BotoCoreError, ClientError


class AWSCostCalculator:
    PRICES = {
        "t3.micro": 0.01,
        "t3.small": 0.02,
        "t3.medium": 0.04,
    }

    def __init__(self, region):
        self.ec2 = boto3.client("ec2", region_name=region)

    def get_instances(self):
        response = self.ec2.describe_instances()
        instances = []

        for reservation in response["Reservations"]:
            instances.extend(reservation["Instances"])

        return instances

    def calculate_instance_cost(self, instance):
        instance_type = instance["InstanceType"]
        price_per_hour = self.PRICES.get(instance_type, 0)

        launch_time = instance["LaunchTime"]
        now = datetime.now(timezone.utc)

        running_hours = (now - launch_time).total_seconds() / 3600
        cost = running_hours * price_per_hour

        return {
            "instance_id": instance["InstanceId"],
            "instance_type": instance_type,
            "running_hours": running_hours,
            "cost": cost,
        }

    def generate_report(self):
        try:
            instances = self.get_instances()

            if not instances:
                print("Brak instancji EC2.")
                return []

            report = []

            for instance in instances:
                result = self.calculate_instance_cost(instance)
                report.append(result)

                print(
                    f"ID: {result['instance_id']}, "
                    f"typ: {result['instance_type']}, "
                    f"czas: {result['running_hours']:.2f} h, "
                    f"koszt: ${result['cost']:.2f}"
                )

            return report

        except (BotoCoreError, ClientError) as error:
            print(f"Błąd AWS: {error}")
            return []


if __name__ == "__main__":
    calculator = AWSCostCalculator("eu-central-1")
    calculator.generate_report()
