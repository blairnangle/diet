# information-diet

Aggregating the content I've consumed.

## Mechanism

- Fetch data from Pocket
- Parse and format
- Write to an S3 bucket that has public read access

## Pocket

Use [this tool](https://reader.fxneumann.de/plugins/oneclickpocket/auth.php) by
[Felix Neumann](https://twitter.com/fxneumann) to get a long-lived access token using the annoying three-legged OAuth
flow.

## Secrets

```yaml
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_ACCOUNT_NUMBER
POCKET_CONSUMER_KEY
POCKET_ACCESS_TOKEN
```
