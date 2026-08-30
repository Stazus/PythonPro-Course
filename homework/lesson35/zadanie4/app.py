import boto3
from botocore.exceptions import ClientError


def create_s3_bucket(bucket_name, region):
    s3 = boto3.client("s3", region_name=region)

    try:
        if region == "us-east-1":
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={
                    "LocationConstraint": region
                }
            )

        print(f"Bucket '{bucket_name}' został utworzony w regionie {region}.")

    except ClientError as error:
        error_code = error.response["Error"]["Code"]

        if error_code in ("BucketAlreadyExists", "BucketAlreadyOwnedByYou"):
            print(f"Bucket '{bucket_name}' już istnieje.")
        else:
            print(f"Błąd AWS: {error}")


if __name__ == "__main__":
    create_s3_bucket(
        "python-course-lesson35-stanislaw",
        "eu-central-1"
    )
