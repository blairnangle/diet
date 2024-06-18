import logging
import os

import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client(service_name="s3")


# The Lambda environment pre-configures a handler logging to stderr.
# If a handler is already configured, `.basicConfig` does not execute.
# Thus, we set the level directly.
def configure_logging():
    if logging.getLogger().hasHandlers():
        logging.getLogger().setLevel(logging.INFO)
    else:
        logging.basicConfig(level=logging.INFO)


def upload_file(file_name: str, bucket: str, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def copy_file(existing_file: str, new_file: str, bucket: str):
    s3_resource = boto3.resource("s3")
    s3_resource.Object(bucket, new_file).copy_from(
        CopySource=f"{bucket}/{existing_file}"
    )
