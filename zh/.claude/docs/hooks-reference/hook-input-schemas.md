# Hook 输入/输出 Schema

本文档记录了每种事件类型中，Claude Code Hook 通过标准输入（stdin）接收到的 JSON 载荷格式。

## PreToolUse

在工具执行前触发。可以**允许**（退出码 0）或**阻断**（退出码 2）。

### PreToolUse: Bash

```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "git commit -m 'feat: add player health system'",
    "description": "Commit changes with message",
    "timeout": 120000
  }
}
```

### PreToolUse: Write

```json
{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "src/gameplay/health.gd",
    "content": "extends Node\n..."
  }
}
```

### PreToolUse: Edit

```json
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "src/gameplay/health.gd",
    "old_string": "var health = 100",
    "new_string": "var health: int = 100"
  }
}
```

### PreToolUse: Read

```json
{
  "tool_name": "Read",
  "tool_input": {
    "file_path": "src/gameplay/health.gd"
  }
}
```

## PostToolUse

在工具完成后触发。**无法阻断**（退出码对阻断无效）。标准错误输出（stderr）的消息会以警告形式显示。

### PostToolUse: Write

```json
{
  "tool_name": "Write",
  "tool_input": {
    "file_path": "assets/data/enemy_stats.json",
    "content": "{\"goblin\": {\"health\": 50}}"
  },
  "tool_output": "File written successfully"
}
```

### PostToolUse: Edit

```json
{
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "assets/data/enemy_stats.json",
    "old_string": "\"health\": 50",
    "new_string": "\"health\": 75"
  },
  "tool_output": "File edited successfully"
}
```

## SubagentStart

在通过 Task 工具派生子 Agent 时触发。

```json
{
  "agent_name": "game-designer",
  "model": "sonnet",
  "description": "Design the combat healing mechanic"
}
```

## SessionStart

在 Claude Code 会话开始时触发。**无标准输入**——Hook 直接运行，其标准输出作为上下文展示给 Claude。

## PreCompact

在上下文窗口压缩前触发。**无标准输入**——Hook 在压缩发生前运行以保存状态。

## Stop

在 Claude Code 会话结束时触发。**无标准输入**——Hook 运行以执行清理和日志记录。

## 退出码参考

| 退出码 | 含义 | 适用事件 |
|-------|------|---------|
| 0 | 允许 / 成功 | 所有事件 |
| 2 | 阻断（stderr 显示给 Claude） | 仅 PreToolUse |
| 其他 | 视为错误，工具继续执行 | 所有事件 |

## 注意事项

- Hook 通过**标准输入（stdin）管道**接收 JSON。使用 `INPUT=$(cat)` 进行捕获。
- 若 `jq` 可用则用其解析，否则退而使用 `grep` 以兼容跨平台场景。
- 在 Windows 上，`grep -P`（Perl 正则）通常不可用，改用 `grep -E`（POSIX 扩展正则）。
- Windows 上路径分隔符可能为 `\`，比较路径时可用 `sed 's|\\|/|g'` 进行规范化。
