# Claude Code Game Studios -- 完整工作流指南

> **如何借助 Agent 架构从零出发到发布一款游戏。**
>
> 本指南带你走过游戏开发的每个阶段，使用 48 个 Agent 体系、68 个斜杠命令
> 和 12 个自动钩子。前提：已安装 Claude Code，并在项目根目录下工作。
>
> 流水线共 7 个阶段，每个阶段都有必须通过的正式门禁（`/gate-check`）才能推进。
> 权威阶段序列定义在 `.claude/docs/workflow-catalog.yaml` 中，由 `/help` 读取。

---

## 目录

1. [快速开始](#快速开始)
2. [阶段 1：概念](#阶段-1概念)
3. [阶段 2：系统设计](#阶段-2系统设计)
4. [阶段 3：技术搭建](#阶段-3技术搭建)
5. [阶段 4：预制作](#阶段-4预制作)
6. [阶段 5：制作](#阶段-5制作)
7. [阶段 6：打磨](#阶段-6打磨)
8. [阶段 7：发布](#阶段-7发布)
9. [横切关注点](#横切关注点)
10. [附录 A：Agent 快速参考](#附录-aagent-快速参考)
11. [附录 B：斜杠命令快速参考](#附录-b斜杠命令快速参考)
12. [附录 C：常用工作流](#附录-c常用工作流)

---

## 快速开始

### 前提条件

开始之前，请确保以下工具已就绪：

- **Claude Code** 已安装且可正常使用
- **Git** 含 Git Bash（Windows）或标准终端（Mac/Linux）
- **jq**（可选，建议安装——钩子在缺失时会回退到 `grep`）
- **Python 3**（可选——部分钩子用于 JSON 校验）

### 第 1 步：克隆并打开

```bash
git clone <repo-url> my-game
cd my-game
```

### 第 2 步：运行 /start

如果是第一次使用：

```
/start
```

此引导式入门会询问你当前所处阶段，并路由到正确的工作流：

- **路径 A** -- 完全没有想法：路由到 `/brainstorm`
- **路径 B** -- 有模糊想法：路由到带种子提示的 `/brainstorm`
- **路径 C** -- 有明确概念：路由到 `/setup-engine` 和 `/map-systems`
- **路径 D1** -- 现有项目，文档较少：正常流程
- **路径 D2** -- 现有项目，已有 GDD/ADR：先运行 `/project-stage-detect`
  再运行 `/adopt` 做存量项目迁移

### 第 3 步：验证钩子是否正常工作

启动新的 Claude Code 会话，应看到 `session-start.sh` 钩子的输出：

```
=== Claude Code Game Studios -- Session Context ===
Branch: main
Recent commits:
  abc1234 Initial commit
===================================
```

出现此输出说明钩子正常工作。若未出现，请检查 `.claude/settings.json`
中的钩子路径是否与你的操作系统匹配。

### 第 4 步：随时寻求帮助

任何时候运行：

```
/help
```

系统会读取 `production/stage.txt` 中的当前阶段，检查已存在的文档，
并告诉你下一步应该做什么。它会区分**必须**执行的步骤与**可选**机会。

### 第 5 步：建立目录结构

目录按需创建。系统期望以下布局：

```
src/                  # 游戏源代码
  core/               # 引擎/框架代码
  gameplay/           # 游戏玩法系统
  ai/                 # AI 系统
  networking/         # 多人网络代码
  ui/                 # UI 代码
  tools/              # 开发工具
assets/               # 游戏资产
  art/                # 精灵图、模型、贴图
  audio/              # 音乐、音效
  vfx/                # 粒子特效
  shaders/            # 着色器文件
  data/               # JSON 配置/平衡数据
design/               # 设计文档
  gdd/                # 游戏设计文档
  narrative/          # 故事、世界观、对话
  levels/             # 关卡设计文档
  balance/            # 平衡性电子表格和数据
  ux/                 # UX 规格说明
docs/                 # 技术文档
  architecture/       # 架构决策记录
  api/                # API 文档
  postmortems/        # 事后总结
tests/                # 测试套件
prototypes/           # 原型（可丢弃）
production/           # 迭代计划、里程碑、发布版本
  sprints/
  milestones/
  releases/
  epics/              # 功能模块与用户故事文件（来自 /create-epics + /create-stories）
  playtests/          # 测试报告
  session-state/      # 临时会话状态（已加入 .gitignore）
  session-logs/       # 会话审计记录（已加入 .gitignore）
```

> **提示：** 不需要在第一天就创建所有目录。进入需要它们的阶段时再创建。
> 重要的是要遵循此结构，因为**规则系统**会根据文件路径强制执行标准。
> `src/gameplay/` 中的代码适用游戏玩法规则，`src/ai/` 中的代码适用 AI 规则，依此类推。

---

## 阶段 1：概念

### 本阶段目标

从"没有想法"或"模糊想法"出发，产出一份结构化的游戏概念文档，
包含明确的设计支柱和玩家旅程。这是确定**做什么**和**为什么做**的阶段。

### 阶段 1 流水线

```
/brainstorm  -->  game-concept.md  -->  /design-review  -->  /setup-engine
     |                                        |                    |
     v                                        v                    v
  10 个概念      含支柱、MDA、            对概念文档进行         引擎版本固定在
  MDA 分析       核心循环、USP 的         验证                   technical-preferences.md
  玩家动机       概念文档
                                                                   |
                                                                   v
                                                             /map-systems
                                                                   |
                                                                   v
                                                            systems-index.md
                                                            （所有系统、依赖关系、
                                                             优先级层级）
```

### 步骤 1.1：用 /brainstorm 头脑风暴

这是你的起点。运行头脑风暴技能：

```
/brainstorm
```

或加上类型提示：

```
/brainstorm roguelike deckbuilder
```

**发生了什么：** 头脑风暴技能引导你完成一个协作式 6 阶段创意过程，
使用专业工作室级别的创意技巧：

1. 询问你的兴趣、主题和约束条件
2. 生成 10 个概念种子，附 MDA（机制、动态、体验）分析
3. 你选出 2-3 个最喜欢的进行深度分析
4. 进行玩家动机映射和目标受众定位
5. 你选定获胜概念
6. 将其正式化为 `design/gdd/game-concept.md`

概念文档包含：

- 电梯演讲（一句话描述）
- 核心幻想（玩家想象自己在做什么）
- MDA 分解
- 目标受众（Bartle 玩家类型、人口统计）
- 核心循环图
- 独特卖点（USP）
- 可对比的同类游戏及差异点
- 游戏支柱（3-5 个不可妥协的设计价值观）
- 反支柱（游戏刻意回避的内容）

### 步骤 1.2：审查概念（可选，但建议执行）

```
/design-review design/gdd/game-concept.md
```

在继续之前验证结构完整性。

### 步骤 1.3：选择引擎

```
/setup-engine
```

或指定引擎：

```
/setup-engine godot 4.6
```

**`/setup-engine` 的作用：**

- 将命名规范、性能预算和引擎专属默认值填入 `.claude/docs/technical-preferences.md`
- 检测知识盲区（引擎版本比 LLM 训练数据更新），建议交叉参考 `docs/engine-reference/`
- 在 `docs/engine-reference/` 中创建版本锁定的参考文档

**为什么重要：** 设置引擎后，系统就知道要使用哪些引擎专属 Agent。
选择 Godot 后，`godot-specialist`、`godot-gdscript-specialist`
和 `godot-shader-specialist` 将成为你的主要专家。

### 步骤 1.4：将概念分解为系统

在编写各个 GDD 之前，先列举游戏需要的所有系统：

```
/map-systems
```

这将创建 `design/gdd/systems-index.md` — 一个主追踪文档，其中：

- 列出游戏所需的每个系统（战斗、移动、UI 等）
- 映射系统之间的依赖关系
- 分配优先级层级（MVP、垂直切片、Alpha、完整愿景）
- 确定设计顺序（基础层 > 核心层 > 功能层 > 表现层 > 打磨层）

此步骤是进入阶段 2 的**必要条件**。来自 155 个游戏事后分析的研究表明，
跳过系统枚举在制作阶段会产生 5-10 倍的额外成本。

### 阶段 1 门禁

```
/gate-check concept
```

**通过要求：**

- 引擎已在 `technical-preferences.md` 中配置
- `design/gdd/game-concept.md` 存在且包含设计支柱
- `design/gdd/systems-index.md` 存在且包含依赖顺序

**裁定结果：** PASS / CONCERNS / FAIL。CONCERNS 在承认风险后可通过。
FAIL 阻止推进。

---

## 阶段 2：系统设计

### 本阶段目标

创建所有定义游戏玩法的设计文档。此阶段不写代码——纯粹是设计。
系统索引中识别的每个系统都要获得自己的 GDD（游戏设计文档），
逐节编写、单独审查，然后对所有 GDD 进行一致性交叉检查。

### 阶段 2 流水线

```
/map-systems next  -->  /design-system  -->  /design-review
       |                     |                     |
       v                     v                     v
  从系统索引中         逐节引导            验证 8 个
  选出下一个系统       GDD 创作            必需章节
                       （增量写入）        APPROVED/NEEDS REVISION
       |
       |  （对每个 MVP 系统重复）
       v
/review-all-gdds
       |
       v
  跨 GDD 一致性 + 游戏设计理论审查
  PASS / CONCERNS / FAIL
```

### 步骤 2.1：编写系统 GDD

按依赖顺序设计每个系统，使用引导式工作流：

```
/map-systems next
```

这会选出优先级最高的未设计系统，并移交给 `/design-system`，
引导你逐节创建其 GDD。

也可直接设计指定系统：

```
/design-system combat-system
```

**`/design-system` 的作用：**

1. 读取你的游戏概念、系统索引以及上下游 GDD
2. 运行技术可行性预检（领域映射 + 可行性简报）
3. 逐节引导你完成 8 个必需 GDD 章节
4. 每节遵循：情境 > 问题 > 选项 > 决策 > 草稿 > 批准 > 写入
5. 批准后立即将每节写入文件（防崩溃丢失）
6. 标记与已批准 GDD 的冲突
7. 按类别路由到专家 Agent（数学由 systems-designer，经济由 economy-designer，
   故事系统由 narrative-director）

**8 个必需 GDD 章节：**

| # | 章节 | 内容 |
|---|------|------|
| 1 | **概述** | 对该系统的一段话摘要 |
| 2 | **玩家幻想** | 玩家使用此系统时的想象/感受 |
| 3 | **详细规则** | 明确无歧义的机制规则 |
| 4 | **公式** | 每个计算公式，含变量定义和取值范围 |
| 5 | **边界情况** | 特殊情况下会发生什么？明确解决。 |
| 6 | **依赖关系** | 此系统连接的其他系统（双向） |
| 7 | **调节旋钮** | 设计师可安全调整的数值及安全范围 |
| 8 | **验收标准** | 如何测试此系统是否正常工作？具体可测量。 |

另加**游戏手感**章节：手感参考、输入响应（毫秒/帧数）、
动画手感目标（起手/主动/恢复）、打击感时刻、重量感配置。

### 步骤 2.2：审查每份 GDD

在开始下一个系统之前，先验证当前系统：

```
/design-review design/gdd/combat-system.md
```

检查所有 8 个章节的完整性、公式清晰度、边界情况解决方案、
双向依赖关系以及可测试的验收标准。

**裁定结果：** APPROVED / NEEDS REVISION / MAJOR REVISION。
只有 APPROVED 的 GDD 才能继续推进。

### 步骤 2.3：不需要完整 GDD 的小改动

对于不需要完整 GDD 的调整、小改动或微调：

```
/quick-design "为侧面攻击添加 10% 伤害加成"
```

这会在 `design/quick-specs/` 中创建轻量级规格说明，而非完整的 8 节 GDD。
适用于数值调整、数字修改和小型添加。

### 步骤 2.4：跨 GDD 一致性审查

所有 MVP 系统 GDD 单独获批后：

```
/review-all-gdds
```

同时读取**所有** GDD 并进行两阶段分析：

**第一阶段 -- 跨 GDD 一致性：**
- 依赖关系双向性（A 引用 B，B 是否引用 A？）
- 系统间的规则矛盾
- 指向已重命名或删除系统的过时引用
- 所有权冲突（两个系统声明同一职责）
- 公式取值范围兼容性（系统 A 的输出是否符合系统 B 的输入？）
- 验收标准交叉检查

**第二阶段 -- 设计理论（游戏设计整体性）：**
- 竞争性进度循环（两个系统争夺同一奖励空间？）
- 认知负荷（玩家是否同时面对超过 4 个活跃系统？）
- 主导策略（某种方案让所有其他方案变得无关紧要？）
- 经济循环分析（来源和消耗是否平衡？）
- 跨系统难度曲线一致性
- 支柱对齐与反支柱违规
- 玩家幻想连贯性

**输出：** `design/gdd/gdd-cross-review-[日期].md` 含裁定结果。

### 步骤 2.5：叙事设计（如适用）

如果游戏含有故事、世界观或对话，此时开始构建：

1. **世界观构建** -- 使用 `world-builder` 定义派系、历史、地理和世界规则
2. **故事结构** -- 使用 `narrative-director` 设计故事弧、角色弧和叙事节拍
3. **角色卡** -- 使用 `narrative-character-sheet.md` 模板

### 阶段 2 门禁

```
/gate-check systems-design
```

**通过要求：**

- `systems-index.md` 中所有 MVP 系统状态均为 `Status: Approved`
- 每个 MVP 系统都有经过审查的 GDD
- 跨 GDD 审查报告存在（`design/gdd/gdd-cross-review-*.md`），
  裁定结果为 PASS 或 CONCERNS（非 FAIL）

---

## 阶段 3：技术搭建

### 本阶段目标

做出关键技术决策，将其记录为 ADR（架构决策记录），
通过审查进行验证，并产出一份控制清单为程序员提供扁平可执行的规则。
同时建立 UX 基础。

### 阶段 3 流水线

```
/create-architecture  -->  /architecture-decision (x N)  -->  /architecture-review
        |                          |                                   |
        v                          v                                   v
  覆盖所有系统的           按决策生成 ADR               验证完整性、
  主架构文档               存于 docs/architecture/       依赖顺序、
                           adr-*.md                      引擎兼容性
                                                                      |
                                                                      v
                                                         /create-control-manifest
                                                                      |
                                                                      v
                                                         扁平程序员规则表
                                                         docs/architecture/
                                                         control-manifest.md
        本阶段还包含：
        -------------------
        /ux-design  -->  /ux-review
        无障碍需求文档
        交互模式库
```

### 步骤 3.1：主架构文档

```
/create-architecture
```

在 `docs/architecture/architecture.md` 中创建总体架构文档，
涵盖系统边界、数据流和集成点。

### 步骤 3.2：架构决策记录（ADR）

每个重大技术决策执行：

```
/architecture-decision "NPC AI 用状态机还是行为树"
```

**发生了什么：** 技能引导你创建含以下内容的 ADR：
- 上下文和决策驱动因素
- 所有选项含优缺点及引擎兼容性
- 所选方案及理由
- 后果（正面、负面、风险）
- 依赖关系（依赖于、使能、阻塞、顺序说明）
- 已解决的 GDD 需求（通过 TR-ID 关联）

ADR 的生命周期：拟议中 > 已接受 > 已取代/已废弃。

**门禁检查前至少需要 3 条基础层 ADR。**

**改造现有 ADR：** 如果存量项目中已有 ADR：

```
/architecture-decision retrofit docs/architecture/adr-005.md
```

系统会检测缺失的模板章节并仅添加那些章节，不会覆盖现有内容。

### 步骤 3.3：架构审查

```
/architecture-review
```

综合验证所有 ADR：
- ADR 依赖关系的拓扑排序（检测循环依赖）
- 引擎兼容性验证
- GDD 修订标记（基于 ADR 选择标记需要更新的 GDD 章节）
- TR-ID 注册表维护（`docs/architecture/tr-registry.yaml`）

### 步骤 3.4：控制清单

```
/create-control-manifest
```

取所有已接受的 ADR，产出扁平程序员规则表：

```
docs/architecture/control-manifest.md
```

包含按代码层级组织的必须遵守的模式、禁止的模式和护栏。
之后创建的用户故事会嵌入控制清单的版本日期，以便检测过时。

### 步骤 3.5：无障碍需求

使用模板创建 `design/accessibility-requirements.md`。
确定一个层级（基础 / 标准 / 全面 / 示范），并填写 4 轴特性矩阵
（视觉、运动、认知、听觉）。

此文档在阶段 3 中是必需的，因为 UX 规格说明（在阶段 4 编写）
会引用此层级——它是设计前提，而非 UX 交付物。

### 阶段 3 门禁

```
/gate-check technical-setup
```

**通过要求：**

- `docs/architecture/architecture.md` 存在
- 至少 3 条 ADR 存在且状态为已接受
- 架构审查报告存在
- `docs/architecture/control-manifest.md` 存在
- `design/accessibility-requirements.md` 存在

---

## 阶段 4：预制作

### 本阶段目标

为关键界面创建 UX 规格说明，为高风险机制制作原型，
将设计文档转化为可实施的用户故事，规划第一个迭代，
并构建一个能证明核心循环有趣的垂直切片。

### 阶段 4 流水线

```
/ux-design  -->  /prototype  -->  /create-epics  -->  /create-stories  -->  /sprint-plan
    |                |                  |                   |                       |
    v                v                  v                   v                       v
  UX 规格说明    可丢弃           production/中       production/中           带优先级用户故事
  design/ux/     原型             的功能模块文件      的用户故事文件          的第一个迭代
                 prototypes/      epics/*/EPIC.md     epics/*/story-*.md      production/sprints/
                                  （每模块一个）      （每行为一个）          sprint-*.md
    |                                                      |
    v                                                      v
 /ux-review                                          /story-readiness
 （在创建功能模块前                                  （在开发用户故事前
  验证规格说明）                                      验证每个故事）
                                                           |
                                                           v
                                                       /dev-story
                                                     （实施故事，
                                                      路由到合适的 Agent）
                         |
                         v
                   垂直切片
                   （可玩 build，
                    3 次无引导测试）
```

### 步骤 4.1：关键界面的 UX 规格说明

在编写功能模块之前，先创建 UX 规格说明，让用户故事编写者了解有哪些界面
以及必须支持哪些玩家交互。

**UX 规格说明：**

```
/ux-design main-menu
/ux-design core-gameplay-hud
```

三种模式：界面/流程、HUD 和交互模式。输出到 `design/ux/`。
每份规格说明包含：玩家需求、布局区域、状态、交互地图、
数据需求、触发的事件、无障碍、本地化。

系统会读取阶段 3 中编写的 `accessibility-requirements.md` 和
`technical-preferences.md` 中的输入方法配置，以驱动无障碍和输入覆盖检查——
无需在每个界面重新指定。

> **提示：** `/design-system` 会为每个有 UI 需求的系统输出 📌 UX 标记。
> 使用这些标记作为需要规格说明的界面清单。

**交互模式库：**

```
/ux-design interaction-patterns
```

创建 `design/ux/interaction-patterns.md` — 16 种标准控件加上游戏专属模式
（物品栏格子、技能图标、HUD 进度条、对话框等），含动画和音效标准。

**UX 审查：**

```
/ux-review all
```

验证 UX 规格说明是否符合 GDD 要求及无障碍层级。
裁定结果：APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED。

### 步骤 4.2：原型化高风险机制

不是所有内容都需要原型。当满足以下条件时才制作原型：
- 机制新颖且不确定是否有趣
- 技术方案有风险且不确定是否可行
- 两种设计选项都看似可行，需要亲身感受差异

```
/prototype "带动量的抓钩移动"
```

**发生了什么：** 技能与你协作定义假设、成功标准和最小范围。
`prototyper` Agent 在隔离的 git 工作树（`isolation: worktree`）中工作，
确保可丢弃的代码不会污染 `src/`。

**关键规则：** `prototype-code` 规则刻意放宽编码标准——
允许硬编码数值，不需要测试——但含假设和发现的 README 是强制要求。

### 步骤 4.3：从设计文档创建功能模块和用户故事

```
/create-epics layer: foundation
/create-stories [epic-slug]   # 对每个功能模块重复
/create-epics layer: core
/create-stories [epic-slug]   # 对每个核心功能模块重复
```

`/create-epics` 读取你的 GDD、ADR 和架构来定义功能模块范围——
每个架构模块对应一个功能模块。`/create-stories` 将每个功能模块分解为
`production/epics/[slug]/` 中可实施的用户故事文件。每个故事嵌入：
- GDD 需求引用（TR-ID，非引用文本——保持新鲜）
- ADR 引用（仅来自已接受的 ADR；拟议中的 ADR 会导致 `Status: Blocked`）
- 控制清单版本日期（用于检测过时）
- 引擎专属实施说明
- 来自 GDD 的验收标准

用户故事存在后，运行 `/dev-story [story-path]` 来实施一个——
系统会自动路由到正确的程序员 Agent。

### 步骤 4.4：开发前验证用户故事

```
/story-readiness production/stories/combat-damage-calc.md
```

检查：设计完整性、架构覆盖、范围清晰度、完成定义。
裁定结果：READY / NEEDS WORK / BLOCKED。

### 步骤 4.5：工作量估算

```
/estimate production/stories/combat-damage-calc.md
```

提供含风险评估的工作量估算。

### 步骤 4.6：规划第一个迭代

```
/sprint-plan new
```

**发生了什么：** `producer` Agent 协作进行迭代规划：
- 询问迭代目标和可用时间
- 将目标分解为必须有 / 应该有 / 好有的任务
- 识别风险和阻碍
- 创建 `production/sprints/sprint-01.md`
- 填充 `production/sprint-status.yaml`（机器可读的故事跟踪）

### 步骤 4.7：垂直切片（硬性门禁）

进入制作阶段之前，必须构建并测试一个垂直切片：

- 一个从头到尾可玩的完整端到端核心循环
- 代表性品质（不全是占位内容）
- 在至少 3 次会话中进行无引导游玩
- 编写测试报告（`/playtest-report`）

这是**硬性门禁** -- 如果人类未进行无引导游玩，`/gate-check` 会自动 FAIL。

### 阶段 4 门禁

```
/gate-check pre-production
```

**通过要求：**

- `design/ux/` 中至少 1 份 UX 规格说明经过审查
- UX 审查完成（APPROVED 或 NEEDS REVISION 且风险已记录）
- 至少 1 个原型含 README
- `production/stories/` 中存在用户故事文件
- 至少 1 个迭代计划存在
- 至少 1 份测试报告存在（垂直切片在 3+ 次会话中进行游玩）

---

## 阶段 5：制作

### 本阶段目标

这是核心制作循环。以迭代为单位工作（通常 1-2 周），
逐个故事地实施功能，跟踪进度，并通过结构化完成审查关闭用户故事。
此阶段持续到游戏内容完整为止。

### 阶段 5 流水线（每次迭代）

```
/sprint-plan new  -->  /story-readiness  -->  实施  -->  /story-done
       |                     |                    |                |
       v                     v                    v                v
  创建迭代           验证故事            编写代码         8 阶段审查：
  sprint-status.yaml  READY 裁定          测试通过         验证标准，
  已填充                                               检查偏差，
                                                             更新故事状态
       |
       |  （每个故事重复，直到迭代完成）
       v
  /sprint-status  （随时快速查看 30 行快照）
  /scope-check    （如果范围在增长）
  /retrospective  （迭代结束时）
```

### 步骤 5.1：故事生命周期

制作阶段以**故事生命周期**为核心：

```
/story-readiness  -->  实施  -->  /story-done  -->  下一个故事
```

**1. 故事就绪检查：** 在开始一个故事之前进行验证：

```
/story-readiness production/stories/combat-damage-calc.md
```

检查设计完整性、架构覆盖、ADR 状态（若 ADR 仍为拟议中则阻塞）、
控制清单版本（若过时则警告）以及范围清晰度。
裁定结果：READY / NEEDS WORK / BLOCKED。

**2. 实施：** 与合适的 Agent 协作：

- `gameplay-programmer` 用于游戏玩法系统
- `engine-programmer` 用于核心引擎工作
- `ai-programmer` 用于 AI 行为
- `network-programmer` 用于多人游戏
- `ui-programmer` 用于 UI 代码
- `tools-programmer` 用于开发工具

所有 Agent 都遵循协作协议：读取设计文档，提出澄清问题，
展示架构选项，获得你的批准，然后实施。

**3. 故事完成：** 故事完成后：

```
/story-done production/stories/combat-damage-calc.md
```

运行 8 阶段完成审查：
1. 查找并读取故事文件
2. 加载引用的 GDD、ADR 和控制清单
3. 验证验收标准（自动可检查、手动、延后）
4. 检查 GDD/ADR 偏差（BLOCKING / ADVISORY / OUT OF SCOPE）
5. 提示进行代码审查
6. 生成完成报告（COMPLETE / COMPLETE WITH NOTES / BLOCKED）
7. 更新故事 `Status: Complete` 及完成说明
8. 显示下一个就绪故事

审查中发现的技术债务会记录到 `docs/tech-debt-register.md`。

### 步骤 5.2：迭代跟踪

随时检查进度：

```
/sprint-status
```

从 `production/sprint-status.yaml` 读取的 30 行快速快照。

如果范围在增长：

```
/scope-check production/sprints/sprint-03.md
```

将当前范围与原始计划对比，标记范围增加，建议削减内容。

### 步骤 5.3：内容跟踪

```
/content-audit
```

将 GDD 规定的内容与已实施的内容进行对比。提前发现内容缺口。

### 步骤 5.4：设计变更传播

GDD 在用户故事创建后发生变化时：

```
/propagate-design-change design/gdd/combat-system.md
```

对 GDD 进行 Git diff，找出受影响的 ADR，生成影响报告，
并引导你完成取代/更新/保留决策。

### 步骤 5.5：多系统功能（团队编排）

对于跨多个领域的功能，使用团队技能：

```
/team-combat "带持续治疗和净化的治疗技能"
/team-narrative "第二幕故事内容"
/team-ui "物品栏界面重设计"
/team-level "森林地牢关卡"
/team-audio "战斗音频优化"
```

每个团队技能协调一个 6 阶段协作工作流：
1. **设计** -- game-designer 提问，展示选项
2. **架构** -- lead-programmer 提出代码结构
3. **并行实施** -- 专家同时工作
4. **整合** -- gameplay-programmer 将所有内容整合
5. **验证** -- qa-tester 针对验收标准运行检查
6. **报告** -- 协调者汇总状态

编排是自动的，但**决策点仍由你掌控**。

### 步骤 5.6：迭代回顾和下一个迭代

迭代结束时：

```
/retrospective
```

分析计划与完成、迭代速度、阻碍和可操作的改进建议。

然后规划下一个迭代：

```
/sprint-plan new
```

### 步骤 5.7：里程碑审查

在里程碑检查点：

```
/milestone-review "alpha"
```

产出功能完成度、质量指标、风险评估和通过/不通过建议。

### 阶段 5 门禁

```
/gate-check production
```

**通过要求：**

- 所有 MVP 用户故事完成
- 测试：3 次会话，覆盖新玩家、中期游戏和难度曲线
- 有趣假设得到验证
- 测试数据中无混乱循环

---

## 阶段 6：打磨

### 本阶段目标

游戏功能已完整。现在让它变得优秀。
此阶段专注于性能、平衡性、无障碍、音频、视觉打磨和测试。

### 阶段 6 流水线

```
/perf-profile  -->  /balance-check  -->  /asset-audit  -->  /playtest-report (x3)
       |                  |                    |                    |
       v                  v                    v                    v
  分析 CPU/GPU       分析公式和          验证命名规范、      覆盖：新玩家、
  内存，优化         数据是否有          格式、大小          中期游戏、
  瓶颈               进度断层                                难度曲线

  /tech-debt  -->  /team-polish
       |                |
       v                v
  跟踪并优先排序   协调打磨工作：
  技术债务          性能 + 美术 +
                    音频 + UX + QA
```

### 步骤 6.1：性能分析

```
/perf-profile
```

引导你完成结构化性能分析：
- 建立目标（帧率、内存、平台）
- 按影响排名识别瓶颈
- 生成含代码位置和预期收益的可操作优化任务

### 步骤 6.2：平衡性分析

```
/balance-check assets/data/combat_damage.json
```

分析平衡数据中的统计异常值、进度曲线断层、退化策略和经济失衡。

### 步骤 6.3：资产审计

```
/asset-audit
```

验证所有资产的命名规范、文件格式标准和大小预算。

### 步骤 6.4：游玩测试（必需：3 次会话）

```
/playtest-report
```

生成结构化游玩测试报告。需要 3 次会话，覆盖：
- 新玩家体验
- 中期游戏系统
- 难度曲线

### 步骤 6.5：技术债务评估

```
/tech-debt
```

扫描 TODO/FIXME/HACK 注释、代码重复、过于复杂的函数、
缺少的测试和过时的依赖。每个条目都有分类和优先级。

### 步骤 6.6：协调打磨工作

```
/team-polish "战斗系统"
```

并行协调 4 位专家：
1. 性能优化（performance-analyst）
2. 视觉打磨（technical-artist）
3. 音频打磨（sound-designer）
4. 手感/果汁感（gameplay-programmer + technical-artist）

你设置优先级；团队在每一步经过你批准后执行。

### 步骤 6.7：本地化与无障碍

```
/localize src/
```

扫描硬编码字符串、破坏翻译的字符串拼接、未考虑文本扩展的文本，
以及缺失的语言文件。

无障碍性按照阶段 3 无障碍需求文档中承诺的层级进行审计。

### 阶段 6 门禁

```
/gate-check polish
```

**通过要求：**

- 至少 3 份游玩测试报告存在
- 协调打磨工作已完成（`/team-polish`）
- 无阻塞性性能问题
- 已满足无障碍层级要求

---

## 阶段 7：发布

### 本阶段目标

游戏已打磨、测试完毕、准备就绪。现在发布它。

### 阶段 7 流水线

```
/release-checklist  -->  /launch-checklist  -->  /team-release
        |                       |                      |
        v                       v                      v
  跨代码、内容、           全部门             协调：
  商店、法务的             验证（按部门        构建、QA 签字、
  发布前验证               通过/不通过）        部署、发布

                    另外：/changelog, /patch-notes, /hotfix
```

### 步骤 7.1：发布清单

```
/release-checklist v1.0.0
```

生成全面的发布前清单，涵盖：
- 构建验证（所有平台均可编译运行）
- 认证要求（特定平台）
- 商店元数据（描述、截图、宣传片）
- 法律合规（最终用户许可协议、隐私政策、年龄分级）
- 存档兼容性
- 数据分析验证

### 步骤 7.2：发布就绪（全面验证）

```
/launch-checklist
```

全部门交叉验证：

| 部门 | 检查内容 |
|------|---------|
| **工程** | 构建稳定性、崩溃率、内存泄漏、加载时间 |
| **设计** | 功能完整性、教程流程、难度曲线 |
| **美术** | 资产质量、缺失贴图、LOD 层级 |
| **音频** | 缺失音效、混音电平、空间音频 |
| **QA** | 按严重级别统计的开放 Bug 数量、回归测试套件通过率 |
| **叙事** | 对话完整性、世界观一致性、错别字 |
| **本地化** | 所有字符串已翻译、无截断、语言测试 |
| **无障碍** | 合规清单、辅助功能测试 |
| **商店** | 元数据完整、截图已审批、定价已设定 |
| **市场营销** | 媒体包就绪、发布预告片、社交媒体已排期 |
| **社区** | 更新说明草稿、FAQ 已准备、支持渠道就绪 |
| **基础设施** | 服务器已扩容、CDN 已配置、监控已启动 |
| **法务** | EULA 已最终确定、隐私政策、COPPA/GDPR 合规 |

每个条目获得**通过 / 不通过**状态。全部通过才能发布。

### 步骤 7.3：生成面向玩家的内容

```
/patch-notes v1.0.0
```

从 Git 历史和迭代数据生成玩家友好的更新说明。
将开发者语言翻译为玩家语言。

```
/changelog v1.0.0
```

生成内部更新日志（更偏技术性，面向团队）。

### 步骤 7.4：协调发布

```
/team-release
```

协调发布经理、QA 和 DevOps 完成：
1. 发布前验证
2. 构建管理
3. 最终 QA 签字
4. 部署准备
5. 通过/不通过决策

### 步骤 7.5：发布

`validate-push` 钩子会在推送到 `main` 或 `develop` 时发出警告。
这是刻意设计的——发布推送应该是深思熟虑的：

```bash
git tag v1.0.0
git push origin main --tags
```

### 步骤 7.6：发布后

**热修复工作流**，用于处理关键生产环境 Bug：

```
/hotfix "玩家在物品栏超过 99 个物品时丢失存档"
```

绕过正常迭代流程，但保留完整审计记录：
1. 创建热修复分支
2. 实施修复
3. 确保反向合并到开发分支
4. 记录事件

**事后总结**（待发布稳定后）：

```
按照 .claude/docs/templates/post-mortem.md 中的模板，
请 Claude 创建事后总结
```

---

## 横切关注点

这些主题适用于所有阶段。

### 总监审查模式

总监门禁是在关键工作流步骤检查工作的专家 Agent。
默认在每个检查点运行。你可以控制审查力度。

**在 `/start` 期间设置一次审查强度。** 保存到 `production/review-mode.txt`。

| 模式 | 运行内容 | 适合场景 |
|------|---------|---------|
| `full` | 所有总监门禁在每一步运行 | 新项目、学习系统 |
| `lean` | 总监仅在阶段转换时运行（`/gate-check`） | 有经验的开发者 |
| `solo` | 无总监审查 | 游戏马拉松、原型、最高速度 |

**单次覆盖**（不更改全局设置）：

```
/brainstorm space horror --review full
/architecture-decision --review solo
```

`--review` 标志适用于所有使用门禁的技能。任何时候通过直接编辑
`production/review-mode.txt` 或重新运行 `/start` 来更改全局模式。

完整门禁定义和检查模式：`.claude/docs/director-gates.md`

---

### 协作协议

本系统是**用户驱动的协作式**，而非自主运行。

**模式：** 问题 > 选项 > 决策 > 草稿 > 批准

每次 Agent 交互都遵循此模式：
1. Agent 提出澄清问题
2. Agent 展示 2-4 个选项，含权衡和推理
3. 你做出决策
4. Agent 根据你的决策起草内容
5. 你审查并细化
6. Agent 在写入前询问"我可以将此写入 [filepath] 吗？"

完整协议和示例见 `docs/COLLABORATIVE-DESIGN-PRINCIPLE.md`。

### AskUserQuestion 工具

Agent 使用 `AskUserQuestion` 工具进行结构化选项展示。
模式是"先解释再确认"：在对话文本中先进行完整分析，
然后用简洁的 UI 选择器完成决策。适用于设计选择、架构决策和战略性问题。
不适用于开放式探索性问题或简单的是/否确认。

### Agent 协调（三层体系）

```
第一层（总监）：  creative-director, technical-director, producer
                                          |
第二层（负责人）：game-designer, lead-programmer, art-director,
                  audio-director, narrative-director, qa-lead,
                  release-manager, localization-lead
                                          |
第三层（专家）：  gameplay-programmer, engine-programmer,
                  ai-programmer, network-programmer, ui-programmer,
                  tools-programmer, systems-designer, level-designer,
                  economy-designer, world-builder, writer,
                  technical-artist, sound-designer, ux-designer,
                  qa-tester, performance-analyst, devops-engineer,
                  analytics-engineer, accessibility-specialist,
                  live-ops-designer, prototyper, security-engineer,
                  community-manager, godot-specialist,
                  godot-gdscript-specialist, godot-shader-specialist,
                  unity-specialist, unity-csharp-specialist,
                  unreal-specialist, unreal-blueprint-specialist,
                  unreal-cpp-specialist
```

**协调规则：**
- 垂直委派：总监 > 负责人 > 专家。复杂决策不得跨层。
- 横向咨询：同层 Agent 可相互咨询，但不得在自身领域外做出约束性决策。
- 冲突解决：设计冲突交由 `creative-director`。技术冲突交由 `technical-director`。
  范围冲突交由 `producer`。
- 不得单方面跨领域更改。

### 自动钩子（安全防护网）

系统有 12 个自动运行的钩子：

| 钩子 | 触发时机 | 作用 |
|------|---------|------|
| `session-start.sh` | 会话开始 | 显示分支、近期提交，检测 active.md 以便恢复 |
| `detect-gaps.sh` | 会话开始 | 检测新项目（无引擎、无概念）并建议运行 `/start` |
| `pre-compact.sh` | 压缩前 | 将会话状态转储到对话中以便自动恢复 |
| `post-compact.sh` | 压缩后 | 提醒 Claude 从 `active.md` 恢复会话状态 |
| `notify.sh` | 通知事件 | 通过 PowerShell 显示 Windows 通知 |
| `validate-commit.sh` | 提交前 | 检查设计文档引用、有效 JSON、无硬编码数值 |
| `validate-push.sh` | 推送前 | 推送到 main/develop 时发出警告 |
| `validate-assets.sh` | 提交前 | 检查资产命名和大小 |
| `validate-skill-change.sh` | 技能文件写入 | 在 `.claude/skills/` 变更后建议运行 `/skill-test` |
| `log-agent.sh` | Agent 启动 | 记录 Agent 调用日志（审计记录） |
| `log-agent-stop.sh` | Agent 停止 | 完成 Agent 审计记录（启动 + 停止） |
| `session-stop.sh` | 会话结束 | 最终会话日志记录 |

### 上下文恢复能力

**会话状态文件：** `production/session-state/active.md` 是持续更新的检查点。
每次重要里程碑后更新它。任何中断（压缩、崩溃、`/clear`）后，先读取此文件。

**增量写入：** 创建多节文档时，每节批准后立即写入文件。
这意味着已完成的章节在崩溃和上下文压缩后仍可保留。
关于已写入章节的先前讨论可安全压缩。

**自动恢复：** `session-start.sh` 钩子自动检测并预览 `active.md`。
`pre-compact.sh` 钩子在压缩前将状态转储到对话中。

**迭代状态跟踪：** `production/sprint-status.yaml` 是机器可读的故事跟踪器。
由 `/sprint-plan`（初始化）和 `/story-done`（状态更新）写入。
由 `/sprint-status`、`/help` 和 `/story-done`（下一个故事）读取。
消除了脆弱的 Markdown 扫描。

### 存量项目接入

对于已有部分文档的现有项目：

```
/adopt
```

或针对性接入：

```
/adopt gdds
/adopt adrs
/adopt stories
/adopt infra
```

系统会审计现有文档的**格式**（而非仅检查是否存在），
将缺口按 BLOCKING/HIGH/MEDIUM/LOW 分类，建立有序迁移计划，
并写入 `docs/adoption-plan-[日期].md`。
核心原则：迁移而非替换——永远不会重新生成现有工作，只填补缺口。

各个技能也支持改造模式：

```
/design-system retrofit design/gdd/combat-system.md
/architecture-decision retrofit docs/architecture/adr-005.md
```

这些技能会检测哪些章节已有、哪些缺失，只填补缺口。

### 门禁系统

阶段门禁是正式检查点。用转换名称运行 `/gate-check`：

```
/gate-check concept              # 概念 -> 系统设计
/gate-check systems-design       # 系统设计 -> 技术搭建
/gate-check technical-setup      # 技术搭建 -> 预制作
/gate-check pre-production       # 预制作 -> 制作
/gate-check production           # 制作 -> 打磨
/gate-check polish               # 打磨 -> 发布
```

**裁定结果：**
- **PASS** -- 所有要求已满足，可推进到下一阶段
- **CONCERNS** -- 要求已满足但存在已承认的风险，可通过
- **FAIL** -- 要求未满足，阻止推进并提供具体补救措施

门禁通过后，`production/stage.txt` 会更新（仅在此时），
控制状态行和 `/help` 的行为。

### 反向文档化

对于代码存在但没有设计文档的情况（存量项目接入后常见）：

```
/reverse-document src/gameplay/combat/
```

读取现有代码，从中生成 GDD 格式的设计文档。

---

## 附录 A：Agent 快速参考

### "我需要做 X——用哪个 Agent？"

| 我需要... | Agent | 层级 |
|----------|-------|------|
| 提出游戏创意 | `/brainstorm` 技能 | -- |
| 设计游戏机制 | `game-designer` | 2 |
| 设计具体公式/数字 | `systems-designer` | 3 |
| 设计游戏关卡 | `level-designer` | 3 |
| 设计战利品表/经济系统 | `economy-designer` | 3 |
| 构建世界观 | `world-builder` | 3 |
| 编写对话 | `writer` | 3 |
| 规划故事 | `narrative-director` | 2 |
| 规划迭代 | `producer` | 1 |
| 做出创意决策 | `creative-director` | 1 |
| 做出技术决策 | `technical-director` | 1 |
| 实施游戏玩法代码 | `gameplay-programmer` | 3 |
| 实施核心引擎系统 | `engine-programmer` | 3 |
| 实施 AI 行为 | `ai-programmer` | 3 |
| 实施多人游戏 | `network-programmer` | 3 |
| 实施 UI | `ui-programmer` | 3 |
| 构建开发工具 | `tools-programmer` | 3 |
| 审查代码架构 | `lead-programmer` | 2 |
| 创建着色器/视觉特效 | `technical-artist` | 3 |
| 定义视觉风格 | `art-director` | 2 |
| 定义音频风格 | `audio-director` | 2 |
| 设计音效 | `sound-designer` | 3 |
| 设计 UX 流程 | `ux-designer` | 3 |
| 编写测试用例 | `qa-tester` | 3 |
| 规划测试策略 | `qa-lead` | 2 |
| 性能分析 | `performance-analyst` | 3 |
| 搭建 CI/CD | `devops-engineer` | 3 |
| 设计数据分析 | `analytics-engineer` | 3 |
| 检查无障碍性 | `accessibility-specialist` | 3 |
| 规划实时运营 | `live-ops-designer` | 3 |
| 管理发布 | `release-manager` | 2 |
| 管理本地化 | `localization-lead` | 2 |
| 快速原型开发 | `prototyper` | 3 |
| 审计安全性 | `security-engineer` | 3 |
| 与玩家沟通 | `community-manager` | 3 |
| Godot 专项帮助 | `godot-specialist` | 3 |
| GDScript 专项帮助 | `godot-gdscript-specialist` | 3 |
| Godot 着色器帮助 | `godot-shader-specialist` | 3 |
| GDExtension 模块 | `godot-gdextension-specialist` | 3 |
| Unity 专项帮助 | `unity-specialist` | 3 |
| Unity DOTS/ECS | `unity-dots-specialist` | 3 |
| Unity 着色器/视觉特效 | `unity-shader-specialist` | 3 |
| Unity Addressables | `unity-addressables-specialist` | 3 |
| Unity UI Toolkit | `unity-ui-specialist` | 3 |
| Unreal 专项帮助 | `unreal-specialist` | 3 |
| Unreal GAS | `ue-gas-specialist` | 3 |
| Unreal Blueprints | `ue-blueprint-specialist` | 3 |
| Unreal 网络同步 | `ue-replication-specialist` | 3 |
| Unreal UMG/CommonUI | `ue-umg-specialist` | 3 |

### Agent 层级体系

```
                    creative-director / technical-director / producer
                                         |
          ---------------------------------------------------------------
          |            |           |           |          |        |       |
    game-designer  lead-prog  art-dir  audio-dir  narr-dir  qa-lead  release-mgr
          |            |           |           |          |        |        |
     specialists  programmers  tech-art  snd-design  writer   qa-tester  devops
     （systems,   （gameplay,            （sound）   （world-  （perf,    （analytics,
      economy,     engine,                           builder）  access.）  security）
      level）      ai, net,
                   ui, tools）
```

**升级规则：** 如果两个 Agent 意见不一，向上升级。
设计冲突交由 `creative-director`。技术冲突交由 `technical-director`。
范围冲突交由 `producer`。

---

## 附录 B：斜杠命令快速参考

### 全部 66 个命令（按类别）

#### 入门与导航（5 个）

| 命令                      | 用途              | 阶段        |
| ----------------------- | --------------- | --------- |
| `/start`                | 引导式入门，路由到正确工作流  | 任意（第一次会话） |
| `/help`                 | 上下文感知的"下一步做什么？" | 任意        |
| `/project-stage-detect` | 完整项目审计以确定当前阶段   | 任意        |
| `/setup-engine`         | 配置引擎、锁定版本、设置偏好  | 1         |
| `/adopt`                | 存量项目审计和迁移计划     | 任意（现有项目）  |

#### 游戏设计（6 个）

| 命令 | 用途 | 阶段 |
|------|------|------|
| `/brainstorm` | 含 MDA 分析的协作式创意开发 | 1 |
| `/map-systems` | 将概念分解为系统索引 | 1-2 |
| `/design-system` | 引导式逐节 GDD 创作 | 2 |
| `/quick-design` | 小改动的轻量级规格说明 | 2+ |
| `/review-all-gdds` | 跨 GDD 一致性和设计理论审查 | 2 |
| `/propagate-design-change` | 找出受 GDD 变更影响的 ADR/故事 | 5 |

#### UX 与界面（2 个）

| 命令 | 用途 | 阶段 |
|------|------|------|
| `/ux-design` | 创作 UX 规格说明（界面/流程、HUD、模式） | 4 |
| `/ux-review` | 验证 UX 规格说明的无障碍性和 GDD 对齐 | 4 |

#### 架构（4 个）

| 命令 | 用途 | 阶段 |
|------|------|------|
| `/create-architecture` | 主架构文档 | 3 |
| `/architecture-decision` | 创建或改造 ADR | 3 |
| `/architecture-review` | 验证所有 ADR、依赖顺序 | 3 |
| `/create-control-manifest` | 从已接受 ADR 生成扁平程序员规则 | 3 |

#### 用户故事与迭代（8 个）

| 命令 | 用途 | 阶段 |
|------|------|------|
| `/create-epics` | 将 GDD + ADR 转化为功能模块（每个模块一个） | 4 |
| `/create-stories` | 将单个功能模块分解为用户故事文件 | 4 |
| `/dev-story` | 实施用户故事——路由到正确的程序员 Agent | 5 |
| `/sprint-plan` | 创建或管理迭代计划 | 4-5 |
| `/sprint-status` | 快速 30 行迭代快照 | 5 |
| `/story-readiness` | 验证故事是否可实施 | 4-5 |
| `/story-done` | 8 阶段故事完成审查 | 5 |
| `/estimate` | 含风险评估的工作量估算 | 4-5 |

#### 审查与分析（10 个）

| 命令                  | 用途                           | 阶段   |
| ------------------- | ---------------------------- | ---- |
| `/design-review`    | 按 8 节标准验证 GDD                | 1-2  |
| `/code-review`      | 架构代码审查                       | 5+   |
| `/balance-check`    | 游戏平衡性公式分析                    | 5-6  |
| `/asset-audit`      | 资产命名、格式、大小验证                 | 6    |
| `/content-audit`    | GDD 规定内容与已实施内容对比             | 5    |
| `/scope-check`      | 范围蔓延检测                       | 5    |
| `/perf-profile`     | 性能分析工作流                      | 6    |
| `/tech-debt`        | 技术债务扫描和优先级排序                 | 6    |
| `/gate-check`       | 含 PASS/CONCERNS/FAIL 的正式阶段门禁 | 所有转换 |
| `/reverse-document` | 从现有代码生成设计文档                  | 任意   |

#### QA 与测试（9 个）

| 命令 | 用途 | 阶段 |
|------|------|------|
| `/qa-plan` | 为迭代或功能生成 QA 测试计划 | 5 |
| `/smoke-check` | QA 交接前的关键路径冒烟测试门禁 | 5-6 |
| `/soak-test` | 长时游戏会话的浸泡测试方案 | 6 |
| `/regression-suite` | 映射测试覆盖，识别已修复但缺少回归测试的 Bug | 5-6 |
| `/test-setup` | 搭建测试框架和 CI/CD 流水线 | 4 |
| `/test-helpers` | 生成引擎专属测试辅助库 | 4-5 |
| `/test-evidence-review` | 测试文件和手动证据的质量审查 | 5 |
| `/test-flakiness` | 从 CI 日志检测不稳定测试 | 5-6 |
| `/skill-test` | 验证技能文件的结构和行为正确性 | 任意 |

#### 制作管理（6 个）

| 命令 | 用途 | 阶段 |
|------|------|------|
| `/milestone-review` | 里程碑进度和通过/不通过 | 5 |
| `/retrospective` | 迭代回顾分析 | 5 |
| `/bug-report` | 结构化 Bug 报告创建 | 5+ |
| `/bug-triage` | 重新评估开放 Bug 的优先级、严重程度和负责人 | 5+ |
| `/playtest-report` | 结构化游玩测试会话报告 | 4-6 |
| `/onboard` | 新成员入职 | 任意 |

#### 发布（5 个）

| 命令 | 用途 | 阶段 |
|------|------|------|
| `/release-checklist` | 发布前验证 | 7 |
| `/launch-checklist` | 全部门发布就绪验证 | 7 |
| `/changelog` | 自动生成内部更新日志 | 7 |
| `/patch-notes` | 面向玩家的更新说明 | 7 |
| `/hotfix` | 紧急修复工作流 | 7+ |

#### 创意（2 个）

| 命令 | 用途 | 阶段 |
|------|------|------|
| `/prototype` | 在隔离工作树中制作可丢弃原型 | 4 |
| `/localize` | 字符串提取和验证 | 6-7 |

#### 团队编排（9 个）

| 命令 | 用途 | 阶段 |
|------|------|------|
| `/team-combat` | 战斗功能：从设计到实施 | 5 |
| `/team-narrative` | 叙事内容：从结构到对话 | 5 |
| `/team-ui` | UI 功能：从 UX 规格说明到完善实施 | 5 |
| `/team-level` | 关卡：从布局到完整遭遇战 | 5 |
| `/team-audio` | 音频：从方向设定到实施的音频事件 | 5-6 |
| `/team-polish` | 协调打磨：性能 + 美术 + 音频 + QA | 6 |
| `/team-release` | 发布协调：构建 + QA + 部署 | 7 |
| `/team-live-ops` | 实时运营规划：季节性活动、通行证、留存 | 7+ |
| `/team-qa` | 完整 QA 周期：策略、执行、覆盖、签字 | 6-7 |

---

## 附录 C：常用工作流

### 工作流 1："我刚开始，完全没有游戏创意"

```
1. /start（根据你的位置进行路由）
2. /brainstorm（协作式创意开发，选定概念）
3. /setup-engine（锁定引擎和版本）
4. 对概念文档执行 /design-review（可选，建议执行）
5. /map-systems（将概念分解为含依赖关系和优先级的系统）
6. /gate-check concept（验证是否准备好进入系统设计阶段）
7. 每个系统执行 /design-system（引导式 GDD 创作）
```

### 工作流 2："我有设计文档，想开始写代码"

```
1. 对每份 GDD 执行 /design-review（确保设计扎实）
2. /review-all-gdds（跨 GDD 一致性检查）
3. /gate-check systems-design
4. /create-architecture + 每个重大决策执行 /architecture-decision
5. /architecture-review
6. /create-control-manifest
7. /gate-check technical-setup
8. /create-epics layer: foundation + /create-stories [slug]（定义模块，分解为故事）
9. /sprint-plan new
10. /story-readiness -> 实施 -> /story-done（故事生命周期）
```

### 工作流 3："我需要在制作中期添加一个复杂功能"

```
1. /design-system 或 /quick-design（根据范围选择）
2. /design-review 验证
3. 若修改现有 GDD，执行 /propagate-design-change
4. /estimate 评估工作量和风险
5. /team-combat、/team-narrative、/team-ui 等（合适的团队技能）
6. 完成后执行 /story-done
7. 若影响游戏平衡，执行 /balance-check
```

### 工作流 4："生产环境出现问题"

```
1. /hotfix "问题描述"
2. 在热修复分支上实施修复
3. /code-review 审查修复
4. 运行测试
5. /release-checklist 用于热修复构建
6. 部署并反向合并
```

### 工作流 5："我有现有项目，想使用本系统"

```
1. /start（选择路径 D——现有工作）
2. /project-stage-detect（确定当前阶段）
3. /adopt（审计现有文档，建立迁移计划）
4. /design-system retrofit [path]（填补 GDD 缺口）
5. /architecture-decision retrofit [path]（填补 ADR 缺口）
6. 在适当转换点执行 /gate-check
```

---

## 充分利用本系统的技巧

1. **始终先设计，再实现。** 本 Agent 体系建立在"编写代码前先有设计文档"的前提上。Agent 会持续引用 GDD。

2. **横切特性使用团队技能。** 不要手动协调 4 个 Agent——让 `/team-combat`、`/team-narrative` 等技能处理编排工作。

3. **信任规则系统。** 当某条规则标记了代码中的问题时，请修复它。规则中凝聚了来之不易的游戏开发经验（数据驱动数值、帧率无关的 delta time、无障碍访问等）。

4. **主动压缩上下文。** 当上下文使用率达到约 65–70% 时，执行压缩或 `/clear`。压缩前钩子会保存进度。不要等到达到极限再操作。

5. **使用正确层级的 Agent。** 不要让 `creative-director` 编写着色器，也不要让 `qa-tester` 做设计决策。层级体系有其存在的理由。

6. **不确定时运行 /help。** 它会读取你的实际项目状态，并告诉你下一步最重要的单一操作。

7. **将设计交给程序员前先运行 `/design-review`。** 这能提前发现不完整的规格，节省返工成本。

8. **每个主要功能完成后运行 `/code-review`。** 在架构问题扩散前捕获它们。

9. **先对有风险的机制做原型验证。** 一天的原型工作能为一个无法运作的机制节省一周的制作时间。

10. **保持迭代计划的诚实性。** 定期使用 `/scope-check`。范围蔓延是独立游戏失败的头号原因。

11. **用 ADR 记录决策。** 未来的你会感谢现在的你记录了事情**为何**如此构建。

12. **严格执行故事生命周期。** 认领前运行 `/story-readiness`，完成后运行 `/story-done`。这能提前发现偏差，保持流水线的诚实性。

13. **尽早且频繁地写入文件。** 增量章节写入意味着你的设计决策能在崩溃和上下文压缩中存活。文件才是记忆，而非对话本身。
