# Skill 测试规范：/patch-notes

## Skill 摘要

`/patch-notes` 是 Haiku 级 Skill，从现有 changelog 内容生成面向玩家的补丁说明，去除内部任务 ID 和技术术语，改用通俗语言。仅筛选与玩家相关的条目（可见特性和 Bug 修复；内部重构不在其列）。不使用 Director 门控。Skill 在持久化前询问"May I write to `docs/patch-notes-vX.X.md`?"。Verdict 始终为 COMPLETE。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需 Fixture。

- [ ] 包含必填 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含 ≥2 个阶段标题
- [ ] 包含 verdict 关键词：COMPLETE
- [ ] 包含"May I write"语言（Skill 会写入补丁说明文件）
- [ ] 包含下一步交接（例如：分享给社区运营）

---

## Director 门控检查

无。补丁说明生成是快速汇编任务，不调用门控。

---

## 测试用例

### 用例 1：正常路径——Changelog 筛选出面向玩家的条目

**Fixture：**
- `docs/CHANGELOG.md` 存在，包含 5 条条目：
  - "Add dual-wield melee system"（特性——面向玩家）
  - "Fix crash on level transition"（修复——面向玩家）
  - "Add enemy patrol AI"（特性——面向玩家）
  - "Refactor input handler to use event bus"（修复——仅内部）
  - "Update dependency: Godot 4.6"（仅内部）
- 版本为 `v0.4.0`

**输入：** `/patch-notes v0.4.0`

**预期行为：**
1. Skill 读取 `docs/CHANGELOG.md`
2. Skill 筛选出 3 条面向玩家的条目，排除 2 条内部条目
3. Skill 用通俗语言重写条目（无任务 ID，无技术术语）
4. Skill 向用户展示草稿
5. Skill 询问"May I write to `docs/patch-notes-v0.4.0.md`?"
6. 用户批准后写入文件，Verdict 为 COMPLETE

**断言：**
- [ ] 补丁说明中仅出现 3 条条目（2 条内部条目被排除）
- [ ] 条目以无内部任务 ID 的通俗语言撰写
- [ ] 文件路径匹配 `docs/patch-notes-v0.4.0.md`
- [ ] 文件写入前出现"May I write"提示
- [ ] 写入后 Verdict 为 COMPLETE

---

### 用例 2：未找到 Changelog——引导先运行 /changelog

**Fixture：**
- `docs/CHANGELOG.md` 不存在

**输入：** `/patch-notes v0.4.0`

**预期行为：**
1. Skill 尝试读取 `docs/CHANGELOG.md`——未找到
2. Skill 输出："No changelog found — run /changelog first to generate one"
3. 不生成补丁说明，不写入文件

**断言：**
- [ ] changelog 不存在时 Skill 不崩溃
- [ ] 输出明确引导用户运行 `/changelog`
- [ ] 不出现"May I write"提示（没有内容可写入）
- [ ] Verdict 为 BLOCKED（依赖未满足）

---

### 用例 3：设计文件夹包含语气指导——融入输出中

**Fixture：**
- `docs/CHANGELOG.md` 存在，包含面向玩家的条目
- `design/community/tone-guide.md` 存在，指导内容为："upbeat, encouraging tone; avoid passive voice"

**输入：** `/patch-notes v0.4.0`

**预期行为：**
1. Skill 读取 changelog
2. Skill 检测到 `design/community/tone-guide.md` 中的语气指导
3. Skill 在用通俗语言重写条目时应用语气指导
4. 补丁说明使用积极、主动语态的措辞
5. Skill 展示草稿，询问写入，批准后写入

**断言：**
- [ ] Skill 检查 `design/` 中是否存在社区或语气指导文件
- [ ] 语气指导内容影响补丁说明条目的措辞
- [ ] 输出在适用处体现主动语态和积极语气
- [ ] Skill 注明已应用语气指导

---

### 用例 4：补丁说明模板已存在——使用模板而非生成结构

**Fixture：**
- `.claude/docs/templates/patch-notes-template.md` 存在，包含结构化的标题格式
- `docs/CHANGELOG.md` 存在，包含面向玩家的条目

**输入：** `/patch-notes v0.4.0`

**预期行为：**
1. Skill 读取 changelog 并检测到模板存在
2. Skill 将面向玩家的条目填入模板
3. 输出中保留模板的页眉/页脚结构
4. Skill 询问"May I write"并在批准后写入

**断言：**
- [ ] Skill 在从零生成前检查是否存在补丁说明模板
- [ ] 找到模板时使用模板结构（不被默认格式覆盖）
- [ ] 面向玩家的条目插入模板的正确章节
- [ ] 输出注明已使用模板

---

### 用例 5：门控合规——无门控；社区运营为独立步骤

**Fixture：**
- `docs/CHANGELOG.md` 存在，包含面向玩家的条目
- `review-mode.txt` 内容为 `full`

**输入：** `/patch-notes v0.4.0`

**预期行为：**
1. Skill 以 full 模式汇编补丁说明
2. 不调用 Director 门控（社区审核是独立的手动步骤）
3. Skill 在 Haiku 模型下运行——快速汇编
4. Skill 在输出中注明："Consider sharing draft with community manager before publishing"
5. Skill 请求用户批准，确认后写入

**断言：**
- [ ] 无论何种 review 模式，均不调用 Director 门控
- [ ] 输出建议（但不强制要求）社区运营审核
- [ ] Skill 直接从汇编阶段进入"May I write"提示
- [ ] Verdict 为 COMPLETE

---

## 协议合规

- [ ] 生成补丁说明前读取 `docs/CHANGELOG.md`
- [ ] 仅筛选面向玩家的条目
- [ ] 用无内部 ID 的通俗语言重写条目
- [ ] 写入补丁说明文件前始终询问"May I write"
- [ ] 不调用 Director 门控
- [ ] 在 Haiku 模型层运行（快速、低成本）

---

## 覆盖说明

- 所有 changelog 条目均为内部条目（零面向玩家条目）的情况未在测试中覆盖；行为为生成空补丁说明草稿并附警告。
- changelog 标题中的版本号解析属于实现细节，在此不验证。
- 用例 5 中提到的社区运营咨询为建议性质；该步骤由独立 Skill 或手动审核处理。
