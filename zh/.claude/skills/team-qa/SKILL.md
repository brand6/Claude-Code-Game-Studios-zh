---
name: team-qa
description: "通过完整测试周期编排 QA 团队。协调 qa-lead（策略 + 测试计划）与 qa-tester（测试用例编写 + 缺陷报告），为一个冲刺或功能输出完整的 QA 包。覆盖范围：测试计划生成、测试用例编写、冒烟测试门控、手动 QA 执行及签收报告。"
argument-hint: "[sprint | feature: system-name]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Task, AskUserQuestion
agent: qa-lead
---

调用此技能时，请通过结构化测试周期编排 QA 团队。

**决策节点：** 在每个阶段切换处，使用 `AskUserQuestion` 将子代理的方案以可选项形式呈现给用户。在对话中写出代理的完整分析，然后用简洁标签捕获决策。用户必须批准后才能进入下一阶段。

## 团队组成

- **qa-lead** — QA 策略、测试计划生成、故事分类、签收报告
- **qa-tester** — 测试用例编写、缺陷报告编写、手动 QA 文档

## 如何委派

使用 Task 工具将每位团队成员作为子代理启动：
- `subagent_type: qa-lead` — 策略、规划、分类、签收
- `subagent_type: qa-tester` — 测试用例编写和缺陷报告编写

在每个代理的提示中始终提供完整上下文（故事文件路径、QA 计划路径、范围约束）。在可能的情况下并行启动独立的 qa-tester 任务（例如，阶段5中的多个故事可以同时搭建）。

## 流水线

### 阶段 1：加载上下文

在做任何事之前，收集完整范围：

1. 从参数中检测当前冲刺或功能范围：
   - 如果参数是冲刺标识符（如 `sprint-03`）：读取 `production/sprints/[sprint]/` 中的所有故事文件
   - 如果参数是 `feature: [system-name]`：glob 该系统标记的故事文件
   - 如果没有参数：读取 `production/session-state/active.md` 和 `production/sprint-status.yaml`（如果存在）来推断活跃冲刺

2. 读取 `production/stage.txt` 确认当前项目阶段。

3. 统计找到的故事并向用户报告：
   > "QA 周期开始，范围：[冲刺/功能]。找到 [N] 个故事。当前阶段：[stage]。准备好开始 QA 策略了吗？"

### 阶段 2：QA 策略（qa-lead）

通过 Task 启动 `qa-lead` 来审查所有范围内的故事并制定 QA 策略。

提示 qa-lead：
- 读取每个故事文件
- 按类型对每个故事进行分类：**逻辑（Logic）** / **集成（Integration）** / **视觉/手感（Visual/Feel）** / **UI** / **配置/数据（Config/Data）**
- 识别哪些故事需要自动化测试证明，哪些需要手动 QA
- 标记任何缺少验收标准或缺少测试证明的故事（这会阻塞 QA）
- 估算手动 QA 工作量（需要的测试会话数）
- 检查 `tests/smoke/` 中的冒烟测试场景；对每个场景，评估在当前构建下是否可以验证。产出冒烟检查结论：**PASS** / **PASS WITH WARNINGS [列表]** / **FAIL [失败列表]**
- 产出策略摘要表和冒烟检查结果：

  | 故事 | 类型 | 需要自动化 | 需要手动 | 阻塞？ |
  |------|------|-----------|---------|-------|

  **冒烟检查**：[PASS / PASS WITH WARNINGS / FAIL] — [非 PASS 时的详情]

如果冒烟检查结果为 **FAIL**，qa-lead 必须突出列出失败项。冒烟检查失败时，QA 不能推进到策略阶段之后。

将 qa-lead 的完整策略呈现给用户，然后使用 `AskUserQuestion`：

```
question: "QA 策略审查"
options:
  - "没问题——进入测试计划"
  - "在继续之前调整故事类型"
  - "跳过被阻塞的故事，继续处理其余部分"
  - "冒烟检查失败——修复问题后重新运行 /team-qa"
  - "取消——先解决阻塞项"
```

如果冒烟检查 **FAIL**：不要推进到阶段 3。显示失败项并停止。用户必须修复它们并重新运行 `/team-qa`。
如果冒烟检查 **PASS WITH WARNINGS**：在签收报告中记录警告并继续。
如果存在阻塞项：明确列出。用户可以选择跳过被阻塞的故事或取消周期。

### 阶段 3：测试计划生成

使用阶段 2 的策略，生成结构化的测试计划文档。

测试计划应涵盖：
- **范围**：冲刺/功能名称、故事数量、日期
- **故事分类表**：来自阶段 2 策略
- **自动化测试需求**：哪些故事需要测试文件，`tests/` 中的预期路径
- **手动 QA 范围**：哪些故事需要手动演练以及验证什么
- **范围外内容**：本次周期明确不测试的内容及原因
- **准入标准**：QA 开始前必须满足的条件（冒烟检查通过、构建稳定）
- **完成标准**：QA 周期完成的标志（所有故事 PASS 或 FAIL 并已提交缺陷）

