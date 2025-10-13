import json
import logging
import time

import boto3
from requests_oauthlib import OAuth1Session

from common import configure_logging, upload_file, copy_file

configure_logging()


def lambda_handler(event, context):
    logging.info(
        f"Beginning execution of instapaper.py with Lambda event: {str(event)} and Lambda context: {str(context)}"
    )

    secrets_manager_client: boto3.client = boto3.client(
        service_name="secretsmanager",
        region_name="eu-west-2",
    )

    oauth_consumer_id: str = secrets_manager_client.get_secret_value(
        SecretId="diet-instapaper-oauth-consumer-id"
    )["SecretString"]

    oauth_consumer_secret: str = secrets_manager_client.get_secret_value(
        SecretId="diet-instapaper-oauth-consumer-secret"
    )["SecretString"]

    password: str = secrets_manager_client.get_secret_value(
        SecretId="diet-instapaper-password"
    )["SecretString"]

    oauth = OAuth1Session(
        client_key=oauth_consumer_id, client_secret=oauth_consumer_secret
    )

    # Perform xAuth exchange
    response = oauth.post(
        "https://www.instapaper.com/api/1/oauth/access_token",
        data={
            "x_auth_username": "blair.nangle@gmail.com",
            "x_auth_password": password,
            "x_auth_mode": "client_auth",
        },
    )

    if response.status_code == 200:
        tokens = dict(item.split("=") for item in response.text.split("&"))
        oauth_token = tokens["oauth_token"]
        oauth_token_secret = tokens["oauth_token_secret"]
    else:
        print("Failed to get access token:", response.status_code, response.text)

    authed_session = OAuth1Session(
        client_key=oauth_consumer_id,
        client_secret=oauth_consumer_secret,
        resource_owner_key=oauth_token,
        resource_owner_secret=oauth_token_secret,
    )

    # Fetch archived (read) bookmarks
    response = authed_session.post(
        "https://www.instapaper.com/api/1/bookmarks/list",
        data={"folder_id": "archive", "limit": 100},
    )

    if response.status_code == 200:
        bookmarks = response.json()
        # Filter only 'bookmark' type items (the API also returns folder metadata)
        bookmarks = [b for b in bookmarks if b.get("type") == "bookmark"]

        # Sort by most recently read
        sorted_bookmarks = sorted(
            bookmarks, key=lambda b: b.get("progress_timestamp", 0), reverse=True
        )

        content_read_sorted = []
        for bookmark in sorted_bookmarks[:20]:  # Limit to the 20 most recent
            content_read_sorted.append(
                {
                    "title": bookmark["title"],
                    "url": bookmark["url"],
                    "date_read": time.strftime(
                        "%Y-%m-%d", time.localtime(int(bookmark["progress_timestamp"]))
                    ),
                }
            )

        bucket = "diet.blairnangle.com"
        latest_file_name = "instapaper.json"

        with open(f"/tmp/{latest_file_name}", "w") as f:
            json.dump(content_read_sorted, f)

        upload_file(
            file_name=f"/tmp/{latest_file_name}",
            bucket=bucket,
            object_name=latest_file_name,
        )

        dated_file_name = f"instapaper-{time.strftime('%Y-%m-%d')}.json"
        try:
            copy_file(
                existing_file=latest_file_name,
                new_file=dated_file_name,
                bucket=bucket,
            )
            logging.info(f"Successfully archived data to {dated_file_name}")
        except Exception as e:
            logging.error(f"Failed to create daily archive {dated_file_name}: {e}")
    else:
        print("Error:", response.status_code, response.text)
