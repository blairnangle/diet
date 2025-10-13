# diet

Aggregating the content I've consumed.

## Prerequisites

- [Black](https://github.com/psf/black)
- [Terraform](https://developer.hashicorp.com/terraform/downloads)

## Mechanism

- Fetch data from Instapaper/scrape data from Goodreads/Letterboxd RSS feed
- Parse and format
- Write to an S3 bucket that has public read access

## Instapaper

I have registered "diet" as an OAuth application against the [Instapaper API](https://www.instapaper.com/api).

## Goodreads

The Goodreads API no longer accepts signups 🥲, so I'm using
[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to scrape my Goodreads "read" shelf.

This will break at some point.

## Letterboxd

At the time of writing, Letterboxd's API is not available for public signups, *but* they do expose an RSS feed for each
member. E.g., [mine](https://letterboxd.com/blairnangle/rss/). This is straightforward to parse.

## Secrets

Stored as GitHub Actions secrets.

```yaml
# implicitly used by AWS Terraform provider
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY

# explicitly declared in infra/variables.tf
AWS_ACCOUNT_NUMBER

INSTAPAPER_OAUTH_CONSUMER_ID
INSTAPAPER_OAUTH_CONSUMER_SECRET
INSTAPAPER_PASSWORD
```
