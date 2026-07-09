from __future__ import annotations


DISPLAY_STATES = {
    "boot": ("🟦", "BOOT", "NEXUS起動中"),
    "idle": ("🟢", "IDLE", "待機中"),
    "listening": ("👂", "LISTEN", "聞き取り予定"),
    "thinking": ("🧠", "THINK", "処理中"),
    "speaking": ("💬", "SPEAK", "応答予定"),
    "warning": ("🟡", "WARN", "確認が必要"),
    "error": ("🔴", "ERROR", "エラー"),
    "charging": ("🔋", "CHARGE", "充電中"),
    "offline": ("⚫", "OFFLINE", "オフライン"),
}


def render_display_state(mode: str = "idle") -> str:
    icon, label, message = DISPLAY_STATES.get(mode, DISPLAY_STATES["idle"])

    return "\n".join([
        "==============================",
        "NEXUS Sphere Display Mock",
        "==============================",
        f"{icon} {label}",
        message,
        "==============================",
    ])


if __name__ == "__main__":
    print(render_display_state("idle"))
