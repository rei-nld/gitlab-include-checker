variable "region" {
    type = string
    default = "eu-west-3"
}

variable "gitlab_access_token" {
  description = "GitLab Access Token"
  type        = string
  sensitive   = true
}

variable "gitlab_api_url" {
  description = "GitLab API URL"
  type = string
  default = ""
}

variable "ses_mail_sender" {
  description = "SES Sender"
  type = string
  default = ""
}

variable "ses_mail_receiver" {
  description = "SES Receiver"
  type = string
  default = ""
}