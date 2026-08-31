import boto3
from botocore.exceptions import BotoCoreError, ClientError


REGION = "eu-central-1"
SOURCE_DB_IDENTIFIER = "lesson36-postgres-db"
REPLICA_DB_IDENTIFIER = "lesson36-postgres-replica"


def create_read_replica():
    rds = boto3.client("rds", region_name=REGION)

    try:
        print(
            f"Tworzenie Read Replica dla bazy: "
            f"{SOURCE_DB_IDENTIFIER}"
        )

        response = rds.create_db_instance_read_replica(
            DBInstanceIdentifier=REPLICA_DB_IDENTIFIER,
            SourceDBInstanceIdentifier=SOURCE_DB_IDENTIFIER,
            DBInstanceClass="db.t3.micro",
            PubliclyAccessible=False,
            Tags=[
                {
                    "Key": "Type",
                    "Value": "ReadReplica",
                },
                {
                    "Key": "Environment",
                    "Value": "Development",
                },
            ],
        )

        print(
            f"Utworzono Read Replica: "
            f"{response['DBInstance']['DBInstanceIdentifier']}"
        )

        print(
            f"Baza źródłowa: "
            f"{SOURCE_DB_IDENTIFIER}"
        )

        print(
            "Read Replica będzie replikować dane "
            "asynchronicznie z bazy źródłowej."
        )

        return True

    except (BotoCoreError, ClientError) as error:
        print(f"Błąd podczas tworzenia Read Replica: {error}")
        return False


def get_replica_endpoint():
    rds = boto3.client("rds", region_name=REGION)

    try:
        print("Oczekiwanie na dostępność Read Replica...")

        waiter = rds.get_waiter("db_instance_available")
        waiter.wait(
            DBInstanceIdentifier=REPLICA_DB_IDENTIFIER
        )

        response = rds.describe_db_instances(
            DBInstanceIdentifier=REPLICA_DB_IDENTIFIER
        )

        db_instance = response["DBInstances"][0]
        endpoint = db_instance["Endpoint"]["Address"]
        port = db_instance["Endpoint"]["Port"]

        print(f"Read Replica jest dostępna.")
        print(f"Endpoint: {endpoint}")
        print(f"Port: {port}")

    except (BotoCoreError, ClientError) as error:
        print(
            f"Nie można pobrać endpointu Read Replica: "
            f"{error}"
        )


def main():
    if create_read_replica():
        get_replica_endpoint()


if __name__ == "__main__":
    main()
