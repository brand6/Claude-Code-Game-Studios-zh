# Skill Test Spec: /team-combat

## Skill 概述

编排完整的六阶段战斗功能流水线：设计（game-designer）→ 架构 + 引擎专项并行
（lead-programmer + 主引擎专项 agent）→ 实现并行（gameplay-programmer +
ai-programmer + technical-artist + sound-designer）→ 集成测试（lead-programmer）
→ 验证（qa-tester）→ 签收（game-designer + lead-programmer）。
整个流水线通过 ADR 和 GDD 引用进行上下文感知。
裁决：COMPLETE / NEEDS WORK / BLOCKED。
完成后的下一步：`/code-review`、`/balance-check`、`/team-polish`。

---

## 静态断言（结构性）

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 明确包含六个阶段（设计、架构、实现、集成、验证、签收）
- [ ] 包含裁决关键字：COMPLETE、NEEDS WORK、BLOCKED
- [ ] 存在"并行实现"阶段——四个 agent 同时派生
- [ ] 存在文件写入协议；编排者不直接写入文件
- [ ] 子 agent 在任何写入之前强制执行"May I write to [path]?"
- [ ] 存在错误恢复协议——BLOCKED agent 不使整个流水线停止
- [ ] 步骤过渡前使用 `AskUserQuestion`
- [ ] 末尾包含下一步交接：`/code-review`、`/balance-check`、`/team-polish`

---

## 测试用例

### 用例 1：正常路径——所有六个阶段完成，裁决 COMPLETE

**测试夹具：**
- 战斗设计 GDD 位于 `design/gdd/combat.md`
- 相关 ADR 位于 `docs/architecture/` 且状态为 Accepted
- 引擎已在 `.claude/docs/technical-preferences.md` 中配置
- 所有 agent 成功完成任务

**输入：** `/team-combat ranged-attack`

**预期行为：**
1. 上下文收集：读取 `design/gdd/combat.md`、相关 ADR、现有代码文件
2. 阶段 1：派生 game-designer 进行战斗系统设计；输出包含机制说明、数值公式和设计决策
3. `AskUserQuestion` 批准设计后进行阶段 2
4. 阶段 2：并行派生 lead-programmer（架构方案）和引擎专项 agent（引擎特定验证）
5. `AskUserQuestion` 批准架构后进行阶段 3
6. 阶段 3：同时派生 gameplay-programmer、ai-programmer、technical-artist 和 sound-designer——四个 Task 调用同时发出
7. `AskUserQuestion` 批准实现后进行阶段 4
8. 阶段 4：lead-programmer 集成测试；验证所有子系统连接
9. `AskUserQuestion` 批准集成后进行阶段 5
10. 阶段 5：qa-tester 验证；执行功能测试、回归测试
11. `AskUserQuestion` 批准测试后进行阶段 6
12. 阶段 6：game-designer 和 lead-programmer 联合签收；确认设计意图已实现
13. 裁决：COMPLETE
14. 下一步：`/code-review`、`/balance-check`、`/team-polish`

**断言：**
- [ ] 阶段 3 中四个 agent 的 Task 调用同时发出（并行）
- [ ] 每次阶段过渡前使用 `AskUserQuestion`
- [ ] 所有六个阶段均明确标识于输出中
- [ ] 阶段 6 包含 game-designer 和 lead-programmer 两者签收
- [ ] 裁决为 COMPLETE
- [ ] 下一步引用 `/code-review`、`/balance-check`、`/team-polish`

---

### 用例 2：阻塞 agent——ai-programmer 的 ADR 未被 Accepted

**测试夹具：**
- 阶段 3 进行中
- AI 行为的相关 ADR（ADR-012-enemy-ai）状态为 Proposed（不是 Accepted）
- ai-programmer 检测到此情况并阻塞

**输入：** `/team-combat enemy-ai`（阶段 3 场景）

**预期行为：**
1. 阶段 1–2 正常完成
2. 阶段 3：ai-programmer 读取 ADR-012-enemy-ai，发现状态为 Proposed
3. ai-programmer 返回 BLOCKED："ADR-012-enemy-ai 状态为 Proposed——没有已接受的架构决策，无法实现。请先运行 `/architecture-decision` 将 ADR 推进到 Accepted 状态。"
4. gameplay-programmer、technical-artist 和 sound-designer 继续完成各自任务
5. 编排者立即在对话中显示 ai-programmer 的 BLOCKED 状态
6. `AskUserQuestion` 呈现选项：
   - 停止并解决 ADR 问题（推荐）
   - 继续完成其他阶段并在稍后解决 AI 实现问题
