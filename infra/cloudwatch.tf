#resource "aws_lambda_permission" "allow_cloudwatch" {
#  statement_id  = "AllowExecutionFromCloudWatch"
#  action        = "lambda:InvokeFunction"
#  function_name = aws_lambda_function.pocket.function_name
#  principal     = "events.amazonaws.com"
#  source_arn    = aws_cloudwatch_event_rule.test-lambda.arn
#}
#
#resource "aws_cloudwatch_event_rule" "test-lambda" {
#  name                = "run-lambda-function"
#  description         = "Schedule lambda function"
#  schedule_expression = "cron(0 4 * * ? *)"
#}
#
#resource "aws_cloudwatch_event_target" "lambda-function-target" {
#  target_id = "lambda-function-target"
#  rule      = aws_cloudwatch_event_rule.test-lambda.name
#  arn       = aws_lambda_function.pocket.arn
#}
