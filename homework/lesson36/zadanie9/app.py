import os
import socket
import time

import boto3
from botocore.exceptions import BotoCoreError, ClientError


REGION = "eu-central-1"
DB_IDENTIFIER = "lesson36-multiaz-postgres"


def create_rds_instance():
    password = os.environ.get("RDS_MASTER_PASSWORD")

    if not password:
        print("Brak zmiennej środowiskowej RDS_MASTER_PASSWORD.")
        return False

    rds = boto3.client("rds", region_name=REGION)

    try:
        print(f"Tworzenie Multi-AZ RDS: {DB_IDENTIFIER}")

        rds.create_db_instance(
            DBInstanceIdentifier=DB_IDENTIFIER,
            DBInstanceClass="db.t3.micro",
            Engine="postgres",
            MasterUsername="postgresadmin",
            MasterUserPassword=password,
            AllocatedStorage=20,
            StorageType="gp3",
            PubliclyAccessible=False,
            MultiAZ=True,
        )

        print("Czekam na dostępność instancji...")

        waiter = rds.get_waiter("db_instance_available")
        waiter.wait(DBInstanceIdentifier=DB_IDENTIFIER)

        print("Instancja Multi-AZ jest dostępna.")
        return True

    except (BotoCoreError, ClientError) as error:
        print(f"Błąd podczas tworzenia RDS: {error}")
        return False


def get_db_endpoint():
    rds = boto3.client("rds", region_name=REGION)

    response = rds.describe_db_instances(
        DBInstanceIdentifier=DB_IDENTIFIER
    )

    db_instance = response["DBInstances"][0]
    endpoint = db_instance["Endpoint"]["Address"]
    port = db_instance["Endpoint"]["Port"]

    return endpoint, port


def test_connection(endpoint, port):
    print(f"Test połączenia z {endpoint}:{port}")

    start = time.monotonic()

    try:
        with socket.create_connection(
            (endpoint, port),
            timeout=5,
        ):
            elapsed = time.monotonic() - start
            print(f"Połączenie OK ({elapsed:.3f} s)")
            return True

    except OSError:
        elapsed = time.monotonic() - start
        print(f"Brak połączenia ({elapsed:.3f} s)")
        return False


def perform_failover():
    rds = boto3.client("rds", region_name=REGION)

    try:
        print("Rozpoczynam failover...")

        rds.reboot_db_instance(
            DBInstanceIdentifier=DB_IDENTIFIER,
            ForceFailover=True,
        )

        print("Failover został uruchomiony.")
        return True

    except (BotoCoreError, ClientError) as error:
        print(f"Błąd podczas failover: {error}")
        return False


def measure_downtime(endpoint, port):
    print("Pomiar czasu niedostępności...")

    downtime_start = time.monotonic()

    while True:
        if test_connection(endpoint, port):
            downtime = time.monotonic() - downtime_start

            print(
                f"Szacowany czas niedostępności: "
                f"{downtime:.3f} s"
            )

            return downtime

        time.sleep(2)


def main():
    if not create_rds_instance():
        return

    endpoint, port = get_db_endpoint()

    print(f"Endpoint: {endpoint}")
    print(f"Port: {port}")

    print()
    print("=== TEST PRZED FAILOVER ===")
    test_connection(endpoint, port)

    print()
    print("=== FAILOVER ===")

    if not perform_failover():
        return

    print()
    print("=== POMIAR DOWNTIME ===")

    downtime = measure_downtime(endpoint, port)

    print()
    print("=== RAPORT ===")
    print(f"RDS: {DB_IDENTIFIER}")
    print("Tryb: Multi-AZ")
    print(f"Downtime podczas failover: {downtime:.3f} s")


if __name__ == "__main__":
    main()
