import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict
from urllib.parse import parse_qs, urlparse

from nexus.agent.agent import NexusAgent


HOST = "127.0.0.1"
PORT = 8765


SAFE_COMMANDS = {
    "NEXUS現在地",
    "NEXUS開発状況",
    "システム健康診断",
    "コマンド一覧",
    "おすすめ次操作",
    "記憶インデックス",
    "記憶の状態を教えて",
    "記憶レビュー",
    "ファイルインデックス",
    "重要ファイル一覧",
    "docs一覧",
    "tools一覧",
    "scripts一覧",
    "prompts一覧",
    "制作メモ一覧",
    "制作メモ検索: Maya",
    "3DCG作業確認",
    "Maya作業メモ",
}


class DashboardBackend:
    """Small local dashboard backend for safe NEXUS command execution."""

    def __init__(self) -> None:
        self.agent = NexusAgent()

    def run_command(self, command: str) -> Dict[str, Any]:
        command = command.strip()

        if not command:
            return {
                "ok": False,
                "handled": False,
                "error": "No command provided.",
                "result": "",
            }

        if command not in SAFE_COMMANDS:
            return {
                "ok": False,
                "handled": False,
                "error": "Command is not allowed in Dashboard Backend v1.",
                "result": "",
                "allowed_commands": sorted(SAFE_COMMANDS),
            }

        handled, result = self.agent.process(command)

        return {
            "ok": True,
            "handled": handled,
            "error": "",
            "command": command,
            "result": result or "",
        }

    def status(self) -> Dict[str, Any]:
        return {
            "ok": True,
            "name": "Project NEXUS Dashboard Backend",
            "version": "v1",
            "host": HOST,
            "port": PORT,
            "safe_command_count": len(SAFE_COMMANDS),
            "allowed_commands": sorted(SAFE_COMMANDS),
        }


backend = DashboardBackend()


class DashboardRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed = urlparse(self.path)

        if parsed.path == "/":
            self._send_text(self._index_html(), content_type="text/html; charset=utf-8")
            return

        if parsed.path == "/api/status":
            self._send_json(backend.status())
            return

        if parsed.path == "/api/run":
            params = parse_qs(parsed.query)
            command = params.get("command", [""])[0]
            self._send_json(backend.run_command(command))
            return

        self._send_json(
            {
                "ok": False,
                "error": "Not found.",
            },
            status=404,
        )

    def do_POST(self) -> None:
        parsed = urlparse(self.path)

        if parsed.path != "/api/run":
            self._send_json({"ok": False, "error": "Not found."}, status=404)
            return

        length = int(self.headers.get("Content-Length", "0") or "0")
        raw = self.rfile.read(length).decode("utf-8") if length else "{}"

        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            self._send_json({"ok": False, "error": "Invalid JSON."}, status=400)
            return

        command = str(payload.get("command", ""))
        self._send_json(backend.run_command(command))

    def log_message(self, format: str, *args: Any) -> None:
        # Keep terminal output simple during development.
        return

    def _send_json(self, payload: Dict[str, Any], status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_text(self, text: str, content_type: str = "text/plain; charset=utf-8") -> None:
        body = text.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _index_html(self) -> str:
        return """<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <title>Project NEXUS Dashboard Backend</title>
</head>
<body>
  <h1>Project NEXUS Dashboard Backend v1</h1>
  <p>Status: running</p>
  <p>API:</p>
  <ul>
    <li><code>/api/status</code></li>
    <li><code>/api/run?command=NEXUS現在地</code></li>
  </ul>
  <p>Safety: allowed commands only. No shell execution. No destructive actions.</p>
</body>
</html>
"""


def run_server(host: str = HOST, port: int = PORT) -> None:
    server = HTTPServer((host, port), DashboardRequestHandler)
    print("Project NEXUS Dashboard Backend")
    print(f"URL: http://{host}:{port}")
    print("Press Ctrl+C to stop.")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
