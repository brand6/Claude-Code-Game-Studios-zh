---
name: team-level
description: "编排关卡设计团队：level-designer + narrative-director + world-builder + art-director + systems-designer + qa-tester，完整完成一个区域/关卡的创建。"
argument-hint: "[level name or area to design]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, AskUserQuestion, TodoWrite
---

如果未提供参数，输出使用说明并退出，不启动任何 Agent：
> 用法：`/team-level [关卡名称或区域]` — 指定要设计的关卡或区域（如 `forest-clearing-01`、`tavern-interior`、`boss-arena-ice`）。此处不使用 `AskUserQuestion`，直接输出说明。

当本 skill 以参数调用时，按结构化流水线编排关卡团队。

**决策节点：** 在每个步骤切换时，使用 `AskUserQuestion` 将子 Agent 的方案以可选项的形式呈现给用户。在对话中完整展示 Agent 的分析，然后以简洁标签捕捉决策。用户批准后才能进入下一步。

## 团队构成
- **narrative-director** — 叙事目的、剧情节拍、情感基调
- **world-builder** — 世界观背景、派系存在感、历史痕迹、生态
- **art-director** — 视觉目标、色彩方案、风格参考、灯光情绪
- **level-designer** — 空间布局、流线、邂逅位置、谜题结构
- **systems-designer** — 敌人组合、战利品列表、难度调优
- **accessibility-specialist** — 关卡无障碍审查
- **qa-tester** — 测试用例、完成度检查

## 如何委派

使用 Task 工具将每个团队成员作为子 Agent 启动：
- `subagent_type: narrative-director` — 叙事目的与剧情节拍
- `subagent_type: world-builder` — 世界观背景与历史痕迹
- `subagent_type: art-director` — 视觉目标与色彩方案
- `subagent_type: level-designer` — 空间布局与流线
- `subagent_type: systems-designer` — 邂逅设计与系统整合
- `subagent_type: accessibility-specialist` — 关卡无障碍审查
- `subagent_type: qa-tester` — 测试用例与完成度检查

文件写入委派给子 Agent；编排者不直接写入关卡文档。

在每个 Agent 的提示中始终提供完整上下文（关卡名称、已有文档路径、相邻区域引用）。

## 关键约束：步骤 1 → 步骤 2 数据流

**`art-director` 在步骤 1 的输出是步骤 2 的输入，而非步骤 2 的输出。**
`level-designer` 在生成布局之前，必须已收到 `art-director` 对以下内容的具体描述：
- 视觉优先区域与路径（光源点、植被覆盖、地标）
- 色彩方案与灯光情绪
- 影响布局的建筑/自然形态

这避免了"先布局，后视觉匹配"的反模式。

## 相邻区域依赖检查

在进入步骤 2 之前，检查关卡文档是否引用了任何邻近区域（出入口、连通路径）。

对于每个引用区域：
- 使用 Glob 在 `design/levels/` 中查找对应的 `.md` 文件
- 如果该区域的关卡文档**存在**：读取其出入口定义，确保衔接一致性
- 如果该区域的关卡文档**不存在**，通过 `AskUserQuestion` 询问用户：
  - 选项 a：在本关卡文档中将该区域标记为"UNRESOLVED（待关联区域文档创建后填写）"
  - 选项 b：先运行 `/team-level [相邻区域名称]`，再继续

## 流水线

### 步骤 1：叙事、世界观与视觉方向（并行）
并行委派：
- **narrative-director**：
  - 该关卡服务于哪个剧情节拍？
  - 玩家在此的情感弧线是什么？
  - 需要通过环境触发哪些叙事事件？
  - 哪些叙事信息应以环境方式呈现？

- **world-builder**：
  - 该区域的历史与派系背景（曾在此发生过什么？谁控制此地？）
  - 生态与自然特征（动植物、地质）
  - 该区域如何与更广泛的世界历史相联系？
  - 环境故事元素（废墟、遗弃物品、涂鸦、尸体）

- **art-director**：
  - 视觉身份：色调、材质、植被、建筑语言
  - 灯光情绪与时间（早晨、暮色、地下等）
  - 指向重要位置的视觉引导（轮廓、光线、对比）
  - 视觉优先区域与路径
  - 相机构图注意事项

