# Game Studio Agent 架构 —— 快速入门指南

## 这是什么？

这是一套完整的 Claude Code Agent 架构，专为游戏开发而设计。它将 48 个
专业 AI Agent 组织成一个镜像真实游戏开发团队的工作室层级，定义了各自的
职责、委派规则和协调协议。项目内置了 Godot、Unity 和 Unreal 的引擎专家
Agent——每套引擎都配有主要子系统的专属子专家。所有设计 Agent 和模板均以
成熟的游戏设计理论为基础（MDA 框架、自我决定理论、心流理论、Bartle 玩家
类型）。请根据你的项目选用对应的引擎套件。

## 使用方式

### 1. 理解层级结构

Agent 分三个层级：

- **第一层（Opus）**：做高层决策的总监
  - `creative-director` —— 愿景与创意冲突裁决
  - `technical-director` —— 架构与技术决策
  - `producer` —— 排期、协调与风险管理

- **第二层（Sonnet）**：掌管各自领域的部门负责人
  - `game-designer`、`lead-programmer`、`art-director`、`audio-director`、
    `narrative-director`、`qa-lead`、`release-manager`、`localization-lead`

- **第三层（Sonnet/Haiku）**：在各自领域内执行任务的专家
  - 设计师、程序员、美术师、编剧、测试员、工程师

### 2. 选择合适的 Agent

问自己："在真实的工作室里，这件事会交给哪个部门？"

| 我需要…… | 使用这个 Agent |
|-------------|---------------|
| 设计新机制 | `game-designer` |
| 编写战斗代码 | `gameplay-programmer` |
| 创建着色器 | `technical-artist` |
| 编写对话 | `writer` |
| 规划下一个迭代 | `producer` |
| 评审代码质量 | `lead-programmer` |
| 编写测试用例 | `qa-tester` |
| 设计关卡 | `level-designer` |
| 修复性能问题 | `performance-analyst` |
| 搭建 CI/CD | `devops-engineer` |
| 设计战利品表 | `economy-designer` |
| 解决创意冲突 | `creative-director` |
| 做架构决策 | `technical-director` |
| 管理发布流程 | `release-manager` |
| 准备本地化字符串 | `localization-lead` |
| 快速验证机制想法 | `prototyper` |
| 检查代码安全问题 | `security-engineer` |
| 检查无障碍合规性 | `accessibility-specialist` |
| 获取 Unreal Engine 建议 | `unreal-specialist` |
| 获取 Unity 建议 | `unity-specialist` |
| 获取 Godot 建议 | `godot-specialist` |
| 设计 GAS 技能/效果 | `ue-gas-specialist` |
| 定义 Blueprint/C++ 边界 | `ue-blueprint-specialist` |
| 实现 UE 网络同步 | `ue-replication-specialist` |
| 构建 UMG/CommonUI 组件 | `ue-umg-specialist` |
| 设计 DOTS/ECS 架构 | `unity-dots-specialist` |
| 编写 Unity 着色器/VFX | `unity-shader-specialist` |
| 管理 Addressable 资产 | `unity-addressables-specialist` |
| 构建 UI Toolkit/UGUI 界面 | `unity-ui-specialist` |
| 编写地道的 GDScript | `godot-gdscript-specialist` |
| 创建 Godot 着色器 | `godot-shader-specialist` |
| 构建 GDExtension 模块 | `godot-gdextension-specialist` |
| 规划直播活动和赛季 | `live-ops-designer` |
| 为玩家撰写补丁说明 | `community-manager` |
| 头脑风暴新游戏创意 | 使用 `/brainstorm` 技能 |

### 3. 使用斜杠命令完成常见任务

