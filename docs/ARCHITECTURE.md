# Claude Code Game Studios — 系统架构文档

> 生成日期：2026-04-19  
> 版本：中文增强版（基于原版 v1.x 盘点）

---

## 1. 系统定位

Claude Code Game Studios（CCGS）是一个**游戏开发工作室仿真框架**，其本质是一套运行在 Claude Code 会话中的 AI 代理系统。它将传统游戏工作室的组织架构、工作流程和质量门禁转化为 Prompt 工程，让单个 Claude Code 会话具备完整工作室的协作能力。

```
用户（创意总监/制作人） ←→ Claude Code 会话
                              │
              ┌───────────────┴───────────────┐
           Agents                          Skills
        (角色专家)                        (斜杠命令)
              │                               │
        3 层级体系                       7 开发阶段
        48 个 Agent                     74 个 Skill
```

---

## 2. 整体架构层次

```
┌─────────────────────────────────────────────────────────────────┐
│                        用户交互层                                 │
│   斜杠命令 (/start, /brainstorm, ...)  自然语言对话               │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                      Skills 指令层（74个）                        │
│   每个 Skill = 一个 SKILL.md 文件，定义完整的执行流程             │
│   workflow-catalog.yaml 定义各 Skill 在 7 个阶段中的位置         │
└──────────────────────────┬──────────────────────────────────────┘
                           │ 调用
┌──────────────────────────▼──────────────────────────────────────┐
│                      Agents 专家层（48个）                        │
│   Tier 1 — Directors（3个，claude-opus）                         │
│   Tier 2 — Department Leads（8个，claude-sonnet）                │
│   Tier 3 — Specialists（37个，claude-sonnet/haiku）              │
└──────────────────────────┬──────────────────────────────────────┘
                           │ 读写
┌──────────────────────────▼──────────────────────────────────────┐
│                      数据/文件层                                   │
│  design/gdd/   docs/     production/  assets/  src/  tests/     │
└──────────────────────────┬──────────────────────────────────────┘
                           │ 自动触发
┌──────────────────────────▼──────────────────────────────────────┐
│                      Hooks 自动化层（12个）                       │
│   会话生命周期 / 提交验证 / 资产检查 / 间隙检测                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Agent 体系

### 3.1 三层层级

```
Tier 1 — 总监层（模型：Opus 4.6，最大决策权）
┌─────────────────────────────────────────────┐
│  creative-director   最终创意决策权          │
│  technical-director  最终技术决策权          │
│  producer            跨部门协调 & 进度管理   │
└─────────────────────────────────────────────┘
           ↓ 委托
Tier 2 — 部门负责人层（模型：Sonnet 4.6）
┌─────────────────────────────────────────────┐
│  game-designer        核心机制设计           │
│  lead-programmer      代码架构决策           │
│  art-director         视觉标准               │
│  audio-director       音频方向               │
│  narrative-director   叙事架构               │
│  qa-lead              测试策略 & 质量门禁    │
│  release-manager      发布管道               │
│  localization-lead    本地化流程             │
└─────────────────────────────────────────────┘
           ↓ 委托
Tier 3 — 专家层（模型：Sonnet/Haiku）
┌─────────────────────────────────────────────────────────────────┐
│ 通用专家（22个）                                                 │
│  accessibility-specialist  ai-programmer   analytics-engineer   │
│  community-manager         devops-engineer economy-designer      │
│  engine-programmer         gameplay-programmer level-designer    │
│  live-ops-designer         network-programmer performance-analyst│
│  prototyper                qa-tester       security-engineer     │
│  sound-designer            systems-designer technical-artist     │
│  tools-programmer          ui-programmer   ux-designer           │
│  world-builder             writer                               │
│                                                                  │
│ 引擎专属（15个，按需选用）                                        │
│  [Godot] godot-specialist, gdscript, gdextension, csharp, shader│
│  [Unity] unity-specialist, dots, shader, addressables, ui       │
│  [UE5]   unreal-specialist, gas, blueprint, replication, umg    │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Agent 文件结构

每个 Agent 是一个带 YAML frontmatter 的 Markdown 文件：

