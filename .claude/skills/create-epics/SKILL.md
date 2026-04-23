---
name: create-epics
description: "将已批准的 GDD 和架构转化为功能模块 —— 每个架构模块对应一个功能模块。定义范围、治理 ADR、引擎风险和未追踪的需求。不拆分为用户故事 —— 每个功能模块创建后运行 /create-stories [epic-slug]。"
argument-hint: "[system-name | layer: foundation|core|feature|presentation | all] [--review full|lean|solo]"
user-invocable: true
agent: technical-director
allowed-tools: Read, Glob, Grep, Write, Task, AskUserQuestion
---

**输出：** `production/epics/[epic-slug]/EPIC.md` + `production/epics/index.md`

**每个功能模
块完成后的下一步：** `/create-stories [epic-slug]`

**运行时机：** 在 `/create-control-manifest` 和 `/architecture-review` 通过后运行。

调用本技能时：

## 步骤 1：解析参数

解析评审模式（一次性解析，保存供本次运行的所有门禁调用使用）：
1. 若传入了 `--review [full|lean|solo]` → 使用该值
2. 否则读取 `production/review-mode.txt` → 使用其值
3. 否则 → 默认为 `lean`

**调用模式：**
- `/create-epics all` — 按层级顺序处理所有系统
- `/create-epics layer: foundation` — 仅处理 Foundation 层
- `/create-epics layer: core` — 仅处理 Core 层
- `/create-epics layer: feature` — 仅处理 Feature 层
- `/create-epics layer: presentation` — 仅处理 Presentation 层
- `/create-epics [system-name]` — 处理指定系统

若未提供其他参数，使用 `AskUserQuestion`：
- "为哪个系统或哪些系统创建功能模块？"
  - 选项：
    - `[A] 特定系统 —— 提供名称`
    - `[B] 按层级 —— foundation、core、feature 或 presentation`
    - `[C] 全部 —— 为所有 GDD 批准的系统创建功能模块`

将系统名称或层级过滤器保存为 **SCOPE**。

---

## 步骤 2：加载输入

### 2a：摘要扫描（所有模式）

始终加载：
- `design/gdd/systems-index.md` —— 系统列表、层级、状态
- `docs/architecture/` 中的架构概览文档（若存在）
- Glob `docs/architecture/adr-*.md` —— 读取所有 ADR 的摘要（仅标题和决策，而非全文）
- `docs/architecture/tr-registry.yaml` —— 当前需求跟踪
- `docs/architecture/control-manifest.md` —— 编程规则（分层）

若任何必需文件缺失（ADR、控制清单）：
> "未找到 [文件]。功能模块在没有治理文档的情况下创建将是不完整的。是否继续并将受影响的功能模块标记为 INCOMPLETE？"

### 2b：全量加载（每个功能模块创建时）

在定义每个功能模块时（步骤 4），加载完整内容：
- 该系统的完整 GDD：`design/gdd/[system-name].md`
- 该系统治理的 ADR 全文
- 若存在，引用该系统的 ADR 文本

---

## 步骤 3：处理顺序

若 SCOPE = `all` 或层级过滤器：

从系统索引中读取满足过滤条件的所有系统，按层级优先级排序：
1. Foundation
2. Core
3. Feature
4. Presentation

过滤出 GDD 状态为**已批准**或**已设计**的系统（不为未设计系统创建功能模块）。

呈现待处理列表：

```
将为以下系统创建功能模块（按层级顺序）：

Foundation 层：
  - [系统名称]（GDD：已批准）
  - [系统名称]（GDD：已批准）

Core 层：
  - [系统名称]（GDD：已批准）
  ...

每次一个功能模块，并在继续前显示每个功能模块供审批。
```

询问："继续吗？"

---

## 步骤 4：定义每个功能模块

**一次处理一个功能模块。** 在继续下一个之前获取批准。

### 对每个系统：

**4a：加载完整上下文**（来自步骤 2b）

读取系统 GDD 和所有相关 ADR。

**4b：制作人功能模块结构门禁**

**评审模式检查** —— 在生成 PD-EPIC-STRUCT 之前应用：
- `solo` → 跳过。注明："PD-EPIC-STRUCT 已跳过 —— 单人模式。"
- `lean` → 跳过。注明："PD-EPIC-STRUCT 已跳过 —— 精简模式。"
- `full` → 生成门禁。

若评审模式为 `full`：在起草功能模块文件之前，通过 Task 使用门禁 **PD-EPIC-STRUCT** 生成 `producer`。

传递：系统名称、GDD 路径、相关 ADR 列表、系统索引优先级条目。

处理裁定结果：
- `PD-EPIC-STRUCT PASS` → 用裁定摘要继续
- `PD-EPIC-STRUCT CONCERNS(producer)` → 在生成功能模块文件之前呈现顾虑并使用 AskUserQuestion 请求确认
- `PD-EPIC-STRUCT FAIL` → 停止。呈现失败原因并要求用户解决后重新运行

**4c：推导功能模块内容**

确定：

1. **层级**（来自系统索引）
2. **GDD 引用**：`design/gdd/[system-name].md`
3. **架构模块**：GDD 中定义该系统工作方式的代码模块或系统（例如"CombatSystem.gd"、"HealthComponent.cs"）
4. **治理 ADR**：架构中治理该系统实现的 ADR —— 逐个引用 `adr-XXXX-[name].md`
5. **GDD 需求**：从 GDD 或 TR 注册表中提取可追踪的 TRs。对于每个 TR：
   - TR-ID（`TR-[系统]-[编号]`格式）
   - 需求文本（来自 GDD）
   - 当前追踪状态（来自 TR 注册表：Untraced/Planned/In-Progress/Done）
