---
name: team-polish
description: "编排打磨团队：协调 performance-analyst、technical-artist、sound-designer 和 qa-tester，将一个功能或区域优化并打磨至发布质量。"
argument-hint: "[feature or area to polish]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, AskUserQuestion, TodoWrite
---

如果未提供参数，输出使用说明并退出，不启动任何 Agent，不使用 AskUserQuestion：
> 用法：`/team-polish [功能或区域]` — 指定需要打磨的功能或区域（如 `combat system`、`main menu`、`forest level`、`inventory screen`）。

当本 skill 以参数调用时，按结构化流水线编排打磨团队。

**决策节点：** 在每个阶段切换时，使用 `AskUserQuestion` 将子 Agent 的方案以可选项的形式呈现给用户。在对话中完整展示 Agent 的分析，然后以简洁标签捕捉决策。用户批准后才能进入下一阶段。

## 团队构成
- **performance-analyst** — 性能剖析、瓶颈识别、优化优先级
- **engine-programmer** — 引擎层面的瓶颈修复（仅在 performance-analyst 识别出低层根因时调用）
- **technical-artist** — 视觉特效、着色器、视觉反馈打磨
- **sound-designer** — 音频完整性、混音、环境氛围
- **tools-programmer** — 内容管线问题修复（仅在发现内容管线导致的问题时调用）
- **qa-tester** — 边缘情况、浸泡测试、压力测试、回归测试

## 如何委派

使用 Task 工具将每个团队成员作为子 Agent 启动：
- `subagent_type: performance-analyst` — 性能剖析与优化方向
- `subagent_type: engine-programmer` — 引擎层面瓶颈修复（按需调用）
- `subagent_type: technical-artist` — VFX、着色器与视觉打磨
- `subagent_type: sound-designer` — 音频完整性与混音打磨
- `subagent_type: tools-programmer` — 内容管线问题修复（按需调用）
- `subagent_type: qa-tester` — 完整测试与最终验证

文件写入委派给子 Agent；编排者不直接写入代码或配置文件。

在每个 Agent 的提示中始终提供完整上下文（功能描述、相关源文件路径、已知问题）。

## 流水线

### 阶段 1：评估（performance-analyst）
委派给 **performance-analyst**，执行 `/perf-profile`（或等效的引擎内置剖析工具）：
- 确定目标平台的性能预算（帧时间、内存、GPU 预算）
- 剖析目标功能/区域
- 将问题按严重程度排序：
  - 预算超标（发布阻断）
  - 临近预算（需要优先优化）
  - 有优化空间（如有时间可做）
- 识别根本原因：是引擎层面问题（需要 engine-programmer）、资产问题（需要 technical-artist）还是内容管线问题（需要 tools-programmer）？
- 输出：性能评估报告，含优先级排序、根因分析及推荐操作

### 阶段 2：优化（performance-analyst，如需 engine-programmer 则并行）
委派给 **performance-analyst** 处理资产级和配置级优化项：
- 实施推荐的优化方案（LOD 调整、遮挡设置、批处理、资产压缩）
- 处理所有发布阻断项
- 验证优化后的性能指标

**仅在** performance-analyst 识别出以下原因时，额外启动 **engine-programmer**：
- 渲染管线低效
- 物理系统瓶颈
- 内存管理问题
- 引擎内核/框架层面的根因
- **不在此情形下启动**：纯资产质量问题、内容管线缺陷、脚本逻辑问题（由其他 Agent 处理）

**仅在** performance-analyst 识别出内容管线导致的资产问题时，额外启动 **tools-programmer**：
- 资产导入流水线产生的低效问题
- 需要管线修复才能正确生成的 LOD/Mipmap
- 管线层面的批处理优化需求

### 阶段 3：视觉打磨（与阶段 2 并行）
委派给 **technical-artist**（与阶段 2 同步进行）：
- 审查并完善视觉特效（粒子、着色器特效）
- 确保视觉反馈与游戏手感匹配（打击感、移动感、UI 响应）
- 优化着色器以符合性能预算（已从阶段 1 获知预算）
- 完善材质和灯光设置
- 输出：视觉打磨完成报告，包含变更内容和剩余的未解视觉问题

### 阶段 4：音频打磨（与阶段 2 并行）
委派给 **sound-designer**（与阶段 2 同步进行）：
- 审查音频事件覆盖的完整性（是否所有游戏动作都有音效？）
- 验证混音平衡（音量等级、总线路由、闪避规则）
- 完善环境氛围与空间音效
- 检查音频是否存在破音、静音、时机偏差等问题
- 输出：音频打磨完成报告，包含变更内容和剩余问题

### 阶段 5：强化测试（qa-tester）
委派给 **qa-tester**，进行全面测试：
- 针对所有已识别边缘情况编写并执行测试用例
- 运行浸泡测试协议：长时间游戏检测内存泄漏、帧率抖动、状态累积
- 压力测试（同时触发最多邂逅/粒子/音频）
- 回归测试：确认修复未引入新问题
- 在目标平台执行验收测试
- 输出：完整测试报告，包含通过/失败状态、剩余 Bug 和回归验证

### 阶段 6：签署确认
收集并整合所有团队报告，评估发布质量状态：

**检查标准：**
- 所有性能预算超标问题已解决？
- 阶段 5 测试报告无严重或阻断级别的 Bug？
- 视觉和音频打磨完成，无明显缺陷？
- 浸泡测试未发现内存泄漏或稳定性问题？

## Error Recovery Protocol

如果任何通过 Task 启动的 Agent 返回 BLOCKED、报错或无法完成：

1. **立即上报**：在继续依赖阶段之前，向用户报告"[AgentName]: BLOCKED — [原因]"
2. **评估依赖关系**：检查被阻塞 Agent 的输出是否为后续阶段所必需。如果是，在没有用户输入的情况下不要越过该依赖点继续。
3. **通过 AskUserQuestion 提供选项**：
   - 跳过此 Agent 并在最终报告中记录缺口
   - 以更小范围重试
   - 在此停止，先解决阻塞项
4. **始终生成部分报告** — 输出所有已完成的工作。不要因为一个 Agent 被阻塞就丢弃工作成果。

常见阻塞原因：
- 输入文件缺失（Story 未找到、GDD 不存在）→ 重定向到创建该文件的 skill
- ADR 状态为 Proposed → 不实现；先运行 `/architecture-decision`
- 范围过大 → 通过 `/create-stories` 拆分为两个 Story
- ADR 与 Story 之间存在冲突指令 → 浮现冲突，不猜测

## File Write Protocol

所有文件写入（性能报告、测试结果、证据文档）均委派给通过 Task 启动的子 Agent。
每个子 Agent 执行"我可以写入 [path] 吗？"协议。此编排者不直接写入文件。

## Output

摘要报告，涵盖：优化前后性能指标对比、视觉打磨变更、音频打磨变更、测试结果，以及发布准备评估。

## Next Steps

- 如果 READY FOR RELEASE：运行 `/release-checklist` 进行最终发布前验证。
- 如果 NEEDS MORE WORK：在 `/sprint-plan update` 中安排剩余问题，修复后重新运行 `/team-polish`。
- 运行 `/gate-check` 在移交发布前进行正式阶段关口验证。
