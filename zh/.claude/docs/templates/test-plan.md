# QA 计划：[Sprint/Feature Name]

> **日期**：[date]
> **生成方式**：/qa-plan
> **覆盖范围**：[N 个 stories，跨 N 个系统]
> **引擎**：[引擎名称及版本]
> **Sprint 文件**：[Sprint 计划路径]

---

## Story 覆盖摘要

| Story | 类型 | 需要自动化测试 | 需要手动验证 |
|-------|------|--------------|------------|
| [story 标题] | Logic | 单元测试——`tests/unit/[system]/` | 无 |
| [story 标题] | Integration | 集成测试——`tests/integration/[system]/` | 冒烟测试 |
| [story 标题] | Visual/Feel | 无（不可自动化） | 截图 + 负责人签字 |
| [story 标题] | UI | 无（不可自动化） | 手动逐步验证 |
| [story 标题] | Config/Data | 数据验证（可选） | 游戏内数值抽检 |

**合计**：[N] 个 Logic，[N] 个 Integration，[N] 个 Visual/Feel，[N] 个 UI，[N] 个 Config/Data

---

## 需要的自动化测试

### [Story 标题] — Logic

**测试文件路径**：`tests/unit/[system]/[story-slug]_test.[ext]`

**测试内容**：
- [GDD 公式或规则——例："伤害 = 基础值 × 倍数，倍数 ∈ [0.5, 3.0]"]
- [每个命名状态的转换]
- [应/不应发生的每个副作用]

**需覆盖的边界情况**：
- 零值 / 最小输入
- 最大值 / 边界输入
- 无效或空输入
- [GDD 中明确规定的边界情况]

**预估测试数量**：约 [N] 个单元测试

---

### [Story 标题] — Integration

**测试文件路径**：`tests/integration/[system]/[story-slug]_test.[ext]`

**测试内容**：
- [跨系统交互——例："应用增益效果后更新 CharacterStats 并触发 UI 刷新"]
- [往返测试——例："存档 → 读档后还原所有字段"]

---

## 手动 QA 检查清单

### [Story 标题] — Visual/Feel

**验证方式**：截图 + [设计师 / 美术负责人] 签字
**证据文件**：`production/qa/evidence/[story-slug]-evidence.md`
**必须签字人员**：[设计师 / 主程序员 / 美术负责人]

- [ ] [可具体观察的条件——例："命中闪光出现在命中帧，而非下一帧"]
- [ ] [另一个可证伪的条件]

### [Story 标题] — UI

**验证方式**：手动逐步验证
**证据文件**：`production/qa/evidence/[story-slug]-evidence.md`

- [ ] [将每项验收标准转化为手动检查项]

---

## 冒烟测试范围

QA 交接前需验证的关键路径（通过 `/smoke-check` 执行）：

1. 游戏启动到主菜单无崩溃
2. 可正常开始新游戏 / 新会话
3. [本 Sprint 引入或修改的主要机制]
4. [本 Sprint 变更带来回归风险的系统]
5. 存读档周期完整，无数据丢失（如存档系统已存在）
6. 目标硬件上的性能在预算范围内

---

## 测试需求

| Story | 测试目标 | 最少场次 | 目标玩家类型 |
|-------|---------|---------|------------|
| [story] | [需要回答什么问题？] | [N] | [新手玩家 / 有经验玩家 / 等] |

签字要求：测试笔记 → `production/session-logs/playtest-[sprint]-[story-slug].md`

若本 Sprint 不需要测试场次：*本 Sprint 无需测试场次。*

---

## 完成定义——本 Sprint

一个 Story 被视为 DONE，当且仅当以下所有条件均满足：

- [ ] 所有验收标准已验证——有自动化测试结果**或**有记录的手动证据
- [ ] 所有 Logic 和 Integration 类型 Story 的测试文件存在且通过
- [ ] 所有 Visual/Feel 和 UI 类型 Story 的手动证据文档存在
- [ ] 冒烟测试通过（QA 交接前运行 `/smoke-check sprint`）
- [ ] 未引入回归——前 Sprint 的功能仍能通过测试
- [ ] 代码已审查（通过 `/code-review` 或有记录的同行审查）
- [ ] Story 文件通过 `/story-done` 更新为 `Status: Complete`

**需要测试签字方可关闭的 Story**：[列表，或"无"]

---

## 测试结果

*测试完成后填写。*

| Story | 自动化测试 | 手动测试 | 结果 | 备注 |
|-------|-----------|---------|------|------|
| [标题] | PASS | — | PASS | |
| [标题] | — | PASS | PASS | |
| [标题] | FAIL | — | BLOCKED | [描述失败原因] |

---

## 发现的缺陷

| ID | Story | 严重程度 | 描述 | 状态 |
|----|-------|---------|------|------|
| BUG-001 | | S[1-4] | | Open |

---

## 签字确认

- **QA 测试员**：[姓名] — [日期]
- **QA 负责人**：[姓名] — [日期]
- **Sprint 负责人**：[姓名] — [日期]

*模板：`.claude/docs/templates/test-plan.md`*
*生成方式：`/qa-plan` — 请勿编辑此行*
