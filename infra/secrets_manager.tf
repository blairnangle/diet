resource "aws_secretsmanager_secret" "pocket_consumer_key" {
  name = "information-diet-pocket-consumer-key"
}

resource "aws_secretsmanager_secret_version" "pocket_consumer_key" {
  secret_id     = aws_secretsmanager_secret.pocket_consumer_key.id
  secret_string = var.pocket_consumer_key
}

resource "aws_secretsmanager_secret" "pocket_access_token" {
  name = "information-diet-pocket-access-token"
}

resource "aws_secretsmanager_secret_version" "pocket_access_token" {
  secret_id     = aws_secretsmanager_secret.pocket_access_token.id
  secret_string = var.pocket_access_token
}
