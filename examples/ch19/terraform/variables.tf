variable "aws_region" {
  description = "A region where Lambda MicroVMs is available."
  type        = string
  # Launch regions: us-east-1, us-east-2, us-west-2, eu-west-1, ap-northeast-1.
  default = "us-east-1"
}

variable "name" {
  description = "Name prefix for all resources."
  type        = string
  default     = "agent-microvm"
}

variable "artifact_bucket_name" {
  description = "Globally unique S3 bucket name for the code artifact zip."
  type        = string
  default     = "agent-microvm-artifacts-change-me"
}
