from __future__ import annotations


def build_voice_mock_response(input_text: str) -> dict:
    text = input_text.strip()

    if not text:
        intent = "empty"
        response = "音声入力予定テキストが空です。"
    elif "今日" in text or "現在地" in text:
        intent = "today_status"
        response = "今日のNEXUSを表示する想定です。"
    elif "ダッシュボード" in text:
        intent = "dashboard_launch_guide"
        response = "ダッシュボード起動方法を案内する想定です。"
    elif "削除" in text or "git push" in text or "シェル" in text:
        intent = "dangerous_action"
        response = "危険操作の可能性があるため、音声だけでは実行しません。"
    else:
        intent = "general"
        response = "通常のNEXUS応答に渡す想定です。"

    return {
        "input_text": text,
        "recognized_intent": intent,
        "safe_to_auto_execute": intent not in {"dangerous_action"},
        "mock_response": response,
        "note": "実際の録音・読み上げはまだ行わないモックです。",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(build_voice_mock_response("今日のNEXUS"), ensure_ascii=False, indent=2))
