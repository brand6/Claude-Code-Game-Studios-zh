---
name: team-live-ops
description: "编排运营团队，用于上线后的内容规划：协调 live-ops-designer、economy-designer、analytics-engineer、community-manager、writer 和 narrative-director，设计和规划一个赛季、活动或直播内容更新。"
argument-hint: "[season name or event description]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, AskUserQuestion, TodoWrite
---

**参数检查：** 如果未提供赛季名称或活动描述，输出：
> "用法：`/team-live-ops [赛季名称或活动描述]` — 提供要策划的内容（如 `Season 2: Frostfall`、`Halloween event`、`patch-1.3 content update`）。"
然后立即停止，不启动任何子 Agent，不读取任何文件。

当本 skill 以有效参数调用时，按结构化流水线编排运营团队。

**决策节点：** 在每个阶段切换时，使用 `AskUserQuestion` 将子 Agent 的方案以可选项的形式呈现给用户。在对话中完整展示 Agent 的分析，然后以简洁标签捕捉决策。用户批准后才能进入下一阶段。

## 团队构成
- **live-ops-designer** — 赛季设计、留存机制、内容节奏
- **economy-designer** — 赛季经济、进度奖励、货币化设计
- **analytics-engineer** — KPI 框架、成功指标、A/B 测试计划
- **community-manager** — 玩家沟通、公告文案、社区预热
- **narrative-director** — 赛季叙事主题与世界观延续性
- **writer** — 活动对话、季节性文字、公告文本

## 如何委派

使用 Task 工具将每个团队成员作为子 Agent 启动：
- `subagent_type: live-ops-designer` — 赛季范围与留存机制
- `subagent_type: economy-designer` — 经济设计与进度奖励
- `subagent_type: analytics-engineer` — KPI 框架与分析计划
- `subagent_type: community-manager` — 玩家沟通与公告文案
- `subagent_type: narrative-director` — 叙事主题与世界观延续
- `subagent_type: writer` — 活动文字内容

在每个 Agent 的提示中始终提供完整上下文（赛季名称、游戏当前状态、相关 GDD 引用）。

## 流水线

### 阶段 1：赛季范围设定（live-ops-designer）
委派给 **live-ops-designer**：
- 定义赛季范围：持续时长、新内容量、活动日历
- 设计核心留存机制（赛季通行证、每日任务、有限时间活动）
- 确定赛季内容来源（复用现有内容 vs 新制作内容）
- 定义赛季开始/中期/结束三阶段节奏
- 输出：赛季设计文档（范围、日历、留存钩子）

### 阶段 2：叙事主题（narrative-director）
委派给 **narrative-director**：
- 为赛季或活动建立叙事主题
- 将新内容与现有世界观和剧情弧线相连
- 规划叙事揭露节拍（赛季开始、中期揭晓、结局）
- 确保叙事主题不与已定稿的世界观相矛盾
- 输出：叙事主题简报，包含关键剧情节拍和世界观引用

### 阶段 3：经济设计（与阶段 2 并行）
委派给 **economy-designer**：
- 设计赛季进度轨迹（XP 曲线、里程碑、解锁节奏）
- 规划货币化元素（赛季通行证定价、限定道具）
- 确保赛季经济不破坏核心游戏经济平衡
- 输出：赛季经济设计（进度曲线、奖励清单、货币平衡影响）

### 阶段 4：分析计划（与阶段 3 并行）
委派给 **analytics-engineer**：
- 定义赛季成功的 KPI（日活、留存率、赛季通行证转化、活动参与）
- 设计活动内容的 A/B 测试框架
- 规划分析埋点（活动触发、里程碑达成、通行证购买漏斗）
- 输出：分析计划文档（KPI、测试框架、埋点清单）

### 阶段 5：内容写作（并行）
并行委派：
- **narrative-director**：赛季故事内容（过场叙事、世界事件描述、剧情日志条目）
- **writer**：活动文字内容（限时任务文本、季节性道具描述、赛季通行证解锁提示、UI 内容文案）

### 阶段 6：玩家沟通
委派给 **community-manager**：
- 起草赛季/活动发布公告（上线 + 提前预热）
- 制定发布后的社区沟通策略（FAQ、Bug 致歉流程、社区参与话题）
- 规划内容创作者/媒体宣传简报
- 确保沟通语调与赛季叙事主题保持一致
- 输出：玩家沟通文档（发布文案、沟通节奏、FAQ 模板）

### 阶段 7：审查与签署确认

**伦理审查（合规检查，必须执行）：**
在声明 COMPLETE 之前，检查 `design/live-ops/ethics-policy.md`：
- 如果文件**存在**：对照道德政策核查赛季内容（通行证激励机制、计时购买压力、稀缺性设计、面向未成年玩家的机制）
  - 如果发现违规：结论为 **BLOCKED** — 不能声明 COMPLETE。
    报告违规问题及其所在文档位置，让用户决定如何修改设计。
    在违规问题解决前不允许声明 COMPLETE。
  - 如果没有违规：注明"伦理审查通过。"
- 如果文件**不存在**：以醒目提示标注：
  > "⚠ 伦理审查已跳过 — `design/live-ops/ethics-policy.md` 不存在。强烈建议在正式发布前完善并执行此政策。"
  然后继续完成签署确认。

**最终审查：**
- 收集所有团队成员的输出
- 检查叙事主题、经济设计与内容写作之间的一致性
- 核实 KPI 与活动设计目标相对应
- 确认玩家沟通文案能够准确反映实际内容

## 输出文件

- `design/live-ops/seasons/S[N]_[名称].md` — 主赛季设计文档
- `design/live-ops/seasons/S[N]_[名称]_analytics.md` — 分析计划
- `design/live-ops/seasons/S[N]_[名称]_comms.md` — 玩家沟通文档

## Error Recovery Protocol

如果任何通过 Task 启动的 Agent 返回 BLOCKED、报错或无法完成：

1. **立即上报**：在继续依赖阶段之前，向用户报告"[AgentName]: BLOCKED — [原因]"
2. **评估依赖关系**：检查被阻塞 Agent 的输出是否为后续阶段所必需。如果是，在没有用户输入的情况下不要越过该依赖点继续。
3. **通过 AskUserQuestion 提供选项**：
   - 跳过此 Agent 并在最终报告中记录缺口
   - 以更小范围重试
   - 在此停止，先解决阻塞项
4. **始终生成部分报告** — 输出所有已完成的工作。不要因为一个 Agent 被阻塞就丢弃工作成果。

如果 BLOCKED 状态无法解决，以 Verdict: **BLOCKED** 结束，而非 COMPLETE。

## File Write Protocol

所有文件写入（赛季设计文档、分析计划、玩家沟通日历）均委派给通过 Task 启动的子 Agent。
每个子 Agent 执行"我可以写入 [path] 吗？"协议。此编排者不直接写入文件。

## Output

摘要，涵盖：赛季主题与范围、经济设计亮点、成功指标、内容清单、玩家沟通计划，以及生产前需要用户决策的所有未决事项。

Verdict: **COMPLETE** — 赛季计划已生成并移交生产。

## Next Steps

- 对赛季设计文档运行 `/design-review` 进行一致性验证。
- 运行 `/sprint-plan` 为赛季安排内容创作工作。
- 赛季内容准备好部署时，运行 `/team-release`。
