---
name: adopt
description: 存量项目接入 —— 审计现有项目制品的模板格式合规性（不只是存在性），按影响分类缺口，并生成编号的迁移计划。当加入进行中的项目或从旧版本模板升级时运行。与 /project-stage-detect（检查存在的内容）不同 —— 本技能检查现有内容是否真正能与模板的技能一起工作。
argument-hint: "[focus: full | gdds | adrs | stories | infra]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, AskUserQuestion
agent: technical-director
---

# Adopt —— 存量项目接入本框架

本技能审计现有项目产物的**格式合规性**，确认它们是否真的能接入模板技能流水线，然后生成按优先级排序的迁移计划。

**这不是 `/project-stage-detect`。**
`/project-stage-detect` 回答：*存在什么？*
`/adopt` 回答：*现有内容是否真正能与模板技能一起工作？*

一个项目可能拥有 GDD、ADR 和用户故事 —— 但如果这些制品的内部格式不正确，所有格式敏感的技能仍然会静默失败或产生错误结果。

**输出：** `docs/adoption-plan-[日期].md` —— 一个持久化的、可勾选的迁移计划。

**参数模式：**

**审计模式：** `$ARGUMENTS[0]`（空白 = `full`）

- **无参数 / `full`**：完整审计 —— 所有制品类型
- **`gdds`**：仅 GDD 格式合规性
- **`adrs`**：仅 ADR 格式合规性
- **`stories`**：仅用户故事格式合规性
- **`infra`**：仅基础设施制品缺口（注册表、清单、迭代状态、stage.txt）

---

## 第 1 阶段：检测项目状态

在读取之前输出一行：`"正在扫描项目制品..."` —— 这在静默读取阶段确认技能正在运行。

然后静默读取，在呈现其他内容之前完成全部读取。

### 存在性检查
- `production/stage.txt` —— 若存在则读取（权威阶段）
- `design/gdd/game-concept.md` —— 游戏概念是否存在？
- `design/gdd/systems-index.md` —— 系统索引是否存在？
- 统计 GDD 文件数：`design/gdd/*.md`（排除 game-concept.md 和 systems-index.md）
- 统计 ADR 文件数：`docs/architecture/adr-*.md`
- 统计用户故事文件数：`production/epics/**/*.md`（排除 EPIC.md）
- `.claude/docs/technical-preferences.md` —— 引擎是否已配置？
- `docs/engine-reference/` —— 引擎参考文档是否存在？
- Glob `docs/adoption-plan-*.md` —— 若存在之前的计划文件，记录最新文件名

### 推断阶段（若无 stage.txt）
使用与 `/project-stage-detect` 相同的启发式方法：
- `src/` 中有 10 个以上源文件 → 生产
- `production/epics/` 中有用户故事 → 预制作
- ADR 存在 → 技术设置
- systems-index.md 存在 → 系统设计
- game-concept.md 存在 → 概念
- 什么都没有 → 全新项目（不是存量项目接入场景 —— 建议运行 `/start`）

若项目看起来是全新的（根本没有制品），使用 `AskUserQuestion`：
- "这看起来是一个全新项目 —— 未找到现有制品。`/adopt` 适用于有工作需要迁移的项目。你想做什么？"
  - "运行 `/start` —— 开始引导式首次上手"
  - "我的制品在非标准位置 —— 帮我找到它们"
  - "取消"

然后停止 —— 无论用户选择哪个选项，都不继续审计（每个选项通向不同的技能或手动调查）。

报告："检测到阶段：[阶段]。找到：[N] 个 GDD，[M] 个 ADR，[P] 个用户故事。"

---

## 第 2 阶段：格式审计

对于每种制品类型（基于参数模式），不只检查文件是否存在，还要检查它是否包含模板所需的内部结构。

### 2a：GDD 格式审计

对于找到的每个 GDD 文件，通过扫描标题检查 8 个必需章节：

