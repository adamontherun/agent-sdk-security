"""Chapter 13 challenge — turn the decision framework into code.

Given a described deployment, recommend one isolation technology from Part III:
"sandbox", "container", "gvisor", or "microvm". This encodes the chapter's
decision tree; the tests are the four worked scenarios from the chapter.

`scenario` is a dict with any of these keys (all optional, sensible defaults):
    {
        "environment": "laptop" | "ci" | "server",
        "tenancy": "single" | "multi",
        "untrusted_content": bool,   # does it process attacker-influenced input?
        "regulated": bool,           # PII / compliance obligations?
        "kernel_isolation_required": bool,  # a hard "must not share the host kernel"
        "network_egress_control": bool,     # needs a proxy/egress boundary
    }

Implement `recommend(scenario)` with this precedence (first match wins):
  1. kernel_isolation_required, OR (tenancy multi AND regulated) -> "microvm"
  2. tenancy multi AND untrusted_content                         -> "gvisor"
  3. environment == "ci", OR network_egress_control              -> "container"
  4. otherwise                                                    -> "sandbox"
"""


def recommend(scenario: dict) -> str:
    raise NotImplementedError()
