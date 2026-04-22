# Skill Test Spec: /architecture-decision

## Skill 概述

引导逐节编写架构决策记录（ADR）。6 个必需章节：状态、上下文、决策、后果、替代方案、
关联 ADR。引擎版本从 `docs/engine-reference/` 标注。
完整模式：TD-ADR + LP-FEASIBILITY 门控并行 → 两者均 APPROVED 时状态为 Accepted。
精简/独立模式：门控跳过 → 状态为 Proposed。
输出：`docs/architecture/adr-NNN-[name].md`。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 明确列出 6 个必需章节：状态（Status）、上下文（Context）、决策（Decision）、后果（Consequences）、替代方案（Alternatives）、关联 ADR（Related ADRs）
- [ ] 完整模式中 TD-ADR 和 LP-FEASIBILITY 门控并行派生
- [ ] ADR 状态规则：仅当完整模式且两者均 APPROVED 时为 Accepted
- [ ] 精简和独立模式中跳过门控并注明
- [ ] 按章节询问"May I write"
- [ ] 输出路径遵循 `docs/architecture/adr-NNN-[name].md` 模式
- [ ] 末尾包含下一步交接：`/architecture-review` 或 `/create-control-manifest`

---

## 门控检查

### TD-ADR 门控（技术总监审查）

**触发条件：** 完整模式下所有 6 个章节均已起草后

**派生 agent：** technical-director（内部门控 ID：TD-ADR）

**预期行为：**
- technical-director 评审 ADR 草稿，检查技术合理性、引擎兼容性和架构一致性
- 返回裁决：APPROVED / CONCERNS / REJECTED

**断言：**
- [ ] 仅在完整模式下派生 technical-director
- [ ] 精简或独立模式中不派生 TD-ADR
- [ ] TD-ADR 和 LP-FEASIBILITY 在完整模式下并行派生（同时发出 Task 调用）

### LP-FEASIBILITY 门控（首席程序员可行性评审）

**触发条件：** 完整模式下所有 6 个章节均已起草后（与 TD-ADR 并行）

**派生 agent：** lead-programmer（内部门控 ID：LP-FEASIBILITY）

**预期行为：**
- lead-programmer 评估实现可行性、代码复杂度和团队能力匹配
- 返回裁决：APPROVED / CONCERNS / REJECTED

**断言：**
- [ ] 仅在完整模式下派生 lead-programmer
- [ ] 精简或独立模式中不派生 LP-FEASIBILITY
- [ ] LP-FEASIBILITY 和 TD-ADR 并行（同时 Task 调用）

---

## 测试用例

### 用例 1：正常路径——完整模式，两个门控均 APPROVED，状态为 Accepted

**测试夹具：**
- 完整模式：`production/session-state/review-mode.txt` 为 `full`
- 引擎已配置（Godot 4）
- ADR 主题：状态机架构用于敌人 AI
- 两个门控（TD-ADR 和 LP-FEASIBILITY）均返回 APPROVED

**输入：** `/architecture-decision enemy-ai-state-machine`

**预期行为：**
1. 上下文收集：读取现有 ADR 以确定下一个序号（NNN）
2. 立即创建包含所有 6 个章节标题的骨架文件：`docs/architecture/adr-NNN-enemy-ai-state-machine.md`
3. 按章节逐节引导：
   - 提出每个章节的内容建议
   - 逐节询问"May I write section [N]?"
   - 用户批准后写入该章节
4. 引擎版本从 `docs/engine-reference/` 读取后标注在 ADR 中
5. 所有 6 个章节起草完成后，并行派生 TD-ADR 和 LP-FEASIBILITY 门控
6. 两个门控均返回 APPROVED
7. ADR 状态更新为 `Accepted`
8. 输出文件保存，引用下一步：`/architecture-review` 或 `/create-control-manifest`

**断言：**
- [ ] 骨架文件在讨论任何内容之前创建
- [ ] 按章节逐节引导并询问"May I write"
- [ ] 引擎版本在 ADR 中标注
- [ ] TD-ADR 和 LP-FEASIBILITY 的 Task 调用同时发出（并行）
- [ ] 两者均 APPROVED 时 ADR 状态为 Accepted
- [ ] 输出路径遵循 `docs/architecture/adr-NNN-[name].md` 模式
- [ ] 末尾引用 `/architecture-review` 或 `/create-control-manifest`

---

### 用例 2：完整模式，一个门控返回 CONCERNS——状态保持 Proposed

**测试夹具：**
- 完整模式
- TD-ADR 返回 APPROVED
- LP-FEASIBILITY 返回 CONCERNS：实现复杂度过高，团队可能需要额外培训

**输入：** `/architecture-decision network-replication`（门控结果场景）

**预期行为：**
1. 所有 6 个章节起草完成
2. TD-ADR 和 LP-FEASIBILITY 并行派生
3. TD-ADR：APPROVED；LP-FEASIBILITY：CONCERNS
4. 编排者显示：LP-FEASIBILITY 返回 CONCERNS——ADR 状态保持 Proposed
5. 具体 CONCERNS 内容列出（实现复杂度问题）
6. Skill 不将状态设为 Accepted（任何一个门控返回非 APPROVED 时均不 Accepted）
7. `AskUserQuestion` 提供选项：
   - 修订决策章节以简化实现方案，然后重新请求门控审查
   - 保持现状，维持 Proposed 状态并记录 CONCERNS
   - 在此停止，等待团队讨论后再继续

