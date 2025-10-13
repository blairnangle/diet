# Instapaper

resource "aws_secretsmanager_secret" "instapaper_oauth_consumer_id" {
  name = "diet-instapaper-oauth-consumer-id"
}

resource "aws_secretsmanager_secret_version" "instapaper_oauth_consumer_id" {
  secret_id     = aws_secretsmanager_secret.instapaper_oauth_consumer_id.id
  secret_string = var.instapaper_oauth_consumer_id
}

resource "aws_secretsmanager_secret" "instapaper_oauth_consumer_secret" {
  name = "diet-instapaper-oauth-consumer-secret"
}

resource "aws_secretsmanager_secret_version" "instapaper_oauth_consumer_secret" {
  secret_id     = aws_secretsmanager_secret.instapaper_oauth_consumer_secret.id
  secret_string = var.instapaper_oauth_consumer_secret
}

resource "aws_secretsmanager_secret" "instapaper_password" {
  name = "diet-instapaper-password"
}

resource "aws_secretsmanager_secret_version" "instapaper_password" {
  secret_id     = aws_secretsmanager_secret.instapaper_password.id
  secret_string = var.instapaper_password
}
