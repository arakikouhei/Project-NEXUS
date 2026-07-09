# Project NEXUS v2.7 安全確認システム強化

## 目的

v2.7では、球体AIデバイス化に向けて危険操作を分類する。

## 実装対象

- nexus/device/safety.py
- scripts/device_safety_check.py

## 禁止または確認が必要な操作

- ファイル削除
- 任意シェル実行
- Git commit
- Git push
- 有料API呼び出し
- 外部送信
- 常時録音
- 常時カメラ使用
- バッテリー制御
- 冷却制御

## 方針

v3.0では、危険操作を実行せず、判定のみ行う。
