# 技能测试规范：/bug-report

## 技能概要

`/bug-report` 根据用户描述创建结构化的缺陷报告文档。
报告包含以下必要字段：标题、复现步骤、预期行为、实际行为、
严重程度（CRITICAL/HIGH/MEDIUM/LOW）、受影响系统，以及版本/构建号。
若用户的初始描述缺少任何必要字段，技能在生成草稿前追问以补全信息。

技能检查可能重复的报告（对比 `production/bugs/` 中的现有文件），
并提供链接选项而非创建新报告。每份报告在"May I write"确认后
写入 `production/bugs/bug-[日期]-[slug].md`。
不使用 director 门控——缺陷报告是运营工具。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判决关键词：COMPLETE
- [ ] 在写入报告前包含"May I write"协作协议语言
- [ ] 包含下一步交接（例如，`/bug-triage` 重新排优先级，`/hotfix` 处理严重问题）

---

## Director 门控检查

无。`/bug-report` 是运营文档技能。不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——用户描述崩溃问题，生成完整报告

**夹具：**
- `production/bugs/` 目录存在且为空
- 无相似的现有报告

**输入：** `/bug-report`（用户描述："Game crashes when player enters the boss arena"）

**预期行为：**
1. 技能提取：标题 = "Game crashes when entering boss arena"
2. 技能将崩溃报告识别为 CRITICAL 严重程度
3. 技能与用户确认复现步骤、预期（不崩溃）、实际（崩溃）、
   受影响系统（arena/boss）以及版本号
4. 技能生成完整的结构化报告草稿
5. 技能询问"May I write to `production/bugs/bug-2026-04-06-game-crashes-boss-arena.md`?"
6. 批准后写入文件；判决为 COMPLETE

**断言：**
- [ ] 报告中包含所有 7 个必要字段
- [ ] 崩溃报告的严重程度为 CRITICAL
- [ ] 文件名遵循 `bug-[日期]-[slug].md` 规范
- [ ] "May I write"询问包含完整文件路径
- [ ] 判决为 COMPLETE

---

### 用例 2：输入极简——技能追问缺失字段

**夹具：**
- 用户提供："Sometimes the audio cuts out"
- 无现有报告

**输入：** `/bug-report`

**预期行为：**
1. 技能识别缺失的必要字段：复现步骤、预期与实际行为、严重程度、受影响系统、版本号
2. 技能针对每个缺失字段提问（逐一或以结构化提示形式）
3. 用户提供答案
4. 技能从答案中汇总完整报告
5. 技能询问"May I write?"并在批准后写入

**断言：**
- [ ] 至少提出 3 个追问以补全缺失字段
- [ ] 每个必要字段填写完整后才完成报告
- [ ] 所有必要字段均填写完毕前不写入报告
- [ ] 所有字段填写完毕并写入文件后判决为 COMPLETE

---

### 用例 3：可能重复——提供链接选项而非创建新报告

**夹具：**
- `production/bugs/bug-2026-03-20-audio-cut-out.md` 已存在，标题相似，严重程度为 MEDIUM

**输入：** `/bug-report`（用户描述："Audio randomly stops working"）

**预期行为：**
1. 技能扫描现有报告，发现相似的音频缺陷
2. 技能报告："A similar bug report exists: bug-2026-03-20-audio-cut-out.md"
3. 技能提供选项：标记为重复（为现有报告添加注释）或仍然创建新报告
4. 若选择链接：技能在现有文件中添加交叉引用注释（询问"May I update the existing report?"）
5. 若选择创建新报告：正常报告创建流程继续

**断言：**
- [ ] 在创建新报告之前呈现现有相似报告
- [ ] 用户获得选择权（不被强制链接或创建）
- [ ] 若链接：在修改现有文件前询问"May I update"
- [ ] 两条路径的判决均为 COMPLETE

---

### 用例 4：多系统缺陷——报告包含多个系统标签

**夹具：**
- 无现有报告

**输入：** `/bug-report`（用户描述："After finishing a level, the save system
  freezes and the UI doesn't show the completion screen"）

**预期行为：**
1. 技能从描述中识别出 2 个受影响系统：存档系统和 UI
2. 报告草稿在"受影响系统"字段中列出两个系统
3. 评估严重程度（可能为 HIGH——存档冻结有数据丢失风险）
4. 技能询问"May I write"并使用适当的文件名
5. 报告写入，含两个系统标签；判决为 COMPLETE

**断言：**
- [ ] 两个受影响系统均列在报告中
- [ ] 创建一份报告（而非每个系统各一份）
- [ ] 严重程度反映最具影响力的组成部分（存档冻结 → HIGH 或 CRITICAL）
- [ ] 判决为 COMPLETE

---

### 用例 5：Director 门控检查——无门控；缺陷报告是运营工具

**夹具：**
- 任意缺陷描述

**输入：** `/bug-report`

**预期行为：**
1. 技能创建并写入缺陷报告
2. 未调用任何 director agent
3. 输出中无门控 ID

**断言：**
- [ ] 未调用 director 门控
- [ ] 输出中无门控跳过消息
- [ ] 技能在无任何门控检查的情况下达到 COMPLETE

---

## 协议合规

- [ ] 在生成报告草稿前收集所有 7 个必要字段
- [ ] 针对任何缺失的必要字段追问
- [ ] 在创建新报告前检查相似的现有报告
- [ ] 在写入前询问"May I write to `production/bugs/bug-[日期]-[slug].md`?"
- [ ] 文件写入后判决为 COMPLETE

---

## 覆盖说明

- 用户提供的严重程度低于描述影响（例如，崩溃却标记为 LOW）的情况不测试；
  技能可建议更高严重程度，但最终以用户输入为准。
- 版本/构建号字段为必填，但若用户不知道可填"unknown"——
  此为有效值，不单独测试。
- 报告 slug 生成（将标题清理为合法文件名）是不在此处进行断言测试的实现细节。
