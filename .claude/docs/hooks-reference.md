# 活跃 Hooks

Hooks 在 `.claude/settings.json` 中配置，自动触发：

| Hook | 事件 | 触发时机 | 执行动作 |
| ---- | ----- | ------- | ------ |
| `validate-commit.sh` | PreToolUse (Bash) | `git commit` 命令 | 校验设计文档章节、JSON 数据文件、硬编码值、TODO 格式 |
| `validate-push.sh` | PreToolUse (Bash) | `git push` 命令 | 对受保护分支（develop/main）的推送发出警告 |
| `validate-assets.sh` | PostToolUse (Write/Edit) | 资产文件变更 | 检查 `assets/` 中文件的命名规范与 JSON 有效性 |
| `session-start.sh` | SessionStart | 会话开始 | 加载 sprint 上下文、里程碑、git 活动；检测并预览活跃会话状态文件以便恢复 |
| `detect-gaps.sh` | SessionStart | 会话开始 | 检测全新项目（建议运行 /start），以及代码/原型存在但文档缺失时建议运行 /reverse-document 或 /project-stage-detect |
| `pre-compact.sh` | PreCompact | 上下文压缩前 | 在压缩前将会话状态（active.md、已修改文件、WIP 设计文档）转储到对话中，确保内容在摘要后留存 |
| `post-compact.sh` | PostCompact | 压缩完成后 | 提醒 Claude 从 `active.md` 检查点恢复会话状态 |
| `notify.sh` | Notification | 通知事件 | 通过 PowerShell 显示 Windows 浮动通知 |
| `session-stop.sh` | Stop | 会话结束 | 汇总本次成果并更新会话日志 |
| `log-agent.sh` | SubagentStart | Agent 启动 | 审计日志开始 — 记录 subagent 调用及时间戳 |
| `log-agent-stop.sh` | SubagentStop | Agent 停止 | 审计日志结束 — 补全 subagent 记录 |
| `validate-skill-change.sh` | PostToolUse (Write/Edit) | Skill 文件变更 | 提示在任何 `.claude/skills/` 文件写入或编辑后运行 `/skill-test` |

Hook 参考文档：`.claude/docs/hooks-reference/`
Hook 输入 schema 文档：`.claude/docs/hooks-reference/hook-input-schemas.md`
