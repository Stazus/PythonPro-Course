import boto3
from botocore.exceptions import ClientError


def list_ec2_instances():
    ec2 = boto3.client("ec2", region_name="eu-central-1")

    try:
        response = ec2.describe_instances()

        instances_found = False

        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                instances_found = True

                instance_id = instance["InstanceId"]
                instance_type = instance["InstanceType"]
                state = instance["State"]["Name"]
                public_ip = instance.get("PublicIpAddress", "brak")

                print(f"ID: {instance_id}")
                print(f"Typ: {instance_type}")
                print(f"Stan: {state}")
                print(f"Publiczny IP: {public_ip}")
                print("-" * 40)

        if not instances_found:
            print("Brak instancji EC2 w regionie eu-central-1.")

    except ClientError as error:
        print(f"Błąd AWS: {error}")


if __name__ == "__main__":
    list_ec2_instances()
