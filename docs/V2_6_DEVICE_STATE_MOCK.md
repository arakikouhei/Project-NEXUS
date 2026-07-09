# Project NEXUS v2.6 デバイス状態管理モック

## 目的

v2.6では、実物センサーがなくても、球体AIデバイスの状態管理を疑似的に扱えるようにする。

## 実装対象

- nexus/device/state.py
- scripts/device_state_mock.py

## 管理する状態

- power
- battery_level
- temperature_c
- network
- storage
- safety
- mode

## 完了条件

`python3 scripts/device_state_mock.py` で状態JSONが表示される。
