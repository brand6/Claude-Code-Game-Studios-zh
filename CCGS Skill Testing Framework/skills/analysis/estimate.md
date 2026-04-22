# 技能测试规范：/estimate

## 技能概要

`/estimate` 基于故事复杂度、验收标准数量、技术不确定性
和历史冲刺速度来估算任务工作量。估算使用 S/M/L/XL 规模（配合时间范围：
S=几小时，M=1-2 天，L=3-5 天，XL=整个冲刺或以上）。
估算具有建议性质——仅供参考，不会被自动写入故事文件。
每次运行始终产生一个估算（不跳过）。

无 director 门控；`/estimate` 最终建议参考 `/sprint-plan` 进行规划。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判定关键词（S、M、L、XL 规模标签）
- [ ] 不包含"May I write"语言（估算为只读建议性输出）
- [ ] 包含下一步交接（例如 `/sprint-plan` 将估算安排到冲刺中）

---

## Director 门控检查

无。`/estimate` 是只读分析技能，不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——清晰的故事 + 已知技术，估算 M（1-2 天）

**夹具：**
- 故事文件：`production/sprints/sprint-04/stories/enemy-patrol-ai.md`
- 故事包含：
  - 3 个清晰的验收标准
  - 已有 ADR（状态为 Accepted）
  - 引用已有系统（无新依赖）
  - 技术栈已知（Godot 4 + GDScript）
- 历史速度数据：sprint-01、sprint-02、sprint-03 均可用

**输入：** `/estimate production/sprints/sprint-04/stories/enemy-patrol-ai.md`

**预期行为：**
1. 技能读取故事文件
2. 技能分析复杂度因素：
   - 验收标准：3（适中）
   - ADR 状态：Accepted（低不确定性）
   - 无新依赖（低风险）
3. 技能读取历史速度数据——有可用数据
4. 技能输出 M 估算（1-2 天）及理由
5. 不写入故事文件

**断言：**
- [ ] 输出估算（M）及理由
- [ ] 理由引用复杂度因素（AC 数量、ADR 状态、依赖关系）
- [ ] 若有速度数据则予以参考
- [ ] 估算不写入故事文件
- [ ] 每次运行始终产生一个估算

---

### 用例 2：高不确定性——无 ADR 且 AC 模糊，估算 L-XL 并附风险说明

**夹具：**
- 故事文件包含：
  - "实现多人同步"（验收标准模糊）
  - 无相关 ADR
  - 依赖新的网络库（未知风险）
  - 无历史速度参考

**输入：** `/estimate [故事文件]`

**预期行为：**
1. 技能检测高不确定性指标：
   - 模糊 AC："实现多人同步"缺乏精确性
   - 无 ADR（架构决策未定）
   - 未知依赖
2. 技能估算 L-XL 并附风险说明：
   "Estimate: L-XL. High uncertainty due to: missing ADR, vague acceptance criteria,
   unknown dependency risk. Recommend clarifying AC and creating ADR before starting."
3. 不写入任何文件

**断言：**
- [ ] 识别高不确定性指标（无 ADR、模糊 AC、未知依赖）
- [ ] 估算为 L 或 XL（非 S 或 M）
- [ ] 风险说明中列出不确定性来源
- [ ] 建议在开始前澄清 AC 和创建 ADR
- [ ] 不写入任何文件

---

### 用例 3：无速度历史——使用保守默认值并注明

**夹具：**
- 故事文件结构完善，AC 清晰，ADR 已 Accepted
- 无历史冲刺数据（全新项目）

**输入：** `/estimate [故事文件]`

**预期行为：**
1. 技能分析故事内容（看起来是 M 级别的任务）
2. 技能尝试读取历史速度——无可用数据
3. 技能输出估算：M（使用保守默认值，因无速度历史）
4. 估算说明："No historical velocity data available.
   Using conservative industry defaults. Revise after first sprint."

**断言：**
- [ ] 检测到速度数据缺失
- [ ] 仍然产生估算（不因无数据而跳过）
- [ ] 说明中标注使用了保守默认值
- [ ] 建议在第一个冲刺结束后修订估算

---

### 用例 4：冲刺文件包含 4 个故事——各自估算 + 总计

**夹具：**
- `production/sprints/sprint-05/sprint-plan.md` 包含 4 个故事引用
- 各故事有不同的复杂度（S、M、M、L）

**输入：** `/estimate production/sprints/sprint-05/sprint-plan.md`

**预期行为：**
1. 技能读取冲刺计划并识别 4 个故事
2. 技能逐一分析并估算每个故事：
   - 故事 1：S（几小时）
   - 故事 2：M（1-2 天）
   - 故事 3：M（1-2 天）
   - 故事 4：L（3-5 天）
3. 技能计算总计：约 6-9 天（超出 5 天冲刺容量）
4. 技能报告容量风险："Total estimate (6-9 days) exceeds typical 5-day sprint capacity."

**断言：**
- [ ] 4 个故事各自获得估算
- [ ] 计算总工作量
- [ ] 识别容量风险（总计超出典型冲刺容量时）
- [ ] 不修改冲刺计划文件

---

### 用例 5：门控合规性——无门控；/sprint-plan 为推荐下一步

**夹具：**
- 故事文件存在

**输入：** `/estimate [故事文件]`

**预期行为：**
1. 技能完成完整估算
2. 未调用 director 门控
3. 输出建议 `/sprint-plan` 作为下一步

**断言：**
- [ ] 未调用任何 director 门控
- [ ] 建议 `/sprint-plan` 作为下一步
- [ ] 不写入任何文件

---

## 协议合规性

- [ ] 始终产生估算（不跳过）
- [ ] 估算理由引用具体复杂度因素
- [ ] 高不确定性时附风险说明
- [ ] 速度数据缺失时使用保守默认值并注明
- [ ] 不修改任何故事或冲刺文件
- [ ] 建议 `/sprint-plan` 将估算用于实际规划

---

## 覆盖说明

- XL 估算（跨越整个冲刺或需要拆分）会附有故事拆分建议，
  但拆分行为本身超出估算范围，由 `/sprint-plan` 处理。
- 估算校准（将估算与实际完成时间比较以提高精度）超出技能范围，
  由回顾技能处理。
- 基于代码复杂度（而非故事文件）的估算未进行测试；
  此处假定始终有故事文件作为输入。
