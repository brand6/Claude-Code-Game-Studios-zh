# Skill 测试规范：/changelog

## Skill 摘要

`/changelog` 是 Haiku 级 Skill，通过读取 git 提交历史和上次发布 tag 以来已关闭的 Sprint Story 来自动生成面向开发者的更新日志。内容按特性、修复和已知问题分类整理。不使用 Director 门控。该 Skill 在持久化前询问"May I write to `docs/CHANGELOG.md`?"。Verdict 始终为 COMPLETE。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需 Fixture。

- [ ] 包含必填 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含 ≥2 个阶段标题
- [ ] 包含 verdict 关键词：COMPLETE
- [ ] 包含"May I write"语言（Skill 会写入 changelog）
- [ ] 包含下一步交接（例如：运行 /patch-notes 生成面向玩家的版本）

---

## Director 门控检查

无。Changelog 生成是快速汇编任务，不调用门控。

---

## 测试用例

### 用例 1：正常路径——上次发布 tag 以来有多个 Sprint

**Fixture：**
- Git 历史中三个 Sprint 前有一个 `v0.3.0` 标签
- 该标签之后：Sprint 006、007、008 共 12 条提交
- Sprint Story 文件中的任务 ID 与提交消息匹配
- `docs/CHANGELOG.md` 尚不存在

**输入：** `/changelog`

**预期行为：**
1. Skill 读取自 `v0.3.0` 标签以来的 git log
2. Skill 读取 Sprint Story 以交叉引用任务 ID
3. Skill 将条目整理为特性、修复、已知问题三个章节
4. Skill 向用户展示草稿
5. Skill 询问"May I write to `docs/CHANGELOG.md`?"
6. 用户批准后写入文件，Verdict 为 COMPLETE

**断言：**
- [ ] Changelog 涵盖自最新 git tag 以来的提交
- [ ] 条目按特性 / 修复 / 已知问题分类
- [ ] Sprint Story 引用用于丰富提交描述
- [ ] 文件写入前出现"May I write"提示
- [ ] 写入后 Verdict 为 COMPLETE

---

### 用例 2：未找到 Git Tag——使用所有提交，注明版本基线

**Fixture：**
- Git 仓库有提交记录但不存在任何 tag
- 历史中共 20 条提交，分布在 3 个 Sprint

**输入：** `/changelog`

**预期行为：**
1. Skill 检查 git tag——未找到
2. Skill 使用历史中的所有提交作为基线
3. Skill 在输出中注明："No version tag found — using full commit history; version baseline is unset"
4. Skill 仍从可用提交整理出有序的 changelog
5. Skill 询问"May I write"并在批准后写入

**断言：**
- [ ] 当不存在 git tag 时 Skill 不报错
- [ ] 输出明确说明未找到版本基线
- [ ] 使用完整提交历史作为来源
- [ ] 尽管缺少 tag，changelog 仍按章节组织

---

### 用例 3：提交消息缺少任务 ID——按日期分组并注明

**Fixture：**
- 上次 tag 以来 git log 共 8 条提交
- 5 条提交没有任务 ID（如"fix typo"、"tweak values"）
- 3 条提交包含与 Sprint Story 匹配的任务 ID

**输入：** `/changelog`

**预期行为：**
1. Skill 读取提交和 Sprint Story
2. 3 条提交与 Sprint Story 匹配并放入对应章节
3. 5 条未标记提交按日期归入"Misc"或"Other Changes"章节
4. 输出注明："5 commits without task IDs — grouped by date"
5. Skill 在批准后写入 changelog

**断言：**
- [ ] 有任务 ID 的提交放入对应章节（特性或修复）
- [ ] 无任务 ID 的提交单独分组并附注说明
- [ ] 输出标明缺少任务引用的提交数量
- [ ] 无提交被静默丢弃

---

### 用例 4：CHANGELOG.md 已存在——新章节前置，旧条目保留

**Fixture：**
- `docs/CHANGELOG.md` 已存在，包含 `v0.2.0` 和 `v0.3.0` 的章节
- 自 `v0.3.0` tag 以来存在新提交

**输入：** `/changelog`

**预期行为：**
1. Skill 检测到 `docs/CHANGELOG.md` 已存在
2. Skill 汇编自 `v0.3.0` 以来的新条目
3. Skill 展示草稿，新章节前置于现有内容之上
4. Skill 询问"May I write to `docs/CHANGELOG.md`?"（确认前置策略）
5. 用户批准后，新内容前置，旧条目完整保留，Verdict 为 COMPLETE

**断言：**
- [ ] Skill 写入前读取现有 changelog 以检测已有内容
- [ ] 新章节前置（而非追加或覆盖）于现有条目之上
- [ ] 已写入文件中 v0.2.0 和 v0.3.0 的旧 changelog 条目完整保留
- [ ] "May I write"提示体现前置操作

---

### 用例 5：门控合规——无门控；先读后写并获得批准

**Fixture：**
- Git 历史包含自上次 tag 以来的提交
- `review-mode.txt` 内容为 `full`

**输入：** `/changelog`

**预期行为：**
1. Skill 以 full 模式汇编 changelog
2. 不调用 Director 门控（changelog 生成属于汇编任务，不是交付门控）
3. Skill 在 Haiku 模型下运行——快速汇编
4. Skill 请求用户批准，确认后写入文件

**断言：**
- [ ] 无论何种 review 模式，均不调用 Director 门控
- [ ] 输出中不引用任何门控结果
- [ ] Skill 直接从汇编阶段进入"May I write"提示
- [ ] Verdict 为 COMPLETE

---

## 协议合规

- [ ] 汇编前读取 git log 和 Sprint Story 文件
- [ ] 写入 changelog 前始终询问"May I write"
- [ ] 不调用 Director 门控
- [ ] Verdict 始终为 COMPLETE
- [ ] 在 Haiku 模型层运行（快速、低成本）

---

## 覆盖说明

- 仓库未初始化 git 的情况未在测试中覆盖；行为取决于 git 命令失败的处理方式。
- 合并提交（merge commit）与压缩提交（squash commit）在这些测试中未明确区分，属于 git log 解析阶段的实现细节。
- `/patch-notes` Skill 应在 `/changelog` 之后运行以生成面向玩家的输出；该交接在 patch-notes 规范中验证。
