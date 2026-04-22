# Claude Code Game Studios — 游戏工作室 Agent 架构

通过 48 个协同配合的 Claude Code 子智能体管理独立游戏开发。
每个 Agent 负责特定领域，强制执行职责分离与质量保证。

## 技术栈

- **引擎**：[选择：Godot 4 / Unity / Unreal Engine 5]
- **语言**：[选择：GDScript / C# / C++ / Blueprint]
- **版本控制**：Git，采用主干开发模式
- **构建系统**：[选定引擎后填写]
- **资产流水线**：[选定引擎后填写]

> **注意**：Godot、Unity 和 Unreal 均有对应的引擎专属 Agent 及其子专家 Agent。
> 请使用与你所选引擎匹配的 Agent 组。

## 项目结构

@.claude/docs/directory-structure.md

## 引擎版本参考

@docs/engine-reference/godot/VERSION.md

## 技术偏好配置

@.claude/docs/technical-preferences.md

## 协调规则

@.claude/docs/coordination-rules.md

## 协作协议

**以用户为主导的协作，而非自主执行。**
每个任务遵循：**提问 → 选项 → 决策 → 草稿 → 审批**

- Agent 在使用写入/编辑工具前，必须询问「可以将内容写入 [文件路径] 吗？」
- Agent 在请求审批前，必须展示草稿或摘要
- 多文件变更需要对完整变更集进行明确审批
- 没有用户指令不得提交

完整协议及示例请参阅 `docs/COLLABORATIVE-DESIGN-PRINCIPLE.md`。

> **首次使用？** 如果项目尚未配置引擎且没有游戏概念，
> 请运行 `/start` 开始引导式入门流程。

## 编码规范

@.claude/docs/coding-standards.md

## 上下文管理

@.claude/docs/context-management.md
