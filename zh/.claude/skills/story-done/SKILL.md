---
name: story-done
description: "Story 完成时的结尾验收。读取 Story 文件，逐条验证每项验收标准是否已实现，检查 GDD/ADR 偏差，提示代码评审，将 Story 状态更新为 Complete，并推荐下一个就绪 Story。"
argument-hint: "[story-file-path] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Edit, AskUserQuestion, Task
---

# Story 完成验收

本 skill 闭合设计与实现之间的循环。在完成任何 Story 的实现后运行它。
它确保在将 Story 标记为已完成之前，每项验收标准都经过验证；
GDD 和 ADR 偏差被明确记录而非悄然引入；
代码评审被提示而非遗忘；
Story 文件反映实际完成状态。

**输出：** 已更新的 Story 文件（Status: Complete）+ 推荐的下一个 Story。

---

## 阶段 1：找到 Story

解析评审模式（一次确定，本次运行所有关卡检查均使用该值）：
1. 如果传入了 `--review [full|lean|solo]` → 使用该值
2. 否则读取 `production/review-mode.txt` → 使用该值
3. 否则 → 默认使用 `lean`

完整的检查模式说明见 `.claude/docs/director-gates.md`。

**如果提供了文件路径**（如 `/story-done production/epics/core/story-damage-calculator.md`）：直接读取该文件。

**如果未提供参数：**

1. 检查 `production/session-state/active.md` 中当前活跃的 Story。
2. 如果未找到，读取 `production/sprints/` 中最新文件，查找标记为 IN PROGRESS 的 Story。
3. 如果找到多个进行中的 Story，使用 `AskUserQuestion`：
   - "我们要完成哪个 Story？"
   - 选项：列出进行中的 Story 文件名。
4. 如果找不到任何 Story，请用户提供路径。

---

## 阶段 2：读取 Story

完整读取 Story 文件。提取并保留上下文中的以下内容：

- **Story 名称和 ID**
- **GDD 需求 TR-ID**（如 `TR-combat-001`）
- **Manifest 版本**：嵌入在 Story 标题中（如 `2026-03-10`）
- **ADR 引用**
- **验收标准** — 完整列表（每条复选框项）
- **实现文件** — "需创建/修改的文件"列表
- **Story 类型** — Story 标题中的 `Type:` 字段（Logic / Integration / Visual/Feel / UI / Config/Data）
- **引擎注意事项** — 标注的引擎专项约束
- **完成定义** — 如果存在，Story 级别的 DoD
- **估算值与实际范围** — 如果有记录估算值

同时读取：
- `docs/architecture/tr-registry.yaml` — 查找 Story 中的每个 TR-ID。从注册表条目中读取*当前* `requirement` 文本。这是 GDD 所要求内容的权威来源——不要使用 Story 内联引用的需求文本（可能已过期）。
- 引用的 GDD 章节 — 仅查看验收标准和关键规则，不需要完整文档。用于交叉核对注册表文本是否仍然准确。
- 引用的 ADR — 仅查看 Decision 和 Consequences 部分
- `docs/architecture/control-manifest.md` 标题 — 提取当前的 `Manifest Version:` 日期（用于阶段 4 过期检查）

---

## 阶段 3：验证验收标准

对 Story 中的每项验收标准，尝试使用以下三种方法之一进行验证：

### 自动验证（无需询问直接运行）

- **文件存在检查**：使用 `Glob` 查找 Story 声明将创建的文件。
- **测试通过检查**：如果提到了测试文件路径，通过 `Bash` 运行它。
- **无硬编码值检查**：在游戏逻辑代码路径中 `Grep` 应存入配置文件的数字字面量。
- **无硬编码字符串检查**：在 `src/` 中 `Grep` 应在本地化文件中的面向玩家字符串。
- **依赖检查**：如果某条标准声明"依赖 X"，检查 X 是否存在。

