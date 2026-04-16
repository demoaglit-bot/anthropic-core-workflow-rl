import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

from environment import handle_request


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        status, headers, body = handle_request("GET", parsed.path)
        return self._send_response(status, headers, body)

    def do_POST(self):
        parsed = urlparse(self.path)
        status, headers, body = handle_request("POST", parsed.path, self._read_json())
        return self._send_response(status, headers, body)

    def _read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        if not raw:
            return {}
        return __import__("json").loads(raw.decode("utf-8") or "{}")

    def _send_response(self, status, headers, body):
        self.send_response(int(status))
        for header, value in headers.items():
            self.send_header(header, value)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8016"))
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Anthropic Core Workflow RL running at http://127.0.0.1:{port}")
    server.serve_forever()
