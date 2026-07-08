resource "aws_ecs_cluster" "main" {
  name = "${var.name}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_cloudwatch_log_group" "task" {
  name              = "/ecs/${var.name}"
  retention_in_days = 30
}

# Two containers in one task. Under awsvpc networking they share a network
# namespace, so the agent reaches the sidecar over localhost:3128 with no
# service discovery. The agent has HTTP_PROXY set and no credentials; the Squid
# sidecar holds the injected key and forwards only allowlisted domains.
resource "aws_ecs_task_definition" "agent" {
  family                   = var.name
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.task_cpu
  memory                   = var.task_memory
  execution_role_arn       = aws_iam_role.execution.arn
  task_role_arn            = aws_iam_role.task.arn

  container_definitions = jsonencode([
    {
      name      = "agent"
      image     = var.agent_image
      essential = true

      # The agent's HTTP client sends everything to the sidecar. It holds no
      # API key: the credential is injected downstream, at Squid.
      environment = [
        { name = "HTTP_PROXY", value = "http://localhost:3128" },
        { name = "HTTPS_PROXY", value = "http://localhost:3128" },
        { name = "NO_PROXY", value = "localhost,127.0.0.1" }
      ]

      # Do not start the agent until the proxy is accepting connections, or its
      # first outbound call races the sidecar and fails.
      dependsOn = [
        { containerName = "squid", condition = "HEALTHY" }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.task.name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "agent"
        }
      }
    },
    {
      name      = "squid"
      image     = var.squid_image
      essential = true

      portMappings = [
        { containerPort = 3128, protocol = "tcp" }
      ]

      # ECS resolves this ARN at task start and injects the value as an env
      # var inside the sidecar only. It never touches the agent container and
      # never appears in the task definition JSON.
      secrets = [
        {
          name      = "ANTHROPIC_API_KEY"
          valueFrom = aws_secretsmanager_secret.anthropic_api_key.arn
        }
      ]

      # A dependency-free readiness probe: bash opens a TCP connection to the
      # proxy port and exits non-zero if nothing is listening. The ubuntu/squid
      # image ships bash but not squidclient or curl, so a manager query or an
      # HTTP probe would fail on a missing binary rather than on proxy state.
      healthCheck = {
        command  = ["CMD-SHELL", "bash -c '</dev/tcp/127.0.0.1/3128' || exit 1"]
        interval = 15
        timeout  = 5
        retries  = 3
      }

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          "awslogs-group"         = aws_cloudwatch_log_group.task.name
          "awslogs-region"        = var.aws_region
          "awslogs-stream-prefix" = "squid"
        }
      }
    }
  ])
}

resource "aws_ecs_service" "agent" {
  name            = var.name
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.agent.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets = aws_subnet.private[*].id
    # No public IP: the task is not directly reachable from the internet, and
    # its only outbound path is the NAT plus the restrictive task SG.
    assign_public_ip = false
    security_groups  = [aws_security_group.task.id]
  }
}
