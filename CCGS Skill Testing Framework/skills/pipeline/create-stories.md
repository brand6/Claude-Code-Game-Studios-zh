# Skill 测试规范：/create-stories

## Skill 摘要

`/create-stories [epic-name]` 读取 EPIC.md 文件并将其每个要求转化为一个完整的 Story 文件，包含 frontmatter、TR-ID、管理 ADR 引用、控制清单规则（摘自控制清单）和验收标准。Story 写入 `production/epics/[layer]/story-[name].md`。

在 `full` 审核模式下，QL-STORY-READY 门控（QA Lead）在展示给用户前对每个 Story 草稿运行。在 `lean` 或 `solo` 模式下，QL-STORY-READY 被跳过并注明。Skill 在创建每个 Story 文件前询问"May I write"。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需 Fixture。

- [ ] 包含必填 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含 ≥2 个阶段标题
- [ ] 包含 verdict 关键词：COMPLETE、BLOCKED、NEEDS WORK
- [ ] 包含"May I write"协作协议语言（按 Story 逐一批准）
- [ ] 末尾包含下一步交接（`/story-readiness` → `/dev-story`）
- [ ] 说明 QL-STORY-READY 门控行为：full 模式运行，lean/solo 跳过

---

## Director 门控检查

`full` 模式下：QL-STORY-READY（QA Lead）门控对每个 Story 草稿运行，在向用户展示前评估其准备状态。失败的 Story 标记为 NEEDS WORK，并附具体反馈；用户可选择继续或修订。

`lean` 模式下：QL-STORY-READY 被跳过。输出注明："QL-STORY-READY skipped — lean mode"。

`solo` 模式下：QL-STORY-READY 被跳过，注明方式相同。

---

## 测试用例

### 用例 1：正常路径——含 3 个要求的 Epic 创建 3 个 Story

**Fixture：**
- `production/epics/[layer]/EPIC-[name].md` 存在，包含 3 个要求
- 所有管理 ADR 均为 Accepted 状态
- `docs/architecture/control-manifest.md` 存在
- TR 注册表中存在所有 TR-ID
- `production/session-state/review-mode.txt` 内容为 `lean`

**输入：** `/create-stories [epic-name]`

**预期行为：**
1. Skill 读取 EPIC.md、相关 GDD、管理 ADR、控制清单和 TR 注册表
2. 为 3 个要求各起草一个 Story
3. QL-STORY-READY 被跳过（lean 模式）——在输出中注明
4. 展示 3 个 Story 草稿
5. 对每个 Story 逐一询问"May I write `production/epics/[layer]/story-[name].md`?"
6. 批准后写入全部 3 个 Story 文件

**断言：**
- [ ] 任何写入询问前先展示全部 3 个 Story 草稿
- [ ] 逐 Story 询问"May I write"（不是一次性批准）
- [ ] 每个 Story 文件包含：frontmatter、TR-ID（引用注册表）、ADR 引用、控制清单规则、验收标准
- [ ] 输出中注明 QL-STORY-READY 跳过
- [ ] 未经逐 Story 批准 Skill 不写入

---

### 用例 2：失败路径——未找到 Epic 文件

**Fixture：**
- `production/epics/` 目录存在但不含指定的 EPIC 文件

**输入：** `/create-stories [epic-name]`

**预期行为：**
1. Skill 尝试读取 EPIC 文件但失败
2. Skill 输出明确错误："Epic 'epic-name' not found. Run `/create-epics` first."
3. Skill 退出，不创建 Story 文件

**断言：**
- [ ] 未找到 EPIC 文件时 Skill 输出明确错误
- [ ] Skill 推荐运行 `/create-epics` 作为下一步
- [ ] 不写入 Story 文件
- [ ] Verdict 为 BLOCKED

---

### 用例 3：依赖检查——被阻塞的 Story（Proposed ADR）

**Fixture：**
- EPIC.md 包含 3 个要求
- ADR 1（管理 Story 1 和 Story 3）：Accepted
- ADR 2（管理 Story 2）：Proposed

