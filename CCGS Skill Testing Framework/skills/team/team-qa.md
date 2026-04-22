# Skill Test Spec: /team-qa

## Skill 概述

编排七阶段 QA 循环：1. 范围检测 → 2. 策略（qa-lead）→ 3. QA 计划（qa-lead）→
4. 冒烟测试门控（qa-tester）——HARD GATE：FAIL 停止流水线 → 5. 测试用例并行
（qa-tester × 类别）→ 6. 手动 QA（qa-tester）→ 7. 签收报告（qa-lead）。
Bug 报告保存至 `production/qa/bugs/BUG-[NNN]-[short-slug].md`。
裁决：COMPLETE（流水线完成）；签收：APPROVED / APPROVED WITH CONDITIONS / NOT APPROVED。

---

## 静态断言（结构性）

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 明确包含七个阶段
- [ ] 阶段 4 是 HARD GATE——FAIL 时流水线停止
- [ ] 阶段 5 测试用例并行生成
- [ ] Bug 报告路径遵循 `production/qa/bugs/BUG-[NNN]-[short-slug].md` 模式
- [ ] 包含裁决关键字：COMPLETE、APPROVED、APPROVED WITH CONDITIONS、NOT APPROVED
- [ ] 存在文件写入协议；编排者不直接写入文件
- [ ] 子 agent 在任何写入之前强制执行"May I write to [path]?"
- [ ] 存在错误恢复协议
- [ ] 步骤过渡前使用 `AskUserQuestion`

---

## 测试用例

### 用例 1：正常路径——所有阶段完成，签收 APPROVED

**测试夹具：**
- 当前冲刺的故事文件位于 `production/stories/`
- 冒烟测试通过
- 手动测试无严重 bug
- 所有接受标准已满足

**输入：** `/team-qa sprint-12`

**预期行为：**
1. 阶段 1：范围检测——编排者读取 `production/stories/` 以识别冲刺中的故事
2. 阶段 2：派生 qa-lead 定义测试策略（基于风险的优先级、测试类型分类、覆盖目标）
3. `AskUserQuestion` 批准策略后进行阶段 3
4. 阶段 3：派生 qa-lead 创建 QA 测试计划（详细测试场景、测试数据需求、测试环境配置）
5. `AskUserQuestion` 批准 QA 计划后进行阶段 4
6. 阶段 4（HARD GATE）：派生 qa-tester 运行冒烟测试——结果：PASS
7. PASS 时显示"冒烟测试门控：通过"，继续进行阶段 5
8. `AskUserQuestion` 批准进入完整 QA 后发出并行测试用例 Task
9. 阶段 5：并行生成多个测试用例集（按逻辑/集成/视觉/UI 分类）
10. `AskUserQuestion` 批准测试用例后进行阶段 6
11. 阶段 6：派生 qa-tester 执行手动 QA——无严重或阻塞 bug
12. `AskUserQuestion` 批准手动 QA 结果后进行阶段 7
13. 阶段 7：派生 qa-lead 生成签收报告
14. 签收报告裁决：APPROVED；流水线裁决：COMPLETE

**断言：**
- [ ] 阶段 4 冒烟测试 PASS 时显示明确的门控通过信息
- [ ] 阶段 5 测试用例并行生成（按类别同时发出多个 Task）
- [ ] 每次阶段过渡前使用 `AskUserQuestion`
- [ ] 签收报告裁决为 APPROVED
- [ ] 流水线裁决为 COMPLETE
- [ ] 编排者不直接写入任何文件- [ ] 下一步：运行 `/gate-check` 以验证阶段推进。
---

### 用例 2：冒烟测试 FAIL——阶段 4 停止流水线

**测试夹具：**
- 阶段 4 冒烟测试：qa-tester 发现游戏在启动后 30 秒内崩溃（严重错误）

**输入：** `/team-qa sprint-12`（阶段 4 场景）

**预期行为：**
1. 阶段 1–3 正常完成
2. 阶段 4：qa-tester 运行冒烟测试，发现启动崩溃
3. 冒烟测试结果：FAIL
4. 编排者立即显示：**HARD GATE 失败——冒烟测试未通过。阶段 5–7 已停止。在继续完整 QA 之前必须解决崩溃问题。**
5. Bug 报告自动创建：`production/qa/bugs/BUG-001-startup-crash.md`
6. `AskUserQuestion` 呈现选项：
   - 修复崩溃并重新运行冒烟测试
   - 提交紧急修复并重新启动 QA 循环
7. 阶段 5、6、7 在冒烟测试通过之前不启动

**断言：**
- [ ] 冒烟测试 FAIL 时流水线立即停止（HARD GATE 生效）
- [ ] 阶段 5、6、7 在 FAIL 后不启动
- [ ] Bug 报告自动创建并遵循命名模式
- [ ] 编排者输出明确的 HARD GATE 失败信息
- [ ] `AskUserQuestion` 提供修复并重测的选项
- [ ] 裁决为 BLOCKED（非 COMPLETE）
- [ ] Skill 推荐运行 `/smoke-check` 和 `/team-qa` 作为修复步骤

---

### 用例 3：手动 QA 发现严重 Bug——提交 Bug 报告

**测试夹具：**
- 阶段 1–5 已完成
- 阶段 6 手动 QA：qa-tester 在测试库存系统时发现：当库存已满时丢弃物品会永久删除物品而不是提示玩家（数据丢失 bug，严重级别 S2）

