# Skill 测试规范：/retrospective

## Skill 摘要

`/retrospective` 生成结构化的 Sprint 或里程碑回顾报告，涵盖三个类别：进展顺利的方面、不顺利的方面以及行动项。通过读取 Sprint 文件和会话日志来汇编观察结果，然后生成回顾文档。不使用 Director 门控——回顾是团队自我反思的工件。Skill 在持久化前询问"May I write to `production/retrospectives/retro-sprint-NNN.md`?"。Verdict 始终为 COMPLETE（回顾是结构化输出，不是通过/失败评估）。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需 Fixture。

- [ ] 包含必填 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含 ≥2 个阶段标题
- [ ] 包含 verdict 关键词：COMPLETE
- [ ] 包含"May I write"语言（Skill 会写入回顾文档）
- [ ] 包含下一步交接（回顾写入后应做什么）

---

## Director 门控检查

无。回顾是团队自我反思文档，不调用门控。

---

## 测试用例

### 用例 1：正常路径——结果参半的 Sprint

**Fixture：**
- `production/sprints/sprint-005.md` 存在，包含 6 个 Story（4 个 Complete、1 个 Blocked、1 个 Deferred）
- `production/session-logs/` 包含该 Sprint 期间的日志条目
- sprint-005 尚无回顾记录

**输入：** `/retrospective sprint-005`

**预期行为：**
1. Skill 读取 sprint-005 和会话日志
2. Skill 汇编三个回顾类别：进展顺利（4 个 Story 已交付）、不顺利（1 个 Blocked、1 个 Deferred）、行动项（解决阻塞根因）
3. Skill 向用户展示回顾草稿
4. Skill 询问"May I write to `production/retrospectives/retro-sprint-005.md`?"
5. 用户批准后写入文件，Verdict 为 COMPLETE

**断言：**
- [ ] 回顾包含全部三个类别（进展顺利 / 不顺利 / 行动项）
- [ ] Blocked 和 Deferred 的 Story 出现在"不顺利"部分
- [ ] 从被阻塞的 Story 至少生成一条行动项
- [ ] 写入文件前 Skill 询问"May I write"
- [ ] 写入成功后 Verdict 为 COMPLETE

---

### 用例 2：无 Sprint 数据——手动输入回退

**Fixture：**
- 用户调用 `/retrospective sprint-009`
- `production/sprints/sprint-009.md` 不存在
- 无会话日志引用 sprint-009

**输入：** `/retrospective sprint-009`

**预期行为：**
1. Skill 尝试读取 sprint-009——未找到
2. Skill 通知用户未找到 sprint-009 的数据
3. Skill 提示用户手动输入回顾内容（进展顺利、不顺利、行动项）
4. 用户提供输入，Skill 将其格式化为回顾结构
5. Skill 询问"May I write"并在批准后写入文档

**断言：**
- [ ] Sprint 文件不存在时 Skill 不崩溃或生成空文档
- [ ] 提示用户提供手动输入
- [ ] 手动输入格式化为三类别结构
- [ ] 文件写入前仍出现"May I write"提示

---

### 用例 3：回顾文档已存在——提供追加或替换选项

**Fixture：**
- `production/retrospectives/retro-sprint-005.md` 已存在并有内容
- 用户在变更后重新运行 `/retrospective sprint-005`

**输入：** `/retrospective sprint-005`

**预期行为：**
1. Skill 检测到 `retro-sprint-005.md` 已存在
2. Skill 向用户提供选择：追加新观察或替换现有文件
3. 用户选择"替换"，Skill 编写全新回顾
4. Skill 询问"May I write to `production/retrospectives/retro-sprint-005.md`?"（确认覆盖）
5. 文件被覆盖，Verdict 为 COMPLETE

**断言：**
- [ ] 编写前 Skill 检查是否存在已有回顾文件
- [ ] 向用户提供追加或替换选择——不静默覆盖
- [ ] "May I write"提示体现覆盖场景
- [ ] 无论追加还是替换，Verdict 均为 COMPLETE

---

### 用例 4：边缘情况——上一次回顾有未解决行动项

**Fixture：**
- `production/retrospectives/retro-sprint-004.md` 存在，包含 2 个标记为 `[ ]`（未完成）的行动项
- 用户运行 `/retrospective sprint-005`

**输入：** `/retrospective sprint-005`

**预期行为：**
1. Skill 读取最近一次回顾（retro-sprint-004）
2. Skill 检测到 sprint-004 中有 2 个未勾选的行动项
3. Skill 在新回顾中包含"来自 Sprint 004 的遗留项"章节
4. 未解决的项目列出，并注明未在上一个 Sprint 中跟进

**断言：**
- [ ] Skill 读取最近一次回顾以检查未完成的行动项
- [ ] 未解决行动项出现在新回顾的遗留章节中
- [ ] 遗留项与新生成的行动项区别显示
- [ ] 输出注明这些项目在上一个 Sprint 中未被跟进

---

### 用例 5：门控合规——任何模式下均不调用门控

**Fixture：**
- `production/sprints/sprint-005.md` 存在，包含完整的 Story
- `production/session-state/review-mode.txt` 内容为 `full`

**输入：** `/retrospective sprint-005`

**预期行为：**
1. Skill 以 full 模式编写回顾报告
2. 不调用任何 Director 门控（回顾是团队自我反思，非交付门控）
3. Skill 请求用户批准并在确认后写入文件
4. Verdict 为 COMPLETE

**断言：**
- [ ] 无论审核模式如何，均不调用 Director 门控
- [ ] 输出不包含任何门控调用或门控结果注释
- [ ] Skill 直接从编写到"May I write"提示
- [ ] 审核模式文件内容与该 Skill 行为无关

---

## 协议合规

- [ ] 在询问写入前始终向用户展示回顾草稿
- [ ] 写入回顾文件前始终询问"May I write"
- [ ] 不调用 Director 门控
- [ ] Verdict 始终为 COMPLETE（不是通过/失败 Skill）
- [ ] 检查上一次回顾中未解决的行动项

---

## 覆盖范围说明

- 里程碑回顾（相对于 Sprint 回顾）遵循相同模式，但读取里程碑文件而非 Sprint 文件；此处不单独测试。
- 会话日志为空的情况与用例 2（无数据）类似；两种情况下 Skill 均回退至手动输入。
