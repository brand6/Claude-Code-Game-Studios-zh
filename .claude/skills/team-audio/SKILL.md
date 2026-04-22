---
name: team-audio
description: "编排音频团队：audio-director + sound-designer + technical-artist + gameplay-programmer，完成从方向确定到实现落地的完整音频流水线。"
argument-hint: "[feature or area to design audio for]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, AskUserQuestion, TodoWrite
---

如果未提供参数，输出使用说明并退出，不启动任何 Agent：
> 用法：`/team-audio [功能或区域]` — 指定需要设计音频的功能或区域（如 `combat`、`main menu`、`forest biome`、`boss encounter`）。此处不使用 `AskUserQuestion`，直接输出说明。

当本 skill 以参数调用时，按结构化流水线编排音频团队。

**决策节点：** 在每个步骤切换时，使用 `AskUserQuestion` 将子 Agent 的方案以可选项的形式呈现给用户。在对话中完整展示 Agent 的分析，然后以简洁标签捕捉决策。用户批准后才能进入下一步。

1. **读取参数**，确定目标功能或区域（如 `combat`、`main menu`、`forest biome`、`boss encounter`）。

2. **收集上下文**：
   - 读取 `design/gdd/` 中与该功能相关的设计文档
   - 如果存在，读取音频圣经 `design/gdd/sound-bible.md`
   - 读取 `assets/audio/` 中现有的音频资产列表
   - 读取该区域现有的音效设计文档

## 如何委派

使用 Task 工具将每个团队成员作为子 Agent 启动：
- `subagent_type: audio-director` — 音效身份、情感基调、音频调色板
- `subagent_type: sound-designer` — SFX 规格、音频事件、混音分组
- `subagent_type: technical-artist` — 音频中间件、总线结构、内存预算
- `subagent_type: [primary engine specialist]` — 验证该引擎的音频集成方案
- `subagent_type: gameplay-programmer` — 音频管理器、游戏触发器、自适应音乐

在每个 Agent 的提示中始终提供完整上下文（功能描述、现有音频资产、设计文档引用）。

3. **按顺序编排音频团队**：

### 步骤 1：音频方向（audio-director）
启动 `audio-director` Agent，任务：
- 定义该功能/区域的音效身份
- 指定情感基调和音频调色板
- 设定音乐方向（自适应层、音干、过渡）
- 定义音频优先级和混音目标
- 建立自适应音频规则（战斗强度、探索、紧张感）

### 步骤 2：音效设计与音频无障碍（并行）
启动 `sound-designer` Agent，任务：
- 为每个音频事件创建详细的 SFX 规格
- 定义音效类别（环境音、UI、游戏内容、音乐、对话）
- 指定每个音效的参数（音量范围、音调变化、衰减）
- 规划含触发条件的音频事件列表
- 定义混音分组和闪避规则

并行启动 `accessibility-specialist` Agent，任务：
- 识别承载关键游戏信息的音频事件（受到伤害、附近有敌人、目标完成），并为听力障碍玩家提供视觉替代方案
- 指定字幕要求：哪些音频事件需要说明文字、文字格式、屏幕显示时长
- 确认没有任何游戏状态仅通过音频传达（所有内容必须有视觉备选）
- 审查音频事件列表，检查是否有可能对听觉敏感玩家造成问题的事件（高频警报、突然的大音量事件）
- 输出：音频无障碍需求列表，整合到音频事件规格中

### 步骤 3：技术实现（并行）
启动 `technical-artist` Agent，任务：
- 设计音频中间件集成方案（Wwise/FMOD/原生）
- 定义音频总线结构和路由
- 指定各平台音频资产的内存预算
- 规划流式播放与预加载资产策略
- 设计任何音频响应视觉效果

并行启动**主引擎专家**（来自 `.claude/docs/technical-preferences.md` 引擎专家部分），验证集成方案：
- 提议的音频中间件集成方案对该引擎是否符合惯例？（如 Godot 内置 AudioStreamPlayer 与 FMOD、Unity Audio Mixer 与 Wwise、Unreal MetaSounds 与 FMOD 的选择）
- 是否有应使用的引擎专项音频节点/组件模式？
- 当前固定引擎版本中影响集成方案的已知音频系统变更？
- 输出：引擎音频集成注意事项，与 technical-artist 方案合并

如果未配置引擎，跳过专家启动。

### 步骤 4：代码集成（gameplay-programmer）
启动 `gameplay-programmer` Agent，任务：
- 实现音频管理器系统或审查现有系统
- 将音频事件连接到游戏触发器
- 实现自适应音乐系统（如已指定）
- 设置音频遮挡/混响区域
- 为音频事件触发器编写单元测试

4. **汇编音频设计文档**，整合所有团队输出。

5. **保存到** `design/gdd/audio-[功能].md`。

6. **输出摘要**，包含：音频事件数量、预计资产数量、实现任务，以及团队成员之间的未解问题。

结论：**COMPLETE** — 音频设计文档已生成，团队流水线已完成。

如果流水线因未解决的依赖项而中止（如关键无障碍缺口或用户未能解决的缺失 GDD）：

结论：**BLOCKED** — [原因]
## File Write Protocol

所有文件写入（音频设计文档、音效规格、实现文件）均委派给通过 Task 启动的子 Agent。
每个子 Agent 执行"我可以写入 [path] 吗？"协议。此编排者不直接写入文件。

## Next Steps

- 在实现开始前，与 audio-director 审查音频设计文档。
- 使用 `/dev-story` 在设计获批后实现音频管理器和事件系统。
- 音频资产创建后，运行 `/asset-audit` 验证命名和格式合规性。

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