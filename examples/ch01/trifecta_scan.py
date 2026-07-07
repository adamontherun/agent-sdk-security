"""Score a handful of real-shaped agent deployments against the lethal trifecta.

Run it:

    python examples/ch01/trifecta_scan.py

No Claude session or network access is needed — this is pure logic that turns
three yes/no questions about a deployment into a verdict.
"""

LEG_NAMES = ("private_data", "untrusted_content", "external_comms")


def assess(private_data: bool, untrusted_content: bool, external_comms: bool) -> dict:
    values = (private_data, untrusted_content, external_comms)
    present = [name for name, value in zip(LEG_NAMES, values, strict=True) if value]
    return {"present": present, "lethal": len(present) == 3}


# (label, private_data, untrusted_content, external_comms)
DEPLOYMENTS = [
    (
        "Support agent: reads customer records, ingests inbound email, can call webhooks",
        True,
        True,
        True,
    ),
    ("Code reviewer: reads a private repo, no outbound network, posts nothing", True, False, False),
    ("Docs summarizer: fetches public web pages, can email a summary out", False, True, True),
    ("Scratch sandbox: no secrets, ingests untrusted files, no egress", False, True, False),
]


def main() -> None:
    for label, priv, untrusted, egress in DEPLOYMENTS:
        report = assess(priv, untrusted, egress)
        verdict = "LETHAL TRIFECTA" if report["lethal"] else "ok"
        legs = ", ".join(report["present"]) or "none"
        print(f"[{verdict:>15}] {label}")
        print(f"                  legs present: {legs}")


if __name__ == "__main__":
    main()