### 需要确认的人工验证（使用 `AskUserQuestion`）

- 关于主观质量的标准（"响应流畅"、"动画正常播放"）
- 关于游戏行为的标准（"玩家受到伤害时..."、"敌人响应..."）
- 性能标准（"在 X 毫秒内完成"）——询问是否已进行性能分析，或接受为假设通过

将最多 4 个人工验证问题合并为一次 `AskUserQuestion` 调用：

```
question: "[标准]是否满足？"
options: "是——通过", "否——失败", "尚未测试"
```

### 无法验证（标记但不阻塞）

- 需要完整游戏构建才能测试的标准（端到端游戏场景）
- 标记为：`DEFERRED — 需要游戏测试会话`

### 测试标准追溯性

完成上述通过/失败/延迟检查后，将每项验收标准映射到覆盖它的测试：

对于 Story 中的每项验收标准：

1. 是否有测试——单元测试、集成测试或已确认的人工游戏测试——直接验证了该标准？
   - **单元测试**：在 `tests/unit/` 中 `Glob` 和 `Grep` 与标准主题匹配的测试文件或函数名
   - **集成测试**：类似地检查 `tests/integration/`
   - **人工确认**：如果通过 `AskUserQuestion` 以"是——通过"确认了该标准，计为人工测试

2. 生成追溯性表格：

```
| 标准 | 测试 | 状态 |
|------|------|------|
| AC-1: [标准文本] | tests/unit/test_foo.gd::test_bar | COVERED |
| AC-2: [标准文本] | 人工游戏测试确认 | COVERED |
| AC-3: [标准文本] | — | UNTESTED |
```

3. 应用以下升级规则：

   - 如果 **> 50% 的标准为 UNTESTED**：升级为 **BLOCKING** — 测试覆盖不足以确认 Story 实际完成。在覆盖改善之前，阶段 6 的结论不能为 COMPLETE。
   - 如果 **部分（≤ 50%）标准为 UNTESTED**：保持 ADVISORY — 不阻塞完成，但必须出现在完成注记中。
   - 如果 **所有标准均 COVERED**：除在报告中包含表格外无需额外操作。

4. 对于任何 ADVISORY 级别的未测试标准，在阶段 7 的完成注记中添加：
   `"未测试标准：[AC-N 列表]。建议在后续 Story 中补充测试。"`

### 测试证据要求

根据阶段 2 提取的 Story 类型，检查必要证据：

| Story 类型 | 必要证据 | 关卡级别 |
|---|---|---|
| **Logic** | `tests/unit/[系统]/` 中的自动化单元测试——必须存在并通过 | BLOCKING |
| **Integration** | `tests/integration/[系统]/` 中的集成测试 **或** 游戏测试文档 | BLOCKING |
| **Visual/Feel** | `production/qa/evidence/` 中的截图 + 签署确认 | ADVISORY |
| **UI** | 人工演练文档 **或** `production/qa/evidence/` 中的交互测试 | ADVISORY |
| **Config/Data** | `production/qa/smoke-*.md` 中的烟雾测试通过报告 | ADVISORY |

**对于 Logic Story**：首先读取 Story 的 **Test Evidence** 部分提取精确的必要文件路径。用 `Glob` 检查该精确路径。如果精确路径未找到，也在 `tests/unit/[系统]/` 中做广泛搜索（文件可能放在稍有不同的位置）。如果在两处均未找到测试文件：
- 标记为 **BLOCKING**："Logic Story 没有单元测试文件。Story 要求测试位于 `[来自 Test Evidence 部分的精确路径]`。在将 Story 标记为 Complete 之前，请创建并运行该测试。"

**对于 Integration Story**：读取 Story 的 **Test Evidence** 部分获取精确路径。先用 `Glob` 检查精确路径，然后在 `tests/integration/[系统]/` 中广泛搜索，再检查 `production/session-logs/` 中引用此 Story 的游戏测试记录。
如果均未找到：标记为 **BLOCKING**（规则同 Logic）。

