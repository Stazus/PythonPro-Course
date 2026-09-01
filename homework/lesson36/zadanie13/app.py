import boto3
from botocore.exceptions import ClientError
import base64
import time


REGION = "eu-central-1"
AMI_ID = "ami-0f2f6d6f49dbe9fd1"
INSTANCE_TYPE = "t3.micro"

VPC_ID = "vpc-069b5dde967f7b442"

SUBNETS = [
    "subnet-03472013c9113da38",  # eu-central-1a
    "subnet-0757d24b69e768569",  # eu-central-1b
]

SECURITY_GROUP_NAME = "Lesson13ZeroDowntimeSG"
LAUNCH_TEMPLATE_NAME = "Lesson13ZeroDowntimeLT"


ec2 = boto3.client("ec2", region_name=REGION)


def get_or_create_security_group():
    response = ec2.describe_security_groups(
        Filters=[
            {"Name": "group-name", "Values": [SECURITY_GROUP_NAME]},
            {"Name": "vpc-id", "Values": [VPC_ID]},
        ]
    )

    if response["SecurityGroups"]:
        sg_id = response["SecurityGroups"][0]["GroupId"]
        print(f"Security Group już istnieje: {sg_id}")
        return sg_id

    response = ec2.create_security_group(
        GroupName=SECURITY_GROUP_NAME,
        Description="Security Group for Lesson 13 Zero Downtime",
        VpcId=VPC_ID,
    )

    sg_id = response["GroupId"]

    ec2.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[
            {
                "IpProtocol": "tcp",
                "FromPort": 80,
                "ToPort": 80,
                "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
            }
        ],
    )

    print(f"Utworzono Security Group: {sg_id}")
    return sg_id


def get_or_create_launch_template(sg_id):
    try:
        response = ec2.describe_launch_templates(
            LaunchTemplateNames=[LAUNCH_TEMPLATE_NAME]
        )

        if response["LaunchTemplates"]:
            template_id = response["LaunchTemplates"][0]["LaunchTemplateId"]
            print(f"Launch Template już istnieje: {template_id}")
            return template_id

    except ClientError as error:
        if error.response["Error"]["Code"] != "InvalidLaunchTemplateName.NotFoundException":
            raise

    user_data = """#!/bin/bash

dnf update -y
dnf install -y nginx

systemctl enable nginx
systemctl start nginx

cat > /usr/share/nginx/html/index.html <<'EOF'
Lesson 13 - Zero Downtime Deployment
EOF

cat > /usr/share/nginx/html/health <<'EOF'
OK
EOF
"""

    encoded_user_data = base64.b64encode(
        user_data.encode("utf-8")
    ).decode("utf-8")

    response = ec2.create_launch_template(
        LaunchTemplateName=LAUNCH_TEMPLATE_NAME,
        LaunchTemplateData={
            "ImageId": AMI_ID,
            "InstanceType": INSTANCE_TYPE,
            "SecurityGroupIds": [sg_id],
            "UserData": encoded_user_data,
        },
    )

    template_id = response["LaunchTemplate"]["LaunchTemplateId"]

    print(f"Utworzono Launch Template: {template_id}")
    return template_id

def main():
    print("=== LESSON 13 - ZERO DOWNTIME DEPLOYMENT ===")
    print(f"Region: {REGION}")
    print(f"VPC: {VPC_ID}")
    print(f"AMI: {AMI_ID}")

    sg_id = get_or_create_security_group()

    launch_template_id = get_or_create_launch_template(sg_id)

    print()
    print("=== GOTOWE ===")
    print(f"Security Group: {sg_id}")
    print(f"Launch Template: {launch_template_id}")
    print(f"Subnety: {', '.join(SUBNETS)}")


if __name__ == "__main__":
    main()
