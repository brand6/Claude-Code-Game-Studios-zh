# 技能测试规范：/regression-suite

## 技能概要

`/regression-suite` 将测试覆盖率映射到 GDD 需求上。
它读取故事文件中的验收标准（AC），扫描 `tests/` 目录，
并生成覆盖率报告，分为：
- **已覆盖**（每条 AC 都有对应的测试）
- **部分覆盖**（部分但非全部 AC 有测试）
- **未测试**（AC 存在但无对应测试）

技能同时标记孤儿测试文件（存在于 `tests/` 目录但无对应 AC 的测试）。
判决为 FULL COVERAGE（全部覆盖）、GAPS FOUND（存在缺口）
或 CRITICAL GAPS（高优先级 AC 无测试）。
不适用 director 门控。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判决关键词：FULL COVERAGE、GAPS FOUND、CRITICAL GAPS
- [ ] 定义覆盖率状态：已覆盖、部分覆盖、未测试
- [ ] 定义孤儿测试检测
- [ ] 包含下一步交接（例如 `/test-setup` 若框架缺失，`/qa-plan` 若测试计划缺失）

---

## Director 门控检查

无。`/regression-suite` 是 QA 覆盖率工具。不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——所有 AC 都有对应测试，FULL COVERAGE

**夹具：**
- `production/stories/` 中的 3 个故事，每个故事含 2 条 AC（共 6 条 AC）
- `tests/` 目录中有 6 个测试文件，各测试文件通过命名约定明确对应一条 AC

**输入：** `/regression-suite`

**预期行为：**
1. 技能读取故事文件，提取 6 条 AC
2. 技能扫描 `tests/` 目录，找到 6 个测试文件
3. 技能将测试文件映射到 AC——全部 6 条均有覆盖
4. 技能生成覆盖率报告，所有 6 条 AC 均标记为"已覆盖"
5. 判决为 FULL COVERAGE

**断言：**
- [ ] 报告中所有 6 条 AC 均标记为"已覆盖"
- [ ] 判决为 FULL COVERAGE
- [ ] 无孤儿测试消息（所有测试均对应 AC）
- [ ] 未写入任何文件（覆盖率报告为对话形式输出）

---

### 用例 2：3 条 AC 无测试——GAPS FOUND

**夹具：**
- 5 个故事，共 8 条 AC
- `tests/` 目录中有 5 个测试文件（覆盖其中 5 条 AC）
- 3 条 AC 无对应测试

**输入：** `/regression-suite`

**预期行为：**
1. 技能读取故事文件，提取 8 条 AC
2. 技能扫描 `tests/` 目录
3. 技能识别出 3 条 AC 无对应测试
4. 覆盖率报告中，未覆盖的 3 条 AC 按故事标识列出
5. 判决为 GAPS FOUND

**断言：**
- [ ] 3 条无测试的 AC 按名称明确列出
- [ ] 判决为 GAPS FOUND
- [ ] 有测试的 5 条 AC 标记为"已覆盖"

---

### 用例 3：关键优先级 AC 无测试——CRITICAL GAPS

**夹具：**
- 4 个故事，其中一个标记优先级为 CRITICAL（存档系统功能）
- CRITICAL 故事的 AC 无对应测试

**输入：** `/regression-suite`

**预期行为：**
1. 技能读取故事文件，识别出 CRITICAL 优先级标记
2. 技能扫描 `tests/` 目录——CRITICAL 故事的 AC 无测试
3. 技能将该缺口升级为 CRITICAL GAPS（高于普通 GAPS FOUND）
4. 覆盖率报告中，CRITICAL AC 醒目标注
5. 建议立即为 CRITICAL AC 添加测试后再继续
6. 判决为 CRITICAL GAPS

**断言：**
- [ ] CRITICAL 优先级 AC 的缺口单独报告（区别于普通缺口）
- [ ] 判决为 CRITICAL GAPS（不是 GAPS FOUND）
- [ ] 建议中明确要求在继续前添加测试

---

### 用例 4：孤儿测试——无对应 AC 的测试文件

**夹具：**
- 3 个故事，共 6 条 AC，均有对应测试
- `tests/` 目录中额外有 2 个测试文件无法映射到任何已知 AC

**输入：** `/regression-suite`

**预期行为：**
1. 技能读取故事文件，提取 6 条 AC
2. 技能扫描 `tests/` 目录，发现 8 个测试文件（6 个映射正常 + 2 个孤儿）
3. 技能标记 2 个孤儿测试文件，注明"无对应 AC"
4. 孤儿测试单独列出（文件名已知）
5. 因 6 条 AC 均有覆盖，判决为 FULL COVERAGE（附孤儿测试说明）

**断言：**
- [ ] 2 个孤儿测试文件按文件名列出
- [ ] 孤儿测试标记为"no matching AC"
- [ ] 因所有 AC 均有覆盖，判决为 FULL COVERAGE（孤儿测试不降低判决等级）

---

### 用例 5：Director 门控检查——无门控；regression-suite 为覆盖率工具

**夹具：**
- 标准项目设置

**输入：** `/regression-suite`

**预期行为：**
1. 技能生成覆盖率报告
2. 未调用任何 director agent
3. 未写入任何文件

**断言：**
- [ ] 未调用 director 门控
- [ ] 未写入任何文件
- [ ] 输出中无门控跳过消息
- [ ] 判决为 FULL COVERAGE / GAPS FOUND / CRITICAL GAPS

---

## 协议合规

- [ ] 读取故事文件中的 AC
- [ ] 扫描 `tests/` 目录并将测试映射到 AC
- [ ] 识别孤儿测试文件（存在于 tests/ 但无对应 AC）
- [ ] 报告分为：已覆盖/部分覆盖/未测试
- [ ] 所有 AC 均有覆盖时判决为 FULL COVERAGE
- [ ] 存在缺口时判决为 GAPS FOUND
- [ ] 高优先级 AC 无测试时判决为 CRITICAL GAPS
- [ ] 不写入任何文件（报告为对话形式输出）

---

## 覆盖说明

- AC 与测试文件的映射逻辑（命名约定或内容分析）在技能主体中定义；
  此规范仅要求能正确识别覆盖与否。
- "部分覆盖"判决（非全部 AC 有测试）不在此规范中单独测试；
  用例 2 和 3 涵盖了 GAPS FOUND 和 CRITICAL GAPS 的核心路径。
- 此技能为只读，不修改测试文件或故事文件。
