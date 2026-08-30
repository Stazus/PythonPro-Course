import json
import logging
from datetime import datetime
from pathlib import Path
from uuid import uuid4


METADATA_FILE = Path("zadanie19/snapshots.json")
LOG_FILE = Path("zadanie19/recovery.log")


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)


def load_metadata():
    if not METADATA_FILE.exists():
        return []

    with METADATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_metadata(data):
    with METADATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def create_snapshot():
    snapshot_id = f"snap-{uuid4().hex[:8]}"

    snapshot = {
        "snapshot_id": snapshot_id,
        "created_at": datetime.now().isoformat(),
        "ec2": {
            "instance_id": "i-example123",
            "status": "snapshot-created",
        },
        "rds": {
            "database_id": "db-example123",
            "status": "snapshot-created",
        },
    }

    metadata = load_metadata()
    metadata.append(snapshot)
    save_metadata(metadata)

    logging.info(
        "Utworzono snapshot EC2 i RDS: %s",
        snapshot_id,
    )

    return snapshot_id


def store_backup_s3(snapshot_id):
    backup = {
        "snapshot_id": snapshot_id,
        "source_region": "eu-central-1",
        "backup_region": "eu-west-1",
        "bucket": "disaster-recovery-backup",
        "status": "uploaded",
    }

    logging.info(
        "Backup snapshotu %s zapisano w S3 w regionie %s.",
        snapshot_id,
        backup["backup_region"],
    )

    return backup


def restore_from_backup(snapshot_id):
    logging.info(
        "Rozpoczynam odtwarzanie snapshotu %s.",
        snapshot_id,
    )

    logging.info(
        "Odtworzono zasoby EC2 i RDS ze snapshotu %s.",
        snapshot_id,
    )

    return True


def test_recovery():
    logging.info("Rozpoczynam test Disaster Recovery.")

    snapshot_id = create_snapshot()

    store_backup_s3(snapshot_id)

    recovery_success = restore_from_backup(snapshot_id)

    if recovery_success:
        logging.info(
            "Test Disaster Recovery zakończony sukcesem."
        )
    else:
        logging.error(
            "Test Disaster Recovery zakończony niepowodzeniem."
        )


if __name__ == "__main__":
    test_recovery()
