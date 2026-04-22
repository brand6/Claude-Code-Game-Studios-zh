# Skill 测试规范：/sprint-status

## Skill 摘要

`/sprint-status` 是 Haiku 级只读 Skill，读取当前活跃 Sprint 文件和会话状态以生成简洁的 Sprint 健康摘要。按状态统计 Story 数量（Complete / In Progress / Blocked / Not Started）并输出三种 Sprint 健康 Verdict 之一：ON TRACK、AT RISK 或 BLOCKED。不写入文件，不调用任何 Director 门控。专为会话中快速、低成本的状态检查而设计。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需 Fixture。

- [ ] 包含必填 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含 ≥2 个阶段标题或编号检查章节
- [ ] 包含 verdict 关键词：ON TRACK、AT RISK、BLOCKED
- [ ] 不要求"May I write"语言（只读 Skill）
- [ ] 包含下一步交接（根据 Verdict 应做什么）

---

## Director 门控检查

无。`/sprint-status` 是只读报告 Skill，不调用门控。

---

## 测试用例

### 用例 1：正常路径——混合 Sprint，AT RISK 并附具名阻塞项

**Fixture：**
- `production/sprints/sprint-004.md` 存在（活跃 Sprint，在 `active.md` 中有引用）
- Sprint 包含 6 个 Story：
  - 3 个 `Status: Complete`
  - 2 个 `Status: In Progress`
  - 1 个 `Status: Blocked`（阻塞原因："Waiting on physics ADR acceptance"）
- Sprint 结束日期为 2 天后

**输入：** `/sprint-status`

**预期行为：**
1. Skill 读取 `production/session-state/active.md` 以查找活跃 Sprint 引用
2. Skill 读取 `production/sprints/sprint-004.md`
3. Skill 按状态统计 Story：3 Complete、2 In Progress、1 Blocked
4. Skill 检测到被阻塞的 Story 和临近的截止日期
5. Skill 输出 AT RISK Verdict，明确列出阻塞项名称

**断言：**
- [ ] 输出包含按状态划分的 Story 数量明细
- [ ] 输出指出具体被阻塞的 Story 及其阻塞原因
- [ ] 当有 Story 处于 Blocked 状态时，Verdict 为 AT RISK（非 BLOCKED，非 ON TRACK）
- [ ] Skill 不写入任何文件

---

### 用例 2：所有 Story 完成——Sprint COMPLETE Verdict

**Fixture：**
- `production/sprints/sprint-004.md` 存在
- 全部 5 个 Story 状态均为 `Status: Complete`

**输入：** `/sprint-status`

**预期行为：**
1. Skill 读取 Sprint 文件——所有 Story 均为 Complete
2. Skill 输出 ON TRACK Verdict 或 SPRINT COMPLETE 标签
3. Skill 建议运行 `/milestone-review` 或 `/sprint-plan` 作为下一步

**断言：**
- [ ] 所有 Story 完成时，Verdict 为 ON TRACK 或 SPRINT COMPLETE
- [ ] 输出注明 Sprint 已全部完成
- [ ] 下一步建议引用 `/milestone-review` 或 `/sprint-plan`
- [ ] 不写入任何文件

---

### 用例 3：无活跃 Sprint 文件——引导运行 /sprint-plan

**Fixture：**
- `production/session-state/active.md` 中无活跃 Sprint 引用
- `production/sprints/` 目录为空或不存在

**输入：** `/sprint-status`

**预期行为：**
1. Skill 读取 `active.md`——未找到活跃 Sprint 引用
2. Skill 检查 `production/sprints/`——无文件
3. Skill 输出提示：未检测到活跃 Sprint
4. Skill 建议运行 `/sprint-plan` 以创建一个

**断言：**
- [ ] Sprint 文件不存在时 Skill 不报错或崩溃
- [ ] 输出明确说明未找到活跃 Sprint
- [ ] 输出推荐 `/sprint-plan` 作为下一步操作
- [ ] 不输出 Verdict 关键词（无 Sprint 可评估）

---

### 用例 4：边缘情况——陈旧的进行中 Story（标记警告）

**Fixture：**
- `production/sprints/sprint-004.md` 存在
- 一个 Story 状态为 `Status: In Progress`，`active.md` 中注明：`Last updated: 2026-03-30`（比当天会话日期早超过 2 天）
- 无 Story 处于 Blocked 状态

**输入：** `/sprint-status`

**预期行为：**
1. Skill 读取 Sprint 文件和会话状态
2. Skill 检测到该 Story 超过 2 天未更新而仍处于 In Progress
3. Skill 在输出中将该 Story 标记为"stale"
4. Verdict 为 AT RISK（陈旧的进行中 Story 提示存在隐性阻塞）

**断言：**
- [ ] Skill 将 Story 的"最后更新"元数据与会话日期进行比较
- [ ] 陈旧的进行中 Story 在输出中按名称标记
- [ ] 检测到陈旧 Story 时，Verdict 为 AT RISK，而非 ON TRACK
- [ ] 输出不将"stale"与"Blocked"混淆——标签有所区分

---

### 用例 5：门控合规——只读，不调用门控

**Fixture：**
- `production/sprints/sprint-004.md` 存在，包含 4 个 Story（2 个 Complete、2 个 In Progress）
- `production/session-state/review-mode.txt` 内容为 `full`

**输入：** `/sprint-status`

**预期行为：**
1. Skill 读取 Sprint 并生成状态摘要
2. Skill 无论审核模式如何都不调用任何 Director 门控
3. 输出是带 ON TRACK、AT RISK 或 BLOCKED Verdict 的纯状态报告
4. Skill 不提示用户批准，也不询问是否写入文件

**断言：**
- [ ] 在任何审核模式下均不调用 Director 门控
- [ ] 输出不包含任何"May I write"提示
- [ ] Skill 完成并返回 Verdict，无需用户交互
- [ ] 审核模式文件内容与该 Skill 行为无关（或确认不相关）

---

## 协议合规

- [ ] 不使用 Write 或 Edit 工具（只读 Skill）
- [ ] 输出 Verdict 前呈现按状态划分的 Story 数量明细
- [ ] 不请求批准
- [ ] 以基于 Verdict 推荐的下一步结束
- [ ] 运行在 Haiku 模型层级（快速、低成本）

---

## 覆盖范围说明

- 同时有多个活跃 Sprint 的情况未经测试；Skill 读取 `active.md` 所引用的 Sprint。
- Sprint 完成百分比未明确验证；按状态统计的输出隐含了这些数据。
- `solo` 模式的审核模式变体未单独测试；用例 5 中的门控行为对所有模式同等适用。
