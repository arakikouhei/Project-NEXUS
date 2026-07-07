from nexus.dashboard.server import STATIC_DIR, backend


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    index_path = STATIC_DIR / "index.html"

    assert_true(index_path.exists(), "index.html should exist")

    html = index_path.read_text(encoding="utf-8")

    required_texts = [
        "Project NEXUS Dashboard",
        "Command Buttons",
        "NEXUS現在地",
        "システム健康診断",
        "記憶インデックス",
        "ファイルインデックス",
        "制作メモ一覧",
        "Safety: fixed safe commands only",
        "fetch(\"/api/status\")",
        "fetch(\"/api/run\"",
    ]

    for text in required_texts:
        assert_true(text in html, f"missing frontend text: {text}")

    status = backend.status()
    assert_true(status["ok"] is True, "backend status should be ok")

    result = backend.run_command("NEXUS現在地")
    assert_true(result["ok"] is True, "frontend command target should be allowed")
    assert_true(result["handled"] is True, "frontend command target should be handled")

    print("Dashboard Frontend tests passed")
    print("index size:", index_path.stat().st_size)
    print("safe_command_count:", status["safe_command_count"])


if __name__ == "__main__":
    main()