| 必需章节 | 要查找的标题模式 |
|---|---|
| 概述 | `## Overview` |
| 玩家幻想 | `## Player Fantasy` |
| 详细规则 / 设计 | `## Detailed` 或 `## Core Rules` 或 `## Detailed Design` |
| 公式 | `## Formulas` 或 `## Formula` |
| 边界情况 | `## Edge Cases` |
| 依赖关系 | `## Dependencies` 或 `## Depends` |
| 调优旋钮 | `## Tuning` |
| 验收标准 | `## Acceptance` |

对于每个 GDD，记录：
- 哪些章节已存在
- 哪些章节缺失
- 已有章节是否有真实内容或只是占位符文本（`[待设计]` 或同等内容）

同时检查：每个 GDD 的标题块中是否有 `**Status**:` 字段？
有效值：`In Design`、`Designed`、`In Review`、`Approved`、`Needs Revision`。

### 2b：ADR 格式审计

对于找到的每个 ADR 文件，检查这些关键章节：

| 章节 | 缺失的影响 |
|---|---|
| `## Status` | **BLOCKING** —— `/story-readiness` 中的 ADR 状态检查会静默通过一切 |
| `## ADR Dependencies` | HIGH —— `/architecture-review` 中的依赖排序会出问题 |
| `## Engine Compatibility` | HIGH —— 截止日期后的 API 风险未知 |
| `## GDD Requirements Addressed` | MEDIUM —— 可追踪性矩阵丢失覆盖 |
| `## Performance Implications` | LOW —— 不影响流水线关键路径 |

对于每个 ADR，记录：哪些章节存在、哪些缺失、若 Status 章节存在则记录当前 Status 值。

### 2c：systems-index.md 格式审计

若 `design/gdd/systems-index.md` 存在：

1. **括号状态值** —— Grep 查找任何 Status 单元格包含括号的内容：
   `"Needs Revision ("`、`"In Progress ("` 等。
   这些会破坏 `/gate-check`、`/create-stories` 和 `/architecture-review` 中的精确字符串匹配。**BLOCKING。**

2. **有效状态值** —— 检查 Status 列值是否仅来自以下值：
   `Not Started`、`In Progress`、`In Review`、`Designed`、`Approved`、`Needs Revision`
   标记任何无法识别的值。

3. **列结构** —— 检查表格至少包含：系统名称、层级、优先级、状态列。缺少列会降低技能功能。

### 2d：用户故事格式审计

对于每个找到的用户故事文件：

- **`Manifest Version:` 字段** —— 是否在用户故事标题中存在？（LOW —— 缺失时自动通过）
- **TR-ID 引用** —— 用户故事是否包含 `TR-[a-z]+-[0-9]+` 模式？（MEDIUM —— 无法进行失效跟踪）
- **ADR 引用** —— 用户故事是否至少引用了一个 ADR？（检查 `ADR-` 模式）
- **Status 字段** —— 是否存在且可读？
- **验收标准** —— 用户故事是否有复选框列表（`- [ ]`）？

### 2e：基础设施审计

| 制品 | 路径 | 缺失的影响 |
|---|---|---|
| TR 注册表 | `docs/architecture/tr-registry.yaml` | HIGH —— 无稳定的需求 ID |
| 控制清单 | `docs/architecture/control-manifest.md` | HIGH —— 用户故事无层级规则 |
| 清单版本戳记 | 清单标题中：`Manifest Version:` | MEDIUM —— 失效检查盲目 |
| 迭代状态 | `production/sprint-status.yaml` | MEDIUM —— `/sprint-status` 回退到 markdown |
| 阶段文件 | `production/stage.txt` | MEDIUM —— 阶段自动检测不可靠 |
| 引擎参考 | `docs/engine-reference/[引擎]/VERSION.md` | HIGH —— ADR 引擎检查盲目 |
| 架构可追踪性 | `docs/architecture/architecture-traceability.md` | MEDIUM —— 无持久化矩阵 |

