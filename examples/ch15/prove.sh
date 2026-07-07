#!/bin/sh
# Runs the four proofs chapter 15 builds up, against the live lab. Assumes the
# final config (squid.conf.step3-inject, which is what infra/squid/squid.conf
# holds after the chapter) is running: from the repo root,
#
#   sh infra/squid/gen-ca.sh          # once, to mint the proxy CA
#   docker compose up -d --build
#   sh examples/ch15/prove.sh
#
# Everything below is a real client on the lab network. No credential is ever
# passed on a client command line.
set -eu

NET=agent-sdk-security_lab
CERTS="$(cd "$(dirname "$0")/../../infra/squid/certs" && pwd)"
CURL="docker run --rm --network $NET curlimages/curl:latest"
CURL_CA="docker run --rm --network $NET -v $CERTS:/certs:ro curlimages/curl:latest"

# Once bumping is on (step 2 onward) every client must trust the proxy CA, even
# to reach an allowed domain, so these use --cacert. Before bumping was added
# (step 1) a plain client reached allowed domains with no CA at all.
echo "== 1. allowlist: an allowed domain succeeds =="
$CURL_CA -sS -o /dev/null -w "  example.com -> HTTP %{http_code}\n" \
  --cacert /certs/squid-ca.pem -x http://squid:3128 https://example.com

echo "== 2. allowlist: a domain not on the list is blocked =="
$CURL_CA -sS -o /dev/null -w "  ifconfig.me -> HTTP %{http_code}\n" \
  --cacert /certs/squid-ca.pem -x http://squid:3128 https://ifconfig.me || echo "  ifconfig.me -> blocked (connection failed, as intended)"

echo "== 3. bump: the client sees a cert our CA minted, and the proxy logs the URL =="
$CURL_CA -sS -v --cacert /certs/squid-ca.pem \
  -x http://squid:3128 https://httpbin.org/get 2>&1 \
  | grep -iE "subject:|issuer:" | sed 's/^/  /'

echo "== 4. injection: the client sent no Authorization; the upstream received one =="
echo "  -- local mock over plain HTTP --"
$CURL -sS -x http://squid:3128 http://mock-api/headers | grep -i authorization | sed 's/^ */  /'
echo "  -- httpbin.org over bumped HTTPS --"
$CURL_CA -sS --cacert /certs/squid-ca.pem \
  -x http://squid:3128 https://httpbin.org/headers | grep -i authorization | sed 's/^ */  /'