**对于 Visual/Feel 和 UI Story**：在 `production/qa/evidence/` 中 glob 引用此 Story 的文件。如果没有：标记为 ADVISORY —
"未找到人工测试证据。在最终关闭前，使用测试证据模板创建 `production/qa/evidence/[story-slug]-evidence.md` 并获得签署确认。"

**对于 Config/Data Story**：检查是否存在任何 `production/qa/smoke-*.md` 文件。
如果没有：标记为 ADVISORY — "未找到烟雾测试报告。请运行 `/smoke-check`。"

**如果未声明 Story 类型**：标记为 ADVISORY —
"未声明 Story 类型。在 Story 标题中添加 `Type: [Logic|Integration|Visual/Feel|UI|Config/Data]`，以便在未来 Story 关闭时启用测试证据关卡执行。"

任何 BLOCKING 测试证据缺口都会阻止阶段 6 得出 COMPLETE 结论。

---

## 阶段 4：检查偏差

将实现与设计文档进行对比。

自动运行以下检查：

1. **GDD 规则检查**：使用来自 `tr-registry.yaml` 的当前需求文本（通过 Story 的 TR-ID 查找），检查实现是否符合 GDD 目前的要求——而非 Story 编写时的要求。用 `Grep` 在实现文件中搜索当前 GDD 章节中提到的关键函数名、数据结构或类名。

2. **Manifest 版本过期检查**：将 Story 标题中嵌入的 `Manifest Version:` 日期与当前 `docs/architecture/control-manifest.md` 标题中的 `Manifest Version:` 日期对比。
   - 如果匹配 → 静默通过。
   - 如果 Story 版本更旧 → 标记为 ADVISORY：
     `ADVISORY：Story 基于 manifest v[story-date] 编写；当前 manifest 为 v[current-date]。可能适用新规则。请运行 /story-readiness 检查。`
   - 如果 control-manifest.md 不存在 → 跳过此检查。

3. **ADR 约束检查**：读取引用的 ADR 的 Decision 部分。检查 `docs/architecture/control-manifest.md` 中的禁止模式（如果存在）。用 `Grep` 搜索 ADR 中明确禁止的模式。

4. **硬编码值检查**：在游戏逻辑的实现文件中 `Grep` 应放在数据文件中的数字字面量。

5. **范围检查**：实现是否触碰了 Story 声明范围之外的文件？（"需创建/修改的文件"列表之外的文件）

对每个发现的偏差进行分类：

- **BLOCKING** — 实现与 GDD 或 ADR 矛盾（标记为 Complete 之前必须修复）
- **ADVISORY** — 实现与规格存在轻微偏差但功能等效（记录，由用户决定）
- **OUT OF SCOPE** — 触碰了 Story 声明范围之外的额外文件（提醒注意——可能合理或属于范围蔓延）

---

## 阶段 4b：QA 覆盖关卡

**评审模式检查** — 在启动 QL-TEST-COVERAGE 前应用：
- `solo` → 跳过。注明："QL-TEST-COVERAGE 已跳过——Solo 模式。"继续执行阶段 5。
- `lean` → 跳过（非阶段关卡）。注明："QL-TEST-COVERAGE 已跳过——Lean 模式。"继续执行阶段 5。
- `full` → 正常启动。

完成阶段 4 的偏差检查后，通过 Task 使用关卡 **QL-TEST-COVERAGE**（`.claude/docs/director-gates.md`）启动 `qa-lead`。

传入：
- Story 文件路径和 Story 类型
- 阶段 3 中找到的测试文件路径（精确路径，或"未找到"）
- Story 的 `## QA Test Cases` 部分（Story 创建时预先编写的测试规格）
- Story 的 `## Acceptance Criteria` 列表

qa-lead 审查测试是否真正覆盖了规格内容——而不仅仅是文件是否存在。

