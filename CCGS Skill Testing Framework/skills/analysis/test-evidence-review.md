# 技能测试规范：/test-evidence-review

## 技能概要

`/test-evidence-review` 对 `tests/` 文件进行质量审查：命名规范、
断言覆盖、非确定性检测（实时等待、未播种随机数）、隔离问题（直接外部 API 调用）
和幻数（无常量的硬编码值）。技能为只读——不修改测试文件。

可能会建议将调查结果通报 qa-lead agent。
无 director 门控；与 QL-TEST-COVERAGE 门（由 `/gate-check` 处理）不同。
判定结果：PASS（所有测试符合质量标准）、WARNINGS（存在小问题）
或 FAIL（存在非确定性或隔离失败——这些会破坏测试套件可靠性）。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判定关键词：PASS、WARNINGS、FAIL
- [ ] 不包含"May I write"语言（test-evidence-review 为只读技能）
- [ ] 包含下一步交接（例如 `/smoke-check` 或 `/regression-suite` 构建完善的测试套件）

---

## Director 门控检查

无。`/test-evidence-review` 是只读分析技能，不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——所有标准符合，PASS

**夹具：**
- `tests/unit/combat/test_damage_calculation.gd` 存在：
  - 测试函数名描述性强（例如 `test_melee_attack_deals_expected_damage`）
  - 无 `create_timer()`、`await`（非确定性实时等待）
  - 伤害值使用命名常量（`EXPECTED_BASE_DAMAGE = 50`）
  - 无直接外部 API 调用（依赖注入模拟）

**输入：** `/test-evidence-review tests/unit/combat/test_damage_calculation.gd`

**预期行为：**
1. 技能读取测试文件
2. 检查命名规范——描述性测试名称 ✓
3. 检查非确定性——无 `create_timer()`，无未播种 `randf()` ✓
4. 检查隔离——无直接外部调用 ✓
5. 检查幻数——使用命名常量 ✓
6. 判定结果为 PASS

**断言：**
- [ ] 检查测试命名规范
- [ ] 检查非确定性模式（create_timer、await 实时等待）
- [ ] 检查隔离（外部 API 调用）
- [ ] 检查幻数（无常量的硬编码值）
- [ ] 0 个问题 → 判定结果为 PASS
- [ ] 不修改测试文件

---

### 用例 2：使用实时等待（create_timer）——FAIL

**夹具：**
- `tests/integration/save/test_save_load.gd` 包含：
  ```gdscript
  await get_tree().create_timer(2.0).timeout  # 等待存档写入完成
  ```

**输入：** `/test-evidence-review tests/integration/save/test_save_load.gd`

**预期行为：**
1. 技能读取测试文件
2. 检测到 `create_timer(2.0)` 实时等待
3. 将此标记为 HIGH 严重性失败（非确定性：不同系统速度不同）
4. 报告说明："Real-time wait detected (`create_timer`).
   Tests should use signals or mocks to avoid time-dependent behavior."
5. 判定结果为 FAIL

**断言：**
- [ ] 检测到 `create_timer` 实时等待模式
- [ ] 标记为 HIGH 严重性非确定性问题
- [ ] 报告提供修复指导（使用信号或模拟）
- [ ] 判定结果为 FAIL（非 WARNINGS——这会破坏测试可靠性）
- [ ] 测试文件不被修改

---

### 用例 3：直接外部 API 调用——FAIL（隔离失败）

**夹具：**
- `tests/unit/network/test_player_auth.gd` 包含：
  ```gdscript
  var response = await HTTPRequest.new().request("https://auth.example.com/login")
  ```

**输入：** `/test-evidence-review tests/unit/network/test_player_auth.gd`

**预期行为：**
1. 技能读取测试文件
2. 检测到直接外部 HTTP 调用（到真实 URL）
3. 将此标记为 HIGH 严重性隔离失败（单元测试不应访问外部网络）
4. 报告说明："Direct external API call detected. Unit tests must mock HTTP clients
   to ensure isolation."
5. 判定结果为 FAIL

**断言：**
- [ ] 检测到直接外部 API 调用（真实 URL）
- [ ] 标记为 HIGH 严重性隔离失败
- [ ] 报告提供修复指导（模拟 HTTP 客户端）
- [ ] 判定结果为 FAIL
- [ ] 测试文件不被修改

---

### 用例 4：路径未找到——建议运行 /test-setup

**夹具：**
- `tests/` 目录不存在或为空

**输入：** `/test-evidence-review`

**预期行为：**
1. 技能尝试扫描 `tests/`——未找到测试文件
2. 技能输出："No test files found. Run `/test-setup` to scaffold the test framework,
   then `/test-helpers` to generate test utilities."
3. 不生成判定
4. 技能礼貌退出

**断言：**
- [ ] 检测到无测试文件
- [ ] 同时建议 `/test-setup` 和 `/test-helpers`
- [ ] 不生成判定（无测试可审查）

---

### 用例 5：门控合规性——无门控；与 QL-TEST-COVERAGE 门不同

**夹具：**
- `tests/` 包含若干测试文件

**输入：** `/test-evidence-review`

**预期行为：**
1. 技能完成测试证据审查
2. 未调用任何 director 门控
3. 输出区分于 QL-TEST-COVERAGE 门（后者由 `/gate-check` 处理）

**断言：**
- [ ] 未调用任何 director 门控
- [ ] 输出中不出现 QL-TEST-COVERAGE 门 ID
- [ ] 判定结果为 PASS、WARNINGS 或 FAIL

---

## 协议合规性

- [ ] 检查命名规范、非确定性、隔离和幻数
- [ ] 非确定性和隔离问题产生 FAIL 判定（非 WARNINGS）
- [ ] 小问题（命名、幻数）产生 WARNINGS 判定
- [ ] 从不修改测试文件（完全只读）
- [ ] 与 QL-TEST-COVERAGE 门不同（不检查覆盖率百分比）

---

## 覆盖说明

- C#（Unity）测试模式遵循相同的非确定性和隔离规则，但使用
  `Task.Delay()`（而非 `create_timer`）作为实时等待检测的信号。
  此处未单独测试 C# 变体。
- 测试覆盖率（百分比行覆盖率）由 QL-TEST-COVERAGE 门控处理，
  而非此技能——此处明确不进行断言测试。
- 跨多个目录的批量审查遵循相同的逐文件检查模式；
  此处针对单个文件和目录级别进行测试。
