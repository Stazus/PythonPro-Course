import os
import shutil
import boto3


BUCKET_NAME = "python-course-lesson35-stanislaw"
SOURCE_DIR = "zadanie4"
ZIP_NAME = "zadanie4.zip"


def create_zip():
    """Kompresuje folder zadanie4 do pliku ZIP."""
    zip_path = shutil.make_archive(
        base_name="zadanie4",
        format="zip",
        root_dir=SOURCE_DIR,
    )

    print(f"Utworzono archiwum: {zip_path}")
    return zip_path


def upload_to_s3(zip_path):
    """Przesyła archiwum ZIP do bucketu S3 i wyświetla URL."""
    s3 = boto3.client("s3", region_name="eu-central-1")

    object_name = os.path.basename(zip_path)

    s3.upload_file(
        zip_path,
        BUCKET_NAME,
        object_name,
    )

    url = f"https://{BUCKET_NAME}.s3.eu-central-1.amazonaws.com/{object_name}"

    print(f"Plik przesłany do S3: {object_name}")
    print(f"URL: {url}")

    return url


def main():
    zip_path = create_zip()
    upload_to_s3(zip_path)


if __name__ == "__main__":
    main()
