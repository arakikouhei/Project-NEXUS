# Tool Stability v1

Tool Stability v1 adds diagnostics for tool routing and command collisions.

## Commands

- ツール順序
- ツール一覧
- ツール衝突チェック
- ツール診断: 画像分析: tests/assets/sample_vision.png

## Why

As Project NEXUS gains more tools, broad tools can accidentally capture inputs meant for specific tools.

Example:

- Vision command captured by CalculatorTool
- Help command captured by CapabilityTool
- File path command captured by TerminalTool or CalculatorTool

## Rule

Specific tools should be registered before broad tools.
