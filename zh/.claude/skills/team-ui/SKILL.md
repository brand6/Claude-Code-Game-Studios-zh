---
name: team-ui
description: "通过完整的 UX 流水线编排 UI 团队：从 UX 规格说明书编写，经视觉设计、实现、评审，到打磨。集成 /ux-design、/ux-review 及工作室 UX 模板。"
argument-hint: "[UI 功能描述]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, AskUserQuestion, TodoWrite
---
调用此技能时，请通过结构化流水线编排 UI 团队。

**决策节点：** 在每个阶段切换处，使用 `AskUserQuestion` 将子代理的方案以可选项形式呈现给用户。在对话中写出代理的完整分析，然后用简洁标签捕获决策。用户必须批准后才能进入下一阶段。

## 团队组成

- **ux-designer** — 用户流程、线框图、无障碍性、输入处理
- **ui-programmer** — UI 框架、界面、部件、数据绑定、实现
- **art-director** — 视觉风格、布局打磨、与美术圣经保持一致
- **engine UI specialist** — 根据引擎特定最佳实践验证 UI 实现模式（从 `.claude/docs/technical-preferences.md` Engine Specialists → UI Specialist 中读取）
- **accessibility-specialist** — 在阶段4审计无障碍合规性

**此流水线使用的模板：**
- `ux-spec.md` — 标准界面/流程 UX 规格说明书
- `hud-design.md` — HUD 专属 UX 规格说明书
- `interaction-pattern-library.md` — 可复用交互模式
- `accessibility-requirements.md` — 已确定的无障碍等级及需求

## 如何委派

使用 Task 工具将每位团队成员作为子代理启动：
- `subagent_type: ux-designer` — 用户流程、线框图、无障碍性、输入处理
- `subagent_type: ui-programmer` — UI 框架、界面、部件、数据绑定
- `subagent_type: art-director` — 视觉风格、布局打磨、美术圣经一致性
- `subagent_type: [UI engine specialist]` — 引擎特定 UI 模式验证（例如 unity-ui-specialist、ue-umg-specialist、godot-specialist）
- `subagent_type: accessibility-specialist` — 无障碍合规性审计

始终在每个代理的提示中提供完整上下文（功能需求、现有 UI 模式、目标平台）。在流水线允许的情况下并行启动独立代理（例如，阶段4的评审代理可以同时运行）。

## 流水线

### 阶段 1a：上下文收集

设计任何内容之前，先读取并综合以下文档：
- `design/gdd/game-concept.md` — 平台目标与目标受众
- `design/player-journey.md` — 玩家到达此界面时的状态与情境
- 与此功能相关的所有 GDD UI 需求部分
- `design/ux/interaction-patterns.md` — 可复用的现有模式（不要重新发明）
- `design/accessibility-requirements.md` — 已确定的无障碍等级（例如基础、增强、完整）

**若 `design/ux/interaction-patterns.md` 不存在**，立即显示缺口：
> "interaction-patterns.md 不存在——没有现有模式可复用。"

然后使用 `AskUserQuestion` 提供选项：
- (a) 先运行 `/ux-design patterns` 建立模式库，然后继续
- (b) 不使用模式库继续——ui-programmer 将把创建的所有模式视为新模式，并在完成时添加到新的 `design/ux/interaction-patterns.md` 中

不要仅凭功能名称或 GDD 推断或假设模式。如果用户选择 (b)，请在阶段3中明确指示 ui-programmer 将所有模式视为新模式，并在实现完成时将它们记录在 `design/ux/interaction-patterns.md` 中。在最终摘要报告中注明模式库状态（已创建 / 缺失 / 已更新）。

将上下文以简报形式汇总给 ux-designer：玩家正在做什么、他们的需求、适用的约束，以及哪些现有模式相关。

### 阶段 1b：UX 规格说明书编写

调用 `/ux-design [feature name]` 技能，或直接委派给 ux-designer，按 `ux-spec.md` 模板生成 `design/ux/[feature-name].md`。

若设计 HUD，请使用 `hud-design.md` 模板而非 `ux-spec.md`。

> **特殊情况说明：**
> - 专门针对 HUD 设计时，使用 `argument: hud` 调用 `/ux-design`（例如 `/ux-design hud`）。
> - 对于交互模式库，在项目开始时运行一次 `/ux-design patterns`，并在后续阶段引入新模式时更新。

产出：`design/ux/[feature-name].md`，所有必要的规格部分均已填写。

### 阶段 1c：UX 评审

规格说明书完成后，调用 `/ux-review design/ux/[feature-name].md`。

**门控**：在结论为 APPROVED 之前，不得推进到阶段2。若结论为 NEEDS REVISION，ux-designer 必须解决标记的问题并重新运行评审。用户可以明确接受 NEEDS REVISION 的风险并继续，但这必须是有意识的决定——在询问是否继续之前，通过 `AskUserQuestion` 呈现具体问题。

### 阶段 2：视觉设计

委派给 **art-director**：
- 全面审查 UX 规格说明书（流程、线框图、交互模式、无障碍说明）——不仅限于线框图
- 从美术圣经应用视觉处理：颜色、字体排版、间距、动画风格
- 检查视觉设计是否保持无障碍合规：验证色彩对比度，确保颜色从不是表示状态的唯一指示器（形状、文字或图标必须加以强调）
- 明确列出美术流水线所需的所有资源需求：指定尺寸的图标、背景纹理、字体、装饰元素——附精确尺寸和格式要求
- 确保与现有已实现 UI 界面的一致性
- 产出：含样式说明和资源清单的视觉设计规格说明书

