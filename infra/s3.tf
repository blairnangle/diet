resource "aws_s3_bucket" "diet" {
  bucket = "diet.blairnangle.com"
}

resource "aws_s3_bucket_public_access_block" "diet" {
  bucket = aws_s3_bucket.diet.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "diet" {
  bucket = aws_s3_bucket.diet.id
  policy = templatefile("${path.module}/templates/s3.json.tpl", {
    awsAccountNumber = var.aws_account_number,
    lambdaRoleArns   = jsonencode([
      aws_iam_role.goodreads.arn,
      aws_iam_role.letterboxd.arn,
      aws_iam_role.instapaper.arn
    ]),
    bucketName = aws_s3_bucket.diet.bucket
  })
}

locals {
  n_days_to_keep_s3_objects = 365
}

resource "aws_s3_bucket_lifecycle_configuration" "diet" {
  bucket = aws_s3_bucket.diet.id

  rule {
    id     = "delete-objects-older-than-${local.n_days_to_keep_s3_objects}-days"
    status = "Enabled"
    expiration {
      days = local.n_days_to_keep_s3_objects
    }
  }
}

resource "aws_s3_bucket_cors_configuration" "diet" {
  bucket = aws_s3_bucket.diet.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET"]
    allowed_origins = ["*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
}
