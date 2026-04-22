# 技能测试规范：/test-flakiness

## 技能概要

`/test-flakiness` 通过分析测试历史日志（如果可用），或扫描测试源码中常见的不稳定模式（无种子的随机数、真实时间等待、外部 I/O）来检测非确定性测试。无 director 门控。未经用户批准，技能不会写入文件。判定结果：NO FLAKINESS、SUSPECT TESTS FOUND 或 CONFIRMED FLAKY。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证，无需夹具。

- [ ] 包含所需的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判定关键词：NO FLAKINESS、SUSPECT TESTS FOUND、CONFIRMED FLAKY
- [ ] 不要求包含 "May I write" 语言（只读；可选报告写入仍需批准）
- [ ] 包含下一步交接（不稳定性发现之后该做什么）

---

## Director 门控检查

无。不稳定性检测是面向 QA lead 的建议性质量技能；不调用任何门控。

---

## 测试用例

### 用例 1：正常路径——测试历史干净，没有不稳定性

**夹具：**
- `production/qa/test-history/` 中包含 10 次测试运行日志
- 所有测试在这 10 次运行中都稳定通过（每个测试 100% 通过率）
- 没有任何测试表现出失败模式

**输入：** `/test-flakiness`

**预期行为：**
1. 技能从 `production/qa/test-history/` 读取测试历史日志
2. 计算每个测试在 10 次运行中的通过率
3. 所有测试 10 次都通过，没有发现不一致
4. 判定结果为 NO FLAKINESS

**断言：**
- [ ] 在可用时读取测试历史日志
- [ ] 基于所有可用运行计算每个测试的通过率
- [ ] 所有测试稳定通过时，判定结果为 NO FLAKINESS
- [ ] 不写入任何文件

---

### 用例 2：发现疑似测试——历史记录中出现间歇性失败

**夹具：**
- `production/qa/test-history/` 中包含 10 次测试运行日志
- `test_combat_damage_applies_crit_multiplier` 通过 7 次、失败 3 次
- 失败信息不完全一致（有时超时，有时值错误）

**输入：** `/test-flakiness`

**预期行为：**
1. 技能读取测试历史日志并计算通过率
2. `test_combat_damage_applies_crit_multiplier` 的通过率为 70%（阈值：95%）
3. 技能将它标记为 SUSPECT，并显示通过率（7/10）和失败模式
4. 判定结果为 SUSPECT TESTS FOUND
5. 技能建议排查该测试是否存在时序或状态依赖

**断言：**
- [ ] 通过率低于阈值的测试会按名称被标记
- [ ] 每个疑似测试都会显示通过率（分数和百分比）
- [ ] 如果可以检测到，失败模式（例如不一致的错误信息）会被注明
- [ ] 判定结果为 SUSPECT TESTS FOUND
- [ ] 技能会给出调查建议

---

### 用例 3：源码模式——使用了未播种的随机数

**夹具：**
- 没有测试历史日志
- `tests/unit/loot/loot_drop_test.gd` 包含：
  ```gdscript
  var roll = randf()  # 未播种的随机数——非确定性
  assert_gt(roll, 0.5, "Loot should drop above 50%")
  ```

**输入：** `/test-flakiness`

**预期行为：**
1. 技能未找到测试历史日志
2. 技能回退到源码分析
3. 检测到 `randf()` 调用前没有 `seed()`
4. 将该测试标记为 FLAKINESS RISK（源码模式，未确认）
5. 判定结果为 SUSPECT TESTS FOUND（检测到模式，但没有历史记录确认）
6. 技能建议在调用前播种随机数，或 mock 掉随机函数

**断言：**
- [ ] 在没有历史日志时，会使用源码分析作为回退方案
- [ ] 能将未播种的随机数使用识别为不稳定性风险
- [ ] 判定结果为 SUSPECT TESTS FOUND（不是 CONFIRMED FLAKY，因为没有历史记录）
- [ ] 修复建议会提到播种或 mock

---

### 用例 4：没有测试历史——仅做源码分析并查找常见模式

**夹具：**
- `production/qa/test-history/` 不存在
- `tests/` 中有 15 个测试文件
- 扫描发现有 2 个测试使用 `OS.get_ticks_msec()` 做时间断言
- 没有发现其他不稳定模式

**输入：** `/test-flakiness`

**预期行为：**
1. 技能检查测试历史，未找到
2. 技能说明："No test history available — analyzing source code for flakiness patterns only"
3. 扫描全部测试文件，查找常见模式：未播种随机数、真实时间等待、系统时钟使用
4. 发现 2 个测试使用 `OS.get_ticks_msec()`，并将其标记为 FLAKINESS RISK
5. 判定结果为 SUSPECT TESTS FOUND

**断言：**
- [ ] 技能会明确说明当前仅进行源码分析（没有历史记录）
- [ ] 会扫描常见不稳定模式：随机数、基于时间的断言、外部 I/O
- [ ] 用于断言的 `OS.get_ticks_msec()` 会被标记为不稳定性风险
- [ ] 一旦发现源码模式，判定结果就是 SUSPECT TESTS FOUND

---

### 用例 5：门控合规性——无门控；不稳定性报告属于建议性输出

**夹具：**
- 测试历史显示有 1 个 CONFIRMED FLAKY 测试（10 次运行中失败 6 次）
- `review-mode.txt` 内容为 `full`

**输入：** `/test-flakiness`

**预期行为：**
1. 技能分析测试历史，识别出 1 个已确认的不稳定测试
2. 无论 review mode 如何，都不调用 director 门控
3. 判定结果为 CONFIRMED FLAKY
4. 技能展示发现结果，并提供可选的书面报告
5. 如果用户选择写入：询问 "May I write to `production/qa/flakiness-report-[date].md`?"

**断言：**
- [ ] 任意 review mode 下都不调用 director 门控
- [ ] CONFIRMED FLAKY 判定必须基于历史记录证据，而不是仅靠源码模式
- [ ] 可选报告写入在真正写入前必须经过 "May I write"
- [ ] 不稳定性报告是给 qa-lead 的建议性信息；技能不会自动禁用测试

---

## 协议合规性

- [ ] 在可用时读取测试历史日志；不可用时回退到源码分析
- [ ] 明确说明正在使用哪种分析模式（历史记录 vs 仅源码）
- [ ] 对 SUSPECT 分类使用不稳定阈值（例如 95% 通过率）
- [ ] CONFIRMED FLAKY 需要历史记录证据；源码模式只会产生 SUSPECT
- [ ] 不会禁用或修改任何测试文件
- [ ] 不调用 director 门控
- [ ] 判定结果严格为：NO FLAKINESS、SUSPECT TESTS FOUND、CONFIRMED FLAKY 之一

---

## 覆盖说明

- SUSPECT 分类所使用的通过率阈值（例如上文建议的 95%）属于实现细节；测试验证的是能否标记间歇性失败，而不是断言精确阈值。
- 因环境问题导致失败的测试（缺失资源、错误平台等）并不属于不稳定性；技能需要区分环境失败和测试本身的非确定性，这里未显式单测这一点。
