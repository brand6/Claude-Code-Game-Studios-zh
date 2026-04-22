# Skill 测试规范：/create-epics

## Skill 摘要

`/create-epics` 读取所有已批准的 GDD 并将其转化为 EPIC.md 文件，每个系统对应一个。Epic 按层级（Foundation → Core → Feature → Presentation）组织，并在各层级内按优先级顺序处理。每个 EPIC.md 包含范围、管理 ADR、GDD 要求、引擎风险等级和 Definition of Done。Skill 在创建每个 EPIC 文件前询问"May I write"。

在 `full` 审核模式下，PR-EPIC 门控（Producer）在起草 Epic 后、写入任何文件前运行。在 `lean` 或 `solo` 模式下，PR-EPIC 被跳过并注明。Epic 写入 `production/epics/[layer]/EPIC-[name].md`。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需 Fixture。

- [ ] 包含必填 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含 ≥2 个阶段标题
- [ ] 包含 verdict 关键词：CREATED、BLOCKED
- [ ] 包含"May I write"协作协议语言（按 Epic 逐一批准）
- [ ] 末尾包含下一步交接（`/create-stories`）
- [ ] 说明 PR-EPIC 门控行为：full 模式运行，lean/solo 跳过

---

## Director 门控检查

`full` 模式下：PR-EPIC（Producer）门控在 Epic 起草完成后、任何 Epic 文件写入前运行。若 PR-EPIC 返回 CONCERNS，Epic 在"May I write"询问前先修订。

`lean` 模式下：PR-EPIC 被跳过。输出注明："PR-EPIC skipped — lean mode"。

`solo` 模式下：PR-EPIC 被跳过，注明方式相同。

---

## 测试用例

### 用例 1：正常路径——两个已批准 GDD 创建两个 EPIC 文件

**Fixture：**
- `design/gdd/systems-index.md` 存在，列出 2 个系统
- 两个系统均在 `design/gdd/` 中有已批准的 GDD
- `docs/architecture/architecture.md` 存在，包含匹配的模块
- 每个系统至少有一个 Accepted ADR
- `production/session-state/review-mode.txt` 内容为 `lean`

**输入：** `/create-epics`

**预期行为：**
1. Skill 读取系统索引和两个 GDD
2. 起草 2 个 EPIC 定义（层级、GDD 路径、ADR、要求、引擎风险）
3. PR-EPIC 门控被跳过（lean 模式）——在输出中注明
4. 对每个 Epic：询问"May I write `production/epics/[layer]/EPIC-[name].md`?"
5. 批准后写入两个 EPIC 文件
6. 创建或更新 `production/epics/index.md`

**断言：**
- [ ] 任何写入询问前先展示 Epic 摘要
- [ ] 逐 Epic 询问"May I write"（不是一次性批准所有 Epic）
- [ ] 每个 EPIC.md 包含：层级、GDD 路径、管理 ADR、要求表、Definition of Done
- [ ] 输出中注明 PR-EPIC 跳过
- [ ] 写入后更新 `production/epics/index.md`
- [ ] 未经逐 Epic 批准 Skill 不写入 EPIC 文件

---

### 用例 2：失败路径——未找到已批准的 GDD

**Fixture：**
- `design/gdd/systems-index.md` 存在
- `design/gdd/` 中没有已批准状态的 GDD（全部为 Draft 或 In Progress）

**输入：** `/create-epics`

**预期行为：**
1. Skill 读取系统索引并尝试查找已批准的 GDD
2. 未找到已批准的 GDD
3. Skill 输出："No approved GDDs to convert. GDDs must be Approved before creating epics."
4. Skill 建议先运行 `/design-system` 完成 GDD 批准
5. Skill 退出，不创建任何 EPIC 文件

**断言：**
- [ ] 不存在已批准 GDD 时 Skill 以明确消息干净退出
- [ ] 不写入 EPIC 文件
- [ ] Skill 推荐正确的下一步操作
- [ ] Verdict 为 BLOCKED

---

