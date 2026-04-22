---
name: sprint-plan
description: "根据当前里程碑、已完成的工作和可用产能，生成新的迭代计划或更新现有计划。从制作文档和设计积压中提取上下文。"
argument-hint: "[new|update|status] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Task, AskUserQuestion
context: |
  !ls production/sprints/ 2>/dev/null
---

## 阶段 0：解析参数

提取模式参数（`new`、`update` 或 `status`），并解析评审模式（一次性解析，保存供本次运行的所有门禁调用使用）：
1. 若传入了 `--review [full|lean|solo]` → 使用该值
2. 否则读取 `production/review-mode.txt` → 使用其值
3. 否则 → 默认为 `lean`

完整检查模式见 `.claude/docs/director-gates.md`。

---

## 阶段 1：收集上下文

1. **读取当前里程碑**（来自 `production/milestones/`）。

2. **读取上一个迭代**（若存在，来自 `production/sprints/`），以了解速度和遗留工作。

3. **扫描设计文档**（`design/gdd/`），查找标记为可实现的功能。

4. **检查风险登记册**（`production/risk-register/`）。

---

## 阶段 2：生成输出

对于 `new` 模式：

**生成迭代计划**，遵循以下格式并呈现给用户。**尚不询问写入** —— 制作人可行性门禁（阶段 4）将先运行，可能需要修订后才写入文件。

```markdown
# 第 [N] 迭代 -- [开始日期] 至 [结束日期]

## 迭代目标
[一句话描述本迭代对里程碑的贡献]

## 产能
- 总天数：[X]
- 缓冲（20%）：[Y 天，用于计划外工作]
- 可用：[Z 天]

## 任务

### 必须有（关键路径）
| ID | 任务 | 智能体/负责人 | 估计天数 | 依赖项 | 验收标准 |
|----|------|------------|---------|------|---------|

### 应该有
| ID | 任务 | 智能体/负责人 | 估计天数 | 依赖项 | 验收标准 |
|----|------|------------|---------|------|---------|

### 最好有
| ID | 任务 | 智能体/负责人 | 估计天数 | 依赖项 | 验收标准 |
|----|------|------------|---------|------|---------|

## 上一迭代遗留工作
| 任务 | 原因 | 新估计 |
|------|------|------|

## 风险
| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|---------|

## 对外部因素的依赖
- [列出所有外部依赖项]

## 本迭代完成定义
- [ ] 所有"必须有"任务已完成
- [ ] 所有任务通过验收标准
- [ ] QA 计划已存在（`production/qa/qa-plan-sprint-[N].md`）
- [ ] 所有逻辑/集成用户故事有通过的单元/集成测试
- [ ] 冒烟测试通过（`/smoke-check sprint`）
- [ ] QA 签字报告：APPROVED 或 APPROVED WITH CONDITIONS（`/team-qa sprint`）
- [ ] 交付功能中无 S1 或 S2 bug
- [ ] 偏差对应的设计文档已更新
- [ ] 代码已审查并合并
```

对于 `status` 模式：

**生成状态报告**：

```markdown
# 第 [N] 迭代状态 -- [日期]

## 进度：[X/Y 任务完成]（[Z%]）

### 已完成
| 任务 | 完成人 | 备注 |
|------|------|------|

### 进行中
| 任务 | 负责人 | 完成% | 阻塞项 |
|------|------|------|------|

### 未开始
| 任务 | 负责人 | 有风险？ | 备注 |
|------|------|---------|------|

### 阻塞
| 任务 | 阻塞项 | 阻塞项负责人 | 预计解除时间 |
|------|------|-----------|-----------|

## 燃尽评估
[按计划 / 落后 / 超前]
[若落后：正在削减或延后哪些内容]

## 新出现的风险
- [本迭代发现的任何新风险]
```

---

## 阶段 3：写入迭代状态文件

生成新迭代计划后，同时写入 `production/sprint-status.yaml`。
这是故事状态的机器可读事实来源 —— 由 `/sprint-status`、`/story-done` 和 `/help` 直接读取，无需解析 Markdown。

询问："我也可以写入 `production/sprint-status.yaml` 以跟踪故事状态吗？"

格式：