```yaml
---
name: creative-director           # 不可翻译（系统 ID）
description: "..."                # 可翻译（用于 Agent 选择说明）
tools: Read, Glob, Grep, Write    # 允许使用的工具
model: opus                       # 模型选择
maxTurns: 30                      # 最大轮次
memory: user                      # 记忆范围
disallowedTools: Bash             # 禁用工具
skills: [brainstorm, design-review] # 可调用的 Skill
---
```

### 3.3 Agent 间协作规则

| 规则 | 说明 |
|------|------|
| 垂直委托 | 总监 → 负责人 → 专家，不能跨级 |
| 横向协商 | 同级可协商，不可跨域做绑定决策 |
| 冲突上升 | 创意冲突 → creative-director；技术冲突 → technical-director |
| 变更传播 | 跨部门变更由 producer 协调 |
| 域边界 | Agent 不修改其职责域外的文件 |

---

## 4. Skill 体系

### 4.1 Skill 组织方式

```
.claude/skills/
├── [skill-name]/
│   └── SKILL.md        # 完整的执行流程定义
```

每个 SKILL.md 带 YAML frontmatter：

```yaml
---
name: start                     # 与目录名一致
description: "..."              # 触发描述
argument-hint: "[no arguments]" # 命令参数提示
user-invocable: true            # 是否用户可直接调用
agent: creative-director        # 执行此 Skill 的 Agent（可选）
allowed-tools: Read, Glob, AskUserQuestion
model: haiku                    # 可覆盖 Agent 默认模型
---
```

### 4.2 74 个 Skill 分类

| 类别 | Skill 列表 |
|------|-----------|
| **入门导航** | start, help, project-stage-detect, setup-engine, adopt |
| **游戏设计** | brainstorm, map-systems, design-system, quick-design, review-all-gdds, propagate-design-change |
| **美术资产** | art-bible, asset-spec, asset-audit |
| **UX/界面** | ux-design, ux-review |
| **架构** | create-architecture, architecture-decision, architecture-review, create-control-manifest |
| **故事迭代** | create-epics, create-stories, dev-story, sprint-plan, sprint-status, story-readiness, story-done, estimate |
| **评审分析** | design-review, code-review, balance-check, content-audit, scope-check, perf-profile, tech-debt, gate-check, consistency-check |
| **QA 测试** | qa-plan, smoke-check, soak-test, regression-suite, test-setup, test-helpers, test-evidence-review, test-flakiness, skill-test, skill-improve |
| **生产管理** | milestone-review, retrospective, bug-report, bug-triage, reverse-document, playtest-report |
| **发布** | release-checklist, launch-checklist, changelog, patch-notes, hotfix, day-one-patch |
| **创意内容** | prototype, onboard, localize |
| **团队编排** | team-combat, team-narrative, team-ui, team-release, team-polish, team-audio, team-level, team-live-ops, team-qa |

### 4.3 核心调用链

```
用户输入 /start
    │
    ├── 检测项目状态（读文件）
    ├── 询问用户位置（AskUserQuestion）
    └── 路由到→

    /brainstorm ──→ creative-director
        │           (选项呈现 → 用户决策 → 概念文档)
        ▼
    /map-systems ──→ game-designer
        │           (系统分解 → 依赖图 → 优先级)
        ▼
    /design-system ──→ game-designer + creative-director
        │              (GDD 逐节撰写 → 用户审批 → 写入文件)
        ▼
    /create-architecture ──→ technical-director + lead-programmer
        │                    (架构文档 → ADR → 控制清单)
        ▼
    /create-epics ──→ producer
        │             (Epic 分解)
        ▼
    /create-stories ──→ lead-programmer
        │               (Story 拆分 + 验收标准)
        ▼
    /dev-story ──→ lead-programmer → 对应 specialist
        │          (实现 → 测试 → 验收)
        ▼
    /story-done ──→ qa-lead
        │           (验收确认 → 状态更新)
        ▼
    /smoke-check → /gate-check → /sprint-plan（下一迭代）
```

---

## 5. Hook 自动化层

### 5.1 12 个 Hooks

