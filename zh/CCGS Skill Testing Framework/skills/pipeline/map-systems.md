# Skill 测试规范：/map-systems

## Skill 摘要

`/map-systems` 读取游戏概念文档，将游戏分解为独立系统，映射依赖关系并创建系统索引。系统按层级（Foundation → Core → Feature → Presentation）和优先级排列，帮助确定 GDD 编写顺序。

在 `full` 审核模式下，CD-SYSTEMS（Creative Director）和 TD-SYSTEM-BOUNDARY（Technical Director）两个门控并行运行。在 `lean` 或 `solo` 模式下，两个门控均被跳过并注明。Skill 将系统索引写入 `design/systems-index.md`。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需 Fixture。

- [ ] 包含必填 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含 ≥2 个阶段标题
- [ ] 包含 verdict 关键词：COMPLETE、BLOCKED
- [ ] 包含"May I write"协作协议语言（针对 systems-index.md）
- [ ] 末尾包含下一步交接（`/design-system [next-system]`）
- [ ] 说明 CD-SYSTEMS 和 TD-SYSTEM-BOUNDARY 门控行为（full 模式并行）

---

## Director 门控检查

`full` 模式下：CD-SYSTEMS（Creative Director）和 TD-SYSTEM-BOUNDARY（Technical Director）并行生成，对系统分解草稿进行审核。两个门控均通过后，才进行"May I write"询问。

`lean` 模式下：两个门控均被跳过。输出注明："CD-SYSTEMS skipped — lean mode"和"TD-SYSTEM-BOUNDARY skipped — lean mode"。

`solo` 模式下：两个门控均被跳过，以"solo mode"标签注明。

---

## 测试用例

### 用例 1：正常路径——游戏概念存在，全模式分解为 5-8 个系统

**Fixture：**
- `design/gdd/game-concept.md` 存在，描述完整的游戏概念
- `design/gdd/game-pillars.md` 存在
- 不存在 `design/systems-index.md`
- `production/session-state/review-mode.txt` 内容为 `full`

**输入：** `/map-systems`

**预期行为：**
1. Skill 读取 `design/gdd/game-concept.md` 和 `design/gdd/game-pillars.md`
2. 分解为 5-8 个系统，并按层级和优先级排列
3. CD-SYSTEMS 和 TD-SYSTEM-BOUNDARY 并行生成，审核分解结果
4. 两个门控均返回 APPROVED 后展示系统索引草稿
5. 询问"May I write `design/systems-index.md`?"
6. 批准后写入系统索引，并更新会话状态

**断言：**
- [ ] 任何写入询问前先读取游戏概念文档
- [ ] 全模式下 CD-SYSTEMS 和 TD-SYSTEM-BOUNDARY 并行生成
- [ ] 两个门控均通过后才进行"May I write"询问
- [ ] 系统按层级（Foundation/Core/Feature/Presentation）组织
- [ ] 写入前询问"May I write"
- [ ] Verdict 为 COMPLETE

---

### 用例 2：失败路径——未找到游戏概念

**Fixture：**
- `design/gdd/game-concept.md` 不存在

**输入：** `/map-systems`

**预期行为：**
1. Skill 尝试读取 `design/gdd/game-concept.md` 但失败
2. Skill 输出："No game concept found. Run `/brainstorm` to create a game concept before mapping systems."
3. Skill 退出，不进行系统分解

**断言：**
- [ ] 未找到游戏概念时 Skill 以明确消息退出
- [ ] 不写入系统索引
- [ ] Skill 推荐 `/brainstorm` 作为下一步
- [ ] Verdict 为 BLOCKED

---

### 用例 3：Director 门控——CD-SYSTEMS 返回 CONCERNS

**Fixture：**
- 游戏概念存在
- `production/session-state/review-mode.txt` 内容为 `full`
- CD-SYSTEMS 门控返回 CONCERNS（例如某系统与游戏支柱不一致）

**输入：** `/map-systems`

**预期行为：**
1. CD-SYSTEMS 返回带具体反馈的 CONCERNS
2. TD-SYSTEM-BOUNDARY 可以同时通过
3. Skill 在"May I write"询问前向用户呈现 CONCERNS
4. 向用户提供选项：修订系统列表或接受并继续
5. 修订后重新展示系统列表，再进行"May I write"询问

**断言：**
- [ ] CONCERNS 在写入前呈现给用户
- [ ] 向用户提供修订或继续的选择
- [ ] 修订后最终批准前重新展示修订后的系统列表

---

### 用例 4：边缘情况——systems-index.md 已存在

**Fixture：**
- `design/gdd/game-concept.md` 存在
- `design/systems-index.md` 已存在，包含 N 个系统

**输入：** `/map-systems`

**预期行为：**
1. Skill 读取已有的 systems-index.md 并呈现当前状态
2. Skill 询问："systems-index.md already exists with [N] systems. Update with new systems, or review and revise priorities?"
3. 用户选择操作
4. Skill 不静默覆盖已有索引

**断言：**
- [ ] Skill 在继续前检测并读取已有的 systems-index.md
- [ ] 向用户提供更新/审阅选项——不自动覆盖
- [ ] 向用户呈现已有系统数量
- [ ] 用户未选择重新分解时 Skill 不执行完整重新分解

---

### 用例 5：Director 门控——lean 模式和 solo 模式均跳过门控，并注明

**Fixture（lean 模式）：**
- 游戏概念存在
- `production/session-state/review-mode.txt` 内容为 `lean`

**Lean 模式预期行为：**
1. 系统分解完成并起草
2. CD-SYSTEMS 和 TD-SYSTEM-BOUNDARY 均被跳过
3. 输出注明："CD-SYSTEMS skipped — lean mode"和"TD-SYSTEM-BOUNDARY skipped — lean mode"
4. 直接进行"May I write"询问

**断言（lean 模式）：**
- [ ] 两条门控跳过注明均出现在输出中
- [ ] Skill 无需门控批准直接进行"May I write"
- [ ] 用户批准后写入 systems-index.md

**Fixture（solo 模式）：**
- 相同游戏概念，`production/session-state/review-mode.txt` 内容为 `solo`

**Solo 模式预期行为：**
1. 相同分解工作流
2. 两个门控均被跳过——在输出中以"solo mode"注明
3. 进行"May I write"询问

**断言（solo 模式）：**
- [ ] 两条跳过注明均以"solo mode"标签出现
- [ ] 该 Skill 的行为与 lean 模式相同

---

## 协议合规

- [ ] 任何分解前先读取 game-concept.md 和 game-pillars.md
- [ ] 写入前询问"May I write `design/systems-index.md`?"
- [ ] 用户未批准时 systems-index.md 不写入
- [ ] full 模式下 CD-SYSTEMS 和 TD-SYSTEM-BOUNDARY 并行生成
- [ ] lean/solo 输出中按名称和模式注明被跳过的门控
- [ ] 末尾包含下一步交接：`/design-system [next-system]`

---

## 覆盖范围说明

- 循环依赖检测（系统 A 依赖系统 B，系统 B 又依赖 A）是依赖映射阶段的一部分——此处不单独进行 Fixture 测试。
- 优先级层级分配（MVP 启发式方法）作为用例 1 协作工作流的一部分进行评估，而非单独测试。
- `next` 参数模式（将最高优先级未设计系统交接给 `/design-system`）此处未测试——它是索引创建后的便利功能。
