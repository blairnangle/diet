import logging
import os
import time

import json
import requests
import boto3
import boto3.s3

from botocore.exceptions import ClientError


def lambda_handler(event, context):
    secrets_manager_client = boto3.client(
        service_name="secretsmanager",
        region_name="eu-west-2",
    )

    s3_client = boto3.client(service_name="s3")

    consumer_key: str = secrets_manager_client.get_secret_value(
        SecretId="information-diet-pocket-consumer-key"
    )["SecretString"]

    access_token: str = secrets_manager_client.get_secret_value(
        SecretId="information-diet-pocket-access-token"
    )["SecretString"]

    response = requests.post(
        "https://getpocket.com/v3/get",
        data={
            "consumer_key": consumer_key,
            "access_token": access_token,
            "state": "archive",
            "detailType": "complete",
            "count": 20,
        },
    ).json()

    content_read = []
    content_dict = response["list"]
    for content in content_dict.values():
        authors_list = content.get("authors", [])
        if not authors_list:
            authors = ""
        else:
            authors = ", ".join([author["name"] for author in authors_list.values()])

        content_read.append(
            {
                "title": content["resolved_title"],
                "url": content["resolved_url"],
                "authors": authors,
                "date_read": time.strftime(
                    "%Y-%m-%d", time.localtime(int(content["time_read"]))
                ),
            }
        )

    with open("/tmp/pocket.json", "w") as f:
        json.dump(content_read, f)

    copy_file(
        s3_client=s3_client,
        file_to_be_replaced="/tmp/pocket.json",
        bucket="information-diet.blairnangle.com",
    )
    upload_file(
        s3_client=s3_client,
        file_name="/tmp/pocket.json",
        bucket="information-diet.blairnangle.com",
        object_name="pocket.json",
    )


def upload_file(s3_client: boto3.client, file_name: str, bucket: str, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def copy_file(s3_client: boto3.client, file_to_be_replaced: str, bucket: str):
    copy_source = {"Bucket": bucket, "Key": file_to_be_replaced}

    s3_client.meta.client.copy(
        copy_source,
        "information-diet.blairnangle.com",
        f"pocket-replaced-on-{time.strftime('%Y-%m-%d')}.json",
    )
