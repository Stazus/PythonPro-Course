import os

import boto3
from botocore.exceptions import BotoCoreError, ClientError


REGION = "eu-central-1"
DB_IDENTIFIER = "lesson36-postgres-db"
SNAPSHOT_IDENTIFIER = "lesson36-postgres-snapshot"


def create_rds_instance():
    password = os.environ.get("RDS_MASTER_PASSWORD")

    if not password:
        print("Brak zmiennej środowiskowej RDS_MASTER_PASSWORD.")
        return False

    rds = boto3.client("rds", region_name=REGION)

    try:
        rds.create_db_instance(
            DBInstanceIdentifier=DB_IDENTIFIER,
            DBInstanceClass="db.t3.micro",
            Engine="postgres",
            MasterUsername="postgresadmin",
            MasterUserPassword=password,
            AllocatedStorage=20,
            StorageType="gp3",
            PubliclyAccessible=False,
            BackupRetentionPeriod=3,
            MultiAZ=False,
        )

        print(f"Tworzenie instancji RDS: {DB_IDENTIFIER}")

        waiter = rds.get_waiter("db_instance_available")
        waiter.wait(DBInstanceIdentifier=DB_IDENTIFIER)

        print("Instancja RDS jest dostępna.")
        return True

    except (BotoCoreError, ClientError) as error:
        print(f"Błąd podczas tworzenia RDS: {error}")
        return False


def create_snapshot():
    rds = boto3.client("rds", region_name=REGION)

    try:
        response = rds.create_db_snapshot(
            DBSnapshotIdentifier=SNAPSHOT_IDENTIFIER,
            DBInstanceIdentifier=DB_IDENTIFIER,
        )

        print(
            "Utworzono manualny snapshot: "
            f"{response['DBSnapshot']['DBSnapshotIdentifier']}"
        )

    except (BotoCoreError, ClientError) as error:
        print(f"Błąd podczas tworzenia snapshotu: {error}")


def main():
    if create_rds_instance():
        create_snapshot()


if __name__ == "__main__":
    main()