| Hook 文件 | 触发时机 | 职责 |
|-----------|---------|------|
| `session-start.sh` | 会话开始 | 加载项目上下文、显示状态摘要 |
| `session-stop.sh` | 会话结束 | 保存状态快照 |
| `detect-gaps.sh` | 会话开始 | 检测文档缺失（代码存在但设计文档缺失等） |
| `validate-commit.sh` | git commit | 代码质量检查、设计引用检查 |
| `validate-push.sh` | git push | 测试门禁验证 |
| `validate-assets.sh` | 资产变更 | 命名规范、格式检查 |
| `validate-skill-change.sh` | Skill 文件变更 | YAML frontmatter 格式检查 |
| `log-agent.sh` | Agent 启动 | 记录 Agent 调用日志 |
| `log-agent-stop.sh` | Agent 停止 | 记录执行时间和结果 |
| `pre-compact.sh` | 上下文压缩前 | 保存关键状态到文件 |
| `post-compact.sh` | 上下文压缩后 | 恢复状态摘要 |
| `notify.sh` | 通用通知 | 向用户发送状态通知 |

### 5.2 Hooks 数据流

```
SessionStart
    → session-start.sh（读 production/session-state/）
    → detect-gaps.sh（读 src/ + design/，告警缺失文档）

代码修改
    → validate-commit.sh（检查代码规范 + 设计引用完整性）
    → validate-push.sh（运行测试套件）

Asset 修改
    → validate-assets.sh（检查命名规范 + 尺寸预算）

Skill 修改
    → validate-skill-change.sh（YAML frontmatter 格式验证）

上下文管理
    → pre-compact.sh（状态序列化到磁盘）
    → post-compact.sh（状态反序列化，恢复上下文摘要）
```

---

## 6. Rules 路径作用域系统

```
.claude/rules/
├── ai-code.md          → src/ai/**
├── data-files.md       → assets/data/**
├── design-docs.md      → design/gdd/**
├── engine-code.md      → src/core/**
├── gameplay-code.md    → src/gameplay/**
├── narrative.md        → design/narrative/**
├── network-code.md     → src/networking/**
├── prototype-code.md   → prototypes/**
├── shader-code.md      → assets/shaders/**
├── test-standards.md   → tests/**
└── ui-code.md          → src/ui/**
```

Rules 通过 YAML frontmatter 中的 `paths:` 字段绑定到目录，当 Claude Code 操作对应目录的文件时自动加载。

---

## 7. 7 阶段开发流水线

```
Phase 1: Concept（概念期）
    brainstorm → setup-engine → 游戏概念文档 → art-bible → map-systems
    
Phase 2: Systems Design（系统设计期）
    design-system（每个 MVP 系统）→ review-all-gdds → design-review
    
Phase 3: Technical Setup（技术搭建期）
    create-architecture → architecture-decision(s) → create-control-manifest
    → test-setup → create-epics
    
Phase 4: Production（生产期）
    sprint-plan → create-stories → dev-story → story-done
    （反复迭代，每个 Epic 一个 Sprint）
    
Phase 5: Alpha（Alpha 期）
    smoke-check → gate-check alpha → bug-triage → playtest-report
    
Phase 6: Polish（打磨期）
    team-polish → localize → accessibility review → gate-check polish
    
Phase 7: Release（发布期）
    release-checklist → launch-checklist → team-release → 发布
```

---

## 8. 关键数据文件

| 文件 | 职责 | 读取方 |
|------|------|-------|
| `.claude/docs/technical-preferences.md` | 引擎配置 & 项目规范 | 所有 agents、所有 skills |
| `.claude/docs/workflow-catalog.yaml` | 7阶段定义 & Step 元数据 | /help |
| `design/gdd/systems-index.md` | 系统依赖图 & 优先级 | /create-epics, /gate-check |
| `design/registry/entities.yaml` | 游戏实体注册表 | /consistency-check |
| `docs/registry/architecture.yaml` | 架构决策索引 | /architecture-review |
| `docs/architecture/tr-registry.yaml` | 技术需求可追溯矩阵 | /architecture-review |
| `production/sprints/` | Sprint 计划文件 | /sprint-status, /gate-check |
| `production/session-state/` | 会话状态快照 | 会话 Hooks |
| `production/review-mode.txt` | 评审模式配置 | /start, /dev-story |

---

## 9. 目录结构总览

