# CLAUDE.local.md 模板

将本文件复制到项目根目录并命名为 `CLAUDE.local.md`，用于个人偏好覆盖配置。
该文件已加入 .gitignore，不会被提交至版本库。

```markdown
# 个人偏好

## 模型偏好
- 复杂设计任务优先使用 Opus
- 快速查询与简单编辑使用 Haiku

## 工作流偏好
- 代码变更后始终运行测试
- 上下文使用达 60% 时主动压缩
- 不相关任务之间使用 /clear

## 本地环境
- Python 命令：python（或 py / python3）
- Shell：Windows 下的 Git Bash
- IDE：带 Claude Code 扩展的 VS Code

## 沟通风格
- 保持回复简洁
- 所有代码引用中显示文件路径
- 简要说明架构决策

## 个人快捷方式
- 当我说"review"时，对最近修改的文件执行 /code-review
- 当我说"status"时，显示 git status 与 sprint 进度
```

## 设置方法

1. 将本模板复制到项目根目录：`cp .claude/docs/CLAUDE-local-template.md CLAUDE.local.md`
2. 根据个人情况编辑
3. 确认 `CLAUDE.local.md` 已列入 `.gitignore`（Claude Code 从项目根目录读取该文件）