### 步骤 2：空间布局（level-designer）
委派给 **level-designer**，携带**步骤 1 的全部输出**（叙事目的、世界观要素、art-director 的视觉目标）：
- 区域边界、地形特征和核心可导航空间
- 基于视觉引导和空间逻辑的入口/出口位置
- 玩家流线：主路径与探索分支（体现叙事节拍的可读性）
- 邂逅位置与精英/Boss 区域预留（含 systems-designer 调优参数占位符）
- 关卡性能注意事项：遮挡区域、可视范围截断点
- 谜题或互动元素结构（如有）

布局**必须**包含对步骤 1 各 art-director 视觉目标的明确回应：
> "视觉引导目标 [来自 art-director 的原文引用]：通过 [具体布局决策] 实现。"

### 步骤 3：系统设计（systems-designer）
委派给 **systems-designer**，携带布局：
- 每个邂逅位置的敌人组合（类型、数量、精英/普通比例）
- 与调优参数关联的难度建议
- 战利品列表分配（每个位置的类别和概率范围）
- 根据玩家流线测算资源节奏（消耗与补充）
- 识别任何突破性邂逅（玩家可能无法在不补充状态的情况下继续）

### 步骤 4：视觉概念与无障碍（并行）
并行委派：
- **art-director**：
  - 针对该具体关卡布局的视觉概念（场景、照明示意图、材质板）
  - 美术资产需求清单（按优先级排列）
  - 布局与原定视觉方向的偏差（步骤 1）

- **accessibility-specialist**：
  - 是否存在仅靠颜色区分的路线标记？（例：绿色通道 vs 红色通道）
  - 是否有需要时间感知的谜题？（旋转障碍、定时平台）— 是否提供了辅助模式？
  - 关键 NPC 和出口是否在小缩略图上清晰可辨？
  - 对于复杂的导航区域，是否有可选的迷你地图或引导线？
  - 字幕：关卡内对话和叙事音频是否有字幕？
  - **输出：** 无障碍审查报告，分级为：CLEAR（无问题）、ADVISORY（建议优化）、BLOCKING（设计缺陷，必须修复后才能进入步骤 5）

**⚠ 注意：** 如果步骤 4 的 `accessibility-specialist` 报告任何 **BLOCKING** 问题，必须先解决后再进入步骤 5。通过 `AskUserQuestion` 通知用户并请求批准修正方案。

### 步骤 5：QA 与完成度
委派给 **qa-tester**：
- 针对关卡的测试用例（流线遍历、邂逅触发、叙事事件）
- 完成度检查清单（资产引用、碰撞体、出入口连通）
- 性能验证说明（draw call 预算、Lightmap 烘培需求）

## 文件写入协议

编排者不直接写入关卡文档。每个子 Agent 写入其相应的输出部分：
- **level-designer** → `design/levels/[level-name].md`（主文档）
- **art-director**（步骤 1）→ `design/levels/[level-name].md` 中的视觉方向部分
- **art-director**（步骤 4）→ `design/levels/[level-name].md` 中的资产需求部分
- **systems-designer** → `design/levels/[level-name].md` 中的邂逅/战利品部分
- **qa-tester** → `production/qa/[level-name]-test-cases.md`

## 结论

关卡文档完整、无障碍问题已解决、测试用例已生成：

**COMPLETE** — 关卡设计流水线已完成。输出：`design/levels/[level-name].md`

如果流水线因未解决的阻塞问题而中止：

**BLOCKED** — [原因和阻塞项列表]

## 后续步骤

- 运行 `/design-review design/levels/[level-name].md` 验证已完成的关卡设计文档。
- 设计获批后，运行 `/dev-story` 实施关卡内容。
- 运行 `/qa-plan` 为本关卡生成 QA 测试计划。

## 错误恢复协议

若任何子 Agent 返回 BLOCKED、报错或无法完成，立即通过 `AskUserQuestion` 告知用户并给出选项：
- 跳过该 Agent，在最终报告中标注缺口
- 缩小范围后重试
- 停在此处先解决阻塞项

常见阻塞情形：
- ADR 状态为 Proposed → 请勿实施；先运行 `/architecture-decision`
- 范围过大 → 通过 `/create-stories` 拆分为多个故事
- ADR 与故事之间存在冲突指令 → 暴露冲突，不要猜测
