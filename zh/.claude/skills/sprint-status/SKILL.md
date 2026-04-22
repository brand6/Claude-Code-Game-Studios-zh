---
name: sprint-status
description: "快速冲刺状态检查。读取当前冲刺计划，扫描 Story 文件状态，生成简洁的进度快照及燃尽评估和新兴风险。可在冲刺任意时刻运行以快速了解全局。当用户问'冲刺进展如何'、'冲刺更新'、'显示冲刺进度'时使用。"
argument-hint: "[sprint-number or blank for current]"
user-invocable: true
allowed-tools: Read, Glob, Grep
model: haiku
---

# 冲刺状态

这是一个快速情况感知检查，而非冲刺回顾。它读取当前冲刺计划和 Story 文件，
扫描状态标记，并以不超过 30 行的格式生成简洁快照。
如需详细的冲刺管理，请使用 `/sprint-plan update` 或 `/milestone-review`。

**本 skill 为只读操作。** 它不提出变更、不要求写入文件，每次运行最多只给出一条具体建议。

---

## 1. 找到冲刺

**参数：** `$ARGUMENTS[0]`（空白 = 使用当前冲刺）

- 如果提供了参数（如 `/sprint-status 3`），在 `production/sprints/` 中搜索匹配 `sprint-03.md`、`sprint-3.md` 或类似名称的文件，并报告找到的文件。
- 如果没有提供参数，找到 `production/sprints/` 中最近修改的文件，将其视为当前冲刺。
- 如果 `production/sprints/` 不存在或为空，报告："未找到冲刺文件。请使用 `/sprint-plan new` 开始一个冲刺。"然后停止。

完整读取冲刺文件，提取：
- 冲刺编号和目标
- 开始日期和结束日期
- 所有 Story 或任务条目，含优先级（Must Have / Should Have / Nice to Have）、负责人和估算

---

## 2. 计算剩余天数

使用今日日期和冲刺文件中的结束日期，计算：
- 冲刺总天数（结束日期减开始日期）
- 已过天数
- 剩余天数
- 已消耗时间百分比

如果冲刺文件不含明确日期，注明"未找到冲刺日期——跳过燃尽评估。"

---

## 3. 扫描 Story 状态

**首先：检查 `production/sprint-status.yaml` 是否存在。**

如果存在，直接读取——它是状态的权威数据来源。
从 `status` 字段提取每个 Story 的状态，无需扫描 Markdown。
使用其 `sprint`、`goal`、`start`、`end` 字段，而非重新解析冲刺计划。

**如果 `sprint-status.yaml` 不存在**（遗留冲刺或首次使用），回退到 Markdown 扫描：

1. 如果条目引用了 Story 文件路径，检查文件是否存在。读取文件并扫描状态标记：DONE、COMPLETE、IN PROGRESS、BLOCKED、NOT STARTED（不区分大小写）。
2. 如果条目没有文件路径（冲刺计划中的内联任务），在冲刺计划本身中扫描该条目旁边的状态标记。
3. 如果未找到状态标记，归类为 NOT STARTED。
4. 如果引用了文件但文件不存在，归类为 MISSING 并记录。

使用回退方案时，在输出底部添加注意事项：
"⚠ 未找到 `sprint-status.yaml`——状态从 Markdown 推断。请运行 `/sprint-plan update` 生成状态文件。"

可选项（仅快速检查——不做深度扫描）：在 `src/` 中 grep 与 Story 的系统 slug 匹配的目录或文件名，检查是否有实现证据。这仅作参考，不作为确定性状态判断。

### 过期 Story 检测

收集所有 Story 状态后，对每个 IN PROGRESS 的 Story 检查过期情况：

- 对于每个有引用文件的 Story，读取文件并查找 frontmatter 或标题中的 `Last Updated:` 字段（如 `Last Updated: 2026-04-01` 或 `updated: 2026-04-01`）。接受任何合理的日期字段名：`Last Updated`、`Updated`、`last-updated`、`updated_at`。
- 使用今日日期计算距该日期的天数。
- 如果该日期超过 2 天前，将 Story 标记为 **STALE**（过期）。
- 如果 Story 文件中未找到日期字段，注明"无时间戳——无法检查过期情况"。
- 如果 Story 没有引用文件（内联任务），注明"内联任务——无法检查过期情况"。

