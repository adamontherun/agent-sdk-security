"""Chapter 17 reference solution — the host-sizing calculator."""

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
    if per_session_ceiling_gib <= 0:
        raise ValueError("per_session_ceiling_gib must be positive")
    usable = host_ram_gib - overhead_gib
    if usable <= 0:
        return HostPlan(agents=0, usable_ram_gib=max(usable, 0.0), leftover_gib=0.0)
    agents = int(usable // per_session_ceiling_gib)
    leftover = usable - agents * per_session_ceiling_gib
    return HostPlan(agents=agents, usable_ram_gib=usable, leftover_gib=leftover)
