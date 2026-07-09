from __future__ import annotations


DANGEROUS_KEYWORDS = [
    "rm -rf",
    "delete",
    "削除",
    "git commit",
    "git push",
    "os.system",
    "subprocess",
    "shell=True",
    "有料API",
    "外部送信",
    "常時録音",
    "常時カメラ",
    "バッテリー制御",
    "冷却制御",
]


def classify_action(action_text: str) -> dict:
    text = action_text.strip()
    lower_text = text.lower()

    matched = []
    for keyword in DANGEROUS_KEYWORDS:
        target = keyword.lower()
        if target in lower_text:
            matched.append(keyword)

    if matched:
        return {
            "action": text,
            "safety_level": "requires_user_confirmation",
            "auto_execute": False,
            "matched_keywords": matched,
            "reason": "危険または高リスク操作の可能性があります。",
        }

    return {
        "action": text,
        "safety_level": "safe_mock",
        "auto_execute": True,
        "matched_keywords": [],
        "reason": "モック上では安全な確認操作として扱えます。",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(classify_action("今日のNEXUSを表示"), ensure_ascii=False, indent=2))