**输入：** `/team-qa inventory-feature`（阶段 6 场景）

**预期行为：**
1. 阶段 6：qa-tester 执行手动测试，发现库存丢弃 bug
2. qa-tester 创建结构化 bug 报告：`production/qa/bugs/BUG-[NNN]-inventory-discard-data-loss.md`
3. Bug 报告包含：复现步骤、严重级别 S2、影响范围、期望行为 vs 实际行为
4. 子 agent 询问"May I write bug report to `production/qa/bugs/BUG-[NNN]-inventory-discard-data-loss.md`?"
5. 编排者在阶段 6 摘要中显示发现的 bug 列表
6. `AskUserQuestion` 呈现测试结果和 bug 列表
7. 进入阶段 7 签收；qa-lead 鉴于 S2 bug 未修复，签收裁决：NOT APPROVED
8. 报告说明：1 个 S2 bug 阻塞发布，需要修复后重新进行回归测试

**断言：**
- [ ] Bug 报告路径遵循 `production/qa/bugs/BUG-[NNN]-[slug].md` 模式
- [ ] Bug 报告写入前询问用户权限
- [ ] Bug 报告包含复现步骤和严重级别
- [ ] 签收裁决为 NOT APPROVED（存在未修复 S2 bug）
- [ ] 报告明确说明阻塞发布的原因
- [ ] 下一步明确提及重新运行 `/team-qa`

---

### 用例 4：无参数——从会话状态推断或询问

**测试夹具：**
- 场景 A：`production/session-state/current-sprint.txt` 存在，内容为 `sprint-12`
- 场景 B：会话状态文件不存在

**输入：** `/team-qa`（无参数）

**预期行为（场景 A）：**
1. 编排者读取 `production/session-state/current-sprint.txt`
2. 推断目标为 `sprint-12`
3. `AskUserQuestion`："检测到当前冲刺为 sprint-12。是否对 sprint-12 运行 QA？"（确认后继续）

**预期行为（场景 B）：**
1. 会话状态文件不存在，无法推断
2. `AskUserQuestion`："请指定 QA 范围：输入冲刺名称（如 sprint-12）、功能名称或故事 ID"
3. 不猜测或假设范围

**断言：**
- [ ] 有会话状态文件时尝试推断冲刺名称
- [ ] 推断结果通过 `AskUserQuestion` 确认，不自动假定
- [ ] 无法推断时 `AskUserQuestion` 明确请求范围输入
- [ ] 不在用户确认之前派生任何 agent

---

### 用例 5：混合测试结果——PASS / FAIL / BLOCKED

**测试夹具：**
- 阶段 5 并行生成了四类测试用例：逻辑、集成、视觉、UI
- 阶段 6 手动执行：逻辑测试全部通过；集成测试 2 个 FAIL（但非严重）；视觉测试 BLOCKED（测试环境不支持 HDR 渲染）；UI 测试全部通过

**输入：** `/team-qa feature-bundle-3`（阶段 6 场景）

**预期行为：**
1. 阶段 6 摘要清晰展示混合结果：
   - 逻辑：全部 PASS
   - 集成：2 FAIL（非严重，已记录 bug）
   - 视觉：BLOCKED（HDR 环境问题，已记录）
   - UI：全部 PASS
2. FAIL 项自动创建 bug 报告
3. BLOCKED 项记录阻塞原因（HDR 环境不可用）
4. 进入阶段 7；qa-lead 鉴于混合结果签收裁决：APPROVED WITH CONDITIONS
5. 条件：集成 bug 在下一版本修复；视觉测试在 HDR 环境可用时重测

**断言：**
- [ ] 混合结果在报告中按类别清晰展示
- [ ] FAIL 测试自动生成 bug 报告
- [ ] BLOCKED 测试记录阻塞原因而不被静默忽略
- [ ] 签收裁决为 APPROVED WITH CONDITIONS（非 APPROVED 或 NOT APPROVED）
- [ ] 条件内容具体说明（哪个 bug 在何时修复）

---

## 协议合规性

- [ ] 阶段 1 范围检测在派生任何 agent 之前运行（读取故事文件）
- [ ] 阶段 4 是 HARD GATE——FAIL 时立即停止阶段 5–7
- [ ] 阶段 5 测试用例按类别并行生成
- [ ] Bug 报告路径遵循 `production/qa/bugs/BUG-[NNN]-[short-slug].md` 模式
- [ ] 每次阶段过渡前使用 `AskUserQuestion`
- [ ] 编排者不直接写入任何文件
- [ ] 子 agent 在任何写入之前强制执行"May I write to [path]?"
- [ ] BLOCKED 测试被记录，不被静默跳过
- [ ] 流水线裁决为 COMPLETE 或 BLOCKED
- [ ] 签收裁决为 APPROVED、APPROVED WITH CONDITIONS 或 NOT APPROVED

---

## 覆盖率说明

- 冒烟测试中存在多个严重 bug（S1 级）的情况——仅以单一崩溃为例，
  但 HARD GATE 逻辑对所有 FAIL 状态均适用。
- 阶段 5 的分类逻辑（如何将故事分配到测试类别）是 qa-lead 的判断行为，
  未在此 spec 中独立断言。
