import argparse
import json
import mimetypes
from pathlib import Path

import boto3
from botocore.exceptions import BotoCoreError, ClientError


def create_bucket(s3, bucket_name, region):
    if region == "us-east-1":
        s3.create_bucket(Bucket=bucket_name)
    else:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                "LocationConstraint": region,
            },
        )

    print(f"Utworzono bucket: {bucket_name}")


def configure_static_website(s3, bucket_name):
    s3.put_bucket_website(
        Bucket=bucket_name,
        WebsiteConfiguration={
            "IndexDocument": {
                "Suffix": "index.html",
            },
            "ErrorDocument": {
                "Key": "error.html",
            },
        },
    )

    print("Skonfigurowano hosting static website.")


def configure_public_access(s3, bucket_name):
    s3.put_public_access_block(
        Bucket=bucket_name,
        PublicAccessBlockConfiguration={
            "BlockPublicAcls": False,
            "IgnorePublicAcls": False,
            "BlockPublicPolicy": False,
            "RestrictPublicBuckets": False,
        },
    )

    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/*",
            }
        ],
    }

    s3.put_bucket_policy(
        Bucket=bucket_name,
        Policy=json.dumps(policy),
    )

    print("Skonfigurowano publiczny dostęp do plików.")


def upload_website_files(s3, bucket_name, directory):
    website_directory = Path(directory)

    allowed_extensions = {".html", ".css", ".js"}

    for file_path in website_directory.rglob("*"):
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in allowed_extensions:
            continue

        key = file_path.relative_to(website_directory).as_posix()

        content_type, _ = mimetypes.guess_type(file_path)

        if content_type is None:
            content_type = "application/octet-stream"

        s3.upload_file(
            str(file_path),
            bucket_name,
            key,
            ExtraArgs={
                "ContentType": content_type,
            },
        )

        print(
            f"Wysłano: {file_path} "
            f"-> {key} ({content_type})"
        )


def deploy_static_website(bucket_name, region, directory):
    s3 = boto3.client("s3", region_name=region)

    try:
        create_bucket(s3, bucket_name, region)
        configure_static_website(s3, bucket_name)
        configure_public_access(s3, bucket_name)
        upload_website_files(s3, bucket_name, directory)

        url = (
            f"http://{bucket_name}.s3-website."
            f"{region}.amazonaws.com"
        )

        print(f"\nURL strony: {url}")

    except (BotoCoreError, ClientError) as error:
        print(f"Błąd AWS: {error}")


def main():
    parser = argparse.ArgumentParser(
        description="Deploy statycznej strony WWW na Amazon S3."
    )

    parser.add_argument(
        "bucket_name",
        help="Nazwa bucketu S3.",
    )

    parser.add_argument(
        "directory",
        help="Katalog zawierający pliki HTML/CSS/JS.",
    )

    parser.add_argument(
        "--region",
        default="eu-central-1",
        help="Region AWS, domyślnie eu-central-1.",
    )

    args = parser.parse_args()

    deploy_static_website(
        args.bucket_name,
        args.region,
        args.directory,
    )


if __name__ == "__main__":
    main()
