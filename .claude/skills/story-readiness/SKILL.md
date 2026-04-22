---
name: story-readiness
description: "验证 Story 文件是否具备实现条件。检查是否嵌入了 GDD 需求、ADR 引用、引擎注意事项、清晰的验收标准，以及是否存在未解决的设计问题。给出 READY / NEEDS WORK / BLOCKED 结论及具体缺口列表。当用户问'这个 Story 准备好了吗'、'可以开始这个 Story 吗'、'Story X 是否可实现'时使用。"
argument-hint: "[story-file-path or 'all' or 'sprint']"
user-invocable: true
allowed-tools: Read, Glob, Grep, AskUserQuestion, Task
model: haiku
---

# Story 就绪性检查

本 skill 验证 Story 文件是否包含开发者开始实现所需的全部信息——
不会出现冲刺中途的设计中断、不需要猜测、没有模糊的验收标准。
在分配 Story 前运行。

**本 skill 为只读操作。** 它不编辑 Story 文件。它报告发现内容并询问用户是否需要帮助填补缺口。

**输出：** 每个 Story 的结论（READY / NEEDS WORK / BLOCKED）以及每个未就绪 Story 的具体缺口列表。

---

## 阶段 0：解析评审模式

在启动时解析一次评审模式（本次运行所有关卡检查均使用该值）：

1. 如果使用 `--review [full|lean|solo]` 调用 skill → 使用该值
2. 否则读取 `production/review-mode.txt` → 使用该值
3. 否则 → 默认使用 `lean`

完整的检查模式定义见 `.claude/docs/director-gates.md`。

---

## 1. 解析参数

**范围：** `$ARGUMENTS[0]`（空白 = 通过 AskUserQuestion 询问用户）

- **具体路径**（如 `/story-readiness production/epics/combat/story-001-basic-attack.md`）：验证该单个 Story 文件。
- **`sprint`**：从 `production/sprints/`（最新文件）读取当前冲刺计划，提取其引用的每个 Story 路径，逐一验证。
- **`all`**：glob `production/epics/**/*.md`，排除 `EPIC.md` 索引文件，验证找到的每个 Story 文件。
- **无参数**：询问用户验证范围。

如果未提供参数，使用 `AskUserQuestion`：
- "您希望验证什么？"
  - 选项：["特定 Story 文件"，"当前冲刺中的所有 Story"，"production/epics/ 中的所有 Story"，"特定 Epic 的 Story"]

继续前报告范围："正在验证 [N] 个 Story 文件。"

---

## 2. 加载支撑上下文

在检查任何 Story 之前，一次性加载参考文档（不逐 Story 重复加载）：

- `design/gdd/systems-index.md` — 了解哪些系统有已批准的 GDD
- `docs/architecture/control-manifest.md` — 了解存在哪些 manifest 规则
  （如果文件不存在，记录一次"文件缺失"；不要对每个 Story 重复标记）
  如果文件存在，也从标题块中提取 `Manifest Version:` 日期。
- `docs/architecture/tr-registry.yaml` — 按 `id` 索引所有条目。用于验证 Story 中的 TR-ID。如果文件不存在，记录一次；TR-ID 检查将对所有 Story 自动通过（注册表在 Story 之前就已存在，因此注册表缺失意味着 Story 早于 TR 追踪引入之前编写）。
- 所有 ADR 状态字段 — 对于被检查 Story 中引用的每个唯一 ADR，读取 ADR 文件并记录其 `Status:` 字段。缓存这些内容，以避免对每个 Story 重复读取相同的 ADR。
- 当前冲刺文件（如果范围为 `sprint`）— 用于识别 Must Have / Should Have 优先级以便升级决策

---

## 3. Story 就绪性清单

对于每个 Story 文件，评估以下每个检查项。只有所有检查项通过或明确标记为 N/A 并说明原因，Story 才算 READY。

### 设计完整性

