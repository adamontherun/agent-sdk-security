# Pin Terraform and the AWS provider so `terraform init` is reproducible.
# Validated locally with Terraform 1.10.4 and the 5.x AWS provider; no AWS
# credentials are needed for `terraform validate` or `terraform fmt`.
terraform {
  required_version = ">= 1.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.60"
    }
  }
}

provider "aws" {
  region = var.aws_region
}
