import json
import logging
import time

import boto3
import boto3.s3
import requests

from common import copy_file, upload_file


def lambda_handler(event, context):
    logging.info(
        f"Beginning execution of pocket.py with Lambda event: {str(event)} and Lambda context: {str(context)}"
    )

    secrets_manager_client: boto3.client = boto3.client(
        service_name="secretsmanager",
        region_name="eu-west-2",
    )

    consumer_key: str = secrets_manager_client.get_secret_value(
        SecretId="information-diet-pocket-consumer-key"
    )["SecretString"]

    access_token: str = secrets_manager_client.get_secret_value(
        SecretId="information-diet-pocket-access-token"
    )["SecretString"]

    response: json = requests.post(
        "https://getpocket.com/v3/get",
        data={
            "consumer_key": consumer_key,
            "access_token": access_token,
            "state": "archive",
            "detailType": "complete",
            "count": 20,
        },
    ).json()

    content_read: list[dict] = []
    content_dict: dict = response["list"]
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

    bucket = "information-diet.blairnangle.com"
    latest_file_name = "pocket.json"

    with open(f"/tmp/{latest_file_name}", "w") as f:
        json.dump(content_read, f)

    copy_file(
        existing_file=latest_file_name,
        new_file=f"pocket-{time.strftime('%Y-%m-%d')}.json",
        bucket=bucket,
    )
    upload_file(
        file_name=f"/tmp/{latest_file_name}",
        bucket=bucket,
        object_name=latest_file_name,
    )
