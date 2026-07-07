from pathlib import Path

from nexus.dashboard.server import STATIC_DIR, backend


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    html_path = STATIC_DIR / "index.html"
    assert_true(html_path.exists(), "index.html should exist")

    html = html_path.read_text(encoding="utf-8")

    required = [
        "File Panel",
        "file-panel-grid",
        "Important Files",
        "Read-only project file navigation",
        "重要ファイル一覧",
        "docs一覧",
        "tools一覧",
        "scripts一覧",
        "prompts一覧",
        "ファイルインデックス",
    ]

    for item in required:
        assert_true(item in html, f"missing file panel text: {item}")

    for command in [
        "重要ファイル一覧",
        "docs一覧",
        "tools一覧",
        "scripts一覧",
        "prompts一覧",
        "ファイルインデックス",
    ]:
        result = backend.run_command(command)
        assert_true(result["ok"] is True, f"{command} should be allowed")
        assert_true(result["handled"] is True, f"{command} should be handled")
        assert_true("## File Index" in result["result"], f"{command} should return File Index output")

    print("Dashboard File Panel tests passed")


if __name__ == "__main__":
    main()
