# Skill 测试规范：/milestone-review

## Skill 摘要

`/milestone-review` 生成已完成里程碑的综合回顾报告：已交付内容、速度指标、延期事项、已暴露风险以及回顾复盘的种子议题。在 full 模式下，回顾报告编写完成后会运行 PR-MILESTONE Director 门控（Producer 审核范围交付情况）。在 lean 和 solo 模式下跳过门控。Skill 在持久化前询问"May I write to `production/milestones/review-milestone-N.md`?"。Verdict：MILESTONE COMPLETE 或 MILESTONE INCOMPLETE。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需 Fixture。

- [ ] 包含必填 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含 ≥2 个阶段标题
- [ ] 包含 verdict 关键词：MILESTONE COMPLETE、MILESTONE INCOMPLETE
- [ ] 包含"May I write"语言（Skill 会写入回顾文档）
- [ ] 包含下一步交接（回顾写入后应做什么）

---

## Director 门控检查

| 门控 ID      | 触发条件              | 模式限制                   |
|--------------|-----------------------|---------------------------|
| PR-MILESTONE | 回顾文档编写完成后    | 仅 full 模式（非 lean/solo）|

---

## 测试用例

### 用例 1：正常路径——接近完成的里程碑，一个 Story 延期

**Fixture：**
- `production/milestones/milestone-03.md` 存在，包含 8 个 Story
- 7 个 Story 状态为 `Status: Complete`
- 1 个 Story 状态为 `Status: Deferred`（延期至 milestone-04）
- `review-mode.txt` 内容为 `full`

**输入：** `/milestone-review milestone-03`

**预期行为：**
1. Skill 读取 `milestone-03.md` 及所有引用的 Sprint 文件
2. Skill 汇编：7 个已交付，1 个延期；计算速度；无阻塞
3. Skill 向用户展示回顾草稿
4. 调用 PR-MILESTONE 门控，Producer 批准
5. Skill 询问"May I write to `production/milestones/review-milestone-03.md`?"
6. 用户批准后写入文件，Verdict 为 MILESTONE COMPLETE

**断言：**
- [ ] 延期 Story 在回顾中附有其目标里程碑说明
- [ ] 即使有一个延期 Story，Verdict 仍为 MILESTONE COMPLETE
- [ ] full 模式下回顾草稿编写完成后调用 PR-MILESTONE 门控
- [ ] 写入回顾文件前 Skill 询问"May I write"
- [ ] 回顾文档路径匹配 `production/milestones/review-milestone-03.md`

---

### 用例 2：阻塞里程碑——多个 Story 被阻塞

**Fixture：**
- `production/milestones/milestone-03.md` 存在，包含 5 个 Story
- 2 个 Story 状态为 `Status: Complete`
- 3 个 Story 状态为 `Status: Blocked`（各 Story 中列有具名阻塞项）
- `review-mode.txt` 内容为 `full`

**输入：** `/milestone-review milestone-03`

**预期行为：**
1. Skill 读取里程碑和 Sprint 文件
2. Skill 发现 3 个被阻塞的 Story，汇编阻塞详情
3. Verdict 为 MILESTONE INCOMPLETE
4. PR-MILESTONE 门控运行，Producer 注明未解决的阻塞项
5. 批准后写入带阻塞列表的回顾

**断言：**
- [ ] 当有 Story 处于 Blocked 状态时，Verdict 为 MILESTONE INCOMPLETE
- [ ] 每个被阻塞 Story 的名称和阻塞原因均列于回顾中
- [ ] full 模式下即使是 INCOMPLETE Verdict 也仍调用 PR-MILESTONE 门控
- [ ] 文件写入前仍出现"May I write"提示

---

### 用例 3：Full 模式——PR-MILESTONE 返回 CONCERNS

**Fixture：**
- Milestone-03 有 6 个完成的 Story，但其中 2 个不在原始范围内（Sprint 中期添加）
- `review-mode.txt` 内容为 `full`

**输入：** `/milestone-review milestone-03`

**预期行为：**
1. Skill 编写回顾，注明 2 个超范围 Story 已交付
2. PR-MILESTONE 门控调用，Producer 返回 CONCERNS：范围蔓延
3. Skill 将 CONCERNS 呈现给用户，并在回顾中添加"范围蔓延"注记
4. 用户批准修订后的回顾，以 MILESTONE COMPLETE（附注意事项）写入文件

**断言：**
- [ ] PR-MILESTONE 门控的 CONCERNS 在写入前展示给用户
- [ ] 范围蔓延明确注记于已写入的回顾文档中
- [ ] Verdict 为 MILESTONE COMPLETE（已交付 Story）并附 CONCERNS 标注
- [ ] Skill 不压制门控反馈

---

### 用例 4：边缘情况——未找到指定里程碑文件

**Fixture：**
- 用户调用 `/milestone-review milestone-07`
- `production/milestones/milestone-07.md` 不存在

**输入：** `/milestone-review milestone-07`

**预期行为：**
1. Skill 尝试读取 `production/milestones/milestone-07.md`
2. 文件未找到，Skill 输出错误消息
3. Skill 建议检查 `production/milestones/` 中的可用里程碑
4. 不调用门控，不写入文件

**断言：**
- [ ] 里程碑文件不存在时 Skill 不崩溃
- [ ] 输出在错误消息中注明预期文件路径
- [ ] 输出建议检查 `production/milestones/` 以获取有效里程碑名称
- [ ] Verdict 为 BLOCKED（无法回顾不存在的里程碑）

---

### 用例 5：Lean/Solo 模式——PR-MILESTONE 门控跳过

**Fixture：**
- `production/milestones/milestone-03.md` 存在，包含 5 个完成的 Story
- `review-mode.txt` 内容为 `solo`

**输入：** `/milestone-review milestone-03`

**预期行为：**
1. Skill 读取 review 模式——确定为 `solo`
2. Skill 编写回顾草稿
3. PR-MILESTONE 门控跳过；输出注明"[PR-MILESTONE] skipped — Solo mode"
4. Skill 向用户请求直接批准回顾
5. 用户批准后写入回顾文件，Verdict 为 MILESTONE COMPLETE

**断言：**
- [ ] solo（或 lean）模式下不调用 PR-MILESTONE 门控
- [ ] Skill 输出中明确注明跳过
- [ ] 写入前仍需用户直接批准
- [ ] 成功写入后 Verdict 为 MILESTONE COMPLETE

---

## 协议合规

- [ ] 调用 PR-MILESTONE 门控或询问写入前展示已编写的回顾草稿
- [ ] 写入回顾文档前始终询问"May I write"
- [ ] PR-MILESTONE 门控仅在 full 模式下运行
- [ ] lean 和 solo 输出中出现跳过消息
- [ ] Verdict 为 MILESTONE COMPLETE 或 MILESTONE INCOMPLETE，表述清晰

---

## 覆盖说明

- 里程碑包含零个 Story 的情况未在测试中覆盖；遵循 MILESTONE INCOMPLETE 模式，并附注提示里程碑可能尚未规划。
- 速度计算的具体方式（Story 点数 vs. Story 数量）在此处未验证；属于回顾汇编阶段的实现细节。
