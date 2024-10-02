resource "aws_lambda_function" "gitlab-include-checker" {
  function_name = "gitlab-include-checker"

  s3_bucket = resource.aws_s3_object.package.bucket
  s3_key    = resource.aws_s3_object.package.key

  handler = "lambda_function.lambda_handler"
  runtime = "python3.12"
  role    = resource.aws_iam_role.lambda_execution_role.arn

  timeout = 60
  memory_size = 512

  environment {
    variables = {
      GITLAB_API_URL = var.gitlab_api_url
      GITLAB_ACCESS_TOKEN = var.gitlab_access_token
      BUCKET_NAME         = resource.aws_s3_bucket.largest_graveyard_mmxxiv.bucket
      SES_SENDER = var.ses_mail_sender
      SES_RECEIVER = var.ses_mail_receiver
    }
  }

  depends_on = [resource.aws_s3_object.package]
}
