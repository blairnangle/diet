import json
import logging
import time

import feedparser
from feedparser import FeedParserDict

from common import upload_file, copy_file


def to_bool(yes_or_no: str) -> bool:
    lower = yes_or_no.lower()

    return True if lower == "yes" else False


def parse_film(unparsed: dict) -> dict:
    return {
        "title": unparsed.get("letterboxd_filmtitle"),
        "film_year": unparsed.get("letterboxd_filmyear"),
        "date": unparsed.get("letterboxd_watcheddate"),
        "rating": unparsed.get("letterboxd_memberrating"),
        "rewatch?": to_bool(unparsed.get("letterboxd_rewatch")),
        "url": unparsed.get("links")[0].get("href"),
    }


def parse_films() -> list[dict]:
    feed: FeedParserDict = feedparser.parse("https://letterboxd.com/blairnangle/rss")
    last_20: list[dict] = feed.entries[0:20]

    return list(map(lambda u: parse_film(u), last_20))


def lambda_handler(event, context):
    logging.info(
        f"Beginning execution of goodreads.py with Lambda event: {str(event)} and Lambda context: {str(context)}"
    )

    films = parse_films()

    bucket = "diet.blairnangle.com"
    latest_file_name = "letterboxd.json"

    logging.info(f"Writing {latest_file_name} to temporary directory")

    with open(f"/tmp/{latest_file_name}", "w") as f:
        json.dump(films, f)

    new_file_name = f"letterboxd-{time.strftime('%Y-%m-%d')}.json"

    logging.info(f"Copying {latest_file_name} to {new_file_name}")

    copy_file(
        existing_file=latest_file_name,
        new_file=new_file_name,
        bucket=bucket,
    )

    logging.info(f"Uploading {latest_file_name} to {bucket}")

    upload_file(
        file_name=f"/tmp/{latest_file_name}",
        bucket=bucket,
        object_name=latest_file_name,
    )