- [ ] **已引用 GDD 需求**：Story 包含 `design/gdd/` 路径，并引用或链接了该 GDD 中的具体需求、验收标准或规则——而不仅仅是 GDD 文件名。链接到文档但未追溯到具体需求，不算通过。
- [ ] **需求自包含**：Story 中的验收标准在不打开 GDD 的情况下也能理解。开发者不应需要阅读单独的文档才能明白 DONE 是什么意思。
- [ ] **验收标准可测试**：每个标准是具体的、可观察的条件——而不是"实现 X"或"系统正常工作"。
  差例："实现跳跃机制。" 佳例："按住跳跃键时，0.3 秒内跳跃高度达到最大值 5 单位。"
- [ ] **无需判断的验收标准**：像"感觉响应灵敏"或"看起来不错"这样的标准，如果没有定义的基准就无法测试。必须替换为具体的可观察条件或游戏测试协议。

### 架构完整性

- [ ] **已引用 ADR 或说明 N/A**：Story 至少引用一个 ADR，**或**明确说明"不适用 ADR"及简要原因。
  既没有 ADR 引用也没有明确 N/A 说明的 Story，此项不通过。
- [ ] **ADR 状态为 Accepted（非 Proposed）**：对于每个引用的 ADR，使用第 2 节加载的缓存 ADR 状态检查其 `Status:` 字段。
  - 如果 `Status: Accepted` → 通过。
  - 如果 `Status: Proposed` → **BLOCKED**：ADR 可能在被接受之前发生变化，Story 的实现指导可能有误。
    修复：`BLOCKED: ADR-NNNN 状态为 Proposed——等待接受后再实现。`
  - 如果 ADR 文件不存在 → **BLOCKED**：引用的 ADR 缺失。
  - 如果 Story 有明确的"不适用 ADR"N/A 说明，自动通过。
- [ ] **TR-ID 有效且处于 active 状态**：如果 Story 包含 `TR-[系统]-NNN` 引用，在第 2 节加载的 TR 注册表中查找。
  - 如果 ID 存在且 `status: active` → 通过。
  - 如果 ID 存在且 `status: deprecated` 或 `status: superseded-by: ...` →
    NEEDS WORK：需求已被移除或替换。
    修复：更新 Story，引用当前需求 ID，或在不再适用时移除引用。
  - 如果 ID 在注册表中不存在 → NEEDS WORK：ID 未被注册
    （Story 可能早于注册表引入，或注册表需要运行 `/architecture-review`）。
  - 如果 Story 没有 TR-ID 引用，**或**注册表不存在，自动通过。
- [ ] **Manifest 版本为当前版本**：如果 Story 标题中有 `Manifest Version:` 日期，**且** `docs/architecture/control-manifest.md` 存在：
  - 如果 Story 版本与当前 manifest 的 `Manifest Version:` 匹配 → 通过。
  - 如果 Story 版本早于当前 manifest → NEEDS WORK：可能有新规则适用。修复：审查 manifest 变更规则，如果有禁止/必须条目发生变化则更新 Story，然后将 Story 的 `Manifest Version:` 更新为当前版本。
  - 如果 Story 没有 `Manifest Version:` 字段，**或** manifest 不存在，自动通过。
- [ ] **已注明引擎注意事项**：对于此 Story 可能会涉及的任何截止日期后引擎 API，包含实现注意事项或验证要求。如果 Story 明显不涉及引擎 API（如纯数据/配置变更），"N/A——不涉及引擎 API"可接受。
- [ ] **已注明 Control Manifest 规则**：引用了来自 control manifest 的相关层规则，**或**说明了"N/A——manifest 尚未创建"。如果 `docs/architecture/control-manifest.md` 尚不存在，此项自动通过（不对 manifest 创建之前编写的 Story 进行惩罚）。

### 范围清晰度

- [ ] **已提供估算**：Story 包含规模估算（小时、点数或 T 恤尺寸）。没有估算的 Story 无法计划。
- [ ] **已声明范围内/范围外边界**：Story 明确说明了它**不**包含的内容，要么在明确的"范围外"部分，要么在使边界明确无误的措辞中。缺少这一点，实现过程中很可能发生范围蔓延。
- [ ] **已列出 Story 依赖项**：如果此 Story 依赖其他 Story 先完成，那些 Story ID 已列出。如果没有依赖项，明确说明"无"（而不是简单地省略）。

