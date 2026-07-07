variable "aws_region" {
  description = "Region to deploy the agent task into."
  type        = string
  default     = "us-east-1"
}

variable "name" {
  description = "Name prefix for all resources."
  type        = string
  default     = "agent"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC."
  type        = string
  default     = "10.20.0.0/16"
}

variable "agent_image" {
  description = "Container image for the agent (your app running the Agent SDK)."
  type        = string
  default     = "111111111111.dkr.ecr.us-east-1.amazonaws.com/agent:latest"
}

variable "squid_image" {
  description = <<-EOT
    Container image for the Squid egress sidecar. Build this from
    examples/ch18/squid/Dockerfile so the allowlist config is baked in;
    the stock ubuntu/squid image ships an allow-all config.
  EOT
  type        = string
  default     = "111111111111.dkr.ecr.us-east-1.amazonaws.com/agent-squid:latest"
}

variable "task_cpu" {
  description = "Task-level CPU units. 1024 = 1 vCPU."
  type        = number
  default     = 1024
}

variable "task_memory" {
  description = "Task-level memory in MiB."
  type        = number
  default     = 2048
}