| 命令 | 用途 |
|---------|-------------|
| `/start` | 首次入门引导——询问当前所处阶段，引导至对应工作流 |
| `/help` | 情境感知的「下一步做什么？」——读取当前阶段与产物 |
| `/project-stage-detect` | 分析项目状态，检测阶段，识别缺口 |
| `/setup-engine` | 配置引擎及版本，填充参考文档 |
| `/adopt` | 棕地项目的审计与迁移计划 |
| `/brainstorm` | 从零开始的引导式游戏概念构思 |
| `/map-systems` | 将概念拆解为系统，绘制依赖关系，引导逐系统 GDD 创作 |
| `/design-system` | 逐章节引导式创作单一游戏系统的 GDD |
| `/quick-design` | 小幅变更的轻量设计规格——调参、微调、小功能添加 |
| `/review-all-gdds` | 跨 GDD 一致性与游戏设计理论整体评审 |
| `/propagate-design-change` | 查找受 GDD 变更影响的 ADR 和用户故事 |
| `/ux-design` | 创作 UX 规格（界面/流程、HUD、交互模式） |
| `/ux-review` | 验证 UX 规格的无障碍合规性与 GDD 对齐情况 |
| `/create-architecture` | 创作游戏主架构文档 |
| `/architecture-decision` | 创建架构决策记录（ADR） |
| `/architecture-review` | 验证所有 ADR、依赖顺序、GDD 可追溯性 |
| `/create-control-manifest` | 从已接受的 ADR 生成扁平化程序员规则表 |
| `/create-epics` | 将 GDD + ADR 转化为功能模块（每个架构模块一个） |
| `/create-stories` | 将单个功能模块拆解为可实现的用户故事文件 |
| `/dev-story` | 读取故事并实现——路由至正确的程序员 Agent |
| `/sprint-plan` | 创建或更新迭代计划 |
| `/sprint-status` | 快速 30 行迭代快照 |
| `/story-readiness` | 拾取前验证故事是否具备实现条件 |
| `/story-done` | 实现完成后的故事验收评审——核对所有验收标准 |
| `/estimate` | 生成结构化工作量估算 |
| `/design-review` | 评审设计文档 |
| `/code-review` | 评审代码质量与架构 |
| `/balance-check` | 分析游戏平衡性数据 |
| `/asset-audit` | 审计资产合规性 |
| `/content-audit` | GDD 规划内容 vs. 已实现内容——查找缺口 |
| `/scope-check` | 检测相对于计划的范围蔓延 |
| `/perf-profile` | 性能剖析与瓶颈识别 |
| `/tech-debt` | 扫描、追踪和排优先级的技术债务 |
| `/gate-check` | 验证阶段就绪情况（PASS / CONCERNS / FAIL） |
| `/consistency-check` | 扫描所有 GDD 的跨文档不一致（冲突的数值、名称、规则） |
| `/reverse-document` | 从现有代码生成设计/架构文档 |
| `/milestone-review` | 评审里程碑进展 |
| `/retrospective` | 运行迭代/里程碑回顾 |
| `/bug-report` | 创建结构化 bug 报告 |
| `/playtest-report` | 创建或分析测试反馈 |
| `/onboard` | 为某个角色生成入门文档 |
| `/release-checklist` | 验证发布前检查清单 |
| `/launch-checklist` | 完整的上线就绪验证 |
| `/changelog` | 从 git 历史生成变更日志 |
| `/patch-notes` | 为玩家生成补丁说明 |
| `/hotfix` | 带审计追踪的紧急修复流程 |
| `/prototype` | 搭建一次性原型框架 |
| `/localize` | 本地化扫描、提取、验证 |
| `/team-combat` | 编排完整战斗团队流水线 |
| `/team-narrative` | 编排完整叙事团队流水线 |
| `/team-ui` | 编排完整 UI 团队流水线 |
| `/team-release` | 编排完整发布团队流水线 |
| `/team-polish` | 编排完整打磨团队流水线 |
| `/team-audio` | 编排完整音频团队流水线 |
| `/team-level` | 编排完整关卡创作流水线 |
| `/team-live-ops` | 编排直播运营团队（赛季、活动、上线后内容） |
| `/team-qa` | 编排完整 QA 团队周期——测试计划、用例、冒烟测试、验收 |
| `/qa-plan` | 为迭代或功能生成 QA 测试计划 |
| `/bug-triage` | 重新排优先级的 bug 分级，分配至迭代，呈现系统性趋势 |
| `/smoke-check` | 在 QA 移交前运行关键路径冒烟测试（PASS / FAIL） |
| `/soak-test` | 为长时游戏会话生成浸泡测试协议 |
| `/regression-suite` | 将覆盖率映射到 GDD 关键路径，标记缺口，维护回归套件 |
| `/test-setup` | 为项目引擎搭建测试框架 + CI 流水线（仅执行一次） |
| `/test-helpers` | 生成引擎专属测试辅助库和工厂函数 |
| `/test-flakiness` | 从 CI 历史检测不稳定测试，标记以隔离或修复 |
| `/test-evidence-review` | 测试文件与手动证据的质量评审——ADEQUATE / INCOMPLETE / MISSING |
| `/skill-test` | 验证技能文件的合规性与正确性（静态 / 规格 / 审计） |

