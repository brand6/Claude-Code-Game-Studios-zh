# 技能测试规范：/release-checklist

## 技能概要

`/release-checklist` 生成内部发布就绪清单，验证里程碑或冲刺是否已准备好发布。
这与 `/launch-checklist`（面向平台发布）不同——本技能聚焦于内部质量门控：

- 冲刺故事完成度（Done 状态）
- 开放缺陷的严重程度（是否存在 HIGH/CRITICAL 未关闭缺陷）
- QA 签核状态（`production/qa/` 目录）
- 构建稳定性（Smoke 检查状态）
- 更新日志就绪情况（`/changelog` 是否已运行）

清单写入 `production/releases/release-checklist-[日期].md`。
存在 BLOCKING 项目时判决为 RELEASE BLOCKED，
存在 NEEDS ATTENTION 项目时为 CONCERNS，
所有项目通过时为 RELEASE READY。
不适用 director 门控。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判决关键词：RELEASE READY、RELEASE BLOCKED、CONCERNS
- [ ] 在写入清单前包含"May I write"协作协议语言
- [ ] 包含下一步交接（例如 `/launch-checklist` 用于外部发布或 `/gate-check` 用于阶段推进）

---

## Director 门控检查

无。`/release-checklist` 是内部发布运营工具。不适用 director 门控。
（正式阶段推进由 `/gate-check` 管理。）

---

## 测试用例

### 用例 1：正常路径——所有故事完成，无高危缺陷，RELEASE READY

**夹具：**
- `production/sprints/sprint-018.md` 中所有故事状态为 `Done`
- `production/bugs/` 中无 HIGH 或 CRITICAL 严重程度的未关闭缺陷
- `production/qa/qa-plan-sprint-018.md` 包含"QA APPROVED"签核
- 最近一次 smoke 检查通过
- `production/releases/changelog-v1.2.0.md` 存在

**输入：** `/release-checklist`

**预期行为：**
1. 技能读取冲刺故事——所有状态均为 Done
2. 技能读取开放缺陷——无 HIGH/CRITICAL
3. 技能读取 QA 签核——APPROVED
4. 技能确认 smoke 检查通过
5. 技能确认更新日志存在
6. 所有项目标记为 ✅ VERIFIED
7. 技能询问"May I write to `production/releases/release-checklist-[日期].md`?"
8. 清单写入；判决为 RELEASE READY

**断言：**
- [ ] 所有 5 个内部类别均出现在输出中
- [ ] 所有项目标记为 ✅ VERIFIED
- [ ] 判决为 RELEASE READY
- [ ] 写入前询问"May I write"

---

### 用例 2：存在 HIGH 严重程度未关闭缺陷——RELEASE BLOCKED

**夹具：**
- 冲刺故事均已完成
- `production/bugs/` 中有 1 个 HIGH 严重程度的未关闭缺陷

**输入：** `/release-checklist`

**预期行为：**
1. 技能读取开放缺陷，发现 1 个 HIGH 严重程度的缺陷
2. 技能将缺陷标记为 ❌ BLOCKING
3. 其他项目正常通过
4. 总体判决为 RELEASE BLOCKED
5. HIGH 缺陷明确识别（文件名或标题）

**断言：**
- [ ] HIGH 缺陷标记为 ❌ BLOCKING
- [ ] 判决为 RELEASE BLOCKED
- [ ] 阻断缺陷明确识别（不仅说"某个缺陷"）
- [ ] 即使为 RELEASE BLOCKED，清单仍写入（供参考）

---

### 用例 3：更新日志未生成——CONCERNS，不阻断发布

**夹具：**
- 所有故事完成，无高危缺陷，QA 已签核
- 不存在 `production/releases/changelog-v1.3.0.md`

**输入：** `/release-checklist`

**预期行为：**
1. 技能读取更新日志状态——未找到
2. 技能将更新日志项目标记为 ⚠️ NEEDS ATTENTION
3. 其他项目正常通过
4. 总体判决为 CONCERNS（不是 RELEASE BLOCKED）
5. 技能建议运行 `/changelog` 生成更新日志

**断言：**
- [ ] 更新日志项目标记为 ⚠️ NEEDS ATTENTION
- [ ] 判决为 CONCERNS（不是 RELEASE BLOCKED）
- [ ] 建议运行 `/changelog`
- [ ] 仅因更新日志缺失，技能不阻断发布

---

### 用例 4：与之前清单对比——显示变更差异

**夹具：**
- `production/releases/release-checklist-2026-03-25.md` 已存在（上次运行）
- 上次清单：QA 签核为 ⚠️ NEEDS ATTENTION
- 本次运行：QA 签核现为 ✅ VERIFIED

**输入：** `/release-checklist`

**预期行为：**
1. 技能读取上次清单以进行对比
2. 技能在输出中注明状态变更：
   "QA Sign-off: NEEDS ATTENTION → VERIFIED"
3. 新清单写入带新日期的新文件

**断言：**
- [ ] 输出中包含"上次与本次"的差异
- [ ] 新清单写入带新日期的新文件（不覆盖旧文件）
- [ ] 差异摘要准确反映状态变更

---

### 用例 5：Director 门控检查——无门控；release-checklist 为运营工具

**夹具：**
- 标准项目设置

**输入：** `/release-checklist`

**预期行为：**
1. 技能生成并写入清单
2. 未调用任何 director agent
3. 输出中无门控 ID

**断言：**
- [ ] 未调用 director 门控
- [ ] 输出中无门控跳过消息
- [ ] 技能在不经过任何门控检查的情况下达到 RELEASE READY / RELEASE BLOCKED / CONCERNS

---

## 协议合规

- [ ] 覆盖 5 个内部发布类别：故事完成度、开放缺陷严重程度、QA 签核、Smoke 状态、更新日志
- [ ] 每项检查使用 ✅ / ⚠️ / ❌ 前缀
- [ ] 存在 ❌ BLOCKING 项目（HIGH/CRITICAL 缺陷）时判决为 RELEASE BLOCKED
- [ ] 无 BLOCKING 但有 ⚠️ NEEDS ATTENTION 时判决为 CONCERNS
- [ ] 所有项目通过时判决为 RELEASE READY
- [ ] 写入前询问"May I write to `production/releases/release-checklist-[日期].md`?"

---

## 覆盖说明

- 此技能（内部里程碑）与 `/launch-checklist`（平台发布）不同；
  两者使用不同的类别，在不同时间运行。
- Smoke 检查状态读取方式在技能主体中定义（读取最近的 smoke-check 输出或状态文件）；
  此规范仅要求 smoke 状态包含在清单中。
- 存在多个 BLOCKING 缺陷的情况与用例 2 相同处理——所有 BLOCKING 缺陷均列出。