6. **引擎风险**：读取治理 ADR 的"引擎兼容性"章节。若存在引擎风险条目（HIGH/MEDIUM），提取它们。
7. **完成定义**：该功能模块何时完成 —— 来自 GDD 验收标准章节（高层级；逐章节的验收标准将在故事中给出）
8. **范围外**：功能模块**不**包含什么 —— 这对于防止故事蔓延至关重要

若存在未追踪需求：
> "⚠️ [N] 个需求没有 ADR 覆盖。功能模块可以创建，但这些需求对应的故事将标记为 Blocked，直到 ADR 创建完成。优先运行 `/architecture-decision`，或继续并使用占位符。"

---

## 步骤 5：写入功能模块文件

**呈现功能模块草稿供审批后再写入任何文件**。

**5a：呈现功能模块摘要**

> ### 功能模块草稿：[Epic-Slug]
>
> | 字段 | 值 |
> |------|-----|
> | 层级 | [Foundation/Core/Feature/Presentation] |
> | GDD | `design/gdd/[system-name].md` |
> | 架构模块 | [模块或文件名] |
> | 治理 ADR | [adr-XXXX 列表] |
> | 引擎风险 | [HIGH：[描述] / 无] |
>
> **需求：** [TRs 列表，显示 ID + 一句话摘要 + 追踪状态]
>
> **完成定义：** [来自 GDD 验收标准的高层级条件]
>
> **范围外：** [明确的边界]

使用 `AskUserQuestion`：
- "批准 [system-name] 功能模块结构？"
  - 选项：
    - `[A] 批准 —— 写入功能模块文件`
    - `[B] 修改 —— 描述需要调整的内容`
    - `[C] 跳过此系统`

**5b：写入 EPIC.md**

批准后，询问："我可以将此功能模块写入 `production/epics/[epic-slug]/EPIC.md` 吗？"

写入时使用以下完整模板：

```markdown
# EPIC：[系统名称]

> **Slug**：[epic-slug]
> **层级**：[层级]
> **GDD**：design/gdd/[system-name].md
> **架构模块**：[模块名称]
> **状态**：规划中
> **用户故事**：待创建（运行 `/create-stories [epic-slug]`）

## 概述

[来自 GDD 概述章节的 2-3 句摘要，侧重于什么需要构建而非游戏设计。]

## 治理 ADR

| ADR | 决策 | 对本功能模块的影响 |
|-----|------|-----------------|
| [adr-XXXX-name.md] | [一句话决策] | [约束或需求] |

## GDD 需求

| TR-ID | 需求 | 追踪状态 |
|-------|------|---------|
| TR-[system]-001 | [需求文本] | Untraced |
| TR-[system]-002 | [需求文本] | Untraced |

## 引擎风险

[HIGH/MEDIUM/LOW]：[风险描述]

（若无，填写"无 —— 该系统使用已记录的引擎 API"）

## 完成定义

- [ ] 所有故事已通过 `/story-done` 完成审核并关闭
- [ ] [来自 GDD 验收标准的高层级条件]
- [ ] 所有逻辑/集成故事通过自动测试
- [ ] 所有视觉/感受故事通过手动验证
- [ ] 代码审查完成
- [ ] 无已知的 HIGH 严重性 bug

## 范围外

- [明确不在此功能模块范围内的内容]
- [常见误区或蔓延风险]

## 下一步

运行 `/create-stories [epic-slug]` 将本功能模块分解为可实现的故事。
```

**5c：更新功能模块索引**

写入每个功能模块后，检查 `production/epics/index.md` 是否存在。

若不存在：创建并包含表头：
```markdown
# 功能模块索引

| 功能模块 | 层级 | 系统 | GDD | 用户故事 | 状态 |
|---------|------|------|-----|---------|------|
```

追加该功能模块的行：
```
| [epic-slug] | [层级] | [系统名称] | design/gdd/[system].md | 待创建 | 规划中 |
```

询问："我可以更新 `production/epics/index.md` 中的功能模块索引吗？"

---

## 步骤 6：门禁检查提醒

所有功能模块创建后：
- **Foundation + Core 层完成后**：运行 `/gate-check production` 检查生产就绪状态。
- **提醒**：功能模块定义范围，故事定义实现步骤。在开发者开始工作前，为每个功能模块运行 `/create-stories [epic-slug]`。

若评审模式为 `full` 且任何功能模块的门禁收到 CONCERNS：

> **门禁摘要**
> - [N] 个功能模块通过，[N] 个有顾虑，[N] 个失败
> - 顾虑：[逐条列出未解决的顾虑]
>
> 在开始故事分解之前解决已标记的顾虑。

最后输出：

> **完成：[N] 个功能模块已写入。**
>
> 下一步：为每个功能模块运行 `/create-stories [epic-slug]`，或使用 `/sprint-plan` 在安排实现之前规划你的迭代。

---

## 协作协议

- **一次一个功能模块** —— 在继续下一个之前展示并获得批准。不批量写入未经审查的功能模块。
- **对差距进行警告** —— 若系统的 GDD 未批准、缺少 ADR 或 TRs 未追踪，在展示功能模块草稿时注明。
- **写入前询问** —— 始终在写入任何文件之前请求确认（`EPIC.md` 和 `index.md`）。
- **不要发明** —— 每个功能模块字段必须来自真实文档（GDD、ADR、TR 注册表、系统索引）。若信息缺失，将字段标记为 `[MISSING — 在继续前需要此信息]` 而不是猜测。
- **不创建故事** —— 本技能**只**创建功能模块文件。故事分解在每个功能模块之后通过 `/create-stories` 进行。永远不要在 `EPIC.md` 中创建故事文件或列出具体的故事。
