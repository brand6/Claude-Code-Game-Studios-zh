# 技能测试规范：/balance-check

## 技能概要

`/balance-check` 读取 `assets/data/` 中的平衡数据文件（JSON 或 YAML），
将数值与 GDD 中定义的公式进行比较，并识别异常值、偏差和失衡配置。
技能生成一张调查结果表，列出每个检查值、期望值、偏差百分比和严重性评级。

技能可选择询问"May I write the balance report to `production/qa/balance-[日期].md`?"。
不应用修复——仅报告失衡情况。
无 director 门控。判定结果：BALANCED（所有值在容忍范围内）、
CONCERNS（存在轻微偏差）或 OUT OF BALANCE（存在显著偏差）。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判定关键词：BALANCED、CONCERNS、OUT OF BALANCE
- [ ] 在写入平衡报告前包含"May I write"协作协议语言
- [ ] 包含下一步交接（例如 `/design-system` 调整 GDD 公式，或 `/estimate` 估算修复工作量）

---

## Director 门控检查

无。`/balance-check` 是只读分析技能，不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——所有数值在容忍范围内，BALANCED

**夹具：**
- `design/gdd/combat.md` 定义：damage = base_attack × 1.5
- `assets/data/enemies.json`：boss_damage = 450，base_attack = 300（计算得 450 = 300 × 1.5）
- 所有其他值均在公式容忍范围内（±15%）

**输入：** `/balance-check`

**预期行为：**
1. 技能读取战斗 GDD 获取公式
2. 技能读取 `assets/data/enemies.json`
3. 技能计算每个值的偏差（boss_damage 偏差：0%）
4. 0 个超出容忍范围的偏差
5. 技能询问"May I write the balance report?"
6. 写入报告；判定结果为 BALANCED

**断言：**
- [ ] 从 GDD 读取公式（不硬编码）
- [ ] 从数据文件读取数值
- [ ] 计算每个值的偏差百分比
- [ ] 0 个超出容忍范围的偏差 → 判定结果为 BALANCED
- [ ] 报告写入前询问"May I write"

---

### 用例 2：偏差 +40%——HIGH 严重性，OUT OF BALANCE

**夹具：**
- `design/gdd/combat.md` 定义：player_max_health = level × 50
- `assets/data/player.json` 在 10 级时 max_health = 700（期望 500，偏差 +40%）

**输入：** `/balance-check`

**预期行为：**
1. 技能读取公式（level × 50）
2. 技能从数据文件读取值（700）
3. 技能计算偏差：(700-500)/500 = +40%
4. 将 +40% 标记为 HIGH 严重性（超出 ±15% 容忍范围）
5. 判定结果为 OUT OF BALANCE

**断言：**
- [ ] 偏差计算为 +40%
- [ ] 标记为 HIGH 严重性
- [ ] 判定结果为 OUT OF BALANCE（非 CONCERNS）
- [ ] 报告中列出具体的值（700）和期望值（500）

---

### 用例 3：GDD 无公式——建议运行 /design-system，CONCERNS

**夹具：**
- `assets/data/weapons.json` 存在且有伤害数值
- 武器系统的 GDD 不包含伤害公式（可能是新系统）

**输入：** `/balance-check weapons`

**预期行为：**
1. 技能读取武器 GDD——没有伤害公式
2. 技能无法将武器数据与公式进行比较
3. 技能报告："No balance formulas found for weapons in GDD.
   Recommend running `/design-system weapons` to define formulas."
4. 技能不将数值标记为失衡（无参考基准）
5. 判定结果为 CONCERNS（有数值但无公式可校验）

**断言：**
- [ ] 检测到 GDD 中缺少公式
- [ ] 报告中提及 `/design-system weapons` 作为下一步
- [ ] 不将数值误报为失衡（无参考基准）
- [ ] 判定结果为 CONCERNS

---

### 用例 4：孤立引用——数据中有统计值但无对应公式，CONCERNS

**夹具：**
- `assets/data/items.json` 中有 `critical_hit_multiplier = 3.5`
- GDD 无 `critical_hit_multiplier` 对应公式

**输入：** `/balance-check`

**预期行为：**
1. 技能遍历数据文件中的所有统计值
2. 检测到 `critical_hit_multiplier` 在 GDD 中无对应公式
3. 将此标记为孤立引用（MEDIUM 严重性）——数值存在但无公式可校验
4. 报告建议为该统计值设计公式
5. 判定结果为 CONCERNS

**断言：**
- [ ] 检测到 GDD 公式中缺失的数据键（孤立引用）
- [ ] 标记为 MEDIUM 严重性孤立引用
- [ ] 建议设计缺失的公式
- [ ] 判定结果为 CONCERNS

---

### 用例 5：门控合规性——无门控；可选报告写入

**夹具：**
- 平衡数据和 GDD 公式均已配置

**输入：** `/balance-check`

**预期行为：**
1. 技能完成完整的平衡检查
2. 未调用 director 门控
3. 询问"May I write"写入可选报告

**断言：**
- [ ] 未调用任何 director 门控
- [ ] 写入报告时询问"May I write"
- [ ] 报告为可选——若用户拒绝仍返回判定结果

---

## 协议合规性

- [ ] 从 GDD 读取公式（不硬编码期望值）
- [ ] 计算每个值的精确偏差百分比
- [ ] 根据偏差分配 HIGH/MEDIUM/LOW 严重性
- [ ] 在报告中标记孤立引用
- [ ] 写入报告前询问"May I write"（报告为可选）
- [ ] 不修改任何数据文件
- [ ] 返回 BALANCED、CONCERNS 或 OUT OF BALANCE 判定

---

## 覆盖说明

- 容忍范围阈值（±15%）从 `technical-preferences.md` 或 GDD 元数据中读取。
  精确阈值此处未进行断言测试。
- 多个系统同时进行平衡检查遵循相同流程；此处针对单个系统进行测试。
- 技能不生成平衡调整建议——仅标记失衡值；调整工作由设计师处理。
