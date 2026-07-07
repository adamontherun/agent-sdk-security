# Research notes — Agent SDK Security course

Bibliography of sources consulted during the build, organized by topic. Every
load-bearing claim in the book cites its source inline; this file is the
working index used while drafting and fact-checking.

## Primary resource

- [Secure Deployment (Claude Agent SDK docs)](https://code.claude.com/docs/en/agent-sdk/secure-deployment) — threat model, built-in security features, security principles, isolation technologies (sandbox-runtime, containers, gVisor, VMs), credential management / proxy pattern, filesystem configuration. The course's spine; nearly every chapter in Parts I, III, and IV traces back to a section of this page.

## Claude Code / Agent SDK docs

- [Security](https://code.claude.com/docs/en/security) — permission-based architecture, prompt injection safeguards, MCP security, cloud execution security, security best practices.
- [Permissions](https://code.claude.com/docs/en/permissions) — full permission rule syntax (Bash, PowerShell, Read/Edit, WebFetch, MCP, Agent, Cd), wildcard semantics, managed settings, settings precedence, workspace trust.
- [Sandboxing](https://code.claude.com/docs/en/sandboxing) — bubblewrap/Seatbelt mechanics, sandbox modes, `sandbox.filesystem`/`sandbox.network`/`sandbox.credentials` settings, TLS/domain-fronting limitations, managed enforcement.
- [Agent SDK Permissions](https://code.claude.com/docs/en/agent-sdk/permissions) — the six-step SDK evaluation order (hooks → deny → ask → mode → allow → canUseTool), `allowed_tools`/`disallowed_tools`, permission mode table, subagent inheritance warning.
- [Hosting the Agent SDK](https://code.claude.com/docs/en/agent-sdk/hosting) — subprocess model, session patterns (ephemeral/long-running/hybrid/multi-agent), resource sizing, scaling formula, multi-tenant isolation, known limitations.

## Isolation technologies

- [gVisor documentation](https://gvisor.dev/docs/) — Sentry/Gofer architecture, syscall interception model, Docker/Kubernetes integration, performance tradeoffs.
- [Firecracker project site](https://firecracker-microvm.github.io/) — VMM architecture, jailer, vsock networking, boot time (~125ms) and memory overhead (<5 MiB) claims.
- [AWS Fargate security considerations](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-security-considerations.html) — per-task isolated infrastructure, no privileged containers, restricted Linux capabilities, no host access.

## AWS Lambda MicroVMs

- [AWS Lambda introduces MicroVMs (official blog)](https://aws.amazon.com/blogs/aws/run-isolated-sandboxes-with-full-lifecycle-control-aws-lambda-introduces-microvms/) — image-then-launch model, `aws lambda-microvms create-microvm-image`/`run-microvm` CLI, snapshot/resume mechanics, idle-policy suspension, regional availability (us-east-1, us-east-2, us-west-2, eu-west-1, ap-northeast-1), specs (up to 16 vCPU / 32 GB memory / 32 GB disk, ARM64, 8-hour max runtime), `X-aws-proxy-auth` per-session auth.
- [AWS Lambda MicroVMs product page](https://aws.amazon.com/lambda/lambda-microvms/) — positioning against regular Lambda functions, multi-tenant/agent use case framing.
- Confirmed launch date (June 22, 2026) and cross-checked technical claims against independent coverage (InfoQ, The Register) before treating the announcement as current rather than speculative — a new AWS service is exactly the kind of claim stage 2 flags for extra verification.

## Amazon ECS

- [Fargate task networking (`awsvpc` mode)](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-task-networking.html) — one ENI per task, containers in the same task share localhost.
- AWS re:Post threads and [containersonaws.com sidecar patterns](https://containersonaws.com/pattern/nginx-reverse-proxy-sidecar-ecs-fargate-task/) corroborating the sidecar-proxy-via-`HTTP_PROXY`-env-var pattern for Fargate tasks with restricted egress — used as a starting point, verified against AWS's own docs before being stated as a recommendation in ch18.

## Squid

- [Squid: `ssl_bump` configuration directive](https://www.squid-cache.org/Doc/config/ssl_bump/) and [Feature: SslBump Peek and Splice (wiki)](https://wiki.squid-cache.org/Features/SslPeekAndSplice) — step-based (`SslBump1`/`SslBump2`/`SslBump3`) bumping model, `peek`/`stare`/`splice`/`bump`/`terminate` actions.
- [Feature: Squid-in-the-middle SSL Bump (wiki)](https://wiki.squid-cache.org/Features/SslBump) — `http_port ssl-bump` options, `sslcrtd_program` certificate helper, legal/consent caveats around TLS interception.
- [Access Controls in Squid (wiki FAQ)](https://wiki.squid-cache.org/SquidFaq/SquidAcl) and [`acl` configuration directive](https://www.squid-cache.org/Doc/config/acl/) — ACL syntax for `dstdomain`, `ssl::server_name`, `http_access`.
- Configuration examples cross-checked against multiple independent 2026 walkthroughs (OneUptime's Ubuntu/RHEL SSL-bump guides) in addition to the project's own docs/wiki, since Squid's documentation is split across an aging wiki and a terse config reference — the actual `squid.conf` built in ch15 is verified by running it in the Docker lab, not copied from any single source.
- [`ubuntu/squid` image on Docker Hub](https://hub.docker.com/r/ubuntu/squid) — verified via Docker Hub's own registry API (not search results) before use, per the supply-chain-skepticism discipline in stage 2: Canonical-maintained, 47.9M+ pulls at time of writing.

## Package registry checks

- `claude-agent-sdk` on PyPI verified via [PyPI's JSON API](https://pypi.org/pypi/claude-agent-sdk/json) directly (`curl https://pypi.org/pypi/claude-agent-sdk/json`), not a search snippet, before pinning a version in `pyproject.toml`.

## Open questions / to verify per-chapter

- Exact current Envoy `credential_injector` filter config syntax (ch14) — needs its own doc fetch when that chapter is drafted.
- Exact current `aws-cli` version and Terraform AWS provider version supporting `aws_lambda_microvm_*`-equivalent resources, if any exist yet, vs. hand-rolled `aws lambda-microvms` CLI calls inside a null_resource/local-exec (ch19) — Terraform-native support for a service that launched days before this course was written is unlikely to exist yet; verify at drafting time and be explicit in the chapter if the IaC has to shell out to the CLI rather than use a native resource.
