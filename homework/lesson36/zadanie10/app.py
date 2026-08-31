import os

import boto3
from botocore.exceptions import BotoCoreError, ClientError


REGION = "eu-central-1"
ALB_NAME = "lesson36-alb"
TARGET_GROUP_NAME = "lesson36-target-group"
TARGET_PORT = 8000
LISTENER_PORT = 80


def get_instance_ids():
    value = os.environ.get("EC2_INSTANCE_IDS", "")

    instance_ids = [
        instance_id.strip()
        for instance_id in value.split(",")
        if instance_id.strip()
    ]

    if len(instance_ids) != 2:
        print(
            "Brak dwóch instancji EC2. "
            "Ustaw EC2_INSTANCE_IDS w formacie: "
            "i-xxxxxxxx,i-yyyyyyyy"
        )
        return None

    return instance_ids


def get_default_vpc_and_subnets(ec2):
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
        print("Nie znaleziono domyślnego VPC.")
        return None, None

    vpc_id = vpcs[0]["VpcId"]

    subnets_response = ec2.describe_subnets(
        Filters=[
            {
                "Name": "vpc-id",
                "Values": [vpc_id],
            }
        ]
    )

    subnets = subnets_response["Subnets"]

    if len(subnets) < 2:
        print("VPC nie posiada co najmniej dwóch subnetów.")
        return None, None

    subnets = sorted(
        subnets,
        key=lambda subnet: subnet["AvailabilityZone"],
    )

    selected_subnets = []
    availability_zones = set()

    for subnet in subnets:
        az = subnet["AvailabilityZone"]

        if az not in availability_zones:
            selected_subnets.append(subnet["SubnetId"])
            availability_zones.add(az)

        if len(selected_subnets) == 2:
            break

    if len(selected_subnets) < 2:
        print("Nie udało się znaleźć subnetów w dwóch AZ.")
        return None, None

    return vpc_id, selected_subnets


def create_security_group(ec2, vpc_id):
    try:
        response = ec2.create_security_group(
            GroupName="lesson36-alb-sg",
            Description="Security Group for Lesson 36 ALB",
            VpcId=vpc_id,
        )

        security_group_id = response["GroupId"]

        ec2.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    "IpProtocol": "tcp",
                    "FromPort": LISTENER_PORT,
                    "ToPort": LISTENER_PORT,
                    "IpRanges": [
                        {
                            "CidrIp": "0.0.0.0/0",
                            "Description": "HTTP traffic",
                        }
                    ],
                }
            ],
        )

        print(f"Utworzono Security Group: {security_group_id}")

        return security_group_id

    except (BotoCoreError, ClientError) as error:
        print(f"Błąd podczas tworzenia Security Group: {error}")
        return None


def create_target_group(elbv2, vpc_id):
    try:
        response = elbv2.create_target_group(
            Name=TARGET_GROUP_NAME,
            Protocol="HTTP",
            Port=TARGET_PORT,
            VpcId=vpc_id,
            TargetType="instance",
            HealthCheckProtocol="HTTP",
            HealthCheckPort=str(TARGET_PORT),
            HealthCheckPath="/health",
            HealthCheckIntervalSeconds=30,
            HealthCheckTimeoutSeconds=5,
            HealthyThresholdCount=2,
            UnhealthyThresholdCount=2,
            Matcher={
                "HttpCode": "200",
            },
        )

        target_group_arn = response["TargetGroups"][0][
            "TargetGroupArn"
        ]

        print(f"Utworzono Target Group: {TARGET_GROUP_NAME}")
        print(f"Target Group ARN: {target_group_arn}")

        return target_group_arn

    except (BotoCoreError, ClientError) as error:
        print(f"Błąd podczas tworzenia Target Group: {error}")
        return None


def create_load_balancer(
    elbv2,
    security_group_id,
    subnet_ids,
):
    try:
        response = elbv2.create_load_balancer(
            Name=ALB_NAME,
            Subnets=subnet_ids,
            SecurityGroups=[security_group_id],
            Scheme="internet-facing",
            Type="application",
            IpAddressType="ipv4",
        )

        load_balancer = response["LoadBalancers"][0]

        alb_arn = load_balancer["LoadBalancerArn"]
        dns_name = load_balancer["DNSName"]

        print(f"Utworzono ALB: {ALB_NAME}")
        print(f"ALB ARN: {alb_arn}")
        print(f"DNS: {dns_name}")

        return alb_arn, dns_name

    except (BotoCoreError, ClientError) as error:
        print(f"Błąd podczas tworzenia ALB: {error}")
        return None, None


def register_instances(elbv2, target_group_arn, instance_ids):
    try:
        targets = [
            {
                "Id": instance_id,
                "Port": TARGET_PORT,
            }
            for instance_id in instance_ids
        ]

        elbv2.register_targets(
            TargetGroupArn=target_group_arn,
            Targets=targets,
        )

        print("Zarejestrowano instancje EC2:")
        for instance_id in instance_ids:
            print(f" - {instance_id}")

        return True

    except (BotoCoreError, ClientError) as error:
        print(f"Błąd podczas rejestracji instancji: {error}")
        return False


def create_listener(elbv2, alb_arn, target_group_arn):
    try:
        response = elbv2.create_listener(
            LoadBalancerArn=alb_arn,
            Protocol="HTTP",
            Port=LISTENER_PORT,
            DefaultActions=[
                {
                    "Type": "forward",
                    "TargetGroupArn": target_group_arn,
                }
            ],
        )

        listener_arn = response["Listeners"][0]["ListenerArn"]

        print("Utworzono Listener:")
        print(f"Port: {LISTENER_PORT}")
        print(f"Protocol: HTTP")
        print(f"Listener ARN: {listener_arn}")

        return listener_arn

    except (BotoCoreError, ClientError) as error:
        print(f"Błąd podczas tworzenia Listener: {error}")
        return None


def main():
    instance_ids = get_instance_ids()

    if not instance_ids:
        print("Przerwano bez tworzenia zasobów AWS.")
        return

    ec2 = boto3.client(
        "ec2",
        region_name=REGION,
    )

    elbv2 = boto3.client(
        "elbv2",
        region_name=REGION,
    )

    try:
        vpc_id, subnet_ids = get_default_vpc_and_subnets(ec2)

        if not vpc_id:
            return

        print(f"VPC: {vpc_id}")
        print(f"Subnets: {subnet_ids}")

        security_group_id = create_security_group(
            ec2,
            vpc_id,
        )

        if not security_group_id:
            return

        target_group_arn = create_target_group(
            elbv2,
            vpc_id,
        )

        if not target_group_arn:
            return

        alb_arn, dns_name = create_load_balancer(
            elbv2,
            security_group_id,
            subnet_ids,
        )

        if not alb_arn:
            return

        if not register_instances(
            elbv2,
            target_group_arn,
            instance_ids,
        ):
            return

        if not create_listener(
            elbv2,
            alb_arn,
            target_group_arn,
        ):
            return

        print()
        print("=== APPLICATION LOAD BALANCER GOTOWY ===")
        print(f"ALB: {ALB_NAME}")
        print(f"DNS: http://{dns_name}")
        print(f"Target Group: {TARGET_GROUP_NAME}")
        print("Listener: HTTP :80")
        print(f"Instancje: {instance_ids}")
        print("Health check: HTTP :8000/health")
        print()
        print("Test ruchu:")
        print(f"curl http://{dns_name}")

    except (BotoCoreError, ClientError) as error:
        print(f"Błąd AWS: {error}")


if __name__ == "__main__":
    main()
