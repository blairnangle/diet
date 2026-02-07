import json
import logging
import time
from email.utils import parsedate_to_datetime

import feedparser
from feedparser import FeedParserDict

from common import configure_logging, upload_file, copy_file

configure_logging()

goodreads_user_id: str = "74431442"
rss_base_url: str = f"https://www.goodreads.com/review/list_rss/{goodreads_user_id}"


def parse_date(date_str: str) -> str:
    if not date_str or not date_str.strip():
        return ""
    try:
        dt = parsedate_to_datetime(date_str)
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return ""


def clean_url(url: str) -> str:
    return url.split("?")[0] if url else ""


def parse_book(entry: dict, date_field: str) -> dict:
    title = entry.get("title", "")
    author = entry.get("author_name", "")
    link = clean_url(entry.get("link", ""))

    if date_field == "finished":
        date_value = parse_date(entry.get("user_read_at", ""))
    else:
        date_value = parse_date(entry.get("user_date_added", ""))

    return {
        "title": title,
        "url": link,
        "author": author,
        date_field: date_value,
    }


def process_shelf(shelf_name: str) -> None:
    date_field = "finished" if shelf_name == "read" else "started"

    feed: FeedParserDict = feedparser.parse(f"{rss_base_url}?shelf={shelf_name}")
    entries = feed.entries[:20]

    processed_books = [parse_book(entry, date_field) for entry in entries]

    bucket = "diet.blairnangle.com"
    latest_file_name = f"goodreads-{shelf_name}.json"

    logging.info(f"Writing {latest_file_name} to temporary directory")

    with open(f"/tmp/{latest_file_name}", "w") as f:
        json.dump(processed_books, f)

    new_file_name = f"goodreads-{shelf_name}-{time.strftime('%Y-%m-%d')}.json"

    logging.info(f"Uploading {latest_file_name} to {bucket}")

    upload_file(
        file_name=f"/tmp/{latest_file_name}",
        bucket=bucket,
        object_name=latest_file_name,
    )

    logging.info(f"Archiving data to {new_file_name}")

    try:
        copy_file(
            existing_file=latest_file_name,
            new_file=new_file_name,
            bucket=bucket,
        )
        logging.info(f"Successfully archived data to {new_file_name}")
    except Exception as e:
        logging.error(f"Failed to create daily archive {new_file_name}: {e}")


def lambda_handler(event, context):
    logging.info(
        f"Beginning execution of goodreads.py with Lambda event: {str(event)} and Lambda context: {str(context)}"
    )

    process_shelf("read")
    process_shelf("currently-reading")