询问："我可以将 QA 计划写入 `production/qa/qa-plan-[sprint]-[date].md` 吗？"

只有在收到批准后才写入。

### 阶段 4：测试用例编写（qa-tester）

> **冒烟检查**在阶段 2（QA 策略）中执行。如果阶段 2 的冒烟检查返回 FAIL，周期已在那里停止。此阶段仅在阶段 2 冒烟检查为 PASS 或 PASS WITH WARNINGS 时运行。

对于每个需要手动 QA 的故事（视觉/手感、UI、没有自动化测试的集成类故事）：

通过 Task 为每个故事启动 `qa-tester`（尽可能并行运行），提供：
- 故事文件路径
- QA 计划中与该故事相关的部分
- 被测系统的 GDD 验收标准（如有）
- 编写覆盖所有验收标准的详细测试用例的指令

每套测试用例应包括：
- **前置条件**：测试开始前需要的游戏状态
- **步骤**：编号明确的操作
- **预期结果**：应该发生什么
- **实际结果**：留空供测试人员填写
- **通过/失败**：留空

将测试用例呈现给用户审查后再执行。按故事分组。

每组故事（每次 3-4 个）使用 `AskUserQuestion`：

```
question: "【故事组】的测试用例已准备好。开始手动 QA 前是否审查？"
options:
  - "批准——为这些故事开始手动 QA"
  - "修改 [故事名称] 的测试用例"
  - "跳过 [故事名称] 的手动 QA——尚未准备好"
```

### 阶段 6：手动 QA 执行

遍历已批准的手动 QA 列表中的每个故事。

将故事批量分组（每次 3-4 个），对每组使用 `AskUserQuestion`：

```
question: "手动 QA——[故事标题]\n[需要测试内容的简要说明]"
options:
  - "PASS——所有验收标准已验证"
  - "PASS WITH NOTES——发现小问题（之后描述）"
  - "FAIL——标准未满足（之后描述）"
  - "BLOCKED——暂时无法测试（原因）"
```

每次 FAIL 结果后：使用 `AskUserQuestion` 收集失败描述，然后通过 Task 启动 `qa-tester` 在 `production/qa/bugs/` 中编写正式缺陷报告。

缺陷报告命名：`BUG-[NNN]-[short-slug].md`（从目录中已有缺陷递增 NNN）。

收集所有结果后，汇总：
- 故事 PASS：[count]
- 故事 PASS WITH NOTES：[count]
- 故事 FAIL：[count]——已提交缺陷：[IDs]
- 故事 BLOCKED：[count]

### 阶段 7：QA 签收报告

通过 Task 启动 `qa-lead`，使用阶段 4-6 的所有结果生成签收报告。

签收报告格式：

```markdown
## QA 签收报告：[冲刺/功能]
**日期**：[date]
**QA Lead 签收**：[待定]

### 测试覆盖摘要
| 故事 | 类型 | 自动化测试 | 手动 QA | 结果 |
|------|------|-----------|---------|------|
| [title] | 逻辑 | PASS | — | PASS |
| [title] | 视觉 | — | PASS | PASS |

### 发现的缺陷
| ID | 故事 | 严重度 | 状态 |
|----|------|--------|------|
| BUG-001 | [story] | S2 | 开放 |

### 结论：APPROVED / APPROVED WITH CONDITIONS / NOT APPROVED

**条件**（如有）：[在构建推进前必须修复的内容列表]

### 下一步
[基于结论的指导]
```

结论规则：
- **APPROVED**：所有故事 PASS 或 PASS WITH NOTES；无开放的 S1/S2 缺陷
- **APPROVED WITH CONDITIONS**：S3/S4 缺陷开放，或有记录的 PASS WITH NOTES 问题；无 S1/S2 缺陷
- **NOT APPROVED**：任何 S1/S2 缺陷开放；或故事 FAIL 且无文档化的变通方案

按结论给出下一步指导：
- APPROVED："构建已准备好进入下一阶段。运行 `/gate-check` 验证推进。"
- APPROVED WITH CONDITIONS："在推进前解决条件项。S3/S4 缺陷可推迟到打磨阶段。"
- NOT APPROVED："解决 S1/S2 缺陷后重新运行 `/team-qa` 或针对性手动 QA。"

询问："我可以将此 QA 签收报告写入 `production/qa/qa-signoff-[sprint]-[date].md` 吗？"

只有在收到批准后才写入。

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

## 输出

涵盖以下内容的摘要：范围内的故事、冒烟检查结果、手动 QA 结果、已提交的缺陷（含 ID 和严重度），以及最终的 APPROVED / APPROVED WITH CONDITIONS / NOT APPROVED 结论。

结论：**COMPLETE** — QA 周期已完成。
结论：**BLOCKED** — 冒烟检查失败或关键阻塞项阻止了周期完成；已产出部分报告。
