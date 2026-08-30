import io
import time

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from PIL import Image


BUCKET_NAME = "python-course-lesson35-stanislaw"
REGION = "eu-central-1"
THUMBNAIL_PREFIX = "thumbnails/"

processed_objects = set()


def list_new_images(s3):
    response = s3.list_objects_v2(Bucket=BUCKET_NAME)
    new_images = []

    for obj in response.get("Contents", []):
        key = obj["Key"]

        if key.startswith(THUMBNAIL_PREFIX):
            continue

        if not key.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        if key not in processed_objects:
            new_images.append(key)

    return new_images


def create_thumbnail(s3, key):
    response = s3.get_object(
        Bucket=BUCKET_NAME,
        Key=key,
    )

    image_data = response["Body"].read()

    with Image.open(io.BytesIO(image_data)) as image:
        image.thumbnail((200, 200))

        output = io.BytesIO()

        image_format = image.format or "JPEG"
        image.save(output, format=image_format)
        output.seek(0)

        filename = key.split("/")[-1]
        thumbnail_key = f"{THUMBNAIL_PREFIX}{filename}"

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=thumbnail_key,
            Body=output.getvalue(),
            ContentType=(
                "image/png"
                if image_format.upper() == "PNG"
                else "image/jpeg"
            ),
        )

        print(f"Utworzono thumbnail: {thumbnail_key}")


def process_s3_events():
    s3 = boto3.client("s3", region_name=REGION)

    try:
        new_images = list_new_images(s3)

        if not new_images:
            print("Brak nowych obrazów.")

        for key in new_images:
            print(f"Wykryto nowy obraz: {key}")

            try:
                create_thumbnail(s3, key)
                processed_objects.add(key)

            except Exception as error:
                print(
                    f"Błąd podczas przetwarzania "
                    f"{key}: {error}"
                )

    except (BotoCoreError, ClientError) as error:
        print(f"Błąd AWS: {error}")


def main():
    print("Uruchamiam S3 Event Processor...")

    while True:
        process_s3_events()
        time.sleep(10)


if __name__ == "__main__":
    main()
