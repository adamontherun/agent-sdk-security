output "artifact_bucket" {
  description = "S3 bucket the code artifact is uploaded to."
  value       = aws_s3_bucket.artifacts.bucket
}

output "build_role_arn" {
  description = "Pass to `create-microvm-image --build-role-arn`."
  value       = aws_iam_role.build.arn
}

output "execution_role_arn" {
  description = "Pass to `run-microvm --execution-role-arn`."
  value       = aws_iam_role.execution.arn
}
