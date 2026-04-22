# Skill Test Spec: /team-live-ops

## Skill 概述

编排七阶段赛季/活动规划流水线：1. 赛季概念（live-ops-designer）→
2. 叙事主题（narrative-director + writer）→ 3. 经济设计（economy-designer）和
4. 分析规格（analytics-engineer）并行 → 5. 社区策略（community-manager）→
6. 实现规划（live-ops-designer + gameplay-programmer）→ 7. 伦理审查（live-ops-designer）。
阶段 7 参考 `design/live-ops/ethics-policy.md`（若存在）。
输出保存至 `design/live-ops/seasons/`。
下一步：`/design-review`、`/sprint-plan`、`/team-release`。

---

## 静态断言（结构性）

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 明确包含七个阶段
- [ ] 阶段 3 和阶段 4 明确并行派生
- [ ] 阶段 7 包含伦理审查并引用 `design/live-ops/ethics-policy.md`
- [ ] 包含裁决关键字：COMPLETE、BLOCKED
- [ ] 存在文件写入协议；编排者不直接写入文件
- [ ] 子 agent 在任何写入之前强制执行"May I write to [path]?"
- [ ] 存在错误恢复协议
- [ ] 步骤过渡前使用 `AskUserQuestion`
- [ ] 输出路径使用 `design/live-ops/seasons/` 目录
- [ ] 末尾包含下一步交接：`/design-review`、`/sprint-plan`、`/team-release`

---

## 测试用例

### 用例 1：正常路径——七个阶段全部完成，裁决 COMPLETE

**测试夹具：**
- 现有赛季数据位于 `design/live-ops/`
- 伦理政策位于 `design/live-ops/ethics-policy.md`
- 赛季主题：`winter-festival`
- 所有 agent 成功完成任务

**输入：** `/team-live-ops winter-festival`

**预期行为：**
1. 上下文收集：读取现有赛季数据、伦理政策、游戏经济数据
2. 阶段 1：派生 live-ops-designer 定义赛季概念（主题、持续时间、核心活动循环、参与目标）
3. `AskUserQuestion` 批准赛季概念后进行阶段 2
4. 阶段 2：并行派生 narrative-director（叙事弧线、赛季传说）和 writer（活动描述文本、公告草稿）
5. `AskUserQuestion` 批准叙事主题后进行阶段 3+4
6. 阶段 3+4：同时派生 economy-designer（奖励结构、进度曲线、货币收支）和 analytics-engineer（KPI 定义、漏斗分析计划、A/B 测试框架）
7. `AskUserQuestion` 批准经济和分析规格后进行阶段 5
8. 阶段 5：派生 community-manager（公告计划、社区活动、反馈收集策略）
9. `AskUserQuestion` 批准社区策略后进行阶段 6
10. 阶段 6：派生 live-ops-designer 和 gameplay-programmer 制定实现计划
11. `AskUserQuestion` 批准实现计划后进行阶段 7
12. 阶段 7：live-ops-designer 参考 ethics-policy.md 进行伦理审查（掠夺性机制检查、公平性评估、玩家福祉考量）
13. 伦理审查通过；子 agent 询问写入权限后输出保存至 `design/live-ops/seasons/winter-festival.md`
14. 裁决：COMPLETE；下一步：`/design-review`、`/sprint-plan`、`/team-release`

**断言：**
- [ ] 阶段 3 和阶段 4 的 Task 调用同时发出（并行）
- [ ] 每次阶段过渡前使用 `AskUserQuestion`
- [ ] 阶段 7 明确引用 `design/live-ops/ethics-policy.md`
- [ ] 输出保存至 `design/live-ops/seasons/winter-festival.md`
- [ ] 编排者不直接写入任何文件
- [ ] 裁决为 COMPLETE
- [ ] 下一步引用 `/design-review`、`/sprint-plan`、`/team-release`

---

### 用例 2：伦理违规——阶段 7 发现问题，阻塞完成

**测试夹具：**
- 阶段 1–6 已成功完成
- 阶段 7 伦理审查：economy-designer 设计的经济结构包含限时稀有道具（每天只可购买一次，24 小时后消失），ethics-policy.md 明确禁止"创造虚假稀缺性的限时购买压力机制"

**输入：** `/team-live-ops winter-festival`（阶段 7 场景）

