resource "aws_lambda_function" "pocket" {
  image_uri     = "${aws_ecr_repository.pocket.repository_url}:latest"
  function_name = "pocket"
  role          = aws_iam_role.pocket.arn
  package_type  = "Image"
  timeout       = 60
}

resource "aws_iam_role" "pocket" {
  name               = "pocket"
  assume_role_policy = file("./templates/lambda-assume-role.json")
}

resource "aws_iam_policy" "lambda_secrets_manager" {
  policy = templatefile("templates/secrets-manager.json",
    {
      pocketConsumerKeyArn = aws_secretsmanager_secret.pocket_consumer_key.arn,
      pocketAccessTokenArn = aws_secretsmanager_secret.pocket_access_token.arn
    }
  )
}

resource "aws_iam_role_policy_attachment" "lambda_secrets_manager" {
  role       = aws_iam_role.pocket.name
  policy_arn = aws_iam_policy.lambda_secrets_manager.arn
}

resource "aws_iam_policy" "lambda_logging" {
  policy = file("templates/lambda-logging.json")
}

resource "aws_iam_role_policy_attachment" "lambda_logging" {
  role       = aws_iam_role.pocket.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}
