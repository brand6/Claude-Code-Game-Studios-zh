# 技能测试规范：/brainstorm

## 技能概要

`/brainstorm` 引导进行游戏概念构思。它呈现 2-4 个方案及各自的优缺点，
让用户选择并细化概念，最终生成结构化的 `design/gdd/game-concept.md` 文档。
本技能采用协作模式——在提出方案前先提问，并持续迭代直到用户认可概念方向。

在 `full` 审查模式下，概念草稿完成后并行生成四个 director 门控：
CD-PILLARS（creative-director）、AD-CONCEPT-VISUAL（art-director）、
TD-FEASIBILITY（technical-director）和 PR-SCOPE（producer）。
在 `lean` 模式下，所有 4 个内联门控均被跳过（lean 模式仅运行 PHASE-GATE，
而 brainstorm 没有 PHASE-GATE）。在 `solo` 模式下，所有门控均被跳过。
技能在写入 `design/gdd/game-concept.md` 前询问"May I write"。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判决关键词：APPROVED、REJECTED、CONCERNS
- [ ] 包含"May I write"协作协议语言（用于 game-concept.md）
- [ ] 末尾包含下一步交接（`/map-systems`）
- [ ] 在 full 模式下记录 4 个 director 门控：CD-PILLARS、AD-CONCEPT-VISUAL、TD-FEASIBILITY、PR-SCOPE
- [ ] 记录 lean 和 solo 模式下全部 4 个门控均被跳过

---

## Director 门控检查

`full` 模式：用户批准概念草稿后，CD-PILLARS、AD-CONCEPT-VISUAL、TD-FEASIBILITY
和 PR-SCOPE 并行生成。

`lean` 模式：全部 4 个内联门控均被跳过（brainstorm 没有 PHASE-GATE，
因此 lean 模式跳过所有门控）。输出中注明全部 4 个：
"[门控ID] skipped — lean mode"。

`solo` 模式：全部 4 个门控均被跳过。输出中注明全部 4 个：
"[门控ID] skipped — solo mode"。

---

## 测试用例

### 用例 1：正常路径——Full 模式，3 个方案，用户选择一个，所有 4 个 director 批准

**夹具：**
- 不存在 `design/gdd/game-concept.md`
- `production/session-state/review-mode.txt` 内容为 `full`

**输入：** `/brainstorm`

**预期行为：**
1. 技能向用户提问关于类型、规模和目标感受的问题
2. 技能呈现 3 个概念方案，各附优缺点
3. 用户选择一个方案
4. 技能将所选概念细化为结构化草稿
5. 所有 4 个 director 门控并行生成：CD-PILLARS、AD-CONCEPT-VISUAL、TD-FEASIBILITY、PR-SCOPE
6. 所有 4 个返回 APPROVED
7. 技能询问"May I write `design/gdd/game-concept.md`?"
8. 批准后写入概念文档

**断言：**
- [ ] 恰好呈现 3 个概念方案（不是 1 个，也不是 5 个或更多）
- [ ] 所有 4 个 director 门控并行生成（非顺序）
- [ ] 所有 4 个门控完成后才询问"May I write"
- [ ] 在询问"May I write `design/gdd/game-concept.md`?"前不写入概念文件
- [ ] 未经用户批准不写入概念文件
- [ ] 下一步交接指向 `/map-systems`

---

### 用例 2：失败路径——CD-PILLARS 返回 REJECT

**夹具：**
- 概念草稿已完成
- `production/session-state/review-mode.txt` 内容为 `full`
- CD-PILLARS 门控返回 REJECT："The concept has no identifiable creative pillar"

**输入：** `/brainstorm`

**预期行为：**
1. CD-PILLARS 门控返回 REJECT 并附具体反馈
2. 技能将拒绝原因呈现给用户
3. 概念不写入文件
4. 询问用户：重新考虑概念方向，或覆盖拒绝
5. 若选择重新考虑：技能返回概念方案选择阶段