**输入：** `/create-stories [epic-name]`

**预期行为：**
1. Skill 检查所有 Story 的管理 ADR
2. Story 2 在其 ADR 尚未 Accepted 时，ADR 依赖标记为阻塞
3. Story 1 和 Story 3：Status: Ready
4. Story 2：Status: Blocked（依赖 [ADR 编号] 尚未 Accepted）
5. 全部 3 个 Story 草稿展示给用户，含各自状态
6. 全部 3 个 Story 均写入——被阻塞的 Story 以 Blocked 状态写入

**断言：**
- [ ] Story 2 在草稿中标记为 Status: Blocked
- [ ] 阻塞说明包含具体 ADR 编号并推荐运行 `/architecture-decision`
- [ ] Story 1 和 Story 3 在草稿中标记为 Status: Ready
- [ ] 全部 Story 文件写入（被阻塞的 Story 也写入——只是标记为 Blocked）

---

### 用例 4：边缘情况——未提供参数

**Fixture：**
- `production/epics/` 目录存在，包含 ≥2 个 Epic 子目录

**输入：** `/create-stories`（无参数）

**预期行为：**
1. Skill 检测到未提供参数
2. 输出用法错误："No epic specified. Usage: /create-stories [epic-name]"
3. Skill 列出 `production/epics/` 中可用的 Epic
4. 不创建 Story 文件

**断言：**
- [ ] 未提供参数时 Skill 输出用法错误
- [ ] Skill 列出可用 Epic 帮助用户选择
- [ ] 不写入 Story 文件
- [ ] Skill 不在无用户输入的情况下静默选择 Epic

---

### 用例 5：Director 门控——Full 模式运行 QL-STORY-READY；失败的 Story 标记为 NEEDS WORK

**Fixture：**
- EPIC.md 包含 2 个要求
- 两个管理 ADR 均为 Accepted
- `production/session-state/review-mode.txt` 内容为 `full`
- QL-STORY-READY 检查发现其中一个 Story 的验收标准不明确

**输入：** `/create-stories [epic-name]`

**预期行为：**
1. 起草两个 Story
2. 对每个 Story 运行 QL-STORY-READY 检查
3. Story 1 通过 QL-STORY-READY
4. Story 2 未通过 QL-STORY-READY——标记为 NEEDS WORK，并附具体反馈
5. 在"May I write"询问前向用户展示两个 Story（含通过/未通过状态）
6. 用户可选择继续（以 NEEDS WORK 注记写入 Story）或先修订

**断言：**
- [ ] 输出中每个 Story 均显示 QL-STORY-READY 结果
- [ ] Story 2 标记为 NEEDS WORK，并附具体未通过标准
- [ ] Story 1 显示为通过 QL-STORY-READY
- [ ] 写入前向用户提供继续或修订的选择
- [ ] Skill 不在无用户输入的情况下自动阻止 QL-STORY-READY 未通过 Story 的写入

---

## 协议合规

- [ ] 起草 Story 前加载全部上下文（EPIC、GDD、ADR、清单、TR 注册表）
- [ ] 任何"May I write"询问前完整展示 Story 草稿
- [ ] 逐 Story 询问"May I write"（不是一次性批准整批）
- [ ] 被阻塞的 Story 在写入批准前标记——不是写入后才发现
- [ ] TR-ID 引用注册表——要求文本不直接内嵌在 Story 文件中
- [ ] 控制清单规则摘自清单文件，不凭空捏造
- [ ] 末尾包含下一步交接：`/story-readiness` → `/dev-story`

---

## 覆盖率说明

- Integration Story 的测试证明（Playtest 文档替代方案）与 Logic Story 采用相同的批准模式——未独立设计 Fixture 测试。
- Story 排序（基础优先，UI 最后）通过用例 1 的多 Story Fixture 隐式验证。
- Story 规模规则（拆分大型要求组）未在此测试——由 `/create-stories` Skill 的内部逻辑处理。
