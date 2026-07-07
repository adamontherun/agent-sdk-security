# Agent SDK Security

A hands-on course on securing Claude Agent SDK deployments: the permission
pipeline, OS-level sandboxing, container and microVM isolation, and a real
Squid egress proxy you build and run, ending in production deployments on
Amazon ECS and AWS Lambda MicroVMs.

[![Read the Book](https://img.shields.io/badge/📖_Read_the_Book-{{PAGES_HOST_PATH}}-c0392b)]({{PAGES_URL}})

[![{{SCREENSHOT_ALT_TEXT}}]({{SCREENSHOT_PATH}})]({{PAGES_URL}})

This repo is two things: **the book** (20 chapters of prose, nothing to
install) and **the code** (runnable examples, a Docker/Squid lab, and
failing-test challenges, which need an environment). Every chapter in the
book links straight back to Codespaces, so you're never more than one click
from a terminal with Docker and the Python toolchain already available.

## What's covered

- **Part I · Threat Model & Foundations** — why agent security is different, what Claude Code and the Agent SDK already defend against, and the boundaries/least-privilege/defense-in-depth principles the rest of the course builds on.
- **Part II · Permissions & Settings** — the full permission evaluation pipeline, every permission mode, tool-specific rule syntax, hooks, and managed settings for organization-wide policy.
- **Part III · Isolation Technologies** — the built-in sandbox, hardened Docker containers, gVisor, and Firecracker microVMs, with a framework for choosing between them.
- **Part IV · Credentials & the Network Boundary** — the proxy pattern, a real Squid egress proxy built step by step, and filesystem configuration.
- **Part V · Production Deployment** — hosting the Agent SDK, deploying on Amazon ECS, deploying on AWS Lambda MicroVMs, and observability/audit.

## Setup

Don't want to install anything? Open [the book]({{PAGES_URL}}) and click
"Launch Codespace" in any chapter's sidebar — it opens a cloud dev
environment with Docker and the Python toolchain already available.

To run locally, you need [Python 3.12+](https://www.python.org/downloads/),
[uv](https://docs.astral.sh/uv/getting-started/installation/), and
[Docker](https://docs.docker.com/get-docker/):

```sh
uv sync
docker compose up -d
```

The Docker Compose stack backs the Part III/IV hands-on labs (the hardened
container and the Squid proxy). It isn't needed for Parts I, II, or V, whose
examples run as plain Python or `terraform validate`/`aws lambda-microvms`
dry runs against local files.

## Doing challenges

Every chapter has a challenge under `challenges/`: a skeleton file with
failing tests. Edit the skeleton until the tests pass:

```sh
uv run pytest challenges/ch04/
```

Reference solutions live in `solutions/`. No peeking until the tests pass.

## Resetting the lab environment

The Docker/Squid lab accumulates container state (proxy logs, generated CA
certs, cache) as you work through Part III and IV. To reset it:

```sh
docker compose down -v
docker compose up -d
```

## Analytics

The published book uses [PostHog](https://posthog.com) for anonymous reading
analytics (pageviews, which chapters and sections get read, and Codespace
launches) to help improve the course. No personal data is collected and there
is no session recording.