### 2f：技术偏好审计

读取 `.claude/docs/technical-preferences.md`。检查每个字段是否包含 `[TO BE CONFIGURED]`：
- 引擎、语言、渲染、物理 → HIGH（ADR 技能会失败）
- 命名规范 → MEDIUM
- 性能预算 → MEDIUM
- 禁止模式、允许的库 → LOW（设计上默认为空）

---

## 第 3 阶段：分类和排序缺口

将所有审计发现的缺口整理为四个严重性等级：

**BLOCKING** —— 现在就会导致模板技能静默产生错误结果。
示例：ADR 缺少 Status 字段，systems-index 有括号状态值，
引擎未配置但 ADR 已存在。

**HIGH** —— 会导致生成的用户故事缺少安全检查，或基础设施引导会失败。
示例：ADR 缺少 Engine Compatibility 章节，GDD 缺少验收标准
（无法从中生成用户故事），tr-registry.yaml 缺失。

**MEDIUM** —— 降低质量和流水线跟踪，但不中断功能。
示例：GDD 缺少调优旋钮或公式章节，用户故事缺少 TR-ID，
sprint-status.yaml 缺失。

**LOW** —— 事后改进，有则更好但不紧迫。
示例：用户故事缺少 Manifest Version 戳记，GDD 缺少开放问题章节。

统计每个等级的数量。若 BLOCKING 为零且 HIGH 为零：报告项目与模板兼容，只剩咨询性改进。

---

## 第 4 阶段：构建迁移计划

编写一个编号的、有序的行动计划。排序规则：
1. BLOCKING 缺口优先（在任何流水线技能可靠运行之前必须修复）
2. 其次是 HIGH 缺口，基础设施在 GDD/ADR 内容之前（引导需要正确格式）
3. MEDIUM 缺口排序：GDD 缺口在 ADR 缺口之前，ADR 缺口在用户故事缺口之前（用户故事依赖 GDD 和 ADR）
4. LOW 缺口最后

对于每个缺口，生成一个计划条目包含：
- 清晰的问题说明（一句话，无术语）
- 若有技能处理，则提供精确的修复命令
- 若需要直接编辑，则提供手动步骤
- 时间估算（粗略：5 分钟 / 30 分钟 / 1 个会话）
- 用于跟踪的复选框 `- [ ]`

**特殊情况 —— systems-index 括号状态值：**
若存在，这始终是第一项。显示需要更改的确切值和确切的替换文本。提议在写入计划之前立即修复。

**特殊情况 —— ADR 缺少 Status 字段：**
对于每个受影响的 ADR，修复方式为：
`/architecture-decision retrofit docs/architecture/adr-[NNNN]-[slug].md`
将每个 ADR 列为单独的可勾选条目。

**特殊情况 —— GDD 缺少章节：**
对于每个受影响的 GDD，列出缺少哪些章节及修复方式：
`/design-system retrofit design/gdd/[filename].md`

**基础设施引导排序** —— 始终按此顺序呈现：
1. 先修复 ADR 格式（注册表依赖于读取 ADR Status 字段）
2. 运行 `/architecture-review` → 引导 `tr-registry.yaml`
3. 运行 `/create-control-manifest` → 创建带有版本戳记的清单
4. 运行 `/sprint-plan update` → 创建 `sprint-status.yaml`
5. 运行 `/gate-check [阶段]` → 权威地写入 `stage.txt`

**现有用户故事** —— 明确说明：
> "现有用户故事可以与所有模板技能一起使用 —— 所有新的格式检查在字段缺失时会自动通过。
> 在重新生成之前，它们不会受益于 TR-ID 失效跟踪或清单版本检查。
> 这是有意为之：不要重新生成正在进行中的用户故事。"

---

## 第 5 阶段：呈现摘要并请求写入

在写入之前呈现一个紧凑的摘要：