### 阶段 3：实现

实现开始之前，先启动 **engine UI specialist**（从 `.claude/docs/technical-preferences.md` Engine Specialists → UI Specialist 中获取），审查 UX 规格和视觉设计规格，提供引擎特定实现指导：
- 此界面应使用哪个引擎 UI 框架？（例如 Unity 中的 UI Toolkit vs UGUI，Godot 中的 Control nodes vs CanvasLayer，Unreal 中的 UMG vs CommonUI）
- 建议的布局或交互模式是否有引擎特定的注意事项？
- 适合该引擎的推荐部件/节点结构？
- 产出：引擎 UI 实现说明，供 ui-programmer 开始前参考

若未配置引擎，跳过此步骤。

委派给 **ui-programmer**：
- 按 UX 规格说明书和视觉设计规格说明书实现 UI
- **使用 `design/ux/interaction-patterns.md` 中的模式** — 不要重新发明已有规格的模式。若某模式基本合适但需修改，记录偏差并标记供 ux-designer 评审。
- **UI 绝不持有或修改游戏状态** — 仅负责显示；所有玩家操作均通过事件触发
- 所有文本通过本地化系统——不得硬编码面向玩家的字符串
- 同时支持两种输入方式（键盘/鼠标 以及 手柄）
- 按 `design/accessibility-requirements.md` 中确定的等级实现无障碍功能
- 将数据绑定连接到游戏状态
- **若在实现过程中创建了任何新交互模式**（即模式库中尚无的内容），在标记实现完成前将其添加到 `design/ux/interaction-patterns.md`
- 产出：已实现的 UI 功能

### 阶段 4：评审（并行）

并行委派：
- **ux-designer**：验证实现是否与线框图和交互规格一致。测试纯键盘和纯手柄导航。检查无障碍功能是否正常运行。
- **art-director**：验证视觉与美术圣经的一致性。在最低和最高支持分辨率下检查。
- **accessibility-specialist**：验证是否符合 `design/accessibility-requirements.md` 中记录的已确定无障碍等级。将任何违规标记为阻塞项。

三路评审流均必须报告后方可推进到阶段5。

### 阶段 5：打磨

- 处理所有评审反馈
- 验证动画可跳过并遵从玩家的减少动效偏好
- 确认 UI 音效通过音频事件系统触发（不得直接调用音频）
- 在所有支持的分辨率和宽高比下测试
- **验证 `design/ux/interaction-patterns.md` 是最新的** — 若在此功能实现过程中引入了任何新模式，确认已添加到模式库
- **确认所有 HUD 元素遵守 `design/ux/hud.md` 中定义的视觉预算**（元素数量、屏幕区域分配、最大不透明度值）

## 快速参考——何时使用哪个技能

- `/ux-design` — 从零开始为界面、流程或 HUD 编写新的 UX 规格说明书
- `/ux-review` — 在实现前验证已完成的 UX 规格说明书
- `/team-ui [feature]` — 从概念到打磨的完整流水线（内部调用 `/ux-design` 和 `/ux-review`）
- `/quick-design` — 不需要完整新 UX 规格说明书的小型 UI 变更

## 错误恢复协议

如果任何通过 Task 启动的代理返回 BLOCKED、发生错误或无法完成：

1. **立即显示**：在继续依赖阶段之前向用户报告"[AgentName]: BLOCKED — [原因]"
2. **评估依赖关系**：检查被阻塞代理的输出是否是后续阶段所必需的。如果是，在没有用户输入的情况下不得越过该依赖节点继续推进。
3. **通过 AskUserQuestion 提供选项**：
   - 跳过此代理并在最终报告中记录缺口
   - 以更窄范围重试
   - 在此停止并先解决阻塞项
4. **始终产出部分报告** — 输出已完成的内容。不要因为一个代理阻塞就丢弃工作。

常见阻塞项：
- 输入文件缺失（故事未找到、GDD 缺失）→ 重定向到创建它的技能
- ADR 状态为 Proposed → 不要实现；先运行 `/architecture-decision`
- 范围过大 → 通过 `/create-stories` 拆分为两个故事
- ADR 和故事之间的指令冲突 → 显示冲突，不要猜测

## 文件写入协议

所有文件写入（UX 规格说明书、交互模式库更新、实现文件）均委派给子代理和子技能（`/ux-design`、`ui-programmer`）。每个都执行"我可以写入 [path] 吗？"协议。此编排器不直接写入文件。

## 输出

涵盖以下内容的摘要报告：UX 规格状态、UX 评审结论、视觉设计状态、实现状态、无障碍合规性、输入方式支持、交互模式库更新状态，以及任何未解决问题。

结论：**COMPLETE** — UI 功能通过完整流水线交付（UX 规格 → 视觉 → 实现 → 评审 → 打磨）。
结论：**BLOCKED** — 流水线已停止；停止前显示阻塞项及其所在阶段。

## 下一步

- 若最终规格尚未通过审批，运行 `/ux-review`。
- 在关闭故事前对 UI 实现运行 `/code-review`。
- 若需要视觉或音频打磨，运行 `/team-polish`。
