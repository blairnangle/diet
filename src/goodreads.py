import json
import logging
import time
from typing import Optional

import requests
from bs4 import BeautifulSoup

from common import upload_file, copy_file


def remove_whitespace(text: str) -> str:
    return text.strip()


def construct_url(url: str) -> str:
    return f"https://www.goodreads.com{url}"


def flip_author(author: str) -> str:
    if "," not in author:
        return author
    else:
        split = author.split(", ")
        flipped = split[1] + " " + split[0]

        return flipped


def convert_us_date_str_to_iso_str(date: str) -> str:
    short_month_to_number = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12",
    }

    split = list(map(lambda s: s.strip(","), date.split(" ")))
    if len(split) != 3:
        return ""
    else:
        year, month, day = split[2], split[0], split[1]

        return f"{year}-{short_month_to_number[month]}-{day}"


def process_book(raw_book: dict[str]) -> dict[str]:
    return {
        "title": remove_whitespace(raw_book["title"]),
        "url": construct_url(remove_whitespace(raw_book["url"])),
        "author": flip_author(remove_whitespace(raw_book["author"])),
        "finished": convert_us_date_str_to_iso_str(
            remove_whitespace(raw_book["finished"])
        ),
    }


def scrape_book(review: BeautifulSoup) -> dict[str]:
    book = {
        "title": str(
            review.find("td", {"class": "field title"})
            .find("div", {"class": "value"})
            .find("a", recursive=False)
            .find(string=True, recursive=False)
        ),
        "url": str(
            review.find("td", {"class": "field actions"})
            .find("div", {"class": "value"})
            .find("div")
            .find("a", recursive=False)
            .get("href")
        ),
        "author": str(
            review.find("td", {"class": "field author"})
            .find("div", {"class": "value"})
            .find("a", recursive=False)
            .string
        ),
        "finished": str(
            review.find("td", {"class": "field date_read"})
            .find("div", {"class": "value"})
            .find("span", {"class": "date_read_value"})
            .string
        ),
    }

    return book


def scrape_and_process(
    review: BeautifulSoup,
    books: list[dict[str]],
    tag_name: str,
    tag_attributes: dict[str],
) -> Optional[list[dict[str]]]:
    if review is None:
        return
    else:
        try:
            books.append(process_book(scrape_book(review)))
        except Exception as e:
            logging.error(e)
        finally:
            next_review = review.find_next(name=tag_name, attrs=tag_attributes)
            if next_review is not None:
                return scrape_and_process(
                    review=next_review,
                    books=books,
                    tag_name=tag_name,
                    tag_attributes=tag_attributes,
                )
            else:
                return books


def lambda_handler(event, context):
    logging.info(
        f"Beginning execution of goodreads.py with Lambda event: {str(event)} and Lambda context: {str(context)}"
    )

    goodreads_user_id: str = "74431442-blair-nangle"
    my_read_shelf = requests.get(
        f"https://www.goodreads.com/review/list/{goodreads_user_id}?shelf=read&sort=date_read&order=d"
    )
    html: bytes = my_read_shelf.content
    soup: BeautifulSoup = BeautifulSoup(
        markup=html, parser="html.parser", features="lxml"
    )
    processed_books: list[dict[str]] = []
    tag: str = "tr"
    attributes: dict[str] = {"class": "bookalike review"}
    first_review: BeautifulSoup = soup.find(name=tag, attrs=attributes)
    while len(processed_books) < 20:
        processed_books = scrape_and_process(
            review=first_review,
            books=processed_books,
            tag_name=tag,
            tag_attributes=attributes,
        )

    bucket = "information-diet.blairnangle.com"
    latest_file_name = "goodreads.json"

    with open(f"/tmp/{latest_file_name}", "w") as f:
        json.dump(processed_books, f)

    copy_file(
        existing_file=latest_file_name,
        new_file=f"goodreads-{time.strftime('%Y-%m-%d')}.json",
        bucket=bucket,
    )
    upload_file(
        file_name=f"/tmp/{latest_file_name}",
        bucket=bucket,
        object_name=latest_file_name,
    )