```
## 接入审计摘要
检测到阶段：[阶段]
引擎：[已配置 / 未配置]
已审计 GDD：[N] 个（[X] 个完全合规，[Y] 个有缺口）
已审计 ADR：[N] 个（[X] 个完全合规，[Y] 个有缺口）
已审计用户故事：[N] 个

缺口数量：
  BLOCKING: [N] —— 没有这些修复，模板技能将出现故障
  HIGH:     [N] —— 运行 /create-stories 或 /story-readiness 不安全
  MEDIUM:   [N] —— 质量降级
  LOW:      [N] —— 可选改进

预计修复时间：[X 个 blocking 项 × 约 Y 分钟每项 = 大约 Z 小时]
```

在请求写入之前，显示**缺口预览**：
- 将每个 BLOCKING 缺口列为一行，描述实际问题
  （例如 `systems-index.md：3 行有括号状态值`，
  `adr-0002.md：缺少 ## Status 章节`）。不显示数量 —— 显示实际项目。
- 以数量显示 HIGH / MEDIUM / LOW（例如 `HIGH: 4, MEDIUM: 2, LOW: 1`）。

这让用户在提交写入文件之前有足够的上下文来判断范围。

若第 1 阶段发现了之前的接入计划，添加说明：
> "之前的计划存在于 `docs/adoption-plan-[之前日期].md`。新计划将反映当前项目状态 —— 不会与之前的运行进行差异比较。"

使用 `AskUserQuestion`：
- "准备好写入迁移计划了吗？"
  - "是 —— 写入 `docs/adoption-plan-[日期].md`"
  - "先给我看完整的计划预览（暂不写入）"
  - "取消 —— 我将手动处理迁移"

若用户选择"先给我看完整的计划预览"，以 fenced markdown 块的形式输出完整计划。然后再次询问相同的三个选项。

---

## 第 6 阶段：写入接入计划

若批准，将 `docs/adoption-plan-[日期].md` 写入以下结构：

```markdown
# 模板接入计划

> **生成时间**：[日期]
> **项目阶段**：[阶段]
> **引擎**：[名称 + 版本，或"未配置"]
> **模板版本**：v1.0+

按顺序完成以下步骤。完成每项时打勾。
随时运行 `/adopt` 检查剩余缺口。

---

## 步骤 1：修复 BLOCKING 缺口

[每个 blocking 缺口一个子章节，包含问题、修复命令、时间估算、复选框]

---

## 步骤 2：修复高优先级缺口

[每个 HIGH 缺口一个子章节]

---

## 步骤 3：引导基础设施

### 3a. 注册现有需求（创建 tr-registry.yaml）
运行 `/architecture-review` —— 即使 ADR 已经存在，本次运行也会从你现有的 GDD 和 ADR 引导 TR 注册表。
**时间**：1 个会话（审查对于大型代码库可能较长）
- [ ] tr-registry.yaml 已创建

### 3b. 创建控制清单
运行 `/create-control-manifest`
**时间**：30 分钟
- [ ] docs/architecture/control-manifest.md 已创建

### 3c. 创建迭代跟踪文件
运行 `/sprint-plan update`
**时间**：5 分钟（若迭代计划已以 markdown 形式存在）
- [ ] production/sprint-status.yaml 已创建

### 3d. 设置权威项目阶段
运行 `/gate-check [当前阶段]`
**时间**：5 分钟
- [ ] production/stage.txt 已写入

---

## 步骤 4：中优先级缺口

[每个 MEDIUM 缺口一个子章节]

---

## 步骤 5：可选改进

[每个 LOW 缺口一个子章节]

---

## 对现有用户故事的预期

现有用户故事可以与所有模板技能一起使用。新的格式检查在字段缺失时会自动通过 ——
因此不会有任何内容中断。在重新生成之前，它们不会受益于失效跟踪。
不要重新生成正在进行中或已完成的用户故事。

---

## 重新运行

完成步骤 3 后再次运行 `/adopt` 以验证所有 blocking 和 HIGH 缺口已解决。
新的运行将反映项目的当前状态。
```

