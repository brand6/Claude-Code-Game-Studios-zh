# 技能测试规范：/test-flakiness

## 技能概要

`/test-flakiness` 通过两种方式检测不确定性测试（不稳定测试）：
（1）读取 CI 历史日志或 `tests/flaky-test-registry.md` 中的历史测试运行记录，
（2）扫描 `tests/` 中的源码模式（例如未播种 `randf()`、`OS.get_ticks_msec()`、
实时等待）。若两种来源均无，则无法确认不稳定性——只能报告疑似测试。

技能在写入不稳定测试登记册前询问"May I write?"。
无 director 门控。判定结果：NO FLAKINESS（历史记录和源码模式均无发现）、
SUSPECT TESTS FOUND（仅有源码模式，无历史记录证据）
或 CONFIRMED FLAKY（历史记录中存在多次间歇性失败）。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判定关键词：NO FLAKINESS、SUSPECT TESTS FOUND、CONFIRMED FLAKY
- [ ] 包含"May I write"协作协议语言（写入不稳定测试登记册前）
- [ ] 包含下一步交接（例如 `/test-evidence-review` 进行修复指导，或 `/regression-suite` 隔离不稳定测试）

---

## Director 门控检查

无。`/test-flakiness` 是测试维护技能，不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——10 次运行全部通过，NO FLAKINESS

**夹具：**
- CI 运行日志：10 次测试运行，`test_damage_calculation` 全部通过
- `tests/unit/combat/test_damage_calculation.gd`：无不稳定性模式（无 `randf()`、
  无实时等待）

**输入：** `/test-flakiness`

**预期行为：**
1. 技能读取 CI 历史日志（或测试运行记录）
2. `test_damage_calculation` 10/10 次通过
3. 技能扫描源码模式——未检测到不稳定性模式
4. 0 个疑似或确认的不稳定测试
5. 判定结果为 NO FLAKINESS

**断言：**
- [ ] 读取 CI 历史日志或测试运行记录
- [ ] 扫描不稳定性的源码模式
- [ ] 0 个失败或疑似测试 → 判定结果为 NO FLAKINESS
- [ ] 不写入任何文件（无更新可写入）

---

### 用例 2：10 次运行中 3 次失败——SUSPECT TESTS FOUND（历史记录证据）

**夹具：**
- CI 运行日志：`test_network_timeout` 运行 10 次中失败 3 次（成功率 70%）

**输入：** `/test-flakiness`

**预期行为：**
1. 技能读取 CI 运行历史
2. `test_network_timeout` 10 次中失败 3 次——30% 失败率
3. 技能将此标记为 SUSPECT（历史记录中存在间歇性失败）
4. 报告列出 `test_network_timeout`，注明失败率和出现的 CI 运行
5. 技能询问"May I write to `tests/flaky-test-registry.md`?"进行记录
6. 判定结果为 SUSPECT TESTS FOUND

**断言：**
- [ ] 检测到 30% 的间歇性失败率
- [ ] 将 `test_network_timeout` 标记为疑似不稳定测试
- [ ] 报告包含失败率和具体的 CI 运行引用
- [ ] 写入登记册前询问"May I write"
- [ ] 判定结果为 SUSPECT TESTS FOUND

---

### 用例 3：源码模式——未播种 randf()——SUSPECT TESTS FOUND

**夹具：**
- 无 CI 历史日志（或无历史数据）
- `tests/unit/loot/test_loot_table.gd` 包含：
  ```gdscript
  var drop = randf()  # 无播种——每次运行结果不同
  ```

**输入：** `/test-flakiness`

**预期行为：**
1. 技能尝试读取 CI 历史日志——无记录
2. 技能扫描测试源码中的不稳定性模式
3. 检测到未播种 `randf()`——不确定性模式
4. 报告："Unseed `randf()` call detected in `test_loot_table.gd`.
   This test will produce different results on each run."
5. 判定结果为 SUSPECT TESTS FOUND（无历史记录证据——仅源码模式）

**断言：**
- [ ] 检测到未播种的 `randf()` 调用
- [ ] 正确标记为 SUSPECT TESTS FOUND（不是 CONFIRMED FLAKY——无历史记录证据）
- [ ] 报告建议添加固定种子（例如 `seed(12345)`）

---

### 用例 4：无历史记录 + 源码模式（OS.get_ticks_msec）——SUSPECT TESTS FOUND

**夹具：**
- 无 CI 历史日志
- `tests/integration/perf/test_frame_timing.gd` 包含：
  ```gdscript
  var start = OS.get_ticks_msec()
  # ... 一些操作 ...
  assert(OS.get_ticks_msec() - start < 16)  # 假设特定帧时长
  ```

**输入：** `/test-flakiness`

**预期行为：**
1. 技能尝试读取 CI 历史——无记录
2. 技能扫描测试源码——检测到 `OS.get_ticks_msec()` 与时间敏感断言结合
3. 将此标记为疑似不稳定测试（性能测试在不同系统上会失败）
4. 建议使用确定性方法（模拟帧或相对阈值）
5. 判定结果为 SUSPECT TESTS FOUND

**断言：**
- [ ] 检测到 `OS.get_ticks_msec()` 用于时间敏感断言
- [ ] 标记为 SUSPECT TESTS FOUND（非 CONFIRMED FLAKY）
- [ ] 建议确定性测试替代方案

---

### 用例 5：CONFIRMED FLAKY 需要历史记录证据——仅源码模式不足够

**夹具：**
- `tests/unit/ai/test_pathfinding.gd` 包含未播种 `randf()`（源码模式）
- 无 CI 历史日志

**输入：** `/test-flakiness`

**预期行为：**
1. 技能扫描源码——检测到不稳定性模式
2. 无 CI 历史记录——无法确认实际间歇性失败
3. 仅有源码模式 → 判定结果为 SUSPECT TESTS FOUND（非 CONFIRMED FLAKY）
4. 报告解释："Source pattern detected, but no historical run data available
   to confirm flakiness. Rating: SUSPECT TESTS FOUND."

**断言：**
- [ ] 检测到不稳定性源码模式
- [ ] 仅有源码模式时不产生 CONFIRMED FLAKY 判定
- [ ] 正确降级为 SUSPECT TESTS FOUND
- [ ] 报告解释确认不稳定性需要历史记录证据

---

## 协议合规性

- [ ] 从 CI 历史日志读取历史测试运行记录（若存在）
- [ ] 扫描 `tests/` 中的不稳定性源码模式（`randf()`、`create_timer`、`OS.get_ticks_msec`）
- [ ] CONFIRMED FLAKY 需要历史记录证据（仅有源码模式产生 SUSPECT TESTS FOUND）
- [ ] 写入不稳定测试登记册前询问"May I write"
- [ ] 返回 NO FLAKINESS、SUSPECT TESTS FOUND 或 CONFIRMED FLAKY 判定

---

## 覆盖说明

- Unity/C# 中的不稳定性模式（`UnityEngine.Random.value`、`Time.realtimeSinceStartup`）
  遵循相同的源码模式检测方法，但使用 C# 特定 API；此处未单独测试。
- 基础设施不稳定性（CI 机器超时、网络故障）与测试不稳定性不同；
  此处不对 CI 基础设施失败进行断言，仅对测试特定的不稳定性进行断言。
- 批量运行 10 次测试以检测不稳定性的自动化流程
  在技能正文中定义；此处不对 10 次运行计数进行断言，
  而是对检测逻辑进行断言。