### 用例 3：Director 门控——Full 模式在写入前生成 PR-EPIC

**Fixture：**
- 2 个已批准的 GDD 存在
- `production/session-state/review-mode.txt` 内容为 `full`

**Full 模式预期行为：**
1. Skill 起草两个 Epic
2. PR-EPIC 门控生成并审核 Epic 草稿
3. PR-EPIC 返回 APPROVED：正常进行"May I write"询问
4. 批准后写入 Epic 文件

**断言（full 模式）：**
- [ ] 输出中 PR-EPIC 门控作为活跃门控显示
- [ ] PR-EPIC 在任何"May I write"询问前运行
- [ ] PR-EPIC 完成前不写入 Epic 文件

**Fixture（lean 模式）：**
- 相同 GDD
- `production/session-state/review-mode.txt` 内容为 `lean`

**Lean 模式预期行为：**
1. Epic 起草完成
2. PR-EPIC 被跳过——在输出中注明
3. 直接进行"May I write"询问

**断言（lean 模式）：**
- [ ] 输出中出现"PR-EPIC skipped — lean mode"
- [ ] Skill 无需等待 PR-EPIC 直接进行"May I write"

---

### 用例 4：边缘情况——某个 GDD 对应的 Epic 已存在

**Fixture：**
- `production/epics/[layer]/EPIC-[name].md` 已为其中一个已批准 GDD 存在
- 另一个 GDD 没有对应的 EPIC 文件

**输入：** `/create-epics`

**预期行为：**
1. Skill 检测到第一个系统的 EPIC 文件已存在
2. Skill 提供更新而非覆盖选项："EPIC-[name].md already exists. Update it, or skip?"
3. 第二个系统（无现有文件）：正常进行"May I write"

**断言：**
- [ ] Skill 写入前检测是否存在 EPIC 文件
- [ ] 向用户提供"更新"或"跳过"选项——不自动覆盖
- [ ] 新系统的 EPIC 正常创建，无冲突

---

### 用例 5：Director 门控——PR-EPIC 返回 CONCERNS

**Fixture：**
- 2 个已批准的 GDD 存在
- `production/session-state/review-mode.txt` 内容为 `full`
- PR-EPIC 门控返回 CONCERNS（例如某个 Epic 范围过大）

**输入：** `/create-epics`

**预期行为：**
1. PR-EPIC 门控生成并返回带具体反馈的 CONCERNS
2. Skill 在任何写入询问前将 CONCERNS 呈现给用户
3. 向用户提供选项：修订 Epic、接受 CONCERNS 后继续或停止
4. 用户修订后：更新后的 Epic 草稿在"May I write"询问前重新展示
5. CONCERNS 未解决时 Skill 不写入 Epic

**断言：**
- [ ] PR-EPIC 的 CONCERNS 在写入前展示给用户
- [ ] 返回 CONCERNS 时 Skill 不自动写入 Epic
- [ ] 向用户提供清晰的修订、继续或停止选择
- [ ] 修订后最终批准前重新展示修订后的 Epic 草稿

---

## 协议合规

- [ ] 任何"May I write"询问前先向用户展示 Epic 草稿
- [ ] 逐 Epic 询问"May I write"，不是一次性批准整批
- [ ] PR-EPIC 门控（如活跃）在写入询问前运行——不是之后
- [ ] 跳过的门控在输出中按名称和模式注明
- [ ] EPIC.md 内容仅来源于 GDD、ADR 和架构文档——不凭空捏造
- [ ] 末尾包含下一步交接：每个已创建 Epic 对应 `/create-stories [epic-slug]`

---

## 覆盖范围说明

- Core、Feature 和 Presentation 层的处理遵循与 Foundation 相同的逐 Epic 模式——不单独测试层级特定的排序。
- 从管理 ADR 推导引擎风险等级（LOW/MEDIUM/HIGH）通过用例 1 的 Fixture 结构隐式验证。
- `layer: [name]` 和 `[system-name]` 参数模式遵循与默认（所有系统）模式相同的批准流程。
