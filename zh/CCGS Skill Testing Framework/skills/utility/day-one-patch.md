# 技能测试规范：/day-one-patch

## 技能概要

`/day-one-patch` 为首发补丁制定计划，处理在 v1.0 发布时已知但被推迟的问题。
它读取 `production/bugs/` 中的未关闭缺陷报告，以及故事文件中被推迟的验收标准
（状态为 `Done` 但有推迟 AC 备注的故事），并生成带有每项问题预计修复时间的
优先级补丁计划。

补丁计划在"May I write"确认后写入 `production/releases/day-one-patch.md`。
若发现 P0（发布后严重）问题，技能会引导先运行 `/hotfix`，
再继续补丁规划。不适用 director 门控。判决始终为 COMPLETE。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判决关键词：COMPLETE
- [ ] 在写入计划前包含"May I write"协作协议语言
- [ ] 包含下一步交接（例如，P0 问题用 `/hotfix`，后续用 `/release-checklist`）

---

## Director 门控检查

无。`/day-one-patch` 是发布规划工具。不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——3 个已知问题，含修复估算的补丁计划

**夹具：**
- `production/bugs/` 包含 3 个未关闭缺陷，严重程度：1 个 MEDIUM，2 个 LOW
- 冲刺故事中无推迟的 AC
- 所有缺陷均有复现步骤和系统标识

**输入：** `/day-one-patch`

**预期行为：**
1. 技能读取全部 3 个未关闭缺陷
2. 技能分配修复工作量估算：MEDIUM 缺陷 = 1-2 天，LOW 缺陷 = 每个 4 小时
3. 技能生成 MEDIUM 缺陷优先的补丁计划
4. 计划包含：优先顺序、预计时间线、负责系统、修复描述
5. 技能询问"May I write to `production/releases/day-one-patch.md`?"
6. 文件写入；判决为 COMPLETE

**断言：**
- [ ] 计划中包含全部 3 个缺陷
- [ ] 缺陷按严重程度优先排序（MEDIUM 在 LOW 之前）
- [ ] 每项问题提供修复估算
- [ ] 写入前询问"May I write"
- [ ] 判决为 COMPLETE

---

### 用例 2：发布后发现严重问题——P0，触发 /hotfix 指导

**夹具：**
- v1.0 发布后，`production/bugs/` 中发现 CRITICAL 严重程度的缺陷
- 该缺陷导致所有存档文件数据丢失

**输入：** `/day-one-patch`

**预期行为：**
1. 技能读取缺陷并识别出 CRITICAL 严重程度的问题
2. 技能升级："P0 ISSUE DETECTED — data loss bug requires immediate hotfix
   before patch planning can proceed"
3. 技能不将 P0 问题纳入补丁计划时间线
4. 技能明确指引："Run `/hotfix` to resolve this issue first"
5. 发出 P0 指导后：仍然为剩余低严重程度缺陷生成并写入计划；判决为 COMPLETE

**断言：**
- [ ] P0 升级消息在补丁计划之前醒目显示
- [ ] 对 P0 问题明确指向 `/hotfix`
- [ ] P0 问题不在补丁计划时间线中（需要立即处理）
- [ ] 非 P0 问题仍然纳入计划；判决为 COMPLETE

---

### 用例 3：来自故事完成的推迟 AC——自动纳入补丁计划

**夹具：**
- `production/sprints/sprint-008.md` 中有一个状态为 `Done` 的故事，附注：
  "DEFERRED AC: Gamepad vibration on damage — deferred to post-launch patch"
- 同一系统无未关闭缺陷

**输入：** `/day-one-patch`

**预期行为：**
1. 技能读取冲刺故事并检测到推迟的 AC 备注
2. 推迟的 AC 自动作为工作项纳入补丁计划
3. 计划条目："Deferred from sprint-008: Gamepad vibration on damage"
4. 分配修复估算；"May I write"批准后写入补丁计划
5. 判决为 COMPLETE

**断言：**
- [ ] 故事文件中推迟的 AC 自动纳入计划
- [ ] 推迟项目标注来源故事（sprint-008）
- [ ] 推迟的 AC 获得与缺陷条目相同的修复估算
- [ ] 判决为 COMPLETE

---

### 用例 4：无已知问题——含模板注释的空计划

**夹具：**
- `production/bugs/` 为空
- 故事中无推迟的 AC

**输入：** `/day-one-patch`

**预期行为：**
1. 技能读取缺陷——未发现
2. 技能读取故事推迟的 AC——未发现
3. 技能生成附注释的空补丁计划："No known issues at launch"
4. 保留模板结构（标题完整）供将来使用
5. 技能询问"May I write to `production/releases/day-one-patch.md`?"
6. 文件写入；判决为 COMPLETE

**断言：**
- [ ] 写入的文件中出现"No known issues at launch"注释
- [ ] 空计划中保留模板标题
- [ ] 技能在无问题可规划时不报错
- [ ] 判决为 COMPLETE

---

### 用例 5：Director 门控检查——无门控；day-one-patch 是规划工具

**夹具：**
- `production/bugs/` 中存在已知问题

**输入：** `/day-one-patch`

**预期行为：**
1. 技能生成并写入补丁计划
2. 未调用任何 director agent
3. 输出中无门控 ID

**断言：**
- [ ] 未调用 director 门控
- [ ] 输出中无门控跳过消息
- [ ] 技能在不经过任何门控检查的情况下达到 COMPLETE

---

## 协议合规

- [ ] 在生成计划前读取 `production/bugs/` 中的未关闭缺陷
- [ ] 扫描故事文件中的推迟 AC 备注
- [ ] 对 CRITICAL（P0）缺陷升级，明确给出 `/hotfix` 指导
- [ ] 无问题时生成附注释的空计划（不报错）
- [ ] 在写入前询问"May I write to `production/releases/day-one-patch.md`?"
- [ ] 所有路径下判决均为 COMPLETE

---

## 覆盖说明

- 存在多个 CRITICAL 缺陷的情况与用例 2 相同处理；所有 P0 问题一并升级。
- 补丁时间线估算（例如"3 天后提供补丁"）需要人工 QA 和构建时间估算；
  技能基于严重程度使用粗略估算，而非实际团队速度。
- 玩家公告的补丁说明文档（`/patch-notes`）是在补丁计划执行后调用的独立技能。
