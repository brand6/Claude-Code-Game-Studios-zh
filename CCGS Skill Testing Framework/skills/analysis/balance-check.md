# 技能测试规范：/balance-check

## 技能概要

`/balance-check` 读取 `assets/data/` 中的平衡数据文件（JSON 或 YAML），并根据 `design/gdd/` 下定义的设计公式检查每个数值。它会生成一张调查结果表，列出：数值 → 公式 → 偏差 → 严重性。不调用 director 门控（只读分析）。技能可选择写入平衡报告，但仅在用户请求时才会询问 "May I write"。判定结果：BALANCED、CONCERNS 或 OUT OF BALANCE。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证，无需夹具。

- [ ] 包含所需的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判定关键词：BALANCED、CONCERNS、OUT OF BALANCE
- [ ] 包含 "May I write" 语言（用于可选报告写入）
- [ ] 包含下一步交接（发现结果审阅后该做什么）

---

## Director 门控检查

无。平衡检查是只读分析技能；不调用任何门控。

---

## 测试用例

### 用例 1：正常路径——所有平衡数值都在公式容差范围内

**夹具：**
- `assets/data/combat-balance.json` 存在，包含 6 个属性值
- `design/gdd/combat-system.md` 为全部 6 个属性定义了公式，容差为 ±10%
- 6 个数值全部落在容差范围内

**输入：** `/balance-check`

**预期行为：**
1. 技能读取 `assets/data/` 中的所有平衡数据文件
2. 技能读取 `design/gdd/` 中的 GDD 公式
3. 计算每个数值相对于公式的偏差
4. 所有偏差都在 ±10% 容差范围内
5. 输出调查结果表，所有行都显示 PASS
6. 判定结果为 BALANCED

**断言：**
- [ ] 为所有被检查的数值展示调查结果表
- [ ] 每一行都显示：属性名、公式目标值、实际值、偏差百分比
- [ ] 在容差范围内时，所有行都显示 PASS 或等效结果
- [ ] 判定结果为 BALANCED
- [ ] 未经用户批准不写入任何文件

---

### 用例 2：失衡——玩家伤害比公式目标高 40%

**夹具：**
- `assets/data/combat-balance.json` 中有 `player_damage_base: 140`
- `design/gdd/combat-system.md` 公式指定 `player_damage_base = 100`（±10%）
- 其余属性都在容差范围内

**输入：** `/balance-check`

**预期行为：**
1. 技能读取 combat-balance.json，并计算 `player_damage_base` 的偏差
2. 偏差为 +40%，远超 ±10% 容差
3. 技能在调查结果表中将该行标记为 HIGH 严重性
4. 判定结果为 OUT OF BALANCE
5. 技能会在表格前显著提示这个 HIGH 严重性问题

**断言：**
- [ ] `player_damage_base` 这一行显示 +40% 的偏差
- [ ] 当偏差超出容差 2 倍以上时，严重性为 HIGH
- [ ] 只要任一属性存在 HIGH 严重性偏差，判定结果就是 OUT OF BALANCE
- [ ] HIGH 严重性问题会被显式指出，而不是埋在表格行中

---

### 用例 3：没有 GDD 公式——无法校验，并给出指引

**夹具：**
- `assets/data/economy-balance.yaml` 存在，包含 10 个属性值
- `design/gdd/` 中没有任何 GDD 为经济属性定义公式

**输入：** `/balance-check`

**预期行为：**
1. 技能读取平衡数据文件
2. 搜索 GDD 公式定义，但找不到经济属性对应的公式
3. 技能输出："Cannot validate economy stats — no formulas defined. Run /design-system first."
4. 不为经济属性生成调查结果表
5. 判定结果为 CONCERNS（数据存在，但无法校验）

**断言：**
- [ ] GDD 中不存在公式时，技能不会伪造公式目标值
- [ ] 输出会明确指出缺失的公式来源
- [ ] 输出建议运行 `/design-system` 来定义公式
- [ ] 判定结果为 CONCERNS（不是 BALANCED，因为无法验证）

---

### 用例 4：孤立引用——平衡文件引用了未定义的属性

**夹具：**
- `assets/data/combat-balance.json` 包含属性 `legacy_armor_mult: 1.5`
- `design/gdd/combat-system.md` 没有 `legacy_armor_mult` 对应的公式
- 其余属性都有公式定义且都通过校验

**输入：** `/balance-check`

**预期行为：**
1. 技能读取 combat-balance.json 中的全部属性
2. 找不到 `legacy_armor_mult` 在任何 GDD 中的公式
3. 在调查结果表中将 `legacy_armor_mult` 标记为 ORPHAN REFERENCE
4. 其余属性照常评估；在容差范围内的属性显示 PASS
5. 判定结果为 CONCERNS（孤立引用阻止完整校验）

**断言：**
- [ ] `legacy_armor_mult` 以 ORPHAN REFERENCE 状态出现在调查结果表中
- [ ] 孤立引用在表中与公式偏差区分开来
- [ ] 只要发现孤立引用，判定结果就是 CONCERNS
- [ ] 技能不会静默跳过孤立属性

---

### 用例 5：门控合规性——只读；无门控；可选报告需批准

**夹具：**
- 平衡数据和 GDD 公式都存在；其中 1 个属性有 CONCERNS 级偏差（比目标高 15%）
- `review-mode.txt` 内容为 `full`

**输入：** `/balance-check`

**预期行为：**
1. 技能读取数据和 GDD，并生成调查结果表
2. 判定结果为 CONCERNS（有 1 个属性稍微超出范围）
3. 无论 review mode 如何，都不调用 director 门控
4. 技能向用户展示调查结果表
5. 技能提供可选的平衡报告写入
6. 如果用户选择写入：询问 "May I write to `production/qa/balance-report-[date].md`?"
7. 如果用户不选择写入：技能直接结束，不写入文件

**断言：**
- [ ] 任意 review mode 下都不调用 director 门控
- [ ] 调查结果表会直接展示，不会自动写入任何文件
- [ ] 可选报告写入会被提供，但不是强制流程
- [ ] 只有用户选择写报告时，才会出现 "May I write" 提示

---

## 协议合规性

- [ ] 分析前同时读取平衡数据文件和 GDD 公式
- [ ] 调查结果表显示 Value、Formula、Deviation 和 Severity 列
- [ ] 不在未经用户明确批准的情况下写入任何文件
- [ ] 不调用 director 门控
- [ ] 判定结果严格为：BALANCED、CONCERNS、OUT OF BALANCE 之一

---

## 覆盖说明

- `assets/data/` 完全为空的情况未在此测试；该行为沿用 CONCERNS 模式，并提示未找到任何数据文件。
- 容差阈值（±10%、±20%）属于技能实现细节；测试验证的是能否检测并分类偏差，而不是断言精确阈值。
