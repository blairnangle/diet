resource "aws_iam_policy" "lambda_logging" {
  policy = file("templates/lambda-logging.json")
}

resource "aws_lambda_function" "goodreads" {
  image_uri     = "${aws_ecr_repository.goodreads.repository_url}:latest"
  function_name = "goodreads"
  role          = aws_iam_role.goodreads.arn
  package_type  = "Image"
  timeout       = 60
}

resource "aws_iam_role" "goodreads" {
  name               = "goodreads"
  assume_role_policy = file("./templates/lambda-assume-role.json")
}

resource "aws_iam_role_policy_attachment" "goodreads_logging" {
  role       = aws_iam_role.goodreads.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}

resource "aws_lambda_function" "letterboxd" {
  image_uri     = "${aws_ecr_repository.letterboxd.repository_url}:latest"
  function_name = "letterboxd"
  role          = aws_iam_role.letterboxd.arn
  package_type  = "Image"
  timeout       = 60
}

resource "aws_iam_role" "letterboxd" {
  name               = "letterboxd"
  assume_role_policy = file("./templates/lambda-assume-role.json")
}

resource "aws_iam_role_policy_attachment" "letterboxd_logging" {
  role       = aws_iam_role.letterboxd.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}

resource "aws_lambda_function" "instapaper" {
  image_uri     = "${aws_ecr_repository.instapaper.repository_url}:latest"
  function_name = "instapaper"
  role          = aws_iam_role.instapaper.arn
  package_type  = "Image"
  timeout       = 60
}

resource "aws_iam_role" "instapaper" {
  name               = "instapaper"
  assume_role_policy = file("./templates/lambda-assume-role.json")
}

resource "aws_iam_policy" "instapaper_secrets_manager" {
  name = "instapaper-secrets-manager"
  policy = templatefile("templates/secrets-manager.json.tpl",
    {
      resources_json = jsonencode([
        aws_secretsmanager_secret.instapaper_oauth_consumer_id.arn,
        aws_secretsmanager_secret.instapaper_oauth_consumer_secret.arn,
        aws_secretsmanager_secret.instapaper_password.arn
      ])
    }
  )
}

resource "aws_iam_role_policy_attachment" "instapaper_secrets_manager" {
  role       = aws_iam_role.instapaper.name
  policy_arn = aws_iam_policy.instapaper_secrets_manager.arn
}

resource "aws_iam_role_policy_attachment" "instapaper_logging" {
  role       = aws_iam_role.instapaper.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}
