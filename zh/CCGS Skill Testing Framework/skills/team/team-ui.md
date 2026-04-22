# Skill Test Spec: /team-ui

## Skill 概述

编排完整 UX 流水线用于 UI 功能：1a 上下文收集 → 1b UX 规格（ux-designer）→
1c UX 评审门控（BLOCKING）→ 2 视觉设计（art-director）→ 3 实现（引擎 UI 专项优先，
然后 ui-programmer）→ 4 并行评审（ux-designer + art-director + accessibility-specialist）→
5 打磨（technical-artist）。
引用 `design/ux/interaction-patterns.md`（若存在）。
裁决：COMPLETE / BLOCKED。
下一步：`/ux-review`、`/code-review`、`/team-polish`。

---

## 静态断言（结构性）

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 明确包含阶段 1a/1b/1c、2、3、4、5
- [ ] 阶段 1c UX 评审门控是 BLOCKING——NEEDS REVISION 时不进入阶段 2
- [ ] 阶段 4 明确并行派生 ux-designer、art-director 和 accessibility-specialist
- [ ] 包含裁决关键字：COMPLETE、BLOCKED
- [ ] 上下文收集阶段尝试读取 `design/ux/interaction-patterns.md`
- [ ] 存在文件写入协议；编排者不直接写入文件
- [ ] 子 agent 在任何写入之前强制执行"May I write to [path]?"
- [ ] 存在错误恢复协议
- [ ] 步骤过渡前使用 `AskUserQuestion`
- [ ] 末尾包含下一步交接：`/ux-review`、`/code-review`、`/team-polish`

---

## 测试用例

### 用例 1：正常路径——所有阶段完成，裁决 COMPLETE

**测试夹具：**
- GDD 位于 `design/gdd/inventory.md`
- 交互模式库位于 `design/ux/interaction-patterns.md`
- 引擎已配置（Godot 4）
- 所有 agent 成功完成任务

**输入：** `/team-ui inventory-screen`

**预期行为：**
1. 阶段 1a：上下文收集——读取 `design/gdd/inventory.md` 和 `design/ux/interaction-patterns.md`
2. 阶段 1b：派生 ux-designer 创建库存界面 UX 规格（用户流程、交互状态、线框图描述、无障碍要求）
3. 阶段 1c：通过 `/ux-review inventory-screen` 运行 UX 评审门控——结果：APPROVED
4. `AskUserQuestion` 呈现 UX 规格和评审结果；批准后进行阶段 2
5. 阶段 2：派生 art-director 创建视觉设计规格（配色方案、排版、图标风格、动画指导）
6. `AskUserQuestion` 批准视觉设计后进行阶段 3
7. 阶段 3：先派生 godot-ui-specialist（引擎特定实现模式），然后派生 ui-programmer（实现具体代码）
8. `AskUserQuestion` 批准实现后进行阶段 4
9. 阶段 4：并行派生 ux-designer（可用性验证）、art-director（视觉一致性检查）和 accessibility-specialist（无障碍合规检查）
10. `AskUserQuestion` 批准评审后进行阶段 5
11. 阶段 5：派生 technical-artist 进行视觉打磨（着色器效果、动画曲线、细节优化）
12. 子 agent 询问写入权限后保存 UX 规格和相关文档
13. 裁决：COMPLETE；下一步：`/ux-review`、`/code-review`、`/team-polish`

**断言：**
- [ ] 阶段 1a 读取 `design/ux/interaction-patterns.md`（若存在）
- [ ] 阶段 1c UX 评审门控在阶段 2 之前运行
- [ ] 阶段 4 中三个 agent 的 Task 调用同时发出
- [ ] 每次阶段过渡前使用 `AskUserQuestion`
- [ ] 引擎专项 agent（godot-ui-specialist）在 ui-programmer 之前派生
- [ ] 编排者不直接写入任何文件
- [ ] 裁决为 COMPLETE

---

### 用例 2：UX 评审门控失败——NEEDS REVISION 阻塞进入阶段 2

**测试夹具：**
- 阶段 1b UX 规格已创建
- 阶段 1c：`/ux-review` 返回 NEEDS REVISION——原因：缺少禁用状态的交互状态规格

**输入：** `/team-ui settings-screen`（阶段 1c 场景）

**预期行为：**
1. 阶段 1b：ux-designer 创建设置界面 UX 规格（但遗漏了禁用状态）
2. 阶段 1c：通过 `/ux-review settings-screen` 运行评审——返回 **NEEDS REVISION**
3. 编排者立即显示：**UX 评审门控失败——NEEDS REVISION。阶段 2 已阻塞。**
4. 详细说明需要修订的内容：禁用状态交互规格缺失
5. `AskUserQuestion` 呈现选项：
   - 修订 UX 规格以补充禁用状态，然后重新运行评审
   - 用户明确接受风险，强制推进到阶段 2（记录为已知缺口）
