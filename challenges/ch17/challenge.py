"""Chapter 17 challenge — the host-sizing calculator.

Every agent session runs in its own `claude` subprocess, so how many you can
pack onto one host is bounded by RAM. The hosting docs give the formula:

    agents per host = (host RAM - overhead) / (per-session RAM ceiling)

Implement `agents_per_host` to apply it. The count is floored (a fractional
session can't run), and `leftover_gib` is the RAM left after the last whole
session is placed. Guard the degenerate inputs: a non-positive per-session
ceiling is a programming error, and a host whose overhead swallows all its RAM
holds zero sessions rather than a negative number.
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
    """Return a HostPlan for the given host.

      agents:          floor((host_ram - overhead) / per_session_ceiling),
                       never negative.
      usable_ram_gib:  host_ram - overhead, floored at 0.0.
      leftover_gib:    usable RAM minus what the placed sessions consume;
                       0.0 when no session fits.

    Raise ValueError if per_session_ceiling_gib is not positive.
    """
    raise NotImplementedError()