7. 无论选择哪个选项，生成部分报告记录已完成和被阻塞的内容
8. 裁决：BLOCKED（ai-programmer 未完成）

**断言：**
- [ ] ai-programmer 明确引用阻塞原因（ADR-012-enemy-ai，状态 Proposed）
- [ ] 编排者不等待所有并行 agent 完成后才显示 BLOCKED 状态
- [ ] 阶段 3 中其他三个 agent 不因 ai-programmer 阻塞而停止
- [ ] `AskUserQuestion` 提供停止或继续的选项
- [ ] 部分报告记录哪些内容已完成、哪些被阻塞
- [ ] 裁决为 BLOCKED——不为 COMPLETE

---

### 用例 3：无参数——使用指导

**测试夹具：**
- 任何项目状态

**输入：** `/team-combat`（无参数）

**预期行为：**
1. Skill 检测到未提供功能名称
2. 输出使用指导，包含正确的调用格式和示例
3. 不派生任何 agent

**断言：**
- [ ] 无参数时不派生任何 agent
- [ ] 使用信息包含带参数示例的正确格式
- [ ] 不使用 `AskUserQuestion`

---

### 用例 4：并行阶段验证——四个实现 agent 确实同时发出

**测试夹具：**
- 阶段 1 和阶段 2 已完成批准
- 等待阶段 3 执行
- 所有四个 agent（gameplay-programmer、ai-programmer、technical-artist、sound-designer）均可用且未被阻塞

**输入：** `/team-combat melee-combat`（阶段 3 焦点）

**预期行为：**
1. 阶段 3 启动时：编排者在等待任何结果之前发出所有四个 Task 调用
2. 无论哪个 agent 最先完成，其结果先呈现
3. 所有四个结果收集完毕后，`AskUserQuestion` 呈现合并输出
4. 没有 agent 等待另一个 agent 的结果才开始工作

**断言：**
- [ ] 阶段 3 期间没有顺序 agent 执行（没有 agent 等待另一个完成）
- [ ] 四个 agent 的输出均包含在阶段 3 摘要中
- [ ] `AskUserQuestion` 在所有四个结果收集后呈现
- [ ] 编排者不在四个 agent 之间传递中间结果

---

### 用例 5：引擎专项路由——根据配置引擎选择正确的引擎专项 agent

**测试夹具：**
- `.claude/docs/technical-preferences.md` 中配置为 `Godot 4`

**输入：** `/team-combat dodge-roll`

**预期行为：**
1. 阶段 2：引擎专项 agent 为 `godot-specialist`（或更细粒度的 Godot 专项如 `godot-gdscript-specialist`）
2. 引擎专项 agent 根据 Godot 4 惯用法验证架构方案
3. 如果配置为 Unity，则改用 `unity-specialist`；如果为 Unreal，则改用 `unreal-specialist`

**断言：**
- [ ] 派生的引擎专项 agent 与 technical-preferences.md 中配置的引擎匹配
- [ ] 非 Godot 引擎专项 agent 不被派生（无不必要的多引擎专项调用）

---

## 协议合规性

- [ ] 上下文收集（GDD、ADR、现有代码）在派生任何 agent 之前运行
- [ ] 每次阶段过渡前使用 `AskUserQuestion`（用户必须批准才能继续）
- [ ] 阶段 3 并行：四个 Task 调用同时发出，不等待中间结果
- [ ] 编排者不直接写入任何文件——所有写入委托给子 agent
- [ ] 子 agent 在任何写入之前强制执行"May I write to [path]?"
- [ ] BLOCKED agent 立即报告——不被静默跳过
- [ ] 某些 agent 阻塞时始终生成部分报告
- [ ] 裁决为 COMPLETE、NEEDS WORK 或 BLOCKED——不使用其他值
- [ ] 末尾包含下一步交接：`/code-review`、`/balance-check`、`/team-polish`

---

## 覆盖率说明

- 阶段 3 中可能出现多个 agent 同时阻塞的情况——未独立测试，但
  断言的部分报告规则隐式涵盖此场景。
- 阶段 6 签收可能返回 NEEDS WORK（设计意图未实现）——此路径在
  用例 1 中通过裁决关键字的存在进行了隐式测试。
- "重试范围缩小"的错误恢复选项已在断言中列出，但其完整递归行为
  （通过 `/create-stories` 拆分）由 `/create-stories` 规范覆盖。
