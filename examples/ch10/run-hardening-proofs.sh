#!/usr/bin/env bash
# Chapter 10 — prove each hardening flag actually does something.
#
# Every command here was run on macOS with Docker Desktop 27.4.0 (a real Linux
# VM under the hood, so cap-drop / read-only / network-none / pids-limit are all
# enforced by a real Linux kernel). The output quoted in the chapter came from
# running exactly this script. Run it yourself: `bash run-hardening-proofs.sh`.
#
# Uses a clearly-namespaced image name so it will not collide with other
# containers on a shared Docker daemon. Cleans the image up at the end.
set -u
IMG=agent-sdk-security-ch10
HERE="$(cd "$(dirname "$0")" && pwd)"

docker build -t "$IMG" "$HERE"

echo
echo "== PROOF 1: --read-only blocks writes outside a tmpfs mount =="
docker run --rm --read-only --tmpfs /tmp:rw,noexec,nosuid,size=16m --user 1000:1000 "$IMG" \
  sh -c 'echo pwned > /app/escape.txt'        # -> Read-only file system
docker run --rm --read-only --tmpfs /tmp:rw,noexec,nosuid,size=16m --user 1000:1000 "$IMG" \
  sh -c 'echo scratch > /tmp/ok.txt && cat /tmp/ok.txt'   # -> writes fine

echo
echo "== PROOF 2: --network none removes every external interface =="
docker run --rm "$IMG" sh -c 'echo ifaces: $(ls /sys/class/net)'                # has eth0
docker run --rm --network none "$IMG" sh -c 'echo ifaces: $(ls /sys/class/net)' # no eth0
docker run --rm --network none "$IMG" \
  python3 -c "import socket; socket.create_connection(('1.1.1.1',443),timeout=4)"  # unreachable

echo
echo "== PROOF 3: --cap-drop ALL removes CAP_CHOWN =="
docker run --rm --user 0:0 "$IMG" \
  sh -c 'touch /root/f && chown 1000:1000 /root/f && echo chown-OK'              # succeeds
docker run --rm --cap-drop ALL --user 0:0 "$IMG" \
  sh -c 'touch /root/f && chown 1000:1000 /root/f'                               # Operation not permitted

echo
echo "== PROOF 4: --pids-limit caps the process table =="
docker run --rm --pids-limit 16 "$IMG" \
  sh -c 'n=0; while [ $n -lt 40 ]; do sleep 20 & n=$((n+1)); done'               # -> Cannot fork

echo
echo "== FULL HARDENED RUN: the whole flag set, agent self-reports =="
docker run --rm \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=64m \
  --network none \
  --memory 512m \
  --cpus 1 \
  --pids-limit 128 \
  --user 1000:1000 \
  --ipc private \
  "$IMG"

echo
echo "== cleanup =="
docker rmi "$IMG" >/dev/null 2>&1 || true
