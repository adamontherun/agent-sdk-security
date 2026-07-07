"""Reference solution for the chapter 13 isolation-strategy recommender."""


def recommend(scenario: dict) -> str:
    multi = scenario.get("tenancy") == "multi"
    untrusted = scenario.get("untrusted_content", False)
    regulated = scenario.get("regulated", False)
    kernel = scenario.get("kernel_isolation_required", False)
    environment = scenario.get("environment")
    egress = scenario.get("network_egress_control", False)

    if kernel or (multi and regulated):
        return "microvm"
    if multi and untrusted:
        return "gvisor"
    if environment == "ci" or egress:
        return "container"
    return "sandbox"
