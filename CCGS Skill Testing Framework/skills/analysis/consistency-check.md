# 技能测试规范：/consistency-check

## 技能概要

`/consistency-check` 扫描 `design/gdd/` 中的所有 GDD，检查文档之间的内部冲突。它会生成结构化发现表，列名为：System A vs System B、Conflict Type、Severity（HIGH / MEDIUM / LOW）。冲突类型包括：formula mismatch、competing ownership、stale reference 和 dependency gap。

该技能在分析期间保持只读。无 director 门控。若用户请求，可将可选的一致性报告写入 `design/consistency-report-[date].md`，但写入前必须询问 "May I write"。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证，无需夹具。

- [ ] 包含所需的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判定关键词：CONSISTENT、CONFLICTS FOUND、DEPENDENCY GAP
- [ ] 在分析期间不要求包含 "May I write" 语言（只读扫描）
- [ ] 末尾包含下一步交接
- [ ] 明确说明：报告写入是可选的，且需要批准

---

## Director 门控检查

无 director 门控。该技能不会生成任何 director gate agent。一致性检查是机械化扫描；扫描本身不需要 creative 或 technical director 参与。

---

## 测试用例

### 用例 1：正常路径——4 份 GDD 没有冲突

**夹具：**
- `design/gdd/` 中恰好有 4 份系统 GDD
- 所有 GDD 的公式一致（没有相同变量却取值不同的情况）
- 没有两份 GDD 声称拥有同一个游戏实体或机制的所有权
- 所有依赖引用都指向实际存在的 GDD

**输入：** `/consistency-check`

**预期行为：**
1. 技能读取 `design/gdd/` 中全部 4 份 GDD
2. 运行跨 GDD 一致性检查（公式、所有权、引用）
3. 未发现冲突
4. 输出结构化发现表，显示 0 个问题
5. 判定结果：CONSISTENT

**断言：**
- [ ] 在生成输出前，先读取全部 4 份 GDD
- [ ] 即便为空，也会展示发现表（显示 "No conflicts found"）
- [ ] 没有冲突时，判定结果为 CONSISTENT
- [ ] 未经用户批准，技能不会写入任何文件
- [ ] 包含下一步交接

---

### 用例 2：失败路径——两份 GDD 的伤害公式冲突

**夹具：**
- GDD-A 定义伤害公式：`damage = attack * 1.5`
- GDD-B 为同一种实体类型定义伤害公式：`damage = attack * 2.0`
- 两份 GDD 都引用同一个 `attack` 变量

**输入：** `/consistency-check`

**预期行为：**
1. 技能读取所有 GDD，并检测到公式不匹配
2. 发现表包含一条记录：GDD-A vs GDD-B | Formula Mismatch | HIGH
3. 展示具体冲突的公式，而不是只说“存在公式冲突”
4. 判定结果：CONFLICTS FOUND

**断言：**
- [ ] 判定结果为 CONFLICTS FOUND（不是 CONSISTENT）
- [ ] 冲突项会点名两份 GDD 文件
- [ ] 冲突类型为 "Formula Mismatch"
- [ ] 直接公式矛盾时，严重性为 HIGH
- [ ] 发现表中会展示两条冲突公式
- [ ] 技能不会自动解决冲突

---

### 用例 3：部分路径——GDD 引用了一个没有对应 GDD 的系统

**夹具：**
- GDD-A 的 Dependencies 章节将 "system-B" 列为依赖
- `design/gdd/` 中不存在 system-B 的 GDD
- 其余 GDD 都保持一致

**输入：** `/consistency-check`

**预期行为：**
1. 技能读取所有 GDD，并检查依赖引用
2. GDD-A 对 "system-B" 的引用无法解析，因为没有对应 GDD
3. 发现表包含：GDD-A vs (missing) | Dependency Gap | MEDIUM
4. 判定结果：DEPENDENCY GAP（不是 CONSISTENT，也不是 CONFLICTS FOUND）

**断言：**
- [ ] 判定结果为 DEPENDENCY GAP（与 CONSISTENT、CONFLICTS FOUND 区分开）
- [ ] 发现项会点名 GDD-A 和缺失的 system-B
- [ ] 未解析的依赖引用严重性为 MEDIUM
- [ ] 技能会建议运行 `/design-system system-B` 来创建缺失的 GDD

---

### 用例 4：边界情况——未找到任何 GDD

**夹具：**
- `design/gdd/` 目录为空，或该目录不存在

**输入：** `/consistency-check`

**预期行为：**
1. 技能尝试读取 `design/gdd/` 中的文件
2. 未找到任何 GDD 文件
3. 输出错误："No GDDs found in `design/gdd/`. Run `/design-system` to create GDDs first."
4. 不生成发现表
5. 不给出判定结果

**断言：**
- [ ] 未找到 GDD 时，技能会输出清晰的错误信息
- [ ] 不会给出任何判定结果（CONSISTENT / CONFLICTS FOUND / DEPENDENCY GAP）
- [ ] 技能会建议正确的下一步动作（`/design-system`）
- [ ] 技能不会崩溃，也不会生成半成品报告

---

### 用例 5：Director 门控——不生成门控；不读取 review-mode.txt

**夹具：**
- `design/gdd/` 中至少有 2 份 GDD
- `production/session-state/review-mode.txt` 存在，内容为 `full`

**输入：** `/consistency-check`

**预期行为：**
1. 技能读取所有 GDD，并运行一致性扫描
2. 技能不会读取 `production/session-state/review-mode.txt`
3. 任意时刻都不会生成 director gate agent
4. 正常输出发现表和判定结果

**断言：**
- [ ] 不生成任何 director gate agent（没有以 CD-、TD-、PR-、AD- 开头的 gates）
- [ ] 技能不会读取 `production/session-state/review-mode.txt`
- [ ] 输出中不包含任何 "Gate: [GATE-ID]" 或 gate-skipped 条目
- [ ] review mode 不影响该技能的行为

---

## 协议合规性

- [ ] 在生成发现表前读取全部 GDD
- [ ] 如果用户请求报告，必须先完整展示发现表，再询问是否写入
- [ ] 判定结果严格为：CONSISTENT、CONFLICTS FOUND、DEPENDENCY GAP 之一
- [ ] 无 director 门控，也不读取 review-mode.txt
- [ ] 报告写入（若用户请求）必须经过 "May I write" 批准
- [ ] 以与判定结果相符的下一步交接结束

---

## 覆盖说明

- 该技能检查 GDD 之间的结构一致性。更深层的设计理论分析（例如 pillar drift、dominant strategies）由 `/review-all-gdds` 负责。
- 公式冲突检测依赖 GDD 中一致的公式记法；如果同一机制只用非正式描述表达，技能可能无法检测到。
- 冲突严重性规则（HIGH / MEDIUM / LOW）在技能正文中定义，这里不再重复展开。