### 未解决问题

- [ ] **无未解决的设计问题**：Story 中任何验收标准、实现注记或规则声明中不包含标记为"UNRESOLVED"、"TBD"、"TODO"、"?" 或类似标记的文本。
- [ ] **依赖 Story 不处于 DRAFT 状态**：对于列为依赖项的每个 Story，检查文件是否存在且不具有 DRAFT 状态。依赖于 DRAFT 或缺失 Story 的 Story 是 BLOCKED，不只是 NEEDS WORK。

### 资产引用检查

- [ ] **引用的资产存在**：扫描 Story 文本中的资产路径模式
  （包含 `assets/` 的路径，或扩展名为 `.png`、`.jpg`、`.svg`、`.wav`、`.ogg`、`.mp3`、`.glb`、`.gltf`、`.tres`、`.tscn`、`.res` 的文件）。
  - 对于找到的每个资产路径：使用 Glob 检查文件是否存在。
  - 如果任何引用的资产不存在：**NEEDS WORK** — 记录缺失路径。（Story 引用了尚未创建的资产。要么移除引用，要么创建占位符，要么将其标记为对资产创建 Story 的明确依赖。）
  - 如果所有引用的资产都存在：注明"引用的资产已验证：找到 [数量] 个。"
  - 如果 Story 中没有资产路径引用：注明"Story 中未找到资产引用——跳过资产检查。"此项自动通过。
  - 这是仅针对存在性的检查。不验证文件格式或内容。

### 完成定义

- [ ] **至少 3 个可测试的验收标准**：少于 3 个表明 Story 要么过于简单（它应该是一个 Story 吗？）要么规格不足。
- [ ] **如适用已注明性能预算**：如果此 Story 触及游戏循环、渲染或物理的任何部分，应有性能预算或"预计无性能影响——[原因]"的说明。
- [ ] **已声明 Story 类型**：Story 在标题中包含 `Type:` 字段，标识测试类别（Logic / Integration / Visual/Feel / UI / Config/Data）。没有此字段，就无法在 Story 关闭时强制执行测试证据要求。
  修复：在 Story 标题中添加 `Type: [Logic|Integration|Visual/Feel|UI|Config/Data]`。
- [ ] **测试证据要求明确**：如果已设置 Story 类型，Story 包含 `## Test Evidence` 部分，说明证据将存储在哪里（Logic/Integration 的测试文件路径，或 Visual/Feel/UI 的证据文档路径）。
  修复：添加 `## Test Evidence`，注明该 Story 类型的预期证据位置。

---

## 4. 结论分配

为每个 Story 分配以下三个结论之一：

**READY** — 所有清单项通过或有明确的 N/A 理由。
Story 可以立即分配。

**NEEDS WORK** — 一个或多个清单项不通过，但所有依赖 Story 都存在且不处于 DRAFT 状态。Story 可以在分配前修复。

**BLOCKED** — 一个或多个依赖 Story 缺失或处于 DRAFT 状态，**或**某个关键设计问题（在标准或规则中标记为 UNRESOLVED）没有负责人。Story 在阻塞项解决之前不能分配。注意：BLOCKED 的 Story 也可能有 NEEDS WORK 项——两者都要列出。

---

## 5. 输出格式

### 单 Story 输出

```
## Story 就绪性：[Story 标题]
文件：[路径]
结论：[READY / NEEDS WORK / BLOCKED]

### 通过的检查项（N/[总数]）
[简要列出通过项]

### 缺口
- [清单项]：[缺失或错误的具体描述]
  修复：[解决此缺口所需的具体文本]

### 阻塞项（如果 BLOCKED）
- [阻塞原因]：[必须先解决的 Story ID 或设计问题]
```

### 多 Story 汇总输出