---

## 第 6b 阶段：设置评审模式

写入接入计划后（或用户取消写入后），检查 `production/review-mode.txt` 是否存在。

**若存在**：读取并记录当前模式 —— "评审模式已设置为 `[当前值]`。" —— 跳过提示。

**若不存在**：使用 `AskUserQuestion`：

- **提示**："还有一个设置步骤：在工作流中工作时，你希望进行多少设计评审？"
- **选项**：
  - `Full（完整）` —— 主任专家在每个关键工作流步骤进行评审。最适合团队、学习工作流，或希望对每个决策进行彻底反馈时。
  - `Lean（精简，推荐）` —— 主任仅在阶段门禁过渡时（`/gate-check`）参与。跳过每个技能的评审。适合独立开发者和小团队的平衡选择。
  - `Solo（单独）` —— 完全无主任评审。最大化速度。最适合游戏果酱、原型，或评审感觉是负担时。

选择后立即写入 `production/review-mode.txt` —— 无需单独的"我可以写入吗？"：
- `Full（完整）` → 写入 `full`
- `Lean（精简，推荐）` → 写入 `lean`
- `Solo（单独）` → 写入 `solo`

若 `production/` 目录不存在则创建它。

---

## 第 7 阶段：提供第一步行动

写入计划后不要就此停止。选取单个最高优先级缺口，并使用 `AskUserQuestion` 立即提议处理。选择第一个适用的分支：

**若 systems-index.md 中有括号状态值：**
使用 `AskUserQuestion`：
- "最紧迫的修复是 `systems-index.md` —— [N] 行有括号状态值（例如 `Needs Revision (see notes)`），这些值现在就会破坏 /gate-check、/create-stories 和 /architecture-review。我可以直接修复这些。"
  - "现在修复 —— 编辑 systems-index.md"
  - "我自己修复"
  - "完成 —— 留下计划给我"

**若 ADR 缺少 `## Status`（且无括号问题）：**
使用 `AskUserQuestion`：
- "最紧迫的修复是为 [N] 个 ADR 添加 `## Status`：[列出文件名]。
  没有它，/story-readiness 会静默通过所有 ADR 检查。从 [第一个受影响的文件名] 开始？"
  - "是 —— 现在改造 [第一个受影响的文件名]"
  - "逐一改造全部 [N] 个 ADR"
  - "我自己处理 ADR"

**若 GDD 缺少验收标准（且无以上 blocking 问题）：**
使用 `AskUserQuestion`：
- "最紧迫的缺口是 [N] 个 GDD 缺少验收标准：[列出文件名]。
  没有验收标准，/create-stories 无法生成用户故事。从 [最高优先级 GDD 文件名] 开始？"
  - "是 —— 现在为 [GDD 文件名] 添加验收标准"
  - "逐一处理全部 [N] 个 GDD"
  - "我自己处理 GDD"

**若无 BLOCKING 或 HIGH 缺口：**
使用 `AskUserQuestion`：
- "无 blocking 缺口 —— 该项目与模板兼容。接下来做什么？"
  - "带我逐步完成中优先级改进"
  - "运行 /project-stage-detect 进行更广泛的健康检查"
  - "完成 —— 我将按自己的节奏完成计划"

---

## 协作协议

1. **静默读取** —— 在呈现任何内容之前完成完整审计
2. **先显示摘要** —— 让用户在请求写入之前了解范围
3. **写入前询问** —— 创建接入计划文件前始终确认
4. **提议，不强制** —— 计划只是建议；用户决定修复什么以及何时修复
5. **每次一个行动** —— 移交计划后，提供一个具体的下一步，而不是同时要做的六件事
6. **绝不重新生成现有制品** —— 只填补现有内容的缺口；
   不要重写已有内容的 GDD、ADR 或用户故事
