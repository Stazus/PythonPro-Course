from datetime import datetime, timedelta, timezone
from pathlib import Path

import boto3
from botocore.exceptions import BotoCoreError, ClientError


BUCKET_NAME = "python-course-lesson35-stanislaw"
BACKUP_PREFIX = "backups/"
SOURCE_DIRECTORY = Path("zadanie1")


def upload_backup_to_s3():
    s3 = boto3.client("s3", region_name="eu-central-1")

    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        for file_path in SOURCE_DIRECTORY.rglob("*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(SOURCE_DIRECTORY)
                s3_key = f"{BACKUP_PREFIX}backup_{timestamp}/{relative_path}"

                s3.upload_file(
                    str(file_path),
                    BUCKET_NAME,
                    s3_key,
                )

                print(f"Wysłano: {file_path} -> s3://{BUCKET_NAME}/{s3_key}")

    except (BotoCoreError, ClientError) as error:
        print(f"Błąd podczas wysyłania backupu: {error}")


def delete_old_backups():
    s3 = boto3.client("s3", region_name="eu-central-1")
    limit_date = datetime.now(timezone.utc) - timedelta(days=7)

    try:
        response = s3.list_objects_v2(
            Bucket=BUCKET_NAME,
            Prefix=BACKUP_PREFIX,
        )

        for obj in response.get("Contents", []):
            if obj["LastModified"] < limit_date:
                s3.delete_object(
                    Bucket=BUCKET_NAME,
                    Key=obj["Key"],
                )

                print(f"Usunięto stary backup: {obj['Key']}")

    except (BotoCoreError, ClientError) as error:
        print(f"Błąd podczas rotacji backupów: {error}")


if __name__ == "__main__":
    upload_backup_to_s3()
    delete_old_backups()
