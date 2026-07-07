"""Work out how many agent sessions fit on a host.

The hosting docs give one formula for host sizing:

    agents per host = (host RAM - overhead) / (per-session RAM ceiling)

    https://code.claude.com/docs/en/agent-sdk/hosting#scaling-and-concurrency

Each session is its own `claude` subprocess holding its own transcript and
process tree in memory, so concurrency is bounded by RAM, not CPU. This script
turns the formula into a small planner: it floors the division (you can't run
a fractional session) and prints how much headroom is left over.

Run it:

    python examples/ch17/scaling.py

No Claude session or network access is needed.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class HostPlan:
    agents: int
    usable_ram_gib: float
    leftover_gib: float


def agents_per_host(
    host_ram_gib: float,
    overhead_gib: float,
    per_session_ceiling_gib: float,
) -> HostPlan:
    """Return how many sessions fit, given RAM, reserved overhead, and the
    measured per-session ceiling. The count is floored; leftover RAM is what
    remains after the last whole session is placed."""
    if per_session_ceiling_gib <= 0:
        raise ValueError("per_session_ceiling_gib must be positive")
    usable = host_ram_gib - overhead_gib
    if usable <= 0:
        return HostPlan(agents=0, usable_ram_gib=max(usable, 0.0), leftover_gib=0.0)
    agents = int(usable // per_session_ceiling_gib)
    leftover = usable - agents * per_session_ceiling_gib
    return HostPlan(agents=agents, usable_ram_gib=usable, leftover_gib=leftover)


# (label, host RAM, OS/runtime overhead, measured per-session peak RSS) in GiB.
# The 1 GiB starting point from the docs is a floor; a heavier tool load pushes
# the ceiling up, and the same host then holds far fewer sessions.
HOSTS = [
    ("16 GiB host, light 1 GiB sessions", 16, 2, 1),
    ("16 GiB host, heavy 3 GiB sessions", 16, 2, 3),
    ("64 GiB host, heavy 3 GiB sessions", 64, 4, 3),
    ("8 GiB host, one fat 6 GiB session", 8, 2, 6),
]


def main() -> None:
    for label, ram, overhead, ceiling in HOSTS:
        plan = agents_per_host(ram, overhead, ceiling)
        print(f"{label}")
        print(
            f"  ({ram} - {overhead}) / {ceiling}  ->  "
            f"{plan.agents} sessions, {plan.leftover_gib:.1f} GiB left over"
        )


if __name__ == "__main__":
    main()
