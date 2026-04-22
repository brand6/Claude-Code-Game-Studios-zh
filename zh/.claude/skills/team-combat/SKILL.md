---
name: team-combat
description: "编排战斗团队：协调 game-designer、gameplay-programmer、ai-programmer、technical-artist、sound-designer 和 qa-tester，从设计到实现再到验证，端到端完成一个战斗功能。"
argument-hint: "[combat feature description]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, AskUserQuestion, TodoWrite
---
**参数检查：** 如果未提供战斗功能描述，输出：
> "用法：`/team-combat [战斗功能描述]` — 提供要设计和实现的战斗功能描述（如 `melee parry system`、`ranged weapon spread`）。"
然后立即停止，不启动任何子 Agent，不读取任何文件。

当本 skill 以有效参数调用时，按结构化流水线编排战斗团队。

**决策节点：** 在每个阶段切换时，使用 `AskUserQuestion` 将子 Agent 的方案以可选项的形式呈现给用户。在对话中完整展示 Agent 的分析，然后以简洁标签捕捉决策。用户批准后才能进入下一阶段。

## 团队构成
- **game-designer** — 设计机制，定义公式和边缘情况
- **gameplay-programmer** — 实现核心游戏玩法代码
- **ai-programmer** — 实现 NPC/敌人 AI 行为
- **technical-artist** — 创建视觉效果、着色器特效和视觉反馈
- **sound-designer** — 定义音频事件、冲击音效和环境战斗音频
- **引擎专家**（主要）— 验证架构和实现方案符合引擎惯例（从 `.claude/docs/technical-preferences.md` 引擎专家部分读取）
- **qa-tester** — 编写测试用例并验证实现

## 如何委派

使用 Task 工具将每个团队成员作为子 Agent 启动：
- `subagent_type: game-designer` — 设计机制，定义公式和边缘情况
- `subagent_type: gameplay-programmer` — 实现核心游戏玩法代码
- `subagent_type: ai-programmer` — 实现 NPC/敌人 AI 行为
- `subagent_type: technical-artist` — 创建视觉效果、着色器特效、视觉反馈
- `subagent_type: sound-designer` — 定义音频事件、冲击音效、环境音频
- `subagent_type: [primary engine specialist]` — 验证架构和实现方案的引擎惯例
- `subagent_type: qa-tester` — 编写测试用例并验证实现

在每个 Agent 的提示中始终提供完整上下文（设计文档路径、相关代码文件、约束条件）。在流水线允许的情况下并行启动独立 Agent（如第 3 阶段的 Agent 可以同时运行）。

## 流水线

### 阶段 1：设计
委派给 **game-designer**：
- 在 `design/gdd/` 中创建或更新设计文档，覆盖：机制概述、玩家幻想、详细规则、含变量定义的公式、边缘情况、依赖关系、含安全范围的调整参数，以及验收标准
- 输出：完成的设计文档

### 阶段 2：架构
委派给 **gameplay-programmer**（如涉及 AI 则同时委派 **ai-programmer**）：
- 审查设计文档
- 设计代码架构：类结构、接口、数据流
- 识别与现有系统的集成点
- 输出：含文件列表和接口定义的架构草图

然后启动**主引擎专家**验证提议的架构：
- 类/节点/组件结构对当前固定引擎是否符合惯例？（如 Godot 节点层级、Unity MonoBehaviour 与 DOTS、Unreal Actor/Component 设计）
- 是否有应使用的引擎原生系统，而非自定义实现？
- 提议的 API 中是否有在当前固定引擎版本中已弃用或变更的？
- 输出：引擎架构注意事项——在阶段 3 开始前整合到架构中

### 阶段 3：实现（尽可能并行）
并行委派：
- **gameplay-programmer**：实现核心战斗机制代码
- **ai-programmer**：实现 AI 行为（如功能涉及 NPC 反应）
- **technical-artist**：创建视觉效果和着色器特效
- **sound-designer**：定义音频事件列表和混音注意事项

### 阶段 4：集成
- 将游戏玩法代码、AI、视觉效果和音频整合在一起
- 确保所有调整参数已暴露且由数据驱动
- 验证功能与现有战斗系统协同工作

### 阶段 5：验证
委派给 **qa-tester**：
- 根据验收标准编写测试用例
- 测试设计文档中记录的所有边缘情况
- 验证性能影响在预算范围内
- 提交发现的问题缺陷报告

### 阶段 6：签署确认
- 收集所有团队成员的结果
- 报告功能状态：COMPLETE / NEEDS WORK / BLOCKED
- 列出所有未解问题及其负责人

## 错误恢复协议

如果任何通过 Task 启动的 Agent 返回 BLOCKED、报错或无法完成：

1. **立即上报**：在继续依赖阶段之前，向用户报告"[AgentName]: BLOCKED — [原因]"
2. **评估依赖关系**：检查被阻塞 Agent 的输出是否为后续阶段所必需。如果是，在没有用户输入的情况下不要越过该依赖点继续。
3. **通过 AskUserQuestion 提供选项**：
   - 跳过此 Agent 并在最终报告中记录缺口
   - 以更小范围重试
   - 在此停止，先解决阻塞项
4. **始终生成部分报告** — 输出所有已完成的工作。不要因为一个 Agent 被阻塞就丢弃工作成果。

常见阻塞原因：
- 输入文件缺失（Story 未找到、GDD 不存在）→ 重定向到创建该文件的 skill
- ADR 状态为 Proposed → 不实现；先运行 `/architecture-decision`
- 范围过大 → 通过 `/create-stories` 拆分为两个 Story
- ADR 与 Story 之间存在冲突指令 → 浮现冲突，不猜测

## File Write Protocol

所有文件写入（设计文档、实现文件、测试用例）均委派给通过 Task 启动的子 Agent。
每个子 Agent 执行"我可以写入 [path] 吗？"协议。此编排者不直接写入文件。

## Output

摘要报告，涵盖：设计完成状态、每位团队成员的实现状态、测试结果，以及所有未解问题。

结论：**COMPLETE** — 战斗功能已设计、实现并验证。
结论：**BLOCKED** — 一个或多个阶段无法完成；已生成部分报告，未解问题已列出。

## Next Steps

- 在关闭 Story 前，对已实现的战斗代码运行 `/code-review`。
- 运行 `/balance-check` 验证战斗公式和调整参数。
- 如果 VFX、音频或性能打磨有需要，运行 `/team-polish`。
