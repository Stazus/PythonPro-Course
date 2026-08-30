import boto3
from botocore.exceptions import BotoCoreError, ClientError


REGION = "eu-central-1"
SECURITY_GROUP_NAME = "lesson36-web-sg"
SECURITY_GROUP_DESCRIPTION = "Security Group for HTTP and HTTPS"


def create_security_group():
    ec2 = boto3.client("ec2", region_name=REGION)

    try:
        response = ec2.create_security_group(
            GroupName=SECURITY_GROUP_NAME,
            Description=SECURITY_GROUP_DESCRIPTION,
        )

        group_id = response["GroupId"]

        print(f"Utworzono Security Group: {group_id}")

        ec2.authorize_security_group_ingress(
            GroupId=group_id,
            IpPermissions=[
                {
                    "IpProtocol": "tcp",
                    "FromPort": 80,
                    "ToPort": 80,
                    "IpRanges": [
                        {
                            "CidrIp": "0.0.0.0/0",
                            "Description": "HTTP from internet",
                        }
                    ],
                },
                {
                    "IpProtocol": "tcp",
                    "FromPort": 443,
                    "ToPort": 443,
                    "IpRanges": [
                        {
                            "CidrIp": "0.0.0.0/0",
                            "Description": "HTTPS from internet",
                        }
                    ],
                },
            ],
        )

        print("Dodano reguły HTTP (80) i HTTPS (443).")
        print("Pozostałe porty nie zostały otwarte.")

        return group_id

    except (BotoCoreError, ClientError) as error:
        print(f"Błąd podczas tworzenia Security Group: {error}")
        return None


if __name__ == "__main__":
    create_security_group()