```
## Story 就绪性摘要 — [范围] — [日期]

就绪：    [N] 个 Story
待完善：  [N] 个 Story
已阻塞：  [N] 个 Story

### 就绪的 Story
- [Story 标题]（[路径]）

### 待完善
- [Story 标题]：[主要缺口——一行]
- [Story 标题]：[主要缺口——一行]

### 已阻塞的 Story
- [Story 标题]：被 [Story ID / 设计问题] 阻塞

---
[每个未就绪 Story 的完整详情，使用单 Story 格式]
```

### 冲刺升级提示

如果范围为 `sprint` 且任何 Must Have Story 处于 NEEDS WORK 或 BLOCKED 状态，
在输出顶部添加醒目警告：

```
警告：[N] 个 Must Have Story 尚不具备实现条件。
[列出主要缺口或阻塞项。]
在冲刺开始前解决这些问题，或使用 `/sprint-plan update` 重新规划。
```

---

## 6. 协作协议

本 skill 为只读操作。它不提议编辑，也不要求写入文件。

报告发现内容后，提供：

"是否需要帮助填补这些 Story 的缺口？我可以起草缺失的部分供您审阅。"

如果用户对某个具体 Story 回答"是"，在对话中起草缺失的部分。
不使用 Write 或 Edit 工具——写入由用户（或 `/create-stories`）处理。

**重定向规则：**
- 如果 Story 文件完全不存在："此 Story 文件完全缺失。运行 `/create-epics [层]` 然后 `/create-stories [epic-slug]` 以从 GDD 和 ADR 生成 Story。"
- 如果 Story 没有 GDD 引用且工作量看起来较小："此 Story 没有 GDD 引用。如果变更较小（不超过约 4 小时），运行 `/quick-design [描述]` 创建快速设计规格，然后在 Story 中引用该规格。"
- 如果 Story 的范围已超出原始估算："此 Story 的范围似乎已扩大。考虑拆分或在实现开始前升级给制作人。"

---

## 7. 下一 Story 交接

完成单 Story 就绪性检查后（非 `all` 或 `sprint` 范围）：

1. 从 `production/sprints/`（最新）读取当前冲刺文件。
2. 查找满足以下条件的 Story：
   - 状态：READY 或 NOT STARTED
   - 不是刚刚检查的 Story
   - 未被未完成依赖项阻塞
   - 属于 Must Have 或 Should Have 层级

如果找到，最多显示 3 个：

```
### 本冲刺中其他就绪 Story

1. [Story 名称] — [单行描述] — 估算：[X 小时]
2. [Story 名称] — [单行描述] — 估算：[X 小时]

运行 `/story-readiness [路径]` 开始前先验证。
```

如果冲刺文件不存在或未找到其他就绪 Story，静默跳过此部分。

---

## 阶段 8：负责人门禁 — Story 就绪性评审

在生成 QL-STORY-READY 之前，应用阶段 0 中解析的评审模式：

- `solo` → 跳过。记录："QL-STORY-READY 已跳过——Solo 模式。"继续关闭。
- `lean` → 跳过。记录："QL-STORY-READY 已跳过——Lean 模式。"继续关闭。
- `full` → 正常生成。

通过 Task 以门禁 **QL-STORY-READY**（`.claude/docs/director-gates.md`）生成 `qa-lead`。

传入以下上下文：
- Story 标题
- 验收标准列表（Story 验收标准部分的所有条目）
- 依赖状态（所有列出的依赖项及其当前状态：存在 / DRAFT / 缺失）
- 总体结论（阶段 4 的 READY / NEEDS WORK / BLOCKED）

按 `director-gates.md` 中的标准规则处理结论：
- **ADEQUATE** → Story 已通过。继续关闭。
- **GAPS [列表]** → 通过 `AskUserQuestion` 向用户呈现具体缺口：
  选项：`使用建议缺口更新 Story` / `接受并继续` / `进一步讨论`。
- **INADEQUATE** → 呈现具体缺口；询问用户是否更新 Story 或继续。

---

## 推荐后续步骤

- 运行 `/dev-story [story-路径]` 在 Story 就绪后开始实现
- 运行 `/story-readiness sprint` 一次性检查当前冲刺中的所有 Story
- 如果 Story 文件完全缺失，运行 `/create-stories [epic-slug]`
