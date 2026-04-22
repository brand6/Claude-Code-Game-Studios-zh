# Skill 测试规范：/propagate-design-change

## Skill 摘要

`/propagate-design-change design/gdd/[system].md` 在 GDD 修订后扫描所有下游制品（Story、Epic、ADR、TR 注册表）以识别受影响的内容。Skill 生成影响报告并对每个受影响的制品逐一询问"May I write"更新。

在分析阶段（读取 GDD 和制品）Skill 只读；仅在写入阶段（更新受影响的制品）需要用户批准。无 Director 门控——此 Skill 无论审核模式如何均不生成门控代理。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需 Fixture。

- [ ] 包含必填 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含 ≥2 个阶段标题
- [ ] 包含 verdict 关键词：COMPLETE、BLOCKED、NO IMPACT
- [ ] 包含"May I write"协作协议语言（按制品逐一批准）
- [ ] 末尾包含下一步交接（适合对应 verdict）
- [ ] 说明无 Director 门控（不读取 review-mode.txt）

---

## Director 门控检查

无 Director 门控——该 Skill 无论审核模式如何均不生成任何 Director 门控代理。变更传播是一种机械影响追踪操作；不需要创意或技术审核门控。

---

## 测试用例

### 用例 1：正常路径——GDD 修订影响 2 个 Story 和 1 个 Epic

**Fixture：**
- `design/gdd/[system].md` 已修订（有可检测的内容变化）
- `production/epics/[layer]/EPIC-[name].md` 引用该 GDD
- 该 Epic 下 2 个 Story 文件引用受影响的要求
- 其他 Story 未引用该 GDD

**输入：** `/propagate-design-change design/gdd/[system].md`

**预期行为：**
1. Skill 读取已修订的 GDD 和所有潜在受影响的制品
2. 生成影响报告：2 个 Story + 1 个 Epic 受影响，列出其他制品未受影响
3. 向用户展示完整影响报告
4. 对 Epic 询问"May I write `production/epics/[layer]/EPIC-[name].md`?"
5. 对每个受影响的 Story 逐一询问"May I write `production/epics/[layer]/story-[name].md`?"
6. 批准后写入更新的制品

**断言：**
- [ ] 任何"May I write"询问前先向用户展示完整影响报告
- [ ] 逐制品询问"May I write"——不是一次性批准整批
- [ ] 未受影响的制品未被修改
- [ ] Verdict 为 COMPLETE

---

### 用例 2：无影响路径——无下游引用

**Fixture：**
- `design/gdd/[system].md` 已修订
- 无 Story、Epic 或 ADR 文件引用该 GDD

**输入：** `/propagate-design-change design/gdd/[system].md`

**预期行为：**
1. Skill 读取 GDD 并扫描所有下游制品
2. 未找到引用
3. Skill 输出："No downstream artifacts reference this GDD. No updates required."
4. 不提示任何"May I write"
5. Verdict 为 NO IMPACT

**断言：**
- [ ] Skill 完成分析，输出 NO IMPACT 结论
- [ ] 不生成"May I write"提示
- [ ] 不写入任何文件
- [ ] Verdict 为 NO IMPACT

---

### 用例 3：进行中 Story——写入前显示提升警告

**Fixture：**
- GDD 已修订
- 一个受影响的 Story 的 Status 为 In Progress（有人正在实现该 Story）

**输入：** `/propagate-design-change design/gdd/[system].md`

**预期行为：**
1. Skill 生成影响报告，标注 In Progress 的 Story
2. 对进行中的 Story 在"May I write"询问前显示提升警告
3. 警告格式："⚠ CAUTION: story-[name].md is In Progress. Design change may conflict with active implementation."
4. 仍然进行"May I write"询问，用户自行决定

**断言：**
- [ ] 进行中的 Story 的影响报告中包含提升警告
- [ ] 对进行中的 Story 的"May I write"询问前显示警告
- [ ] 警告后仍然进行"May I write"询问（不自动阻止）

---

### 用例 4：边缘情况——未提供参数

**Fixture：**
- 未提供参数

**输入：** `/propagate-design-change`（无参数）

**预期行为：**
1. Skill 检测到未提供参数
2. Skill 输出用法错误："No GDD specified. Usage: /propagate-design-change design/gdd/[system].md"
3. Skill 列出最近修改的 GDD 作为建议（通过 git log）
4. 不进行任何分析

**断言：**
- [ ] 未提供参数时 Skill 输出用法错误
- [ ] 显示正确路径格式的用法示例
- [ ] 未指定目标 GDD 时不进行影响分析
- [ ] Skill 不在无用户输入的情况下静默选择 GDD

---

### 用例 5：Director 门控——无论审核模式如何均不生成门控

**Fixture：**
- GDD 已修订，存在下游引用
- `production/session-state/review-mode.txt` 存在，内容为 `full`

**输入：** `/propagate-design-change design/gdd/[system].md`

**预期行为：**
1. Skill 读取 GDD 并追踪下游引用
2. Skill 不读取 `production/session-state/review-mode.txt`
3. 全程不生成任何 Director 门控代理
4. 生成影响报告，正常进行逐制品批准

**断言：**
- [ ] 不生成 Director 门控代理（无 CD-、TD-、PR-、AD- 前缀的门控）
- [ ] Skill 不读取 `production/session-state/review-mode.txt`
- [ ] 输出不包含任何"Gate: [GATE-ID]"或门控跳过条目
- [ ] 审核模式对该 Skill 行为无影响

---

## 协议合规

- [ ] 生成影响报告前读取已修订的 GDD 和所有可能受影响的制品
- [ ] 任何"May I write"询问前完整展示影响报告
- [ ] 逐制品询问"May I write"——不是一次性批准整批
- [ ] 进行中的 Story 在批准询问前显示提升警告
- [ ] 无 Director 门控——不读取 review-mode.txt
- [ ] 末尾包含适合对应 verdict 的下一步交接（COMPLETE 或 NO IMPACT）

---

## 覆盖范围说明

- ADR 影响（GDD 变更需要更新或新建 ADR 时）遵循与 Story/Epic 更新相同的逐制品批准模式——不单独进行 Fixture 测试。
- TR 注册表影响（GDD 变更需要新建或更新 TR-ID 时）属于分析阶段，不单独进行 Fixture 测试。
- GDD 差异比较方法（检测 GDD 中变更内容）是运行时问题——Fixture 使用预先安排的内容差异。
