---
name: team-release
description: "编排发布团队：协调 release-manager、qa-lead、devops-engineer 和 producer，从发布候选版本执行到部署上线的完整流程。"
argument-hint: "[版本号 或 'next']"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, AskUserQuestion, TodoWrite
---
**参数检查：** 如果未提供版本号：
1. 读取 `production/session-state/active.md` 以及 `production/milestones/` 中最新的文件（如果存在），以推断目标版本。
2. 如果找到版本：报告"未提供版本参数——从里程碑数据推断为 [version]，继续执行。"然后通过 `AskUserQuestion` 确认："正在发布 [version]，是否正确？"
3. 如果无法找到版本：使用 `AskUserQuestion` 询问"应该发布哪个版本号？（例如 v1.0.0）"并等待用户输入后再继续。不要默认使用硬编码的版本字符串。

调用此技能时，请通过结构化流水线编排发布团队。

**决策节点：** 在每个阶段切换处，使用 `AskUserQuestion` 将子代理的方案以可选项形式呈现给用户。在对话中写出代理的完整分析，然后用简洁标签捕获决策。用户必须批准后才能进入下一阶段。

## 团队组成

- **release-manager** — 发布分支、版本管理、变更日志、部署
- **qa-lead** — 测试签收、回归套件、发布质量门控
- **devops-engineer** — 构建流水线、制品、部署自动化
- **security-engineer** — 发布前安全审计（若游戏有在线/多人或玩家数据功能则启用）
- **analytics-engineer** — 验证遥测事件正确触发及仪表板上线
- **community-manager** — 补丁说明、发布公告、面向玩家的通知
- **producer** — 上线/不上线决策、利益相关者沟通、排期

## 如何委派

使用 Task 工具将每位团队成员作为子代理启动：
- `subagent_type: release-manager` — 发布分支、版本管理、变更日志、部署
- `subagent_type: qa-lead` — 测试签收、回归套件、发布质量门控
- `subagent_type: devops-engineer` — 构建流水线、制品、部署自动化
- `subagent_type: security-engineer` — 在线/多人/数据功能的安全审计
- `subagent_type: analytics-engineer` — 遥测事件验证与仪表板就绪确认
- `subagent_type: community-manager` — 补丁说明与发布通信
- `subagent_type: producer` — 上线/不上线决策、利益相关者沟通
- `subagent_type: network-programmer` — 网络代码稳定性签收（若游戏有多人功能则启用）

始终在每个代理的提示中提供完整上下文（版本号、里程碑状态、已知问题）。在流水线允许的情况下并行启动独立代理（例如，阶段3的代理可以同时运行）。

## 流水线

### 阶段 1：发布规划

委派给 **producer**：
- 确认所有里程碑验收标准均已满足
- 识别本次发布中推迟的范围项
- 设定目标发布日期并向团队传达
- 产出：包含范围确认的发布授权

### 阶段 2：发布候选版本

委派给 **release-manager**：
- 从约定的提交切出发布分支
- 在所有相关文件中升级版本号
- 使用 `/release-checklist` 生成发布检查表
- 冻结分支——不允许功能变更，仅允许缺陷修复
- 产出：发布分支名称和检查表

### 阶段 3：质量门控（并行）

并行委派：
- **qa-lead**：执行完整回归测试套件。测试所有关键路径。验证无 S1/S2 缺陷。签收质量。
- **devops-engineer**：为所有目标平台构建发布制品。验证构建干净且可复现。在 CI 中运行自动化测试。
- **security-engineer** *（若游戏有在线功能、多人模式或玩家数据）*：进行发布前安全审计。审查认证、反作弊、数据隐私合规。签收安全状态。
- **network-programmer** *（若游戏有多人模式）*：签收网络代码稳定性。验证延迟补偿、重连处理以及负载下的带宽使用。

### 阶段 4：本地化、性能与分析

委派（如资源允许，可与阶段3并行）：
- 验证所有字符串已翻译（如有 **localization-lead** 则委派）
- 针对目标运行性能基准测试（如有 **performance-analyst** 则委派）
- **analytics-engineer**：验证所有遥测事件在发布构建上正确触发。确认仪表板正在接收数据。检查关键漏斗（引导、进度推进、如适用的货币化）已埋点。
- 产出：本地化、性能与分析签收

