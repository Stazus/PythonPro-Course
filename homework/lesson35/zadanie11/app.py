import boto3
from botocore.exceptions import BotoCoreError, ClientError


SOURCE_BUCKET = "python-course-lesson35-stanislaw"
DESTINATION_BUCKET = "python-course-lesson35-stanislaw-dr"
DESTINATION_REGION = "eu-west-1"


def sync_s3_buckets():
    s3_source = boto3.client("s3", region_name="eu-central-1")
    s3_destination = boto3.client("s3", region_name=DESTINATION_REGION)

    try:
        response = s3_source.list_objects_v2(Bucket=SOURCE_BUCKET)

        objects = response.get("Contents", [])

        if not objects:
            print("Brak obiektów do skopiowania.")
            return

        for obj in objects:
            key = obj["Key"]

            copy_source = {
                "Bucket": SOURCE_BUCKET,
                "Key": key,
            }

            s3_destination.copy_object(
                CopySource=copy_source,
                Bucket=DESTINATION_BUCKET,
                Key=key,
            )

            print(f"Skopiowano: {key}")

    except (BotoCoreError, ClientError) as error:
        print(f"Błąd AWS: {error}")


if __name__ == "__main__":
    sync_s3_buckets()