应用结论：
- **ADEQUATE** → 继续执行阶段 5
- **GAPS** → 标记为 **ADVISORY**："QA 负责人发现覆盖缺口：[列表]。Story 可以完成，但应在后续 Story 中解决缺口。"
- **INADEQUATE** → 标记为 **BLOCKING**："QA 负责人：关键逻辑未经测试。在覆盖改善之前，结论不能为 COMPLETE。具体缺口：[列表]。"

Config/Data Story 跳过此阶段（不需要代码测试）。

---

## 阶段 5：首席程序员代码评审关卡

**评审模式检查** — 在启动 LP-CODE-REVIEW 前应用：
- `solo` → 跳过。注明："LP-CODE-REVIEW 已跳过——Solo 模式。"继续执行阶段 6（完成报告）。
- `lean` → 跳过（非阶段关卡）。注明："LP-CODE-REVIEW 已跳过——Lean 模式。"继续执行阶段 6（完成报告）。
- `full` → 正常启动。

通过 Task 使用关卡 **LP-CODE-REVIEW**（`.claude/docs/director-gates.md`）启动 `lead-programmer`。

传入：实现文件路径、Story 文件路径、相关 GDD 章节、适用的 ADR。

向用户展示结论。如果为 CONCERNS，通过 `AskUserQuestion` 呈现：
- 选项：`修改被标记的问题` / `接受并继续` / `进一步讨论`
如果为 REJECT，在问题解决之前不进入阶段 6 结论。

如果 Story 尚无实现文件（在编码完成前运行了结论），跳过此阶段并注明："LP-CODE-REVIEW 已跳过——未找到实现文件。请在实现完成后运行。"

---

## 阶段 6：展示完成报告

更新任何文件之前，先展示完整报告：

```markdown
## Story 完成：[Story 名称]
**Story**：[文件路径]
**日期**：[今日]

### 验收标准：[X/Y 通过]
- [x] [标准 1] — 自动验证（测试通过）
- [x] [标准 2] — 已确认
- [ ] [标准 3] — 失败：[原因]
- [?] [标准 4] — DEFERRED：需要游戏测试

### 测试标准追溯性
| 标准 | 测试 | 状态 |
|------|------|------|
| AC-1: [文本] | [测试文件::测试名称] | COVERED |
| AC-2: [文本] | 人工确认 | COVERED |
| AC-3: [文本] | — | UNTESTED |

### 测试证据
**Story 类型**：[Logic | Integration | Visual/Feel | UI | Config/Data | 未声明]
**必要证据**：[单元测试文件 | 集成测试或游戏测试 | 截图 + 签署确认 | 演练文档 | 烟雾测试通过报告]
**已找到证据**：[是 — `[路径]` | 否 — BLOCKING | 否 — ADVISORY]

### 偏差
[无] 或：
- BLOCKING：[描述] — [GDD/ADR 引用]
- ADVISORY：[描述] — 用户已接受 / 已标记为技术债务

### 范围
[所有变更均在声明范围内] 或：
- 额外触碰的文件：[列表] — [是否合理或属于范围蔓延]

### 结论：COMPLETE / COMPLETE WITH NOTES / BLOCKED
```

**结论定义：**
- **COMPLETE**：所有标准通过，无阻塞偏差
- **COMPLETE WITH NOTES**：所有标准通过，ADVISORY 偏差已记录
- **BLOCKED**：有失败标准或阻塞偏差，必须先解决

如果结论为 **BLOCKED**：不继续执行阶段 7。列出必须修复的内容。提供修复阻塞项的帮助。

---

## 阶段 7：更新 Story 状态

写入前询问："是否可以更新 Story 文件，将其标记为 Complete 并记录完成注记？"

如果同意，编辑 Story 文件：

1. 更新状态字段：`Status: Complete`
2. 在底部添加 `## Completion Notes` 部分：

