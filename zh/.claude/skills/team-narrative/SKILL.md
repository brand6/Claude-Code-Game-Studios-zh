---
name: team-narrative
description: "编排叙事团队：协调 narrative-director、writer、world-builder 和 level-designer，创作连贯的故事内容、世界观传说和叙事驱动的关卡设计。"
argument-hint: "[narrative content description]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Task, AskUserQuestion, TodoWrite
---

如果未提供叙事内容描述，输出使用说明并退出，不启动任何 Agent，不使用 AskUserQuestion：
> 用法：`/team-narrative [叙事内容描述]` — 提供要创作的叙事内容（如 `final boss confrontation`、`merchant NPC intro dialogue`、`ancient temple lore`）。

当本 skill 以参数调用时，按结构化流水线编排叙事团队。

**决策节点：** 在每个阶段切换时，使用 `AskUserQuestion` 将子 Agent 的方案以可选项的形式呈现给用户。在对话中完整展示 Agent 的分析，然后以简洁标签捕捉决策。用户批准后才能进入下一阶段。

## 团队构成
- **narrative-director** — 叙事目的、剧情节拍、情感基调
- **writer** — 对话文字、世界观文字、道具描述、游戏内文本
- **world-builder** — 传说、派系背景、历史、世界规则
- **art-director** — 角色视觉设计、环境叙事、过场镜头基调
- **level-designer** — 环境叙事落地、叙事触发器
- **localization-lead** — 国际化合规检查、多语言字符限制验证

## 如何委派

使用 Task 工具将每个团队成员作为子 Agent 启动：
- `subagent_type: narrative-director` — 叙事目的与剧情节拍
- `subagent_type: writer` — 对话与游戏内文字创作
- `subagent_type: world-builder` — 传说条目与世界规则
- `subagent_type: art-director` — 角色视觉设计与过场镜头基调
- `subagent_type: level-designer` — 环境叙事落地
- `subagent_type: localization-lead` — i18n 合规审查

文件写入委派给子 Agent；编排者不直接写入叙事文档。

在每个 Agent 的提示中始终提供完整上下文（叙事内容描述、相关 GDD 路径、现有世界观文档引用）。

## 流水线

### 阶段 1：叙事方向（narrative-director）
委派给 **narrative-director**：
- 定义叙事目的：该内容服务于哪个整体故事目标？
- 明确具体的剧情节拍：玩家在此必须学到/感受到/决定什么？
- 设定情感基调和玩家情感弧线
- 识别该叙事依赖哪些已有世界观事实（派系、历史、角色背景）
- 明确该叙事不能违背哪些限制（世界观规则、已确定的剧情）
- 输出：叙事简报（目的、节拍、情感弧线、约束条件）

### 阶段 2：创作（并行）
并行委派：

**world-builder**（基于叙事简报）：
- 创作传说条目（地点、派系、历史事件）
- 定义玩家可在游戏世界中发现的世界规则与历史
- 建立该内容的派系存在感与历史背景
- 确保传说与现有世界规则和实体注册表一致

**writer**（基于叙事简报）：
- 创作对话文字
- 每行对话最多 120 个字符（本地化扩展预留）
- 使用字符串键标注每行（如 `NPC_MERCHANT_INTRO_001`）
- 完整标注说话者姓名和语气/动作标注（用于配音和动画）
- 针对本地化进行创作：避免文化特定的惯用语，保持措辞简洁
- 为每个关键段落提供简要的本地化说明，便于翻译人员理解语境

**art-director**（基于叙事简报）：
- 定义角色视觉设计（服装、姿态、面部表情）
- 规划环境叙事元素（道具、房间布置、视觉细节）
- 明确过场/对话场景的镜头基调（距离、角度、灯光情绪）

### 阶段 3：关卡整合（level-designer）
委派给 **level-designer**，携带阶段 2 的全部输出：
- 将叙事内容落地为关卡中的具体位置和触发器
- 放置环境叙事元素（art-director 规定的道具、布景）
- 配置叙事触发器（临近触发、互动触发、事件触发）
- 确保关卡流线支持叙事节拍的发现顺序

### 阶段 4：叙事连贯性审查（narrative-director）
**narrative-director** 审查阶段 2 和 3 的全部创作成果：
- 对话是否准确传达了预期的叙事目的和情感基调？
- 传说条目是否与现有世界规则一致？
- 关卡中的叙事触发顺序是否与预定的剧情节拍匹配？
- 是否存在角色声音/动机上的不连贯？
- 输出：连贯性审查报告，标注 APPROVED 项和 NEEDS REVISION 项

### 阶段 5：精修（并行）
并行委派：

**writer** 完成最终精修：
- 根据连贯性审查报告修改对话
- 验证所有行均在 120 字符限制内
- 确认所有字符串键已完整标注
- 验证本地化说明的准确性

**localization-lead** 进行 i18n 合规检查：
- 验证字符串键遵循项目本地化规范
- 检查对话行是否有扩展语言（德语/芬兰语）+30% 字符增量的空间
- 标记任何需要格外注意的文化特定内容
- 检查是否有硬编码的数字格式、日期格式或专有名词
- 输出：i18n 合规报告（CLEAR 或 ISSUES FOUND，附具体行号）

**world-builder** 将传说确认为正典级别：
- 将传说条目分类：CANONICAL（正典，整个团队均可使用）vs. PROVISIONAL（待定，仅限该内容使用）
- 将正典传说推送至 `design/registry/entities.yaml` 中的实体注册表
- 标记任何需要进一步确认才能提升为正典的传说

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

## 文件写入协议

编排者不直接写入叙事文档。每个子 Agent 写入其相应部分：
- **writer** → `design/narrative/[content-name]/dialogue.md`
- **world-builder** → `design/narrative/[content-name]/lore.md` 及 `design/registry/entities.yaml`（正典条目）
- **level-designer** → `design/levels/[level-name].md` 的叙事触发器部分
- **narrative-director** → `design/narrative/[content-name]/narrative-brief.md`

## Output

摘要报告，涵盖：叙事简报状态、已创建/更新的传说条目、已创作的对话行数、关卡叙事整合点、连贯性审查结果，以及所有未解决的矛盾。

Verdict: **COMPLETE** — 叙事内容已交付。

如果流水线因未解决的依赖项而中止（如传说矛盾或用户未解决的前置条件）：

Verdict: **BLOCKED** — [原因]

## Next Steps

- 对叙事文档运行 `/design-review` 进行一致性验证。
- 对话定稿后，运行 `/localize extract` 提取新字符串以供翻译。
- 运行 `/dev-story` 在引擎中实现对话触发器和叙事事件。