**预期行为：**
1. 阶段 7 中 live-ops-designer 读取 ethics-policy.md
2. 发现冲突：限时道具机制违反伦理政策中的"禁止虚假稀缺压力机制"条款
3. 编排者立即报告伦理违规："`winter-festival` 的限时稀有道具设计违反了 ethics-policy.md 第 3.2 条——这是一个阻塞赛季发布的 BLOCKING 伦理问题。"
4. `AskUserQuestion` 呈现选项：
   - 将限时稀有道具改为持久可获取物品并继续
   - 完全移除该机制并继续
   - 在此停止，重新设计经济结构（推荐）
5. 在用户解决伦理问题之前，输出文档不被写入

**断言：**
- [ ] 伦理违规在报告中标记为 BLOCKING
- [ ] 具体违规条款（ethics-policy.md 的具体内容）被明确引用
- [ ] 输出文档在伦理问题解决之前不被写入
- [ ] `AskUserQuestion` 提供至少一个解决路径
- [ ] 裁决为 BLOCKED（非 COMPLETE）

---

### 用例 3：无参数——使用指导

**测试夹具：**
- 任何项目状态

**输入：** `/team-live-ops`（无参数）

**预期行为：**
1. Skill 检测到未提供赛季/活动名称
2. 输出使用指导，包含正确调用格式和示例（例如 `winter-festival`、`summer-event`、`season-3`）
3. 不派生任何 agent

**断言：**
- [ ] 无参数时不派生任何 agent
- [ ] 使用信息包含带参数示例的正确格式
- [ ] 不使用 `AskUserQuestion`

---

### 用例 4：阶段 3+4 并行验证——经济和分析 agent 确实同时发出

**测试夹具：**
- 阶段 1 和阶段 2 已完成批准
- 等待阶段 3+4 执行
- economy-designer 和 analytics-engineer 均可用

**输入：** `/team-live-ops spring-event`（阶段 3+4 焦点）

**预期行为：**
1. 阶段 3+4 启动时：编排者同时发出 economy-designer 和 analytics-engineer 的 Task 调用
2. 不等待任何一个 agent 的结果才派生另一个
3. 两个 agent 的结果都收集后，`AskUserQuestion` 呈现合并输出

**断言：**
- [ ] economy-designer 和 analytics-engineer 的 Task 调用同时发出
- [ ] 两个 agent 的输出均包含在阶段 3+4 摘要中
- [ ] 没有顺序执行（一个 agent 不等待另一个的结果）

---

### 用例 5：缺少伦理政策——注明但继续

**测试夹具：**
- `design/live-ops/ethics-policy.md` 不存在
- 所有其他上下文文件存在
- 赛季设计不包含明显违规内容

**输入：** `/team-live-ops anniversary-event`

**预期行为：**
1. 上下文收集：检查 `design/live-ops/ethics-policy.md`——未找到
2. 编排者在对话中注明："注意：未找到 `design/live-ops/ethics-policy.md`——阶段 7 伦理审查将基于通用直播运营最佳实践进行，而非项目特定政策。强烈建议创建伦理政策文档。"
3. 阶段 7 仍进行，但 live-ops-designer 基于行业通用标准（而非项目特定政策）进行审查
4. 最终文档中记录伦理政策缺失并推荐创建
5. 裁决：COMPLETE（政策缺失是可注明的缺口，不是阻塞器）

**断言：**
- [ ] 缺少伦理政策在对话中明确注明——不被静默忽略
- [ ] 因缺少伦理政策，流水线不会停止
- [ ] 阶段 7 仍进行，基于通用最佳实践
- [ ] 最终文档推荐创建伦理政策
- [ ] 裁决为 COMPLETE

---

## 协议合规性

- [ ] 上下文收集（现有赛季数据、伦理政策、经济数据）在派生任何 agent 之前运行
- [ ] 每次阶段过渡前使用 `AskUserQuestion`
- [ ] 阶段 3 和阶段 4 并行：Task 调用同时发出
- [ ] 编排者不直接写入任何文件
- [ ] 子 agent 在任何写入之前强制执行"May I write to [path]?"
- [ ] 伦理违规会阻塞发布并明确引用政策条款
- [ ] 缺少伦理政策被注明但不会停止流水线
- [ ] 输出路径为 `design/live-ops/seasons/[name].md`
- [ ] 裁决为 COMPLETE 或 BLOCKED
- [ ] 末尾包含下一步交接：`/design-review`、`/sprint-plan`、`/team-release`

---

## 覆盖率说明

- 阶段 3+4 中可能出现 economy-designer 的经济结构与 analytics-engineer 的
  KPI 目标冲突的情况——此类跨 agent 冲突的仲裁协议未独立测试。
- 伦理政策的版本控制（不同版本赛季可能适用不同政策版本）超出当前
  spec 范围。
