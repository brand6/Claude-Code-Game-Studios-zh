# 技能测试规范：/launch-checklist

## 技能概要

`/launch-checklist` 生成涵盖所有发布前核查项目的完整发布就绪清单。
清单分为以下类别：法律合规、平台认证状态、商店页面完整性、
构建验证、分析/崩溃报告配置，以及首次运行体验（FTUE）验证。

每项检查项目以 ✅ VERIFIED、⚠️ NEEDS ATTENTION 或 ❌ BLOCKING 标记。
总体判决为 LAUNCH READY（所有项目通过）、LAUNCH BLOCKED（存在 BLOCKING 项目）
或 CONCERNS（存在 NEEDS ATTENTION 项目但无 BLOCKING 项目）。

清单在"May I write"确认后写入
`production/launch/launch-checklist-[日期].md`。
不适用 director 门控——完整发布流水线由 `/team-release` 编排。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判决关键词：LAUNCH READY、LAUNCH BLOCKED、CONCERNS
- [ ] 在写入清单前包含"May I write"协作协议语言
- [ ] 包含 6 个清单类别：法律、平台认证、商店页面、构建验证、分析/崩溃报告、FTUE
- [ ] 末尾包含下一步交接（如 `/team-release` 或 `/day-one-patch`）

---

## Director 门控检查

无。`/launch-checklist` 是发布运营工具。不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——所有项目验证通过，LAUNCH READY

**夹具：**
- `production/launch/` 目录不存在
- 所有平台认证均以 `APPROVED` 标注
- 商店页面元数据（标题、描述、截图）均已填写
- 构建验证：无关键缺陷，smoke 检查通过
- 分析/崩溃报告服务已配置
- FTUE 流程已完成游戏测试且无阻断性问题

**输入：** `/launch-checklist`

**预期行为：**
1. 技能收集 6 个类别的状态（询问用户或读取现有文件）
2. 所有项目标记为 ✅ VERIFIED
3. 技能询问"May I write to `production/launch/launch-checklist-[日期].md`?"
4. 清单写入；总体判决为 LAUNCH READY

**断言：**
- [ ] 所有 6 个类别均出现在输出中
- [ ] 所有项目标记为 ✅ VERIFIED
- [ ] 判决为 LAUNCH READY（大写，准确拼写）
- [ ] 写入前询问"May I write"
- [ ] 文件名使用当前日期

---

### 用例 2：平台认证未提交——LAUNCH BLOCKED

**夹具：**
- 所有其他项目通过
- 平台认证状态为"未提交"

**输入：** `/launch-checklist`

**预期行为：**
1. 技能收集清单状态
2. 技能将平台认证标记为 ❌ BLOCKING
3. 其他项目正常通过
4. 总体判决为 LAUNCH BLOCKED
5. 技能明确说明哪些平台认证为 BLOCKING 状态

**断言：**
- [ ] 平台认证项目标记为 ❌ BLOCKING
- [ ] 判决为 LAUNCH BLOCKED
- [ ] 阻断项目明确识别（不仅说"某些内容被阻断"）
- [ ] 阻断项目已写入清单文件（写入前询问"May I write"）

---

### 用例 3：需要手动检查——CONCERNS，不阻断发布

**夹具：**
- 所有认证均已批准
- 商店页面截图已上传，但未确认是否通过平台截图规范审核
- 无 BLOCKING 项目

**输入：** `/launch-checklist`

**预期行为：**
1. 技能识别商店截图作为 ⚠️ NEEDS ATTENTION 项目
2. 技能请求用户确认截图合规状态
3. 其他项目正常通过
4. 总体判决为 CONCERNS（存在 NEEDS ATTENTION 但无 BLOCKING）
5. 写入清单，标注 CONCERNS 状态和需要注意的具体项目

**断言：**
- [ ] 商店截图项目标记为 ⚠️ NEEDS ATTENTION
- [ ] 判决为 CONCERNS（不是 LAUNCH BLOCKED，也不是 LAUNCH READY）
- [ ] 需要注意的项目明确识别
- [ ] 技能不在 CONCERNS 项目未解决的情况下单方面宣布 LAUNCH READY

---

### 用例 4：与上次清单对比——显示变更差异

**夹具：**
- `production/launch/launch-checklist-2026-03-30.md` 已存在（上次运行结果）
- 上次清单：分析配置为 ⚠️ NEEDS ATTENTION
- 本次运行：分析配置现为 ✅ VERIFIED

**输入：** `/launch-checklist`

**预期行为：**
1. 技能读取上次清单以进行对比
2. 技能注明自上次运行以来的变更：
   "Analytics: NEEDS ATTENTION → VERIFIED"
3. 清单写入带新日期的新文件
4. 差异作为对比摘要呈现

**断言：**
- [ ] 输出中注明"上次与本次"的差异
- [ ] 新清单写入带新日期的新文件（不覆盖上次文件）
- [ ] 差异摘要准确反映状态变更

---

### 用例 5：Director 门控检查——无门控；清单为运营工具

**夹具：**
- 标准项目设置

**输入：** `/launch-checklist`

**预期行为：**
1. 技能生成并写入清单
2. 未调用任何 director agent
3. 输出中无门控 ID

**断言：**
- [ ] 未调用 director 门控
- [ ] 输出中无门控跳过消息
- [ ] 技能在不经过任何门控检查的情况下达到 LAUNCH READY / LAUNCH BLOCKED / CONCERNS

---

## 协议合规

- [ ] 覆盖所有 6 个清单类别：法律、平台认证、商店页面、构建验证、分析/崩溃报告、FTUE
- [ ] 每项检查使用 ✅ / ⚠️ / ❌ 前缀
- [ ] 存在 ❌ BLOCKING 项目时判决为 LAUNCH BLOCKED
- [ ] 无 BLOCKING 但有 ⚠️ NEEDS ATTENTION 项目时判决为 CONCERNS
- [ ] 所有项目均通过时判决为 LAUNCH READY
- [ ] 写入前询问"May I write to `production/launch/launch-checklist-[日期].md`?"

---

## 覆盖说明

- 每个类别的具体子项目（例如年龄评级、GDPR 合规、崩溃报告服务名称）
  在此规范中不作硬编码；仅对类别级别进行断言，具体子项目在技能主体中定义。
- 存在多个 BLOCKING 项目的情况与用例 2 相同处理——
  所有 BLOCKING 项目均在清单中列出。
- 此技能与 `/release-checklist`（内部里程碑清单）不同；
  后者与平台认证和商店页面内容无关。
