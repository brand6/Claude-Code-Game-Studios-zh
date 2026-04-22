# settings.local.json 模板

创建 `.claude/settings.local.json` 用于个人本地覆盖配置，此文件**不应**提交到版本控制。
请将其加入 `.gitignore`。

## settings.local.json 示例

```json
{
  "permissions": {
    "allow": [
      "Bash(git *)",
      "Bash(npm *)",
      "Read",
      "Glob",
      "Grep"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(git push --force *)"
    ]
  }
}
```

## 权限模式

Claude Code 支持多种权限模式。游戏开发推荐配置如下：

### 开发阶段（默认）
使用**普通模式**——Claude 在运行大多数命令前会询问确认。这对生产代码最为安全。

### 原型开发阶段
使用**有限范围自动接受模式**——对一次性代码进行更快的迭代。
仅在 `prototypes/` 目录中工作时使用此模式。

### 代码评审阶段
使用**只读**权限——Claude 只能读取和搜索文件，不能修改。

## 本地自定义 Hooks

你可以在 `settings.local.json` 中添加个人专属 hooks，用于扩展（而非覆盖）项目 hooks。
例如，在构建完成时发送通知：

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'echo Session ended at $(date)'",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```
