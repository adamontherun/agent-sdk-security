# Terraform covers only the surrounding pieces here: the S3 bucket for the code
# artifact and the IAM roles create-microvm-image and run-microvm reference. The
# MicroVM image and lifecycle themselves have no native resource in the AWS
# provider (verified against v5.100.0: zero resources match "microvm"), so those
# steps use the `aws lambda-microvms` CLI in ../scripts. See the chapter.
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
