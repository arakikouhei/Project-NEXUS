# Project NEXUS v2.4 球体ディスプレイ表示モック

## 目的

v2.4では、実物ディスプレイがない状態でも、球体AIデバイスの表示内容をソフトウェア上で表現する。

## 実装対象

- nexus/device/sphere_display.py
- scripts/sphere_display_mock.py

## 表示モード

- boot
- idle
- listening
- thinking
- speaking
- warning
- error
- charging
- offline

## 表示内容

- 短い状態ラベル
- 絵文字
- 説明文
- 将来の小型ディスプレイ用テキスト
