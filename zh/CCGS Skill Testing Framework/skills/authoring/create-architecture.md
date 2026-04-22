# Skill Test Spec: /create-architecture

## Skill 概述

引导骨架优先的架构文档逐节编写。
完整模式：所有章节起草完成后，TD-ARCHITECTURE 和 LP-FEASIBILITY 门控并行运行。
精简/独立模式：门控跳过。
若文档已存在，则进入改造模式。
输出：`docs/architecture/architecture.md`。
下一步：`/architecture-review` 或 `/create-control-manifest`。
裁决：APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 完整模式中 TD-ARCHITECTURE 和 LP-FEASIBILITY 门控并行派生
- [ ] 精简/独立模式中门控跳过并注明
- [ ] 骨架文件优先创建（所有章节标题，内容为空）
- [ ] 按章节询问"May I write section [N]?"
- [ ] Proposed 状态 ADR 引用被标记为风险
- [ ] 输出路径为 `docs/architecture/architecture.md`
- [ ] 裁决关键字：APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED
- [ ] 末尾包含下一步交接：`/architecture-review` 或 `/create-control-manifest`

---

## 门控检查

### TD-ARCHITECTURE 门控（技术总监架构审查）

**触发条件：** 完整模式下所有章节均已起草后

**派生 agent：** technical-director（内部门控 ID：TD-ARCHITECTURE）

**预期行为：**
- technical-director 评审完整架构文档，检查架构完整性、引擎兼容性、系统边界清晰度
- 返回裁决：APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED

**断言：**
- [ ] 仅在完整模式下派生 technical-director
- [ ] 精简/独立模式中不派生
- [ ] 与 LP-FEASIBILITY 并行派生（同时发出 Task 调用）

### LP-FEASIBILITY 门控（首席程序员可行性评审）

**触发条件：** 完整模式下所有章节均已起草后（与 TD-ARCHITECTURE 并行）

**派生 agent：** lead-programmer（内部门控 ID：LP-FEASIBILITY）

**预期行为：**
- lead-programmer 评估实现可行性、技术债务风险、团队能力匹配度
- 返回裁决：APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED

**断言：**
- [ ] 仅在完整模式下派生 lead-programmer
- [ ] 精简/独立模式中不派生
- [ ] 与 TD-ARCHITECTURE 并行（同时 Task 调用）

---

## 测试用例

### 用例 1：正常路径——完整模式，两个门控均 APPROVED

**测试夹具：**
- 完整模式：`production/session-state/review-mode.txt` 为 `full`
- 所有相关 GDD 位于 `design/gdd/`
- 所有引用的 ADR 状态均为 Accepted
- 两个门控均返回 APPROVED

**输入：** `/create-architecture`

**预期行为：**
1. 上下文收集：读取所有 GDD、现有 ADR、引擎参考文档
2. 立即创建包含所有章节标题的骨架文件：`docs/architecture/architecture.md`
3. 按章节逐节引导，每节含独立"May I write"询问
4. 所有章节起草完成后，并行派生 TD-ARCHITECTURE 和 LP-FEASIBILITY
5. 两者均返回 APPROVED
6. 裁决：APPROVED
7. 下一步：`/architecture-review` 或 `/create-control-manifest`

**断言：**
- [ ] 骨架文件在内容讨论之前创建
- [ ] TD-ARCHITECTURE 和 LP-FEASIBILITY 的 Task 调用同时发出
- [ ] 两者均 APPROVED 时裁决为 APPROVED
- [ ] 输出路径为 `docs/architecture/architecture.md`
- [ ] 末尾引用 `/architecture-review` 或 `/create-control-manifest`

---

### 用例 2：完整模式，TD-ARCHITECTURE 返回 MAJOR REVISION

**测试夹具：**
- 完整模式
- TD-ARCHITECTURE 返回 MAJOR REVISION NEEDED：系统边界不清晰，多个系统职责重叠，需要重新设计模块划分
- LP-FEASIBILITY 返回 APPROVED

**输入：** `/create-architecture`（门控评审场景）

