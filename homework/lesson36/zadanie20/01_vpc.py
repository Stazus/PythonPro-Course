import boto3

REGION = "eu-central-1"
VPC_CIDR = "10.20.0.0/16"

ec2 = boto3.client("ec2", region_name=REGION)

# 1. VPC
vpc = ec2.create_vpc(CidrBlock=VPC_CIDR)
vpc_id = vpc["Vpc"]["VpcId"]

ec2.create_tags(
    Resources=[vpc_id],
    Tags=[{"Key": "Name", "Value": "Lesson20-VPC"}],
)

ec2.modify_vpc_attribute(
    VpcId=vpc_id,
    EnableDnsSupport={"Value": True},
)

ec2.modify_vpc_attribute(
    VpcId=vpc_id,
    EnableDnsHostnames={"Value": True},
)

print(f"VPC: {vpc_id}")

# 2. Internet Gateway
igw = ec2.create_internet_gateway()
igw_id = igw["InternetGateway"]["InternetGatewayId"]

ec2.create_tags(
    Resources=[igw_id],
    Tags=[{"Key": "Name", "Value": "Lesson20-IGW"}],
)

ec2.attach_internet_gateway(
    InternetGatewayId=igw_id,
    VpcId=vpc_id,
)

print(f"Internet Gateway: {igw_id}")

# 3. Subnety
subnets = [
    ("Lesson20-Public-1A", "10.20.1.0/24", "eu-central-1a", True),
    ("Lesson20-Public-1B", "10.20.2.0/24", "eu-central-1b", True),
    ("Lesson20-Public-1C", "10.20.3.0/24", "eu-central-1c", True),
    ("Lesson20-Private-1A", "10.20.11.0/24", "eu-central-1a", False),
    ("Lesson20-Private-1B", "10.20.12.0/24", "eu-central-1b", False),
    ("Lesson20-Private-1C", "10.20.13.0/24", "eu-central-1c", False),
]

for name, cidr, az, public in subnets:
    subnet = ec2.create_subnet(
        VpcId=vpc_id,
        CidrBlock=cidr,
        AvailabilityZone=az,
    )

    subnet_id = subnet["Subnet"]["SubnetId"]

    ec2.create_tags(
        Resources=[subnet_id],
        Tags=[
            {"Key": "Name", "Value": name},
            {"Key": "Type", "Value": "Public" if public else "Private"},
        ],
    )

    if public:
        ec2.modify_subnet_attribute(
            SubnetId=subnet_id,
            MapPublicIpOnLaunch={"Value": True},
        )

    print(f"{name}: {subnet_id} ({cidr}, {az})")

print()
print("VPC i 6 subnetów utworzone.")
print(f"VPC_ID={vpc_id}")
print(f"IGW_ID={igw_id}")
