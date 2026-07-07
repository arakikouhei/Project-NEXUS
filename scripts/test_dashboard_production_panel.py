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
        "Production Panel",
        "production-panel-grid",
        "Production Memos",
        "Search: Maya",
        "3DCG Check",
        "Maya Memos",
        "Creative production support",
        "制作メモ一覧",
        "制作メモ検索: Maya",
        "3DCG作業確認",
        "Maya作業メモ",
    ]

    for item in required:
        assert_true(item in html, f"missing production panel text: {item}")

    for command in [
        "制作メモ一覧",
        "制作メモ検索: Maya",
        "3DCG作業確認",
        "Maya作業メモ",
    ]:
        result = backend.run_command(command)
        assert_true(result["ok"] is True, f"{command} should be allowed")
        assert_true(result["handled"] is True, f"{command} should be handled")
        assert_true("## Production Support" in result["result"], f"{command} should return Production Support output")

    print("Dashboard Production Panel tests passed")


if __name__ == "__main__":
    main()