6. 阶段 2 在 UX 评审通过之前不启动（除非用户明确覆盖）

**断言：**
- [ ] NEEDS REVISION 时阶段 2 被阻塞
- [ ] 编排者输出明确的评审失败信息和具体修订要求
- [ ] `AskUserQuestion` 提供修订后重评审的选项
- [ ] 也提供用户强制覆盖的选项（带风险说明）
- [ ] 裁决在门控未通过时为 BLOCKED

---

### 用例 3：无参数——使用指导

**测试夹具：**
- 任何项目状态

**输入：** `/team-ui`（无参数）

**预期行为：**
1. Skill 检测到未提供界面名称
2. 输出使用指导，包含正确调用格式和示例（例如 `inventory-screen`、`main-menu`、`hud`）
3. 不派生任何 agent

**断言：**
- [ ] 无参数时不派生任何 agent
- [ ] 使用信息包含带参数示例的正确格式
- [ ] 不使用 `AskUserQuestion`

---

### 用例 4：阶段 4 并行评审——三个 agent 确实同时发出

**测试夹具：**
- 阶段 1–3 已完成批准
- 等待阶段 4 执行

**输入：** `/team-ui character-select`（阶段 4 焦点）

**预期行为：**
1. 阶段 4 启动时：编排者同时发出 ux-designer、art-director 和 accessibility-specialist 的三个 Task 调用
2. 三个 agent 并行工作，互不等待
3. 所有三个结果收集后，`AskUserQuestion` 呈现合并评审报告

**断言：**
- [ ] 三个 Task 调用同时发出（并行）
- [ ] 三个 agent 的评审结果均包含在阶段 4 报告中
- [ ] 没有顺序执行（一个 agent 不等待另一个完成）

---

### 用例 5：缺少交互模式库——注明缺口并给用户选择

**测试夹具：**
- `design/ux/interaction-patterns.md` 不存在
- 目标界面 GDD 存在

**输入：** `/team-ui crafting-screen`

**预期行为：**
1. 阶段 1a：编排者检查 `design/ux/interaction-patterns.md`——不存在
2. 编排者在对话中显示缺口："交互模式库不存在（`design/ux/interaction-patterns.md`）——没有现有模式可供复用"
3. `AskUserQuestion` 提供选项：
   - 先运行 `/ux-design patterns` 建立模式库，然后继续
   - 继续而不使用模式库——ux-designer 将把创建的所有模式视为新模式，并在完成时添加到新的 `design/ux/interaction-patterns.md` 中
4. Skill 不凭猜测发明或假定模式
5. 若用户选择继续，ui-programmer 被明确告知所有模式均为新模式
6. 最终报告记录模式库状态（已创建 / 仍缺失 / 已更新）

**断言：**
- [ ] 缺少交互模式库时明确在对话中注明——不被静默忽略
- [ ] Skill 不凭猜测发明模式
- [ ] `AskUserQuestion` 提供"先创建模式库"的选项（引用 `/ux-design patterns`）
- [ ] 若用户继续，ui-programmer 被告知将所有模式视为新模式
- [ ] 最终报告记录模式库状态
- [ ] Skill 不因缺少模式库而完全失败——缺口被注明，用户获得选择

---

## 协议合规性

- [ ] 每次阶段过渡前使用 `AskUserQuestion`（用户必须批准才能推进）
- [ ] 阶段 1c UX 评审门控是 BLOCKING——NEEDS REVISION 时阶段 2 不启动
- [ ] 所有文件写入委托给子 agent——编排者不直接调用 Write 或 Edit
- [ ] 阶段 4 的三个 agent 并行派生（同时发出 Task 调用）
- [ ] 遵循错误恢复协议：显示→评估→提供选项→生成部分报告
- [ ] 即使有 agent 阻塞，始终生成部分报告
- [ ] 裁决恰好为 COMPLETE 或 BLOCKED
- [ ] 末尾包含下一步交接：`/ux-review`、`/code-review`、`/team-polish`

---

## 覆盖率说明

- HUD 专项路径（`/team-ui hud` 使用 `hud-design.md` 模板和阶段 5 视觉预算检查）
  未在此独立测试；与主流程共享相同的阶段结构但使用不同模板。
- 交互模式库"原地更新"路径（实现期间添加新模式）在用例 1 步骤 8 中
  隐式验证——专门测试已知新模式的夹具会进一步加强覆盖率。
- 引擎 UI 专项不可用（未配置引擎）——Skill 规格指出"若未配置引擎则跳过"；
  此路径在用例 1 中通过断言覆盖，但未给予独立夹具。
