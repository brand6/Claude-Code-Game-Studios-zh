# 技能测试规范：/perf-profile

## 技能概要

`/perf-profile` 进行结构化性能分析。若提供了分析器数据（帧时间日志、
内存转储、draw call 统计），技能会分析数据并对照 `technical-preferences.md`
中定义的性能预算进行比较。若无数据，技能会生成手动性能检查清单。

技能可选择询问"May I write the performance report to `production/qa/perf-[日期].md`?"。
若存在之前的报告，技能会进行差量比较（当前 vs. 之前）以显示变化趋势。
不应用性能修复——仅分析和报告。
无 director 门控（但建议咨询 performance-analyst agent）。
判定结果：WITHIN BUDGET、CONCERNS 或 OVER BUDGET。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判定关键词：WITHIN BUDGET、CONCERNS、OVER BUDGET
- [ ] 在写入性能报告前包含"May I write"协作协议语言
- [ ] 包含下一步交接（例如 `/smoke-check` 构建验证，或建议咨询 performance-analyst）

---

## Director 门控检查

无。`/perf-profile` 是分析技能，不适用 director 门控。

---

## 测试用例

### 用例 1：提供帧数据——检测 draw call 峰值，CONCERNS

**夹具：**
- `technical-preferences.md` 预算：目标 60fps，draw calls ≤ 200
- 帧时间日志（作为分析器输出）：
  - 平均帧时间：16.3ms（略超 16.7ms 预算）
  - Draw calls：峰值 340（超出预算 70%）
  - 内存使用：正常

**输入：** `/perf-profile [帧时间日志文件]`

**预期行为：**
1. 技能读取 `technical-preferences.md` 获取性能预算
2. 技能分析帧时间数据
3. 识别出两个问题：
   - Draw call 峰值 340（超出预算 70%）——HIGH 严重性
   - 平均帧时间稍微超过预算——MEDIUM 严重性
4. 内存在预算内——无问题
5. 技能询问"May I write the perf report?"；写入后判定结果为 CONCERNS

**断言：**
- [ ] 从 `technical-preferences.md` 读取性能预算（不硬编码）
- [ ] 检测到 draw call 峰值为 HIGH 严重性问题
- [ ] 内存在预算内——不误报
- [ ] 写入报告前询问"May I write"
- [ ] 判定结果为 CONCERNS

---

### 用例 2：无分析器数据——输出手动检查清单

**夹具：**
- 没有帧时间日志或分析器输出文件

**输入：** `/perf-profile`

**预期行为：**
1. 技能检测到无数据提供
2. 技能生成手动性能检查清单：
   - 帧时间检查项（CPU/GPU 界定测试）
   - 内存检查项（基线 + 会话中泄漏检测）
   - Draw call 检查项（分析器截图说明）
   - 移动端热状态检查（如适用）
3. 技能输出检查清单但不写入报告（无实际数据可记录）
4. 无法给出判定（无数据）；输出说明："Provide profiler output to generate verdict."

**断言：**
- [ ] 检测到无数据提供
- [ ] 输出结构化的手动检查清单
- [ ] 不生成判定（无数据 → 无 WITHIN BUDGET/CONCERNS/OVER BUDGET 判定）
- [ ] 请求提供分析器数据以获得判定

---

### 用例 3：所有帧均超预算——OVER BUDGET + 优先级列表

**夹具：**
- 帧时间日志显示持续超预算：
  - 平均帧时间：28ms（超出 60fps 预算 67%）
  - Draw calls：始终 ≥ 400
  - 内存：超出预算 30%

**输入：** `/perf-profile [帧时间日志]`

**预期行为：**
1. 技能分析数据——3 个指标均超预算
2. 按影响优先级对问题排序（高严重性在前）
3. 判定结果为 OVER BUDGET
4. 报告包含按优先级排列的问题列表：
   1. Draw call 优化（最高影响）
   2. 内存使用（高影响）
   3. 帧时间总体（待 draw call 修复后再评估）

**断言：**
- [ ] 识别所有 3 个超预算指标
- [ ] 按影响降序优先排列问题
- [ ] 判定结果为 OVER BUDGET
- [ ] 报告写入前询问"May I write"

---

### 用例 4：存在之前的报告——差量比较

**夹具：**
- `production/qa/perf-2025-02-10.md` 存在（之前的报告）
- 新的帧时间数据可用

**输入：** `/perf-profile [新帧时间数据]`

**预期行为：**
1. 技能检测到 `production/qa/` 中有之前的性能报告
2. 技能分析新数据
3. 技能将新数据与之前的报告比较：
   - Draw calls：之前 340 → 现在 250（改善了 26%）
   - 帧时间：之前 18ms → 现在 16ms（改善）
4. 报告包含趋势指标（↑ 改善，↓ 恶化）
5. 判定结果为 WITHIN BUDGET（优化后改善明显）

**断言：**
- [ ] 检测到之前的性能报告
- [ ] 将新数据与之前的报告进行比较
- [ ] 趋势指标（改善/恶化）包含在报告中
- [ ] 判定反映当前数据（非之前的数据）

---

### 用例 5：门控合规性——无 director 门控；建议 performance-analyst

**夹具：**
- 帧时间数据可用

**输入：** `/perf-profile [数据]`

**预期行为：**
1. 技能完成分析
2. 未调用 director 门控
3. 若发现严重性能问题，报告建议咨询 performance-analyst agent

**断言：**
- [ ] 未调用任何 director 门控
- [ ] 发现严重性能问题时建议咨询 performance-analyst（可选，非强制）
- [ ] 写入报告时询问"May I write"

---

## 协议合规性

- [ ] 从 `technical-preferences.md` 读取性能预算（不硬编码）
- [ ] 无数据时生成手动检查清单
- [ ] 存在之前的报告时进行差量比较
- [ ] 写入报告前询问"May I write"（报告为可选）
- [ ] 不应用性能修复
- [ ] 返回 WITHIN BUDGET、CONCERNS 或 OVER BUDGET 判定（有数据时）

---

## 覆盖说明

- GPU 专项分析（着色器编译峰值、GPU 内存带宽）遵循相同的分析模式，
  但需要特定的 GPU 分析器数据格式；此处未单独测试。
- 多会话中的性能趋势（超过 2 个数据点）遵循相同的差量比较模式；
  此处仅测试单次比较。
- 估算性能影响（优化某指标可节省多少 ms）超出此技能的分析范围，
  由 performance-analyst agent 处理。
