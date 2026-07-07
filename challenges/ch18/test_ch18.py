CLEAN = {
    "family": "agent",
    "taskRoleArn": "arn:aws:iam::111:role/agent-task",
    "executionRoleArn": "arn:aws:iam::111:role/agent-exec",
    "containerDefinitions": [
        {
            "name": "agent",
            "environment": [
                {"name": "LOG_LEVEL", "value": "info"},
                {"name": "HTTPS_PROXY", "value": "http://localhost:3128"},
            ],
            "secrets": [
                {
                    "name": "ANTHROPIC_API_KEY",
                    "valueFrom": "arn:aws:secretsmanager:us-east-1:111:secret:anthropic",
                }
            ],
        },
        {"name": "squid"},
    ],
}


def test_clean_definition_passes(subject):
    assert subject.audit_task_definition(CLEAN) == []


def test_missing_roles(subject):
    td = {"containerDefinitions": []}
    assert subject.audit_task_definition(td) == [
        "missing_execution_role",
        "missing_task_role",
    ]


def test_shared_role_is_flagged(subject):
    td = {
        "taskRoleArn": "arn:aws:iam::111:role/same",
        "executionRoleArn": "arn:aws:iam::111:role/same",
        "containerDefinitions": [],
    }
    assert "shared_role" in subject.audit_task_definition(td)


def test_privileged_container(subject):
    td = {
        "taskRoleArn": "a",
        "executionRoleArn": "b",
        "containerDefinitions": [{"name": "agent", "privileged": True}],
    }
    assert subject.audit_task_definition(td) == ["privileged_container"]


def test_plaintext_secret_in_environment(subject):
    td = {
        "taskRoleArn": "a",
        "executionRoleArn": "b",
        "containerDefinitions": [
            {
                "name": "agent",
                "environment": [
                    {"name": "ANTHROPIC_API_KEY", "value": "sk-ant-xxx"},
                    {"name": "DB_PASSWORD", "value": "hunter2"},
                    {"name": "LOG_LEVEL", "value": "info"},
                ],
            }
        ],
    }
    assert subject.audit_task_definition(td) == ["plaintext_secret"]


def test_findings_are_deduplicated_and_sorted(subject):
    td = {
        "containerDefinitions": [
            {"name": "a", "privileged": True},
            {"name": "b", "privileged": True},
        ]
    }
    result = subject.audit_task_definition(td)
    assert result == sorted(result)
    assert result.count("privileged_container") == 1
