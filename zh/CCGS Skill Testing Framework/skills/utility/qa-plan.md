# 技能测试规范：/qa-plan

## 技能概要

`/qa-plan` 为冲刺或里程碑生成结构化的 QA 测试计划。
它读取故事文件，提取验收标准（AC），
并参照 `coding-standards.md` 中的分类规则为每条 AC 分配测试类型：
单元测试（Logic）、集成测试（Integration）、视觉验证（Visual）、
UI 测试（UI）或配置数据验证（Config Data）。

计划写入 `production/qa/qa-plan-sprint-NNN.md`。
若该冲刺的 QA 计划已存在，技能提供增量更新而非覆盖。
不适用 director 门控。判决始终为 COMPLETE。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判决关键词：COMPLETE
- [ ] 在写入计划前包含"May I write"协作协议语言
- [ ] 包含下一步交接（例如 `/smoke-check` 或 `/story-readiness`）

---

## Director 门控检查

无。`/qa-plan` 是 QA 流水线工具。不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——4 个故事，生成完整测试计划

**夹具：**
- `production/sprints/sprint-020.md` 包含 4 个故事，每个故事含清晰的 AC
- `production/qa/` 目录存在但无 sprint-020 的计划

**输入：** `/qa-plan sprint-020`

**预期行为：**
1. 技能读取 sprint-020.md，提取 4 个故事和各自的 AC
2. 技能为每条 AC 分配测试分类
3. 技能生成测试计划，包含：
   - 每条 AC 对应的测试类型（Logic/Integration/Visual/UI/Config Data）
   - 自动化测试（按类型分组）
   - 手动测试用例
   - 测试计划摘要
4. 技能询问"May I write to `production/qa/qa-plan-sprint-020.md`?"
5. 计划写入；判决为 COMPLETE

**断言：**
- [ ] 所有 4 个故事的 AC 均出现在测试计划中
- [ ] 每条 AC 分配了测试类型
- [ ] 写入前询问"May I write"
- [ ] 文件名格式正确：`qa-plan-sprint-020.md`
- [ ] 判决为 COMPLETE

---

### 用例 2：故事无 AC——标记为 UNTESTABLE

**夹具：**
- `production/sprints/sprint-021.md` 包含 3 个故事；其中一个故事无 AC 章节（或 AC 为空）

**输入：** `/qa-plan sprint-021`

**预期行为：**
1. 技能读取 3 个故事
2. 技能检测到一个故事无 AC
3. 该故事在测试计划中标记为 `UNTESTABLE — no acceptance criteria defined`
4. 其他 2 个故事正常生成测试计划
5. 测试计划摘要注明："1 story marked UNTESTABLE"
6. 写入计划；判决为 COMPLETE

**断言：**
- [ ] 无 AC 的故事标记为 UNTESTABLE
- [ ] 其他故事的测试项不受影响
- [ ] 摘要中统计 UNTESTABLE 故事的数量
- [ ] 判决为 COMPLETE（不因 UNTESTABLE 故事而阻断）

---

### 用例 3：QA 计划已存在——提供增量更新

**夹具：**
- `production/qa/qa-plan-sprint-022.md` 已存在（2 个故事的测试计划）
- sprint-022.md 已更新，新增了第 3 个故事

**输入：** `/qa-plan sprint-022`

**预期行为：**
1. 技能读取 sprint-022.md，发现 3 个故事（比现有计划多 1 个）
2. 技能读取现有 `qa-plan-sprint-022.md`
3. 技能识别差异：第 3 个故事需要新增
4. 技能生成增量更新（仅第 3 个故事的 AC），而非重新生成整个计划
5. 技能询问"May I update `production/qa/qa-plan-sprint-022.md`?"
6. 更新写入；判决为 COMPLETE

**断言：**
- [ ] 技能读取现有计划（不直接覆盖）
- [ ] 输出中提及"updating"而非"creating"
- [ ] 询问"May I update"（不是"May I write"——因为是更新操作）
- [ ] 判决为 COMPLETE

---

### 用例 4：找不到冲刺文件——报错

**夹具：**
- 不存在 `production/sprints/sprint-099.md`

**输入：** `/qa-plan sprint-099`

**预期行为：**
1. 技能尝试读取 `production/sprints/sprint-099.md`——未找到
2. 技能输出："Error: sprint-099.md not found in production/sprints/"
3. 技能建议运行 `/sprint-plan` 先创建冲刺，或检查冲刺编号是否正确
4. 不生成测试计划，不写入文件

**断言：**
- [ ] 冲刺文件未找到时输出错误消息
- [ ] 建议运行 `/sprint-plan` 作为修复步骤
- [ ] 不写入任何文件
- [ ] 不发出 COMPLETE 判决——技能终止于报错状态

---

### 用例 5：Director 门控检查——无门控；qa-plan 为流水线工具

**夹具：**
- 标准冲刺设置

**输入：** `/qa-plan`

**预期行为：**
1. 技能生成并写入 QA 计划
2. 未调用任何 director agent
3. 输出中无门控 ID

**断言：**
- [ ] 未调用 director 门控
- [ ] 输出中无门控跳过消息
- [ ] 技能在不经过任何门控检查的情况下达到 COMPLETE

---

## 协议合规

- [ ] 读取冲刺故事文件以提取 AC
- [ ] 参照 `coding-standards.md` 分类为以下测试类型之一：Logic、Integration、Visual、UI、Config Data
- [ ] 无 AC 的故事标记为 UNTESTABLE（不阻断计划生成）
- [ ] 计划已存在时提供增量更新
- [ ] 写入或更新前询问"May I write/update"
- [ ] 所有情况下判决均为 COMPLETE（除冲刺文件未找到的报错情况外）

---

## 覆盖说明

- 测试类型分类逻辑（Logic/Integration/Visual/UI/Config Data）依赖于
  `coding-standards.md` 中定义的规则；此规范不对具体分类决策进行硬编码。
- QA 计划执行（实际测试运行）是手动步骤，超出本技能范围。
- 测试计划中的具体测试用例措辞（断言名称等）是实现细节，
  不在此规范中进行断言。
