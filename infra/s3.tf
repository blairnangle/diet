resource "aws_s3_bucket" "information_diet" {
  bucket = "information-diet.blairnangle.com"
}

resource "aws_s3_bucket_public_access_block" "information_diet" {
  bucket = aws_s3_bucket.information_diet.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "information_diet" {
  bucket = aws_s3_bucket.information_diet.id
  policy = templatefile("${path.module}/templates/s3.json", {
    awsAccountNumber = var.aws_account_number,
    lambdaRoleArn    = aws_iam_role.pocket.arn,
    bucketName       = aws_s3_bucket.information_diet.bucket
  })
}

locals {
  n_days_to_keep_s3_objects = 365
}

resource "aws_s3_bucket_lifecycle_configuration" "information_diet" {
  bucket = aws_s3_bucket.information_diet.id

  rule {
    id     = "delete-objects-older-than-${local.n_days_to_keep_s3_objects}-days"
    status = "Enabled"
    expiration {
      days = local.n_days_to_keep_s3_objects
    }
  }
}

resource "aws_s3_bucket_cors_configuration" "information_diet" {
  bucket = aws_s3_bucket.information_diet.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET"]
    allowed_origins = ["*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
}
