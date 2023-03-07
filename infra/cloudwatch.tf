resource "aws_lambda_permission" "allow_cloudwatch_to_trigger_lambda" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.pocket.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.nightly_cron.arn
}

resource "aws_cloudwatch_event_rule" "nightly_cron" {
  name                = "nightly-cron"
  description         = "Schedule lambda function"
  schedule_expression = "cron(0 4 * * ? *)"
}

resource "aws_cloudwatch_event_target" "nightly_cron_pocket" {
  target_id = "nightly-cron-pocket"
  rule      = aws_cloudwatch_event_rule.nightly_cron.name
  arn       = aws_lambda_function.pocket.arn
}

#resource "aws_cloudwatch_event_target" "nightly_cron_goodreads" {
#  target_id = "nightly-cron-goodreads"
#  rule      = aws_cloudwatch_event_rule.nightly_cron.name
#  arn       = aws_lambda_function.goodreads.arn
#}