### 4. 使用模板创建新文档

模板位于 `.claude/docs/templates/`：

- `game-design-document.md` —— 新机制和系统
- `architecture-decision-record.md` —— 技术决策
- `architecture-traceability.md` —— 将 GDD 需求映射到 ADR 再到用户故事 ID
- `risk-register-entry.md` —— 新风险
- `narrative-character-sheet.md` —— 新角色
- `test-plan.md` —— 功能测试计划
- `sprint-plan.md` —— 迭代规划
- `milestone-definition.md` —— 新里程碑
- `level-design-document.md` —— 新关卡
- `game-pillars.md` —— 核心设计支柱
- `art-bible.md` —— 视觉风格参考
- `technical-design-document.md` —— 逐系统技术设计
- `post-mortem.md` —— 项目/里程碑回顾
- `sound-bible.md` —— 音频风格参考
- `release-checklist-template.md` —— 平台发布检查清单
- `changelog-template.md` —— 玩家向补丁说明
- `release-notes.md` —— 玩家向发布说明
- `incident-response.md` —— 线上事故响应手册
- `game-concept.md` —— 初始游戏概念（MDA、SDT、心流、Bartle）
- `pitch-document.md` —— 向干系人进行的项目提案
- `economy-model.md` —— 虚拟经济设计（水龙头/水槽模型）
- `faction-design.md` —— 派系身份、世界观与游戏角色
- `systems-index.md` —— 系统拆解与依赖关系映射
- `project-stage-report.md` —— 项目阶段检测输出
- `design-doc-from-implementation.md` —— 将现有代码逆向文档化为 GDD
- `architecture-doc-from-code.md` —— 将代码逆向文档化为架构文档
- `concept-doc-from-prototype.md` —— 将原型逆向文档化为概念文档
- `ux-spec.md` —— 逐界面 UX 规格（布局区域、状态、事件）
- `hud-design.md` —— 全游戏 HUD 理念、区域与元素规格
- `accessibility-requirements.md` —— 全项目无障碍级别与功能矩阵
- `interaction-pattern-library.md` —— 标准 UI 控件与游戏专属交互模式
- `player-journey.md` —— 6 阶段情感弧线与按时间尺度划分的留存钩子
- `difficulty-curve.md` —— 难度维度、新手引导坡度与跨系统交互
- `test-evidence.md` —— 记录手动测试证据的模板（截图、演练记录）

`.claude/docs/templates/collaborative-protocols/` 下还有（由 Agent 使用，通常不直接编辑）：

- `design-agent-protocol.md` —— 设计 Agent 的「提问-选项-草稿-审批」周期
- `implementation-agent-protocol.md` —— 程序员 Agent 从拾取故事到 `/story-done` 的周期
- `leadership-agent-protocol.md` —— 总监层 Agent 的跨部门委派与升级规则

### 5. 遵循协调规则

1. 工作沿层级向下流动：总监 → 负责人 → 专家
2. 冲突沿层级向上升级
3. 跨部门工作由 `producer` 协调
4. Agent 不得在未经委派的情况下修改其领域之外的文件
5. 所有决策均需记录在案

## 新项目的第一步

**不知道从哪里开始？** 运行 `/start`。它会询问你当前所处的阶段，并将
你引导至对应的工作流。对你的游戏、引擎或经验水平不做任何假设。

如果你已经清楚自己的需求，可以直接跳至对应路径：

### 路径 A：「我完全不知道要做什么」