```yaml
# 由 /sprint-plan 自动生成。由 /story-done 更新。
# 请勿手动编辑 —— 使用 /story-done 更新故事状态。

sprint: [N]
goal: "[迭代目标]"
start: "[YYYY-MM-DD]"
end: "[YYYY-MM-DD]"
generated: "[YYYY-MM-DD]"
updated: "[YYYY-MM-DD]"

stories:
  - id: "[epic-story，例如 1-1]"
    name: "[故事名称]"
    file: "[production/stories/path.md]"
    priority: must-have        # must-have | should-have | nice-to-have
    status: ready-for-dev      # backlog | ready-for-dev | in-progress | review | done | blocked
    owner: ""
    estimate_days: 0
    blocker: ""
    completed: ""
```

从迭代计划的任务表初始化每个故事：
- "必须有"任务 → `priority: must-have`，`status: ready-for-dev`
- "应该有"任务 → `priority: should-have`，`status: backlog`
- "最好有"任务 → `priority: nice-to-have`，`status: backlog`

对于 `update` 模式：读取现有 `sprint-status.yaml`，保留未变化故事的状态，添加新故事，移除已取消的故事。

---

## 阶段 4：制作人可行性门禁

**评审模式检查** —— 在生成 PR-SPRINT 之前应用：
- `solo` → 跳过。注明："PR-SPRINT 已跳过 —— 单人模式。"进入阶段 5（QA 计划门禁）。
- `lean` → 跳过（非阶段门禁）。注明："PR-SPRINT 已跳过 —— 精简模式。"进入阶段 5（QA 计划门禁）。
- `full` → 正常生成。

在最终确定迭代计划之前，通过 Task 使用门禁 **PR-SPRINT** 生成 `producer`（见 `.claude/docs/director-gates.md`）。

传递：拟定故事列表（标题、估计、依赖项）、团队总产能（小时/天数）、上一迭代的遗留工作、里程碑约束和截止日期。

呈现制作人的评估。若为 UNREALISTIC，修订故事选择（将故事推迟到"应该有"或"最好有"），然后再请求写入批准。若有 CONCERNS，呈现给用户并让其决定是否调整。

处理制作人裁定后，询问："我可以将此迭代计划写入 `production/sprints/sprint-[N].md` 吗？"若是，写入文件（若需要则创建目录）。裁定结果：**COMPLETE** —— 迭代计划已创建。若否：裁定结果：**BLOCKED** —— 用户拒绝写入。

写入后，追加：

> **范围检查：** 若本迭代包含超出原始功能模块范围的故事，在开始实现之前运行 `/scope-check [epic]` 以检测范围蔓延。

---

## 阶段 5：QA 计划门禁

在关闭迭代计划之前，检查本迭代是否存在 QA 计划。

使用 `Glob` 查找 `production/qa/qa-plan-sprint-[N].md` 或 `production/qa/` 中引用本迭代编号的任何文件。

**若找到 QA 计划**：在迭代计划输出中注明 —— "QA 计划：`[path]`" —— 然后继续。

**若无 QA 计划**：不要静默通过。明确提示：

> "本迭代没有 QA 计划。没有 QA 计划意味着测试需求未定义 —— 开发人员不会知道从 QA 角度来说"完成"是什么，并且没有 QA 计划，迭代无法通过"生产 → 打磨"门禁。
>
> 在开始任何实现之前运行 `/qa-plan sprint`。这需要一个会话，并为每个故事生成所需的测试用例需求。"

使用 `AskUserQuestion`：
- 提示："未找到本迭代的 QA 计划。您希望如何继续？"
- 选项：
  - `[A] 现在运行 /qa-plan sprint —— 我将在开始实现之前完成它（推荐）`
  - `[B] 暂时跳过 —— 我明白在"生产 → 打磨"门禁时 QA 签字将被阻塞`

若 [A]：以"迭代计划已写入。下一步运行 `/qa-plan sprint` —— 然后开始实现。"结束。
若 [B]：在迭代计划文档中添加警告块：

```markdown
> ⚠️ **无 QA 计划**：本迭代在没有 QA 计划的情况下启动。在实现最后一个故事之前运行 `/qa-plan sprint`。
> "生产 → 打磨"门禁需要 QA 签字报告，而 QA 签字报告需要 QA 计划。
```

---

## 阶段 6：后续步骤

迭代计划写入且 QA 计划状态确认后：

- `/qa-plan sprint` —— **在实现开始前必须运行** —— 为每个故事定义测试用例，使开发人员针对 QA 规格实现，而非空白起点
- `/story-readiness [story-file]` —— 在开始故事前验证其就绪状态
- `/dev-story [story-file]` —— 开始实现第一个故事
- `/sprint-status` —— 迭代进行中检查进度
- `/scope-check [epic]` —— 在实现开始前验证无范围蔓延
