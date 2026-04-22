# 技能测试规范：/bug-triage

## 技能概要

`/bug-triage` 读取 `production/bugs/` 中所有未关闭的缺陷报告，
并生成按严重程度（CRITICAL → HIGH → MEDIUM → LOW）排序的分类优先级表。
它运行于 Haiku 模型（只读，格式化/排序任务），不产生任何文件写入——
分类结果以对话形式输出。技能标记缺少复现步骤的缺陷，
并通过对比标题和受影响系统来识别可能重复的报告。

判决始终为 TRIAGED——本技能仅提供建议和信息。不适用 director 门控。
输出旨在帮助制作人或 QA 负责人优先处理下一步要解决的缺陷。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判决关键词：TRIAGED
- [ ] 不包含"May I write"语言（技能为只读）
- [ ] 包含下一步交接（例如，`/bug-report` 创建新报告，`/hotfix` 处理严重缺陷）

---

## Director 门控检查

无。`/bug-triage` 是只读建议技能。不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——5 个不同严重程度的缺陷，生成排序表

**夹具：**
- `production/bugs/` 包含 5 个缺陷报告文件：
  - bug-2026-03-10-audio-crash.md（CRITICAL）
  - bug-2026-03-12-score-overflow.md（HIGH）
  - bug-2026-03-14-ui-overlap.md（MEDIUM）
  - bug-2026-03-15-typo-tutorial.md（LOW）
  - bug-2026-03-16-vfx-flicker.md（HIGH）

**输入：** `/bug-triage`

**预期行为：**
1. 技能读取全部 5 个缺陷报告文件
2. 从每个文件中提取严重程度、标题、系统和复现状态
3. 技能生成分类表，排序为：CRITICAL 优先，然后 HIGH、MEDIUM、LOW
4. 相同严重程度内，缺陷按日期排序（最早的在前）
5. 判决为 TRIAGED

**断言：**
- [ ] 分类表恰好有 5 行
- [ ] CRITICAL 缺陷出现在两个 HIGH 缺陷之前
- [ ] HIGH 缺陷出现在 MEDIUM 和 LOW 缺陷之前
- [ ] 判决为 TRIAGED
- [ ] 未写入任何文件

---

### 用例 2：未找到缺陷报告——提示运行 /bug-report

**夹具：**
- `production/bugs/` 目录存在但为空（或不存在）

**输入：** `/bug-triage`

**预期行为：**
1. 技能扫描 `production/bugs/` 未找到报告
2. 技能输出："No open bug reports found in production/bugs/"
3. 技能建议运行 `/bug-report` 创建缺陷报告
4. 不生成分类表

**断言：**
- [ ] 输出明确说明未找到缺陷
- [ ] 建议运行 `/bug-report` 作为下一步
- [ ] 技能不报错——能优雅处理空目录
- [ ] 判决为 TRIAGED（附"未找到缺陷"说明）

---

### 用例 3：缺陷缺少复现步骤——标记为 NEEDS REPRO INFO

**夹具：**
- `production/bugs/` 包含 3 个缺陷报告；其中一个"复现步骤"章节为空

**输入：** `/bug-triage`

**预期行为：**
1. 技能读取全部 3 个报告
2. 技能检测到缺少复现步骤的报告
3. 该缺陷在分类表中附 `NEEDS REPRO INFO` 标签
4. 其他缺陷正常分类
5. 判决为 TRIAGED

**断言：**
- [ ] `NEEDS REPRO INFO` 标签出现在缺少复现步骤的缺陷旁
- [ ] 被标记的缺陷仍包含在表中（不被排除）
- [ ] 其他缺陷不受影响
- [ ] 判决为 TRIAGED

---

### 用例 4：可能重复的缺陷——在分类输出中标记

**夹具：**
- `production/bugs/` 包含 2 个标题相似的缺陷报告：
  - bug-2026-03-18-player-fall-through-floor.md
  - bug-2026-03-20-player-clips-through-floor.md
  - 两者均影响"Physics"系统，严重程度相同

**输入：** `/bug-triage`

**预期行为：**
1. 技能读取两个报告，检测到标题相似 + 相同系统 + 相同严重程度
2. 两个缺陷均包含在分类表中
3. 每个均附 `POSSIBLE DUPLICATE` 标签并交叉引用另一个报告
4. 不合并或删除任何缺陷——标记为建议性质
5. 判决为 TRIAGED

**断言：**
- [ ] 两个缺陷均出现在表中（不合并）
- [ ] 两个均标记 `POSSIBLE DUPLICATE`
- [ ] 每个交叉引用另一个（通过文件名或标题）
- [ ] 判决为 TRIAGED

---

### 用例 5：Director 门控检查——无门控；分类为建议性工具

**夹具：**
- `production/bugs/` 包含任意数量的报告

**输入：** `/bug-triage`

**预期行为：**
1. 技能生成分类表
2. 未调用任何 director agent
3. 输出中无门控 ID
4. 未调用写入工具

**断言：**
- [ ] 未调用 director 门控
- [ ] 未调用写入工具
- [ ] 输出中无门控跳过消息
- [ ] 判决为 TRIAGED，不经过任何门控检查

---

## 协议合规

- [ ] 在生成分类表前读取 `production/bugs/` 中的所有文件
- [ ] 按严重程度排序（CRITICAL → HIGH → MEDIUM → LOW）
- [ ] 标记缺少复现步骤的缺陷
- [ ] 通过标题/系统相似性标记可能重复的缺陷
- [ ] 不写入任何文件
- [ ] 所有情况下判决均为 TRIAGED（即使为空）

---

## 覆盖说明

- 缺陷报告格式异常（完全缺少严重程度字段）的情况不作夹具测试；
  技能会将其标记为 `UNKNOWN SEVERITY` 并排在表格末尾。
- 状态转换（将缺陷标记为已解决）超出本技能范围——bug-triage 为只读。
- 重复检测启发式方法（标题相似度 + 相同系统）为近似匹配；
  精确匹配逻辑在技能主体中定义。