```markdown
## Completion Notes
**完成时间**：[日期]
**标准**：[X/Y 通过]（[任何延迟项列表]）
**偏差**：[无] 或 [ADVISORY 偏差列表]
**测试证据**：[Logic：测试文件路径 | Visual/Feel：证据文档路径 | 不需要（Config/Data）]
**代码评审**：[待处理 / 完成 / 已跳过]
```

3. 如果存在 ADVISORY 偏差，询问："是否应将这些记录到 `docs/tech-debt-register.md` 的技术债务中？"

4. **更新 `production/sprint-status.yaml`**（如果存在）：
   - 找到匹配此 Story 文件路径或 ID 的条目
   - 设置 `status: done` 和 `completed: [今日日期]`
   - 更新顶层 `updated` 字段
   - 这是静默更新——无需额外批准（上一步已批准）

### 会话状态更新

更新 Story 文件后，静默追加到 `production/session-state/active.md`：

    ## 会话摘录 — /story-done [日期]
    - 结论：[COMPLETE / COMPLETE WITH NOTES / BLOCKED]
    - Story：[Story 文件路径] — [Story 标题]
    - 技术债务记录：[N 项，或"无"]
    - 推荐下一步：[下一个就绪 Story 的标题和路径，或"未识别到"]

如果 `active.md` 不存在，以此块作为初始内容创建文件。
在对话中确认："会话状态已更新。"

---

## 阶段 8：推荐下一个 Story

完成后，帮助开发者保持动力：

1. 从 `production/sprints/` 读取当前冲刺计划。
2. 找到以下状态的 Story：
   - 状态：READY 或 NOT STARTED
   - 未被其他未完成 Story 阻塞
   - 属于 Must Have 或 Should Have 层级

展示：

```
### 下一步
以下 Story 已就绪，可以开始：
1. [Story 名称] — [一行描述] — 估算：[X 小时]
2. [Story 名称] — [一行描述] — 估算：[X 小时]

开始前运行 `/story-readiness [路径]` 确认 Story 已具备实现条件。
```

如果本冲刺中没有更多 Must Have Story（全部 Complete 或 Blocked）：

```
### 冲刺收尾流程

所有 Must Have Story 已完成。推进之前需要 QA 签署确认。
按以下顺序运行：

1. `/smoke-check sprint` — 验证关键路径端到端仍可正常运行
2. `/team-qa sprint` — 完整 QA 周期：测试用例执行、缺陷分类、签署报告
3. `/gate-check` — QA 批准后推进到下一阶段

在 `/team-qa` 返回 APPROVED 或 APPROVED WITH CONDITIONS 之前，请勿运行 `/gate-check`。
```

如果仍有未开始的 Should Have Story，在收尾流程旁边一并展示，让用户选择：现在关闭冲刺，还是继续推进更多工作。

如果没有更多就绪 Story 但 Must Have Story 仍在进行中（尚未 Complete）：
"没有更多 Story 可开始——[N] 个 Must Have Story 仍在进行中。在冲刺收尾之前，继续完成这些 Story。"

---

## 协作协议

- **未经用户批准，不要将 Story 标记为完成** — 阶段 7 需要明确的"同意"才会编辑任何文件。
- **不要自动修复失败的标准** — 报告后询问如何处理。
- **偏差是事实，不是判断** — 中立地呈现；由用户决定是否可以接受。
- **BLOCKED 结论是建议性的** — 用户可以选择覆盖并直接标记为完成；如果这样做，明确记录风险。
- 对代码评审提示和批量人工标准确认使用 `AskUserQuestion`。

---

## 推荐下一步

- 运行 `/story-readiness [下一个-story-路径]` 在开始实现之前验证下一个 Story
- 如果所有 Must Have Story 已完成：运行 `/smoke-check sprint` → `/team-qa sprint` → `/gate-check`
- 如果记录了技术债务：通过 `/tech-debt` 追踪，保持债务登记册的更新