**预期行为：**
1. 所有章节起草完成
2. TD-ARCHITECTURE 和 LP-FEASIBILITY 并行评审
3. TD-ARCHITECTURE 返回 MAJOR REVISION NEEDED
4. 编排者显示：裁决为 MAJOR REVISION NEEDED——需要重大修订
5. 具体问题列出（系统边界问题、职责重叠）
6. 因有 MAJOR REVISION NEEDED，不以 APPROVED 状态最终化文档
7. `AskUserQuestion` 提供选项：
   - 重新设计受影响的架构章节后重新提交评审
   - 在此停止，与技术总监深入讨论后再继续

**断言：**
- [ ] TD-ARCHITECTURE 返回 MAJOR REVISION NEEDED 时，裁决不为 APPROVED
- [ ] 具体修订原因（系统边界问题）在输出中列出
- [ ] `AskUserQuestion` 提供修订并重评审的选项
- [ ] 裁决为 MAJOR REVISION NEEDED

---

### 用例 3：精简模式——门控跳过

**测试夹具：**
- 精简模式：`production/session-state/review-mode.txt` 为 `lean`

**输入：** `/create-architecture`

**预期行为：**
1. 骨架文件创建；按章节逐节完成
2. 所有章节完成后，无门控派生
3. 输出注明："[TD-ARCHITECTURE] 跳过——精简模式；[LP-FEASIBILITY] 跳过——精简模式"
4. 裁决：APPROVED（精简模式下完成即视为 APPROVED，但注明未经门控审查）

**断言：**
- [ ] 精简模式下不派生 TD-ARCHITECTURE 和 LP-FEASIBILITY
- [ ] 两个门控的跳过均明确注明（含模式名称）
- [ ] 无门控输出

---

### 用例 4：改造模式——架构文档已存在

**测试夹具：**
- `docs/architecture/architecture.md` 已存在，包含部分章节

**输入：** `/create-architecture`

**预期行为：**
1. Skill 读取现有 `docs/architecture/architecture.md`
2. 编排者注明："发现现有架构文档——进入改造模式"
3. 分析现有内容，识别完整章节 vs 缺失章节
4. `AskUserQuestion` 提供：
   - 仅补充缺失章节
   - 修订特定章节（用户指定）
   - 从头重写整个架构文档

**断言：**
- [ ] 发现现有架构文档时不被静默覆盖
- [ ] 编排者识别哪些章节已完整、哪些需要补充
- [ ] `AskUserQuestion` 提供改造选项

---

### 用例 5：引用 Proposed 状态 ADR——标记为风险

**测试夹具：**
- 架构文档引用 ADR-007-physics-backend，其状态为 Proposed（非 Accepted）
- 编写"物理系统"章节时引用此 ADR

**输入：** `/create-architecture`（章节写作场景）

**预期行为：**
1. 编写"物理系统"章节时，Skill 检测到 ADR-007-physics-backend 状态为 Proposed
2. 在该章节中嵌入风险说明："⚠ 风险：ADR-007-physics-backend（物理后端架构）状态为 Proposed——此架构决策尚未最终确定，该章节依赖可能变更的决策。"
3. TD-ARCHITECTURE 和 LP-FEASIBILITY 门控仍正常派生（风险标记不阻塞门控）
4. 风险标记包含具体 ADR 编号和标题

**断言：**
- [ ] Proposed 状态 ADR 引用在章节起草时被检测到并标记为风险
- [ ] 风险说明嵌入架构文档的相关章节中
- [ ] TD-ARCHITECTURE 和 LP-FEASIBILITY 仍正常派生（风险不阻塞门控）
- [ ] 风险标记包含具体 ADR 编号和标题

---

## 协议合规性

- [ ] 骨架文件在任何章节内容讨论之前创建
- [ ] 按章节逐节询问"May I write [章节]?"
- [ ] 完整模式中 TD-ARCHITECTURE 和 LP-FEASIBILITY 并行派生
- [ ] 精简/独立模式跳过门控并明确注明
- [ ] Proposed 状态 ADR 引用在文档中标记为风险
- [ ] 末尾包含下一步交接：`/architecture-review` 或 `/create-control-manifest`

---

## 覆盖率说明

- 架构文档所需章节列表在 Skill 主体和 `/architecture-review` Skill 中定义——
  未在此 spec 中重新枚举。
- 架构文档中的引擎版本标注（与 ADR 标注并行）是编写工作流的一部分——
  通过用例 1 隐式测试。
- 改造模式下单次会话中更新多个章节遵循相同的逐章节批准模式——
  未独立测试多章节改造场景。
