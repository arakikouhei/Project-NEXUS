# Project NEXUS v2.2 今日の作業確認 / 次にやること

## 目的

v2.2では、ユーザーが次に何をするべきか迷わないようにする。

## 表示する情報

- 現在の開発段階
- 次の推奨作業
- 安全な保存手順
- ダッシュボード起動方法
- テストコマンド

## 実装対象

- nexus/daily/workflow.py
- scripts/nexus_today.py

## 完了条件

`python3 scripts/nexus_today.py` で、現在地と次の行動が表示される。