```
Claude-Code-Game-Studios/
├── CLAUDE.md                    # 主配置（系统行为入口）
├── README.md                    # 项目说明
├── UPGRADING.md                 # 升级指南
│
├── .claude/
│   ├── settings.json            # Hooks 权限、安全规则
│   ├── statusline.sh            # 会话状态栏脚本
│   ├── agents/                  # 48 个 Agent 定义
│   ├── skills/                  # 74 个 Skill（每个子目录一个 SKILL.md）
│   ├── rules/                   # 11 个路径作用域规则
│   ├── hooks/                   # 12 个自动化 Hook 脚本
│   ├── agent-memory/            # Agent 持久记忆存储
│   └── docs/
│       ├── workflow-catalog.yaml    # 7阶段流水线定义
│       ├── templates/               # 39 个文档模板
│       ├── hooks-reference/         # 6 个 Hook 说明文档
│       └── *.md                     # 11 个系统参考文档
│
├── design/
│   ├── CLAUDE.md
│   ├── gdd/                     # 游戏设计文档（运行时生成）
│   ├── narrative/               # 叙事文档（运行时生成）
│   └── registry/entities.yaml  # 游戏实体注册表
│
├── docs/
│   ├── WORKFLOW-GUIDE.md        # 完整工作流指南
│   ├── COLLABORATIVE-DESIGN-PRINCIPLE.md
│   ├── engine-reference/        # 引擎参考（Godot/Unity/UE5）
│   ├── examples/                # 11 个示例会话
│   ├── architecture/            # ADR 目录（运行时生成）
│   └── registry/architecture.yaml
│
├── src/                         # 游戏源代码（运行时生成）
├── assets/                      # 游戏资产（运行时生成）
├── tests/                       # 测试套件（运行时生成）
├── prototypes/                  # 原型代码（运行时生成）
├── production/                  # Sprint/里程碑跟踪（运行时生成）
└── tools/                       # 构建工具（运行时生成）
```

---

## 10. 关键设计决策

### 10.1 协作而非自治

系统的核心设计原则是「协作式顾问」而非「自治生成」：
- Agent 提问 → 呈现选项（含利弊分析）→ 用户决策 → Agent 起草 → 用户审批 → Agent 写入
- 任何文件写入前必须获得用户明确授权（"May I write to X?"）

### 10.2 门禁驱动的阶段推进

每个阶段结束通过 `/gate-check` 产出 PASS/CONCERNS/FAIL 裁定。裁定是**建议性的**，用户始终可以选择是否推进，但门禁会记录所有未解决的问题。

### 10.3 垂直委托的信息安全

Agent 不能修改其职责域外的文件，防止职责混乱和文件互相覆盖。跨域操作必须通过 producer 显式委托。

### 10.4 多层验证体系

```
代码质量 → Rules（路径作用域规则）
文档完整性 → Hooks（detect-gaps）
阶段就绪 → gate-check（7阶段门禁）
跨文档一致性 → consistency-check
设计质量 → design-review + review-all-gdds
```

---

## 11. 扩展点（新功能接入位置）

| 扩展类型 | 接入位置 | 说明 |
|---------|---------|------|
| 新 Agent | `.claude/agents/` 新增 .md | 必须包含 YAML frontmatter |
| 新 Skill | `.claude/skills/新目录/SKILL.md` | 加入 workflow-catalog.yaml |
| 新 Hook | `.claude/hooks/` 新增 .sh | 在 settings.json 注册 |
| 新代码规则 | `.claude/rules/` 新增 .md | 设定 paths: frontmatter |
| 新文档模板 | `.claude/docs/templates/` 新增 .md | 在对应 Skill 中引用 |
| 新引擎支持 | `docs/engine-reference/新引擎/` | 配套 agent 文件 |

---

## 12. 性能与成本考量

| 模型层级 | 适用场景 | 典型 Skill |
|---------|---------|-----------|
| Haiku | 只读状态检查、格式化、简单查询 | /help, /sprint-status, /story-readiness |
| Sonnet | 实现、设计、单系统分析 | /dev-story, /design-system（默认）|
| Opus | 多文档综合、高风险门禁、跨系统评审 | /review-all-gdds, /architecture-review, /gate-check |

**成本控制原则**：
- 只在综合性任务使用 Opus
- Haiku 用于只读 + 格式化工作
- /clear 在长会话后强制清理上下文
- pre-compact.sh Hook 在压缩前保存关键状态到磁盘