### 阶段 5：上线/不上线

委派给 **producer**：
- 收集以下人员的签收：qa-lead、release-manager、devops-engineer、security-engineer（如在阶段3启用）、network-programmer（如在阶段3启用）以及 technical-director
- 评估所有未解决问题——是否阻塞或可以发货？
- 作出上线/不上线决策
- 产出：包含理由的发布决策

**若 producer 宣布不上线（NO-GO）：**
- 立即呈现决策："PRODUCER: NO-GO — [理由，例如阶段3发现 S1 缺陷]。"
- 使用 `AskUserQuestion` 并提供选项：
  - 修复阻塞项并重新运行受影响阶段
  - 将发布推迟到更晚日期
  - 覆盖 NO-GO 并附文档化理由（用户必须提供书面理由）
- **完全跳过阶段6** — 不得进行打标签、部署到预发布、部署到生产，也不得启动 community-manager。
- 产出部分报告，汇总阶段1-5以及跳过（阶段6）的内容和原因。
- 结论：**BLOCKED** — 发布未部署。

### 阶段 6：部署（仅限上线时）

委派给 **release-manager** + **devops-engineer**：
- 在版本控制中为发布打标签
- 使用 `/changelog` 生成变更日志
- 部署到预发布环境进行最终冒烟测试
- 部署到生产环境
- 发布后监控 48 小时

同时委派给 **community-manager**（与部署并行）：
- 使用 `/patch-notes [version]` 完成补丁说明
- 准备发布公告（应用商店页面更新、社交媒体、社区帖子）
- 如有 S3+ 问题随版本发货，起草已知问题公告
- 产出：所有面向玩家的发布通信，在确认部署后发布

### 阶段 7：发布后

- **release-manager**：生成发布报告（已发货内容、推迟内容、指标）
- **producer**：更新里程碑跟踪，与利益相关者沟通
- **qa-lead**：监控新报告的缺陷是否有回归
- **community-manager**：发布所有面向玩家的通信，监控社区情绪
- **analytics-engineer**：确认线上仪表板健康；若任何关键事件缺失则告警
- 如发生问题，排期发布后回顾会议

## 错误恢复协议

如果任何通过 Task 启动的代理返回 BLOCKED、发生错误或无法完成：

1. **立即显示**：在继续依赖阶段之前向用户报告"[AgentName]: BLOCKED — [原因]"
2. **评估依赖关系**：检查被阻塞代理的输出是否是后续阶段所必需的。如果是，在没有用户输入的情况下不得越过该依赖节点继续推进。
3. **通过 AskUserQuestion 提供选项**：
   - 跳过此代理并在最终报告中记录缺口
   - 以更窄范围重试
   - 在此停止并先解决阻塞项
4. **始终产出部分报告** — 输出已完成的内容。不要因为一个代理阻塞就丢弃工作。

常见阻塞项：
- 输入文件缺失（故事未找到、GDD 缺失）→ 重定向到创建它的技能
- ADR 状态为 Proposed → 不要实现；先运行 `/architecture-decision`
- 范围过大 → 通过 `/create-stories` 拆分为两个故事
- ADR 和故事之间的指令冲突 → 显示冲突，不要猜测

## 文件写入协议

所有文件写入（发布检查表、变更日志、补丁说明、部署脚本）均委派给子代理和子技能。每个都执行"我可以写入 [path] 吗？"协议。此编排器不直接写入文件。

## 输出

涵盖以下内容的摘要报告：发布版本、范围、质量门控结果、上线/不上线决策、部署状态和监控计划。

结论：**COMPLETE** — 发布已执行并部署。
结论：**BLOCKED** — 发布已停止；上线/不上线为 NO 或存在无法解决的硬性阻塞项。

## 下一步

- 发布后监控仪表板 48 小时。
- 若发布过程中出现重大问题，运行 `/retrospective`。
- 成功部署后将 `production/stage.txt` 更新为 `Live`。
