from pathlib import Path

import boto3
from botocore.exceptions import ClientError


def upload_jpg_files(directory, bucket_name):
    s3 = boto3.client("s3")
    directory_path = Path(directory)

    for file_path in directory_path.glob("*.jpg"):
        try:
            s3.upload_file(
                str(file_path),
                bucket_name,
                file_path.name
            )
            print(f"Wysłano: {file_path.name}")

        except ClientError as error:
            print(f"Błąd podczas wysyłania {file_path.name}: {error}")


if __name__ == "__main__":
    upload_jpg_files(
        "zadanie5/images",
        "python-course-lesson35-stanislaw"
    )
