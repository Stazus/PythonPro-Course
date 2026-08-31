import logging
import os
import smtplib
from datetime import datetime, timedelta
from email.message import EmailMessage

import boto3
from botocore.exceptions import BotoCoreError, ClientError


REGION = "eu-central-1"

DB_IDENTIFIER = os.environ.get(
    "RDS_DB_IDENTIFIER",
    "lesson36-postgres-db",
)

LOG_FILE = os.environ.get(
    "BACKUP_LOG_FILE",
    "zadanie12/backup.log",
)

RETENTION_DAYS = 7


logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def send_email(subject, body):
    smtp_host = os.environ.get("SMTP_HOST")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_password = os.environ.get("SMTP_PASSWORD")
    email_to = os.environ.get("EMAIL_TO")

    if not all(
        [
            smtp_host,
            smtp_user,
            smtp_password,
            email_to,
        ]
    ):
        logging.warning(
            "Brak konfiguracji SMTP. "
            "Email nie został wysłany."
        )
        return

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = smtp_user
    message["To"] = email_to
    message.set_content(body)

    try:
        with smtplib.SMTP(
            smtp_host,
            smtp_port,
            timeout=10,
        ) as server:
            server.starttls()
            server.login(
                smtp_user,
                smtp_password,
            )
            server.send_message(message)

        logging.info("Wysłano powiadomienie email.")

    except Exception as error:
        logging.error(
            f"Błąd podczas wysyłania emaila: {error}"
        )


def create_snapshot(rds):
    timestamp = datetime.now().strftime(
        "%Y%m%d-%H%M%S"
    )

    snapshot_identifier = (
        f"{DB_IDENTIFIER}-automated-{timestamp}"
    )

    try:
        response = rds.create_db_snapshot(
            DBSnapshotIdentifier=snapshot_identifier,
            DBInstanceIdentifier=DB_IDENTIFIER,
        )

        snapshot = response["DBSnapshot"]

        logging.info(
            "Utworzono snapshot: %s",
            snapshot["DBSnapshotIdentifier"],
        )

        return snapshot["DBSnapshotIdentifier"]

    except (BotoCoreError, ClientError) as error:
        logging.error(
            f"Błąd podczas tworzenia snapshotu: {error}"
        )
        return None


def delete_old_snapshots(rds):
    cutoff_date = datetime.now(
    ) - timedelta(days=RETENTION_DAYS)

    deleted = 0

    try:
        paginator = rds.get_paginator(
            "describe_db_snapshots"
        )

        pages = paginator.paginate(
            DBInstanceIdentifier=DB_IDENTIFIER,
            SnapshotType="manual",
        )

        for page in pages:
            for snapshot in page["DBSnapshots"]:
                snapshot_id = snapshot[
                    "DBSnapshotIdentifier"
                ]

                created_at = snapshot[
                    "SnapshotCreateTime"
                ].replace(tzinfo=None)

                if created_at < cutoff_date:
                    try:
                        rds.delete_db_snapshot(
                            DBSnapshotIdentifier=snapshot_id
                        )

                        logging.info(
                            "Usunięto stary snapshot: %s",
                            snapshot_id,
                        )

                        deleted += 1

                    except (
                        BotoCoreError,
                        ClientError,
                    ) as error:
                        logging.error(
                            "Błąd podczas usuwania "
                            "snapshotu %s: %s",
                            snapshot_id,
                            error,
                        )

        logging.info(
            "Usunięto %d snapshotów starszych niż %d dni.",
            deleted,
            RETENTION_DAYS,
        )

        return deleted

    except (BotoCoreError, ClientError) as error:
        logging.error(
            f"Błąd podczas pobierania snapshotów: {error}"
        )
        return 0


def check_rds_instance(rds):
    try:
        response = rds.describe_db_instances(
            DBInstanceIdentifier=DB_IDENTIFIER
        )

        instance = response["DBInstances"][0]

        status = instance["DBInstanceStatus"]

        logging.info(
            "Status RDS %s: %s",
            DB_IDENTIFIER,
            status,
        )

        return status == "available"

    except rds.exceptions.DBInstanceNotFoundFault:
        logging.warning(
            "Nie znaleziono instancji RDS: %s",
            DB_IDENTIFIER,
        )
        return False

    except (BotoCoreError, ClientError) as error:
        logging.error(
            f"Błąd podczas sprawdzania RDS: {error}"
        )
        return False


def main():
    logging.info(
        "=== START AUTOMATYCZNEGO BACKUPU RDS ==="
    )

    rds = boto3.client(
        "rds",
        region_name=REGION,
    )

    if not check_rds_instance(rds):
        message = (
            f"Backup nie został wykonany.\n"
            f"Nie znaleziono dostępnej instancji RDS: "
            f"{DB_IDENTIFIER}"
        )

        logging.warning(message)

        send_email(
            "RDS backup - brak instancji",
            message,
        )

        return

    snapshot_id = create_snapshot(rds)

    deleted = delete_old_snapshots(rds)

    if snapshot_id:
        message = (
            "Automatyczny backup RDS zakończony.\n\n"
            f"Instancja: {DB_IDENTIFIER}\n"
            f"Utworzony snapshot: {snapshot_id}\n"
            f"Usunięte stare snapshoty: {deleted}\n"
            f"Retencja: {RETENTION_DAYS} dni"
        )

        logging.info(
            "Backup zakończony pomyślnie."
        )

        send_email(
            "RDS backup - zakończony",
            message,
        )

    else:
        message = (
            f"Backup RDS zakończony błędem.\n"
            f"Instancja: {DB_IDENTIFIER}"
        )

        logging.error(
            "Backup zakończony bez utworzenia snapshotu."
        )

        send_email(
            "RDS backup - błąd",
            message,
        )

    logging.info(
        "=== KONIEC AUTOMATYCZNEGO BACKUPU RDS ==="
    )


if __name__ == "__main__":
    main()
