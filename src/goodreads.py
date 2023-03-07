import json
import time

import requests
from bs4 import BeautifulSoup

from common import upload_file, copy_file


def remove_whitespace(text: str):
    return text.strip()


def flip_author(author: str):
    if "," in author:
        author = author.split(", ")
        author = author[1] + " " + author[0]
    return author


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


def process_book(raw_book: dict[str]):
    raw_book["title"] = remove_whitespace(raw_book["title"])
    raw_book["author"] = flip_author(remove_whitespace(raw_book["author"]))
    raw_book["finished_on"] = convert_us_date_str_to_iso_str(
        remove_whitespace(raw_book["finished_on"])
    )

    return raw_book


def lambda_handler(event, context):
    my_read_shelf = requests.get(
        "https://www.goodreads.com/review/list/74431442-blair-nangle?shelf=read"
    )
    html = my_read_shelf.content
    soup = BeautifulSoup(html, "html.parser")
    reviews = soup.find_all("tr", {"class": "bookalike review"})
    raw_books = []
    for review in reviews:
        book = {
            "title": str(
                review.find("td", {"class": "field title"})
                .find("div", {"class": "value"})
                .find("a", recursive=False)
                .string
            ),
            "author": str(
                review.find("td", {"class": "field author"})
                .find("div", {"class": "value"})
                .find("a", recursive=False)
                .string
            ),
            "finished_on": str(
                review.find("td", {"class": "field date_read"})
                .find("div", {"class": "value"})
                .find("span", {"class": "date_read_value"})
                .string
            ),
        }
        raw_books.append(book)

    processed_books = list(map(process_book, raw_books))

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