**断言（CONCERNS）：**
- [ ] ADR 状态为 Proposed（非 Accepted）
- [ ] CONCERNS 内容列于输出中
- [ ] 任何一个门控返回 CONCERNS 时 Skill 不设置 Accepted 状态
- [ ] 精简/独立模式下 ADR 状态始终为 Proposed（无论内容质量如何）

**断言（精简/独立模式）：**
- [ ] 精简模式下 ADR 状态为 Proposed
- [ ] 独立模式下 ADR 状态为 Proposed
- [ ] 精简或独立模式下无门控输出

---

### 用例 3：精简模式——两个门控均跳过，状态为 Proposed

**测试夹具：**
- 精简模式：`production/session-state/review-mode.txt` 为 `lean`

**输入：** `/architecture-decision ui-framework`

**预期行为：**
1. 骨架文件创建
2. 按章节逐节引导写作
3. 6 个章节全部完成后，无门控派生
4. 输出注明："[TD-ADR] 跳过——精简模式；[LP-FEASIBILITY] 跳过——精简模式"
5. ADR 状态设为 Proposed
6. 裁决：COMPLETE（精简模式下 Proposed 是正常结果）

**断言：**
- [ ] 精简模式下不派生 TD-ADR 和 LP-FEASIBILITY
- [ ] 两个门控的跳过均明确注明（带模式名称）
- [ ] ADR 状态为 Proposed（精简模式下的正常结果）
- [ ] 输出中无门控内容

---

### 用例 4：ADR 已存在——更新或取代

**测试夹具：**
- `docs/architecture/adr-005-save-system.md` 已存在，状态为 Accepted
- 用户希望修订保存系统架构

**输入：** `/architecture-decision save-system`

**预期行为：**
1. 上下文收集：发现 `adr-005-save-system.md` 已存在
2. 编排者在对话中注明："发现现有 ADR：adr-005-save-system.md（状态：Accepted）"
3. `AskUserQuestion` 提供选项：
   - 更新现有 ADR（adr-005 修订版，状态重置为 Proposed 直至重新评审）
   - 创建取代 ADR（新 adr-NNN，`Related ADRs` 中引用"取代 adr-005"）
4. 根据用户选择，执行相应路径
5. 若创建取代 ADR：adr-005 的状态更新为 Superseded

**断言：**
- [ ] 发现现有 ADR 时明确注明，不被静默覆盖
- [ ] `AskUserQuestion` 提供更新或取代的选项
- [ ] 创建取代 ADR 时，旧 ADR 状态更新为 Superseded
- [ ] 取代 ADR 在 `Related ADRs` 章节引用被取代的 ADR

---

### 用例 5：ADR 状态规则矩阵

**测试夹具：** 各种模式和门控结果组合

**输入：** 多个场景

**状态规则矩阵：**

| 模式 | TD-ADR | LP-FEASIBILITY | 预期 ADR 状态 |
|------|--------|----------------|--------------|
| 完整 | APPROVED | APPROVED | Accepted |
| 完整 | APPROVED | CONCERNS | Proposed |
| 完整 | CONCERNS | APPROVED | Proposed |
| 完整 | REJECTED | APPROVED | Proposed |
| 精简 | 跳过 | 跳过 | Proposed |
| 独立 | 跳过 | 跳过 | Proposed |

**断言（CONCERNS）：**
- [ ] ADR 状态为 Proposed（frontmatter/标题中显示 `Status: Proposed`）
- [ ] CONCERNS 列于输出中
- [ ] 任何门控返回 CONCERNS 时 Skill 不设置 Accepted 状态

**断言（精简/独立）：**
- [ ] 精简模式下 ADR 状态为 Proposed
- [ ] 独立模式下 ADR 状态为 Proposed
- [ ] 精简或独立模式下无门控输出

---

## 协议合规性

- [ ] 所有 6 个必需章节在门控审查之前完成起草
- [ ] 引擎版本从 `docs/engine-reference/` 标注在 ADR 中
- [ ] 起草期间按章节询问"May I write"
- [ ] 完整模式中 TD-ADR 和 LP-FEASIBILITY 并行派生
- [ ] 精简/独立模式跳过门控时明确注明（含模式名称）
- [ ] ADR 状态：仅在完整模式且两者均 APPROVED 时为 Accepted
- [ ] 末尾包含下一步交接：`/architecture-review` 或 `/create-control-manifest`

---

## 覆盖率说明

- ADR 自动编号（自增 NNN）逻辑未独立测试——
  Skill 通过读取现有 ADR 文件名来分配下一个编号。
- 关联 ADR 章节的链接类型（取代/关联）通过用例 4 进行了
  结构性测试，但并非所有链接类型均独立验证。
- TR 注册表更新（当 ADR 中定义了新的 TR-ID 时）作为写入阶段的一部分——
  通过用例 1 隐式测试。
