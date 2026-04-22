# Skill 测试规范：/sprint-plan

## Skill 摘要

`/sprint-plan` 读取当前里程碑文件和待办 Story，然后按实现层级和优先级分数生成编号新 Sprint。在 full 模式下，Sprint 草稿编写完成后运行 PR-SPRINT Director 门控（Producer 审核计划）。在 lean 和 solo 模式下跳过门控。Skill 在持久化前询问"May I write to `production/sprints/sprint-NNN.md`?"。Verdict：COMPLETE（Sprint 已生成并写入）或 BLOCKED（因缺少数据或门控失败而无法继续）。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需 Fixture。

- [ ] 包含必填 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含 ≥2 个阶段标题
- [ ] 包含 verdict 关键词：COMPLETE、BLOCKED
- [ ] 包含"May I write"语言（Skill 会写入 Sprint 文件）
- [ ] 包含下一步交接（Sprint 写入后应做什么）

---

## Director 门控检查

| 门控 ID   | 触发条件          | 模式限制                   |
|-----------|-------------------|---------------------------|
| PR-SPRINT | Sprint 草稿构建后 | 仅 full 模式（非 lean/solo）|

---

## 测试用例

### 用例 1：正常路径——待办包含 Story，生成 Sprint

**Fixture：**
- `production/milestones/milestone-02.md` 存在，容量为 `10 story points`
- 待办包含分布在 2 个 Epic 中、优先级混合的 5 个未开始 Story
- `production/session-state/review-mode.txt` 内容为 `full`
- 下一个 Sprint 编号为 `003`（001 和 002 已存在）

**输入：** `/sprint-plan`

**预期行为：**
1. Skill 读取当前里程碑以获取容量和目标
2. Skill 读取待办中所有未开始的 Story，按层级 + 优先级排序
3. Skill 起草 sprint-003，将 Story 纳入容量范围
4. Skill 在调用门控前向用户展示草稿
5. Skill 调用 PR-SPRINT 门控（full 模式），Producer 批准
6. Skill 询问"May I write to `production/sprints/sprint-003.md`?"
7. 用户批准后写入文件

**断言：**
- [ ] Story 先按实现层级后按优先级排序
- [ ] Sprint 草稿在任何写入或门控调用前展示
- [ ] full 模式下草稿准备好后调用 PR-SPRINT 门控
- [ ] 写入 Sprint 文件前 Skill 询问"May I write"
- [ ] 写入文件路径匹配 `production/sprints/sprint-003.md`
- [ ] 写入成功后 Verdict 为 COMPLETE

---

### 用例 2：阻塞路径——待办为空

**Fixture：**
- `production/milestones/milestone-02.md` 存在
- 任何 Epic 待办中均无未开始的 Story

**输入：** `/sprint-plan`

**预期行为：**
1. Skill 读取待办——无未开始的 Story
2. Skill 输出"No unstarted stories in backlog"
3. Skill 建议运行 `/create-stories` 以填充待办
4. 不调用门控，不写入文件

**断言：**
- [ ] Verdict 为 BLOCKED
- [ ] 输出包含"No unstarted stories"或等效消息
- [ ] 输出推荐 `/create-stories`
- [ ] 不调用 PR-SPRINT 门控
- [ ] 不调用任何写入工具

---

### 用例 3：门控返回 CONCERNS——Sprint 超载，修订后再写入

**Fixture：**
- 待办 8 个 Story 共 16 点，里程碑容量为 10 点
- `review-mode.txt` 内容为 `full`

**输入：** `/sprint-plan`

**预期行为：**
1. Skill 起草包含全部 8 个 Story 的 Sprint（超出容量）
2. PR-SPRINT 门控运行，Producer 返回 CONCERNS：Sprint 超载
3. Skill 向用户呈现 CONCERNS 并询问延期哪些 Story
4. 用户选择延期 3 个 Story，Sprint 修订为 5 个 Story / 10 点
5. Skill 询问"May I write"（包含修订后的 Sprint），批准后写入

**断言：**
- [ ] PR-SPRINT 门控的 CONCERNS 在任何写入前呈现给用户
- [ ] 门控反馈后允许修订 Sprint
- [ ] 写入文件的是修订后的 Sprint（而非原始版本）
- [ ] 修订并写入后 Verdict 为 COMPLETE

---

### 用例 4：Lean 模式——PR-SPRINT 门控跳过

**Fixture：**
- 待办 4 个 Story，里程碑容量为 8 点
- `review-mode.txt` 内容为 `lean`

**输入：** `/sprint-plan`

**预期行为：**
1. Skill 读取审核模式——确认为 `lean`
2. Skill 起草 Sprint 并展示给用户
3. PR-SPRINT 门控被跳过，输出注明"[PR-SPRINT] skipped — Lean mode"
4. Skill 直接向用户请求 Sprint 批准
5. 用户批准后写入 Sprint 文件

**断言：**
- [ ] lean 模式下不调用 PR-SPRINT 门控
- [ ] 跳过在输出中明确注明
- [ ] 写入前仍需要用户批准（跳过门控 ≠ 跳过批准）
- [ ] 写入后 Verdict 为 COMPLETE

---

### 用例 5：边缘情况——上一个 Sprint 仍有未完成 Story

**Fixture：**
- `production/sprints/sprint-002.md` 存在，包含 2 个状态为 `Status: In Progress` 的 Story
- 待办中有 5 个新的未开始 Story
- `review-mode.txt` 内容为 `full`

**输入：** `/sprint-plan`

**预期行为：**
1. Skill 读取 sprint-002 并检测到 2 个未完成（进行中）的 Story
2. Skill 标记："Sprint 002 有 2 个未完成 Story——在规划 Sprint 003 之前请确认是否结转"
3. Skill 向用户提供选择：结转 Story、延期，或取消
4. 用户确认结转；结转的 Story 以 `[CARRY]` 标签前置加入新 Sprint
5. 构建 Sprint 草稿；PR-SPRINT 门控运行；批准后写入 Sprint

**断言：**
- [ ] Skill 检查最近的 Sprint 文件中是否有未完成的 Story
- [ ] 在 Sprint 规划继续之前请求用户确认结转
- [ ] 结转的 Story 在新 Sprint 草稿中以区分标签显示
- [ ] Skill 不静默忽略上一个 Sprint 的未完成 Story

---

## 协议合规

- [ ] 在调用 PR-SPRINT 门控或询问写入之前展示 Sprint 草稿
- [ ] 写入 Sprint 文件前始终询问"May I write"
- [ ] PR-SPRINT 门控仅在 full 模式下运行
- [ ] lean 和 solo 模式输出中显示跳过消息
- [ ] Verdict 在 Skill 输出末尾明确说明

---

## 覆盖率说明

- 里程碑文件不存在的情况未被明确测试；行为遵循 BLOCKED 模式，并建议运行 `/gate-check` 进行里程碑推进。
- Solo 模式行为等同于 lean（跳过门控，仍需用户批准），未独立测试。
- 并行 Story 选择算法未在此测试；这些是 sprint-plan 子代理的单元问题。
