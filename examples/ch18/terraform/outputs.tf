output "cluster_name" {
  description = "ECS cluster running the agent service."
  value       = aws_ecs_cluster.main.name
}

output "task_definition_arn" {
  description = "ARN of the agent task definition."
  value       = aws_ecs_task_definition.agent.arn
}

output "task_role_arn" {
  description = "Task role assumed by the agent container (no policies attached)."
  value       = aws_iam_role.task.arn
}

output "execution_role_arn" {
  description = "Execution role used by the ECS agent to start the task."
  value       = aws_iam_role.execution.arn
}

output "log_group" {
  description = "CloudWatch log group carrying both containers' logs."
  value       = aws_cloudwatch_log_group.task.name
}
