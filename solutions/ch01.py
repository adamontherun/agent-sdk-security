"""Chapter 1 reference solution — model the lethal trifecta."""

LEG_NAMES = ("private_data", "untrusted_content", "external_comms")


def assess_trifecta(
    private_data: bool,
    untrusted_content: bool,
    external_comms: bool,
) -> dict:
    values = (private_data, untrusted_content, external_comms)
    present = [name for name, value in zip(LEG_NAMES, values, strict=True) if value]
    lethal = len(present) == 3
    return {
        "present": present,
        "lethal": lethal,
        "breakable_by_cutting": list(present) if lethal else [],
    }