STALE Story 将包含在输出表格中，并汇总到"需要关注"部分（见第 5 阶段输出格式）。

**过期 Story 升级处理**：如果任何 IN PROGRESS Story 被标记为 STALE，燃尽评估至少升级为 **At Risk**——即使完成百分比处于正常的 On Track 范围内。记录此升级原因："At Risk — [N] 个 Story [N] 天内无进展。"

---

## 4. 燃尽评估

计算：
- 已完成任务数（DONE 或 COMPLETE）
- 进行中任务数（IN PROGRESS）
- 受阻任务数（BLOCKED）
- 未开始任务数（NOT STARTED 或 MISSING）
- 完成百分比：（完成数 / 总数）× 100

通过将完成百分比与已消耗时间百分比对比来评估燃尽情况：

- **On Track（正常）**：完成百分比在已消耗时间百分比 10 个百分点以内或超前
- **At Risk（存在风险）**：完成百分比落后已消耗时间百分比 10–25 个百分点
- **Behind（落后）**：完成百分比落后已消耗时间百分比超过 25 个百分点

如果无法获取日期，跳过燃尽评估并报告"On Track / At Risk / Behind：未知——未找到冲刺日期。"

---

## 5. 输出

总输出不超过 30 行。使用以下格式：

```markdown
## Sprint [N] 状态 — [今日日期]
**冲刺目标**：[来自冲刺计划]
**剩余天数**：[总天数中的 N 天]（[% 已消耗时间]）

### 进度：[完成/总数]（[%]）

| Story / 任务         | 优先级     | 状态        | 负责人  | 阻塞原因       |
|----------------------|-----------|-------------|--------|---------------|
| [标题]              | Must Have | DONE        | [负责人]|               |
| [标题]              | Must Have | IN PROGRESS | [负责人]|               |
| [标题]              | Must Have | BLOCKED     | [负责人]| [简要原因]    |
| [标题]              | Should Have| NOT STARTED | [负责人]|               |

### 需要关注
| Story / 任务         | 状态        | 最后更新       | 过期天数   | 备注           |
|----------------------|-------------|---------------|-----------|----------------|
| [标题]              | IN PROGRESS | [日期或 N/A]  | [N 天]    | [STALE / 无时间戳——无法检查过期情况 / 内联任务——无法检查过期情况] |

*（如果没有 IN PROGRESS Story 过期或有时间戳问题，完全省略此部分。）*

### 燃尽：[On Track / At Risk / Behind]
[1-2 句话。如果落后：哪些 Must Have 面临风险。如果正常：确认并注明团队可考虑推进的 Should Have。]

### 面临风险的 Must Have
[列出所有 BLOCKED 或 NOT STARTED 且冲刺剩余时间不足 40% 的 Must Have Story。如果没有，写"无。"]

### 新兴风险
[通过 Story 扫描发现的任何风险：文件缺失、级联阻塞、无负责人的 Story。如果没有，写"未识别到风险。"]

### 建议
[一条具体行动，或"冲刺进展正常——无需操作。"]
```

---

## 6. 快速升级规则

在输出前应用这些规则，如果触发，则将标记放在输出最顶部（状态表格上方）：

**严重标记** — 如果 Must Have Story 处于 BLOCKED 或 NOT STARTED 状态且冲刺剩余时间不足 40%：

```
冲刺存在风险：[N] 个 Must Have Story 未完成，冲刺时间已消耗 [X]%。
建议使用 `/sprint-plan update` 重新规划。
```

**完成标记** — 如果所有 Must Have Story 都已 DONE：

```
所有 Must Have 已完成。团队可从 Should Have 待办列表中选取任务。
```

**缺失 Story 标记** — 如果任何引用的 Story 文件不存在：

```
注意：冲刺计划引用的 [N] 个 Story 文件缺失。
运行 `/story-readiness sprint` 验证 Story 文件覆盖情况。
```

---

## 协作协议

本 skill 为只读操作，仅报告磁盘上文件中观测到的事实。

- 不更新冲刺计划
- 不更改 Story 状态
- 不提议缩减范围（那是 `/sprint-plan update` 的职责）
- 每次运行最多给出一条建议

如需查看某个 Story 的详细信息，用户可直接读取 Story 文件或运行 `/story-readiness [路径]`。

如需冲刺重新规划，请使用 `/sprint-plan update`。
如需冲刺结束回顾，请使用 `/milestone-review`。
