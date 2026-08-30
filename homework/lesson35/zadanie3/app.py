import boto3
from botocore.exceptions import BotoCoreError, ClientError


def list_aws_regions():
    ec2 = boto3.client("ec2", region_name="eu-central-1")

    try:
        response = ec2.describe_regions(AllRegions=True)

        print("Regiony AWS dla usługi EC2:\n")

        for region in response["Regions"]:
            print(
                f"{region['RegionName']} - "
                f"{region['Endpoint']}"
            )

    except (BotoCoreError, ClientError) as error:
        print(f"Błąd AWS: {error}")


if __name__ == "__main__":
    list_aws_regions()
