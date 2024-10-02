# gitlab-include-checker

This automated deployment with Terraform sets up an AWS Lambda function to check .gitlab-ci.yml files in GitLab projects.

## Prerequisites

Make sure you have the following:
- An AWS account with permissions to create resources such as IAM roles, Lambda functions, and S3 buckets.
- A GitLab access token with the **read_api** permission.

## Resources used in Terraform

- **AWS Provider:** Specifies the AWS region to use for deployment.
- **IAM Role:** Creates an IAM role allowing the Lambda function to access necessary AWS services.
- **IAM Role Policy:** Attaches a policy to the IAM role, defining permissions required for the Lambda function, such as access to CloudWatch logs, S3 buckets, and SES for email sending.
- **S3 Bucket:** Creates an S3 bucket where the Lambda function's code will be stored.
- **SES:** Creates a SES email identity, the email will need to be verified after deployment.
- **Lambda:** Defines the Lambda function, specifying the source code from the S3 bucket, Python 3.12 runtime, associated IAM role, and environment variables including the GitLab access token.

## Environment variables

`GITLAB_API_URL` : Your GitLab API Endpoint

`GITLAB_ACCESS_TOKEN` : Your GitLab Access Token

`BUCKET_NAME` : The name of the bucket that will store the .csv files

`SES_SENDER` : SES Sender

`SES_RECEIVER` : SES Receiver

## Deployment

```bash
git clone 
cd gitlab-include-checker
terraform init
terraform apply -var gitlab_access_token="YOUR_GITLAB_ACCESS_TOKEN" \
-var gitlab_api_url="YOUR_GITLAB_API_URL" \
-var ses_mail_sender="YOUR_SES_MAIL_SENDER" \
-var ses_mail_receiver="YOUR_SES_MAIL_RECEIVER"
```
