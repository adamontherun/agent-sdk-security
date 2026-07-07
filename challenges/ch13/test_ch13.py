def test_single_developer_laptop(subject):
    assert subject.recommend({"environment": "laptop", "tenancy": "single"}) == "sandbox"


def test_ci_pipeline(subject):
    assert subject.recommend({"environment": "ci", "tenancy": "single"}) == "container"


def test_multi_tenant_untrusted_content(subject):
    assert (
        subject.recommend({"tenancy": "multi", "untrusted_content": True, "environment": "server"})
        == "gvisor"
    )


def test_regulated_pii(subject):
    assert (
        subject.recommend({"tenancy": "multi", "regulated": True, "untrusted_content": True})
        == "microvm"
    )


def test_hard_kernel_isolation_requirement_wins(subject):
    # Even a single-tenant laptop asking for kernel isolation escalates.
    assert (
        subject.recommend({"environment": "laptop", "kernel_isolation_required": True}) == "microvm"
    )


def test_egress_control_needs_a_container_boundary(subject):
    assert (
        subject.recommend({"environment": "server", "network_egress_control": True}) == "container"
    )


def test_empty_scenario_defaults_to_sandbox(subject):
    assert subject.recommend({}) == "sandbox"
