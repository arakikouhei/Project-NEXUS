from nexus.dashboard.server import SAFE_COMMANDS, backend


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    status = backend.status()

    assert_true(status["ok"] is True, "status ok should be true")
    assert_true(status["safe_command_count"] == len(SAFE_COMMANDS), "safe command count mismatch")
    assert_true("NEXUS現在地" in status["allowed_commands"], "NEXUS現在地 should be allowed")

    result = backend.run_command("NEXUS現在地")
    assert_true(result["ok"] is True, "NEXUS現在地 should be allowed")
    assert_true(result["handled"] is True, "NEXUS現在地 should be handled")
    assert_true("Current Stage" in result["result"], "result should include Current Stage")

    blocked = backend.run_command("rm -rf /")
    assert_true(blocked["ok"] is False, "dangerous command should be blocked")
    assert_true("not allowed" in blocked["error"], "blocked command should explain not allowed")

    empty = backend.run_command("")
    assert_true(empty["ok"] is False, "empty command should fail")
    assert_true("No command provided" in empty["error"], "empty command should explain missing command")

    print("Dashboard Backend tests passed")
    print("safe_command_count:", status["safe_command_count"])


if __name__ == "__main__":
    main()
