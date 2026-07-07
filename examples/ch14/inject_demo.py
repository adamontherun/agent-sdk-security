#!/usr/bin/env python3
"""The proxy pattern in about forty lines, with no Docker and no Squid.

This is the idea chapter 15 then builds for real: a client (standing in for the
agent) sends a request with no credential; a proxy in front of it injects the
credential and forwards; the upstream sees an authenticated request. The client
never held the secret.

Run it:  python3 examples/ch14/inject_demo.py
It starts a mock upstream and the injecting proxy on localhost, makes one
unauthenticated request through the proxy, and prints what each side saw.
"""

import json
import threading
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

INJECTED = "Bearer sk-demo-INJECTED-BY-PROXY"


def make_upstream():
    class Upstream(BaseHTTPRequestHandler):
        def do_GET(self):
            body = json.dumps({"authorization": self.headers.get("Authorization")})
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body.encode())

        def log_message(self, *args):
            pass  # keep the demo output clean

    return HTTPServer(("127.0.0.1", 0), Upstream)


def make_proxy(upstream_url):
    class Proxy(BaseHTTPRequestHandler):
        def do_GET(self):
            # Forward to the upstream, adding the credential the client omitted.
            req = urllib.request.Request(upstream_url, headers={"Authorization": INJECTED})
            with urllib.request.urlopen(req) as resp:  # noqa: S310 (localhost only)
                payload = resp.read()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, *args):
            pass

    return HTTPServer(("127.0.0.1", 0), Proxy)


def main() -> int:
    upstream = make_upstream()
    up_url = f"http://127.0.0.1:{upstream.server_address[1]}/"
    proxy = make_proxy(up_url)
    px_url = f"http://127.0.0.1:{proxy.server_address[1]}/"

    for server in (upstream, proxy):
        threading.Thread(target=server.serve_forever, daemon=True).start()

    # The client sends NO Authorization header.
    with urllib.request.urlopen(px_url) as resp:  # noqa: S310 (localhost only)
        seen = json.loads(resp.read())

    print("client sent Authorization:   None")
    print(f"upstream received:           {seen['authorization']}")
    ok = seen["authorization"] == INJECTED
    print("proxy injected the credential" if ok else "injection FAILED")

    upstream.shutdown()
    proxy.shutdown()
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
