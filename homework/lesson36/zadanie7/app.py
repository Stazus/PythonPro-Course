import boto3
from botocore.exceptions import ClientError


REGION = "eu-central-1"
TARGET_GROUP_NAME = "lesson36-target-group"
PORT = 8000
HEALTH_CHECK_PATH = "/health"
HEALTH_CHECK_INTERVAL = 30


def get_default_vpc_id():
    ec2 = boto3.client("ec2", region_name=REGION)

    response = ec2.describe_vpcs(
        Filters=[
            {
                "Name": "is-default",
                "Values": ["true"],
            }
        ]
    )

    vpcs = response["Vpcs"]

    if not vpcs:
        raise RuntimeError("Nie znaleziono domyślnego VPC.")

    return vpcs[0]["VpcId"]


def create_target_group():
    try:
        vpc_id = get_default_vpc_id()

        elbv2 = boto3.client("elbv2", region_name=REGION)

        response = elbv2.create_target_group(
            Name=TARGET_GROUP_NAME,
            Protocol="HTTP",
            Port=PORT,
            VpcId=vpc_id,
            TargetType="instance",
            HealthCheckProtocol="HTTP",
            HealthCheckPort=str(PORT),
            HealthCheckPath=HEALTH_CHECK_PATH,
            HealthCheckIntervalSeconds=HEALTH_CHECK_INTERVAL,
        )

        target_group = response["TargetGroups"][0]

        print("Utworzono Target Group:")
        print(f"Nazwa: {target_group['TargetGroupName']}")
        print(f"ARN: {target_group['TargetGroupArn']}")
        print(f"Protokół: {target_group['Protocol']}")
        print(f"Port: {target_group['Port']}")
        print(f"VPC: {target_group['VpcId']}")
        print(f"Health check: {HEALTH_CHECK_PATH}")
        print(f"Interwał health check: {HEALTH_CHECK_INTERVAL} sekund")

    except ClientError as error:
        print(f"Błąd podczas tworzenia Target Group: {error}")
    except RuntimeError as error:
        print(f"Błąd: {error}")


if __name__ == "__main__":
    create_target_group()
