# Agent 协调规则

1. **纵向委托**：领导层 Agent 向部门负责人委托，部门负责人再向专员委托。
   复杂决策不得越级。
2. **横向咨询**：同层 Agent 可互相咨询，但不得在自身领域之外做出约束性决策。
3. **冲突解决**：两个 Agent 意见不一致时，向共同上级升级。若无共同上级，
   设计冲突升级至 `creative-director`，技术冲突升级至 `technical-director`。
4. **变更传播**：当一项设计变更影响多个领域时，由 `producer` Agent 协调传播。
5. **禁止单边跨域修改**：Agent 未经明确授权，不得修改其指定目录以外的文件。

## 模型层级分配

Skills 与 Agent 根据任务复杂度分配到对应模型层级：

| 层级 | 模型 | 适用场景 |
|------|-------|-------------|
| **Haiku** | `claude-haiku-4-5-20251001` | 只读状态检查、格式化、简单查询——无需创意判断 |
| **Sonnet** | `claude-sonnet-4-6` | 实现、设计编写、单系统分析——大多数工作的默认选择 |
| **Opus** | `claude-opus-4-6` | 多文档综合、高风险阶段门禁裁定、跨系统整体评审 |

使用 `model: haiku` 的 Skills：`/help`、`/sprint-status`、`/story-readiness`、`/scope-check`、
`/project-stage-detect`、`/changelog`、`/patch-notes`、`/onboard`

使用 `model: opus` 的 Skills：`/review-all-gdds`、`/architecture-review`、`/gate-check`

其余 Skills 默认使用 Sonnet。创建新 Skill 时：只读取并格式化则分配 Haiku；
需综合 5 个以上文档且输出高风险则分配 Opus；否则不设置（默认 Sonnet）。

## Subagents 与 Agent 团队

本项目使用两种不同的多 Agent 模式：

### Subagents（当前模式，始终可用）

在单个 Claude Code 会话内通过 `Task` 生成。被所有 `team-*` Skills 及编排 Skills 使用。
Subagent 共享会话的权限上下文，在会话内按顺序或并行运行，并将结果返回给父级。

**何时并行生成**：若两个 subagent 的输入相互独立（均不需要对方的输出才能开始），
则同时发出两个 Task 调用，而非等待。例如：`/review-all-gdds` 的阶段 1（一致性）
与阶段 2（设计理论）相互独立——同时生成两者。

### Agent 团队（实验性——需手动开启）

多个独立的 Claude Code *会话*同时运行，通过共享任务列表协调。
每个会话有独立的上下文窗口和 token 预算。
需要设置环境变量 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`。

**适合使用 Agent 团队的场景**：
- 工作跨越多个不会触及同一文件的子系统
- 每个工作流预计耗时 >30 分钟，且能从真正的并行中获益
- 高级 Agent（technical-director、producer）需要协调 3 个以上专员会话同时处理不同 epic

**不适合使用 Agent 团队的场景**：
- 一个会话的输出是另一个的输入（改用顺序 subagent）
- 任务在单个会话上下文内即可完成（改用 subagent）
- 成本敏感——每位团队成员独立消耗 tokens

**当前状态**：本项目尚未使用。首次采用时在此处记录。

## 并行任务协议

当编排 Skill 生成多个独立 Agent 时：

1. 在等待任何结果之前，先发出所有独立的 Task 调用
2. 在进入下一个依赖阶段之前，收集所有结果
3. 若任何 Agent 处于 BLOCKED 状态，立即上报——不得悄无声息地跳过
4. 若部分 Agent 完成而其他阻塞，始终产出部分报告