1. **运行 `/start`**（或 `/brainstorm open`）—— 引导式创意探索：
   你感兴趣的方向、玩过的游戏、你的约束条件
   - 生成 3 个概念，帮你选定一个，定义核心循环和设计支柱
   - 产出游戏概念文档，并推荐引擎
2. **搭建引擎** —— 运行 `/setup-engine`（使用头脑风暴阶段的推荐结果）
   - 配置 CLAUDE.md，检测知识缺口，填充参考文档
   - 创建 `.claude/docs/technical-preferences.md`，包含命名规范、
     性能预算和引擎专属默认值
   - 如果引擎版本超出 LLM 的训练数据范围，将从网络获取
     最新文档，确保 Agent 推荐正确的 API
3. **验证概念** —— 运行 `/design-review design/gdd/game-concept.md`
4. **拆解系统** —— 运行 `/map-systems` 映射所有系统及依赖关系
5. **设计各系统** —— 按依赖顺序运行 `/design-system [系统名]`
   （或 `/map-systems next`）编写 GDD
6. **测试核心循环** —— 运行 `/prototype [核心机制]`
7. **进行游戏测试** —— 运行 `/playtest-report` 验证假设
8. **规划首个迭代** —— 运行 `/sprint-plan new`
9. 开始开发

### 路径 B：「我知道自己想做什么」

如果你已有游戏概念和引擎选型：

1. **搭建引擎** —— 运行 `/setup-engine [引擎] [版本]`
   （例如 `/setup-engine godot 4.6`）—— 同时创建技术偏好配置
2. **编写游戏支柱** —— 委托给 `creative-director`
3. **拆解系统** —— 运行 `/map-systems` 列举系统及依赖关系
4. **设计各系统** —— 按依赖顺序运行 `/design-system [系统名]` 编写 GDD
5. **创建初始 ADR** —— 运行 `/architecture-decision`
6. **创建首个里程碑** 在 `production/milestones/` 下
7. **规划首个迭代** —— 运行 `/sprint-plan new`
8. 开始开发

### 路径 C：「我有游戏概念，但不知道选哪个引擎」

如果你有概念但不确定哪个引擎最合适：

1. **不带参数运行 `/setup-engine`** —— 它会询问你游戏的需求
   （2D/3D、目标平台、团队规模、语言偏好），并根据你的回答推荐引擎
2. 从路径 B 的第 2 步继续

### 路径 D：「我有一个现有项目」

如果你已有设计文档、原型或代码：

1. **运行 `/start`**（或 `/project-stage-detect`）—— 分析现有内容，
   识别缺口，推荐后续步骤
2. **运行 `/adopt`**（如果你已有 GDD、ADR 或用户故事）—— 审计
   内部格式合规性，生成带编号的迁移计划以填补缺口，
   同时不覆盖你的现有工作
3. **按需配置引擎** —— 如果尚未配置，运行 `/setup-engine`
4. **验证阶段就绪情况** —— 运行 `/gate-check` 了解当前状态
5. **规划下一个迭代** —— 运行 `/sprint-plan new`

## 文件结构参考

```
CLAUDE.md                          -- 主配置文件（先读这个，约 60 行）
.claude/
  settings.json                    -- Claude Code 钩子与项目设置
  agents/                          -- 48 个 Agent 定义（YAML frontmatter）
  skills/                          -- 68 个斜杠命令定义（YAML frontmatter）
  hooks/                           -- 12 个钩子脚本（.sh），由 settings.json 连接
  rules/                           -- 11 个路径专属规则文件
  docs/
    quick-start.md                 -- 本文件
    technical-preferences.md       -- 项目专属标准（由 /setup-engine 填充）
    coding-standards.md            -- 编码与设计文档标准
    coordination-rules.md          -- Agent 协调规则
    context-management.md          -- 上下文预算与压缩指令
    directory-structure.md         -- 项目目录布局
    workflow-catalog.yaml          -- 7 阶段流水线定义（由 /help 读取）
    setup-requirements.md          -- 系统前置条件（Git Bash、jq、Python）
    settings-local-template.md     -- 个人 settings.local.json 指南
    templates/                     -- 37 个文档模板
```
