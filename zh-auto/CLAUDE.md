# Claude Code Game Studios — 自动化游戏开发 Agent 架构

通过协同配合的 Claude Code 子智能体管理独立游戏开发。
用户主导创意与决策，AI 主导开发与测试。

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

## 目标用户

本框架的目标用户是**游戏策划**，对程序和美术有大概了解但不深入。
向用户呈现技术决策时，必须附带游戏体验层面的影响解释，避免使用未经说明的专业术语。

## 协作协议

**用户主导决策，AI 自主执行。**
每个任务分为两个阶段：

- **决策阶段**：用户深度参与，确定创意方向和设计决策
  - Agent 提出问题、呈现选项、解释权衡
  - 用户做出所有创意与战略决策
  - 设计文档需用户审批后写入
- **执行阶段**：AI 自主完成开发和测试
  - 需求冻结后，AI 自主拆分任务、编码、测试、提交
  - 仅在阻塞性问题时上报用户
  - 用户在最终验收时审查成果

完整协议及示例请参阅 `docs/COLLABORATIVE-DESIGN-PRINCIPLE.md`。

> **首次使用？** 如果项目尚未配置引擎且没有游戏概念，
> 请运行 `/start` 开始引导式入门流程。

## 编码规范

@.claude/docs/coding-standards.md

## 上下文管理

@.claude/docs/context-management.md
