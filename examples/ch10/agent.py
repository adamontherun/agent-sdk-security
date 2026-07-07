"""A stand-in for the agent payload.

This is not the Agent SDK. It is a few probes that report, from inside the
container, what the host's run-time flags actually allow: whether the root
filesystem is writable, whether any network interface exists, and which user
the process runs as. Running it under different `docker run` flag sets is how
chapter 10 proves each hardening flag does what the docs claim.
"""

import os
import socket


def probe_identity() -> None:
    print(f"uid={os.getuid()} gid={os.getgid()}")


def probe_rootfs_write() -> None:
    target = "/app/escape.txt"
    try:
        with open(target, "w") as handle:
            handle.write("agent was here\n")
        print(f"rootfs-write: WROTE {target}")
        os.remove(target)
    except OSError as exc:
        print(f"rootfs-write: BLOCKED ({exc.strerror})")


def probe_tmpfs_write() -> None:
    target = "/tmp/scratch.txt"
    try:
        with open(target, "w") as handle:
            handle.write("scratch\n")
        print(f"tmpfs-write:  WROTE {target}")
    except OSError as exc:
        print(f"tmpfs-write:  BLOCKED ({exc.strerror})")


def probe_network() -> None:
    interfaces = sorted(os.listdir("/sys/class/net"))
    print(f"net-ifaces:   {interfaces}")
    try:
        socket.create_connection(("1.1.1.1", 443), timeout=4).close()
        print("net-connect:  REACHED 1.1.1.1:443")
    except OSError as exc:
        print(f"net-connect:  BLOCKED ({exc.strerror or exc})")


if __name__ == "__main__":
    probe_identity()
    probe_rootfs_write()
    probe_tmpfs_write()
    probe_network()