**断言：**
- [ ] CD-PILLARS 返回 REJECT 时概念不写入
- [ ] 拒绝反馈原文呈现给用户
- [ ] 用户获得重新考虑或覆盖的选项
- [ ] 用户选择重新考虑时，技能返回概念构思阶段

---

### 用例 3：Lean 模式——所有 4 个门控被跳过；用户确认后写入概念

**夹具：**
- 不存在游戏概念
- `production/session-state/review-mode.txt` 内容为 `lean`

**输入：** `/brainstorm`

**预期行为：**
1. 呈现概念方案，用户选择一个
2. 概念细化为结构化草稿
3. 所有 4 个 director 门控被跳过——每个注明："[门控ID] skipped — lean mode"
4. 技能询问用户确认概念是否准备好写入
5. 用户确认后询问"May I write `design/gdd/game-concept.md`?"
6. 批准后写入概念

**断言：**
- [ ] 所有 4 个门控跳过注释出现：
  "CD-PILLARS skipped — lean mode"、"AD-CONCEPT-VISUAL skipped — lean mode"、
  "TD-FEASIBILITY skipped — lean mode"、"PR-SCOPE skipped — lean mode"
- [ ] 仅在用户确认后写入概念（lean 模式下不需要 director 批准）
- [ ] 仍然在写入前询问"May I write"

---

### 用例 4：Solo 模式——所有门控被跳过；仅需用户批准即可写入概念

**夹具：**
- 不存在游戏概念
- `production/session-state/review-mode.txt` 内容为 `solo`

**输入：** `/brainstorm`

**预期行为：**
1. 呈现概念方案，用户选择一个
2. 向用户展示概念草稿
3. 所有 4 个 director 门控被跳过——每个注明"solo mode"
4. 询问"May I write `design/gdd/game-concept.md`?"
5. 用户批准后写入概念

**断言：**
- [ ] 所有 4 个跳过注释出现，带有"solo mode"标签
- [ ] 不生成任何 director agent
- [ ] 仅需用户批准即可写入概念
- [ ] 行为其他方面与 lean 模式等同

---

### 用例 5：Director 门控——PR-SCOPE 返回 CONCERNS（规模过大）

**夹具：**
- 概念草稿已完成
- `production/session-state/review-mode.txt` 内容为 `full`
- PR-SCOPE 门控返回 CONCERNS："The concept scope would require 18+ months for a solo developer"

**输入：** `/brainstorm`

**预期行为：**
1. PR-SCOPE 门控返回 CONCERNS 并附具体规模反馈
2. 技能将规模顾虑呈现给用户
3. 规模顾虑在写入前记录到概念草稿中
4. 询问用户：缩减规模、接受顾虑并记录，或重新考虑
5. 若接受顾虑：概念写入时嵌入"Scope Risk"注释

**断言：**
- [ ] 在询问"May I write"之前向用户展示 PR-SCOPE 顾虑
- [ ] 在未展示规模顾虑的情况下不写入概念
- [ ] 若用户接受：规模顾虑记录在概念文件中
- [ ] 技能不因 PR-SCOPE CONCERNS 自动拒绝概念（由用户决定）

---

## 协议合规

- [ ] 用户确认前呈现 2-4 个概念方案并附优缺点
- [ ] 用户确认概念方向后才调用 director 门控
- [ ] full 模式下所有 4 个 director 门控并行生成
- [ ] lean 和 solo 模式下所有 4 个门控均被跳过——每个均注明名称
- [ ] 在写入前询问"May I write `design/gdd/game-concept.md`?"
- [ ] 以下一步交接 `/map-systems` 结束

---

## 覆盖范围说明

- AD-CONCEPT-VISUAL 门控（美术总监可行性评估）与其他 3 个门控一起在并行生成中归为一组——不单独进行 Fixture 测试。
- 迭代概念细化循环（用户拒绝所有方案，Skill 生成新方案）未经 Fixture 测试——它遵循与方案选择阶段相同的模式。
- game-concept.md 文档结构（必填章节）在 Skill 主体中定义，不在测试断言中重新列举。
