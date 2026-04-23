# 升级 Claude Code Game Studios

本指南介绍如何将现有游戏项目仓库从一个模板版本升级到下一个版本。

**查找当前版本**，请在 git 日志中执行：
```bash
git log --oneline | grep -i "release\|setup"
```
或在 `README.md` 中查看版本徽章。

---

## 目录

- [升级策略](#升级策略)
- [v0.4.x → v1.0](#v04x--v10)
- [v0.4.0 → v0.4.1](#v040--v041)
- [v0.3.0 → v0.4.0](#v030--v040)
- [v0.2.0 → v0.3.0](#v020--v030)
- [v0.1.0 → v0.2.0](#v010--v020)

---

## 升级策略

拉取模板更新有三种方式。请根据你的仓库设置情况选择合适的策略。

### 策略 A — Git 远端合并（推荐）

**最适合**：你从模板克隆了仓库，并在其基础上有自己的提交。

```bash
# 将模板添加为远端（一次性设置）
git remote add template https://github.com/Donchitos/Claude-Code-Game-Studios.git

# 拉取新版本
git fetch template main

# 合并到你的分支
git merge template/main --allow-unrelated-histories
```

Git 只会标记那些模板和你都修改过的文件中的冲突。逐一解决冲突——保留你的游戏内容，接受结构性改进。然后提交合并结果。

**提示**：最容易冲突的文件是 `CLAUDE.md` 和
`.claude/docs/technical-preferences.md`，因为你已经在其中填入了引擎和项目设置。请保留你的内容，接受结构性变更。

---

### 策略 B — 精挑特定提交（cherry-pick）

**最适合**：你只需要某个特定功能（例如仅需要新技能，不需要完整更新）。

```bash
git remote add template https://github.com/Donchitos/Claude-Code-Game-Studios.git
git fetch template main

# 精挑你需要的特定提交
git cherry-pick <commit-sha>
```

各版本的提交 SHA 值列在下方各版本章节中。

---

### 策略 C — 手动复制文件

**最适合**：你没有用 git 来设置模板（只是下载了 zip 包）。

1. 在你的仓库旁边下载或克隆新版本。
2. 直接复制 **"可安全覆盖"** 列表中的文件。
3. 对于 **"需谨慎合并"** 列表中的文件，并排打开两个版本，手动合并结构性变更，同时保留你的内容。

---

## v0.4.1

**发布时间**：2026-04-02
**核心主题**：美术方向集成、资产规格流水线

### 变更内容

| 类别 | 变更 |
|------|------|
| **新技能** | `/art-bible` — 逐节引导式视觉标识撰写（共 9 节）。每节必须产生美术总监（art-director）Task 子任务。AD-ART-BIBLE 签发门禁。技术准备阶段必须运行。 |
| **新技能** | `/asset-spec` — 每个资产的视觉规格与 AI 生成提示词生成器。读取美术圣经 + GDD/关卡/角色文档。输出至 `design/assets/specs/` 目录及 `design/assets/asset-manifest.md`。支持全量/精简/单人三种模式。 |
| **新总监门禁（3 个）** | `AD-CONCEPT-VISUAL`（头脑风暴第 4 阶段）、`AD-ART-BIBLE`（美术圣经签发）、`AD-PHASE-GATE`（门禁检查面板） |
| **`/brainstorm` 更新** | 在允许工具列表中添加了 `Task`（此前缺失——导致所有总监子任务无法启动）。锁定支柱后，美术总监与创意总监并行启动。视觉身份锚点写入 game-concept.md。 |
| **`/gate-check` 更新** | 美术总监作为第 4 个并行总监加入（AD-PHASE-GATE）。视觉工件检查：视觉身份锚点（概念门禁）、美术圣经（技术准备门禁）、AD-ART-BIBLE 签发 + 角色视觉档案（预制作门禁）。 |
| **`/team-level` 更新** | 美术总监加入步骤 1 并行启动（在布局之前确立视觉方向）。关卡设计师现在将美术总监的目标作为明确约束条件。步骤 4 美术总监的角色修正为仅负责制作概念。 |
| **`/team-narrative` 更新** | 美术总监加入第 2 阶段并行启动（角色视觉设计、环境叙事、电影感基调）。 |
| **`/design-system` 更新** | 路由表扩展，加入美术总监 + 技术美术，适用于战斗、UI、对话、动画/VFX、角色等类别。7 类系统类别的视觉/音频部分现为必填项（附美术总监 Task 子任务）。 |
| **`workflow-catalog.yaml`** | `/art-bible` 添加至技术准备阶段（必须）。`/asset-spec` 添加至预制作阶段（可选，可重复运行）。 |

### 可安全覆盖的文件

**需新增的文件：**
```
.claude/skills/art-bible/SKILL.md
.claude/skills/asset-spec/SKILL.md
.claude/docs/director-gates.md
```

**可直接覆盖的现有文件（无用户内容）：**
```
.claude/skills/brainstorm/SKILL.md
.claude/skills/gate-check/SKILL.md
.claude/skills/team-level/SKILL.md
.claude/skills/team-narrative/SKILL.md
.claude/skills/design-system/SKILL.md
.claude/docs/workflow-catalog.yaml
README.md
UPGRADING.md
```

### 需谨慎合并的文件

无——本次所有变更均为无用户内容的基础设施文件。

---

## v0.4.x → v1.0

**发布时间**：2026-03-29
**提交范围**：`6c041ac..HEAD`
**核心主题**：总监门禁系统、门禁强度模式、Godot C# 专家

### 变更内容

| 类别 | 变更 |
|------|------|
| **新系统** | 总监门禁——跨所有工作流技能共享的具名审查检查点。定义于 `.claude/docs/director-gates.md` |
| **新功能** | 门禁强度模式：`full`（全部总监门禁）、`lean`（仅阶段门禁）、`solo`（无总监）。通过 `/start` 期间的 `production/review-mode.txt` 全局设置，或在任何启用门禁的技能上用 `--review [mode]` 覆盖单次运行 |
| **新 Agent** | `godot-csharp-specialist` — Godot 4 项目的 C# 代码质量专家 |
| **技能更新（13 个）** | 所有启用门禁的技能现在可解析 `--review [full\|lean\|solo]` 并在参数提示中包含该选项：`brainstorm`、`map-systems`、`design-system`、`architecture-decision`、`create-architecture`、`create-epics`、`create-stories`、`sprint-plan`、`milestone-review`、`playtest-report`、`prototype`、`story-done`、`gate-check` |
| **`/start` 更新** | 新增第 3b 阶段——在引导流程中设置审查模式，写入 `production/review-mode.txt` |
| **`/setup-engine` 更新** | 为 Godot 新增语言选择步骤（GDScript 或 C#） |
| **文档** | `director-gates.md` — 完整门禁目录；`WORKFLOW-GUIDE.md` — 总监审查模式章节；`README.md` — 门禁强度自定义说明 |

---

### 可安全覆盖的文件

**需新增的文件：**
```
.claude/agents/godot-csharp-specialist.md
.claude/docs/director-gates.md
```

**可直接覆盖的现有文件（无用户内容）：**
```
.claude/skills/brainstorm/SKILL.md
.claude/skills/map-systems/SKILL.md
.claude/skills/design-system/SKILL.md
.claude/skills/architecture-decision/SKILL.md
.claude/skills/create-architecture/SKILL.md
.claude/skills/create-epics/SKILL.md
.claude/skills/create-stories/SKILL.md
.claude/skills/sprint-plan/SKILL.md
.claude/skills/milestone-review/SKILL.md
.claude/skills/playtest-report/SKILL.md
.claude/skills/prototype/SKILL.md
.claude/skills/story-done/SKILL.md
.claude/skills/gate-check/SKILL.md
.claude/skills/start/SKILL.md
.claude/skills/quick-design/SKILL.md
.claude/skills/setup-engine/SKILL.md
README.md
docs/WORKFLOW-GUIDE.md
UPGRADING.md
```

---

### 需谨慎合并的文件

本次发布无需手动合并的文件。所有变更均为无用户内容的基础设施文件。

---

### 新功能详解

#### 总监门禁系统

所有主要工作流技能现在引用 `.claude/docs/director-gates.md` 中定义的具名门禁检查点。门禁通过领域前缀和名称标识（例如 `CD-CONCEPT`、`TD-ARCHITECTURE`、`LP-CODE-REVIEW`）。每个门禁定义了要启动的总监、需要传入的输入内容、裁定结果的含义，以及精简/单人模式下的行为。

技能使用 `Task` 并传入门禁 ID 和文档化的输入内容来启动门禁，而不是将总监提示词内联在技能正文中。这使技能主体保持整洁，并确保门禁行为在所有工作流阶段保持一致。

#### 门禁强度模式

三种模式让你控制总监审查的介入程度：

- **`full`**（默认）— 所有总监门禁在每个审查检查点都运行
- **`lean`** — 跳过技能内的总监审查；`/gate-check` 中的阶段门禁仍然运行
- **`solo`** — 任何地方都不运行总监门禁；`/gate-check` 仅检查工件是否存在

在 `/start` 期间全局设置（写入 `production/review-mode.txt`）。可在任何启用门禁的技能上用 `--review [mode]` 覆盖单次运行：

```
/design-system combat --review lean
/gate-check concept --review full
/brainstorm my-game-idea --review solo
```

---

### 升级后操作

1. 运行一次 `/start` 来设置你偏好的审查模式——或者手动创建 `production/review-mode.txt`，内容为 `full`、`lean` 或 `solo`。
2. 如果你处于项目进行中，请查阅 `.claude/docs/director-gates.md`，了解哪些门禁适用于你当前的阶段。
3. 运行 `/skill-test static all` 验证所有技能通过结构检查。

---

## v0.4.0 → v0.4.1

**发布时间**：2026-03-26
**提交范围**：`04ed5d5..HEAD`
**核心主题**：通用化 Agent、新技能、技能修复

### 变更内容

| 类别 | 变更 |
|------|------|
| **新技能（1 个）** | `/consistency-check` — 跨 GDD 实体一致性扫描器 |
| **技能修复（所有 team-*）** | 新增无参数守卫、正式 `Verdict: COMPLETE / BLOCKED` 关键词、逐步骤 AskUserQuestion 门禁、相邻区域依赖检查（team-level）、伦理执行（team-live-ops）、附阶段跳过的 NO-GO 路径（team-release） |
| **Agent 修复（4 个）** | 游戏设计师、系统设计师、经济系统设计师、运营活动设计师的语言通用化——删除了 RPG 特定术语 |

---

### 可安全覆盖的文件

**需新增的文件：**
```
.claude/skills/consistency-check/SKILL.md
```

**可直接覆盖的现有文件（无用户内容）：**
```
.claude/skills/team-combat/SKILL.md      ← 无参数守卫、裁定关键词、门禁改进
.claude/skills/team-narrative/SKILL.md   ← 无参数守卫、裁定关键词、门禁改进
.claude/skills/team-ui/SKILL.md          ← 无参数守卫、裁定关键词、门禁改进
.claude/skills/team-release/SKILL.md     ← 无参数守卫、裁定关键词、NO-GO 路径
.claude/skills/team-polish/SKILL.md      ← 无参数守卫、裁定关键词、门禁改进
.claude/skills/team-audio/SKILL.md       ← 无参数守卫、裁定关键词、门禁改进
.claude/skills/team-level/SKILL.md       ← 无参数守卫、裁定关键词、相邻区域检查
.claude/skills/team-live-ops/SKILL.md    ← 无参数守卫、裁定关键词、伦理执行
.claude/skills/team-qa/SKILL.md          ← 无参数守卫、裁定关键词、门禁改进
.claude/skills/map-systems/SKILL.md      ← 裁定关键词
.claude/skills/create-epics/SKILL.md     ← "May I write" 协议修复、裁定关键词
.claude/skills/create-stories/SKILL.md   ← 裁定关键词
.claude/agents/game-designer.md          ← 语言通用化
.claude/agents/systems-designer.md       ← 语言通用化
.claude/agents/economy-designer.md       ← 语言通用化
.claude/agents/live-ops-designer.md      ← 语言通用化
```

---

### 需谨慎合并的文件

本次发布无需手动合并的文件。所有变更均为无用户内容的基础设施文件。

---

### 升级后操作

1. 运行 `/skill-test catalog` 验证所有技能已被索引。
2. 编辑任何技能后，运行 `/skill-test lint [skill-name]` 检查结构合规性。
3. 如果你自定义过任何 team-* 技能，请查阅更新后的版本——无参数守卫和 `Verdict:` 关键词现在是所有 team-* 技能的必填要求。

---

## v0.3.0 → v0.4.0

**发布时间**：2026-03-21
**提交范围**：`b1cad29..HEAD`
**核心主题**：完整 UX/UI 流水线、完整用户故事生命周期、存量项目迁入、全面 QA/测试框架、流水线完整性，新增 29 个技能

### 变更内容

| 类别 | 变更 |
|------|------|
| **新技能（17 个）** | `/ux-design`、`/ux-review`、`/help`、`/quick-design`、`/review-all-gdds`、`/story-readiness`、`/story-done`、`/sprint-status`、`/adopt`、`/create-architecture`、`/create-control-manifest`、`/create-epics`、`/create-stories`、`/dev-story`、`/propagate-design-change`、`/content-audit`、`/architecture-review` |
| **新技能 QA（12 个）** | `/qa-plan`、`/smoke-check`、`/soak-test`、`/regression-suite`、`/test-setup`、`/test-helpers`、`/test-evidence-review`、`/test-flakiness`、`/skill-test`、`/bug-triage`、`/team-live-ops`、`/team-qa` |
| **新钩子（4 个）** | `log-agent-stop.sh` — Agent 审计追踪停止；`notify.sh` — Windows 桌面通知；`post-compact.sh` — 压缩后会话恢复提醒；`validate-skill-change.sh` — 技能编辑后建议运行 `/skill-test` |
| **新模板（8 个）** | `ux-spec.md`、`hud-design.md`、`accessibility-requirements.md`、`interaction-pattern-library.md`、`player-journey.md`、`difficulty-curve.md` 以及 2 个迁入计划模板 |
| **新基础设施** | `workflow-catalog.yaml`（7 阶段流水线，供 `/help` 读取）、`docs/architecture/tr-registry.yaml`（稳定的 TR-ID）、`production/sprint-status.yaml` 数据结构 |
| **技能更新** | `/gate-check` — 3 个门禁现在需要 UX 工件；预制作门禁需要垂直切片（硬门禁） |
| **技能更新** | `/sprint-plan` — 写入 `sprint-status.yaml`；`/sprint-status` 读取它 |
| **技能更新** | `/story-done` — 8 阶段完成审查，更新用户故事文件，显示下一个就绪用户故事 |
| **技能更新** | `/design-review` — 移除架构缺口检查（阶段不对应） |
| **技能更新** | `/team-ui` — 完整 UX 流水线（ux-design → ux-review → 团队阶段） |
| **Agent 更新** | 14 个专家 Agent — 添加 `memory: project` |
| **Agent 更新** | `prototyper` — `isolation: worktree`（原型工作在隔离的 git 分支中进行） |
| **模型路由** | 在协调规则中记录了 Haiku/Sonnet/Opus 层级分配；技能在 frontmatter 中声明所属层级 |
| **目录 CLAUDE.md** | 脚手架生成了 `design/CLAUDE.md`、`src/CLAUDE.md`、`docs/CLAUDE.md` — 各目录的路径作用域指令 |
| **流水线完整性** | TR-ID 稳定性、清单版本控制、ADR 状态门禁、TR-ID 引用而非直接引用 |
| **GDD 模板** | 新增 `## 游戏手感` 章节（输入响应性、动画目标、冲击时刻） |

---

### 可安全覆盖的文件

**需新增的文件：**
```
.claude/skills/ux-design/SKILL.md
.claude/skills/ux-review/SKILL.md
.claude/skills/help/SKILL.md
.claude/skills/quick-design/SKILL.md
.claude/skills/review-all-gdds/SKILL.md
.claude/skills/story-readiness/SKILL.md
.claude/skills/story-done/SKILL.md
.claude/skills/sprint-status/SKILL.md
.claude/skills/adopt/SKILL.md
.claude/skills/create-architecture/SKILL.md
.claude/skills/create-control-manifest/SKILL.md
.claude/skills/create-epics/SKILL.md
.claude/skills/create-stories/SKILL.md
.claude/skills/dev-story/SKILL.md
.claude/skills/propagate-design-change/SKILL.md
.claude/skills/content-audit/SKILL.md
.claude/skills/architecture-review/SKILL.md
.claude/skills/qa-plan/SKILL.md
.claude/skills/smoke-check/SKILL.md
.claude/skills/soak-test/SKILL.md
.claude/skills/regression-suite/SKILL.md
.claude/skills/test-setup/SKILL.md
.claude/skills/test-helpers/SKILL.md
.claude/skills/test-evidence-review/SKILL.md
.claude/skills/test-flakiness/SKILL.md
.claude/skills/skill-test/SKILL.md
.claude/skills/bug-triage/SKILL.md
.claude/skills/team-live-ops/SKILL.md
.claude/skills/team-qa/SKILL.md
.claude/hooks/log-agent-stop.sh
.claude/hooks/notify.sh
.claude/hooks/post-compact.sh
.claude/hooks/validate-skill-change.sh
.claude/docs/workflow-catalog.yaml
.claude/docs/templates/ux-spec.md
.claude/docs/templates/hud-design.md
.claude/docs/templates/accessibility-requirements.md
.claude/docs/templates/interaction-pattern-library.md
.claude/docs/templates/player-journey.md
.claude/docs/templates/difficulty-curve.md
design/CLAUDE.md
src/CLAUDE.md
docs/CLAUDE.md
```

**可直接覆盖的现有文件（无用户内容）：**
```
.claude/skills/gate-check/SKILL.md
.claude/skills/sprint-plan/SKILL.md
.claude/skills/sprint-status/SKILL.md
.claude/skills/design-review/SKILL.md
.claude/skills/team-ui/SKILL.md
.claude/skills/story-readiness/SKILL.md
.claude/skills/story-done/SKILL.md
.claude/docs/templates/game-design-document.md    ← 添加游戏手感章节
README.md
docs/WORKFLOW-GUIDE.md
UPGRADING.md
```

**Agent 文件可覆盖**（前提是你未在其中写入自定义提示词）：
```
.claude/agents/prototyper.md         ← 添加 isolation: worktree
.claude/agents/art-director.md       ← 添加 memory: project
.claude/agents/audio-director.md     ← 添加 memory: project
.claude/agents/economy-designer.md   ← 添加 memory: project
.claude/agents/game-designer.md      ← 添加 memory: project
.claude/agents/gameplay-programmer.md ← 添加 memory: project
.claude/agents/lead-programmer.md    ← 添加 memory: project
.claude/agents/level-designer.md     ← 添加 memory: project
.claude/agents/narrative-director.md ← 添加 memory: project
.claude/agents/systems-designer.md   ← 添加 memory: project
.claude/agents/technical-artist.md   ← 添加 memory: project
.claude/agents/ui-programmer.md      ← 添加 memory: project
.claude/agents/ux-designer.md        ← 添加 memory: project
.claude/agents/world-builder.md      ← 添加 memory: project
```

---

### 需谨慎合并的文件

#### `.claude/settings.json`

本版本新注册了四个钩子。如果你未自定义 `settings.json`，覆盖是安全的。否则，请手动添加以下钩子条目：

- `log-agent-stop.sh` — `SubagentStop` 事件（Agent 审计追踪停止）
- `notify.sh` — `Notification` 事件（Windows 桌面通知）
- `post-compact.sh` — `PostCompact` 事件（会话恢复提醒）
- `validate-skill-change.sh` — `PostToolUse` 事件，过滤 `.claude/skills/` 的写入

#### 自定义 Agent 文件

如果你在 Agent `.md` 文件中添加了项目专属知识，请执行 diff 并手动将 `memory: project` 行添加到合适的 YAML frontmatter 中。创意总监和技术总监 Agent 有意保留 `memory: user`——只有专家 Agent 才需要 `memory: project`。

---

### 新功能详解

#### 完整用户故事生命周期

用户故事现在有两个技能强制执行的正式生命周期：

- **`/story-readiness`** — 在开发者认领用户故事之前验证其是否已具备实施条件。检查设计（GDD 需求已关联）、架构（ADR 已被采纳）、范围（验收标准可测试）和 DoD（清单版本当前）。裁定结果：READY / NEEDS WORK / BLOCKED。
- **`/story-done`** — 实施完成后的 8 阶段完成审查。验证每条验收标准、检查 GDD/ADR 偏差、触发代码审查、将用户故事文件更新为 `Status: Complete`，并显示下一个就绪用户故事。

流程：`/story-readiness` → 实施 → `/story-done` → 下一个用户故事

#### 完整 UX/UI 流水线

- **`/ux-design`** — 逐节引导式 UX 规格撰写。三种模式：屏幕/流程、HUD 或交互模式库。读取 GDD UI 需求和玩家旅程。输出至 `design/ux/`。
- **`/ux-review`** — 根据 GDD 对齐度、无障碍等级和模式库验证 UX 规格。裁定结果：APPROVED / NEEDS REVISION / MAJOR REVISION。
- **`/team-ui`** 已更新：第 1 阶段现在将 `/ux-design` + `/ux-review` 作为视觉设计开始前的硬门禁。

#### 存量项目迁入

**`/adopt`** 将现有项目迁入模板格式。审计 GDD、ADR、用户故事、系统索引和基础设施的内部结构。将缺口分级（BLOCKING/HIGH/MEDIUM/LOW）。构建有序迁移计划。不会重新生成现有工件——只填补缺口。

参数模式：`full | gdds | adrs | stories | infra`

另外：`/design-system retrofit [path]` 和 `/architecture-decision retrofit [path]` 可检测现有文件并仅添加缺失章节。

#### 迭代追踪 YAML

`production/sprint-status.yaml` 现在是权威的用户故事追踪格式：
- 由 `/sprint-plan` 写入（初始化所有用户故事），由 `/story-done` 写入（设置状态为 `done`）
- 由 `/sprint-status`（快速快照）和 `/help`（生产阶段的逐故事状态）读取
- 状态值：`backlog | ready-for-dev | in-progress | review | done | blocked`
- 文件不存在时，优雅地回退到 Markdown 扫描

#### `/help` — 上下文感知的下一步建议

`/help` 读取你的当前阶段和进行中的工作，检查哪些工件已完成，并精确告诉你下一步该做什么——一个必须完成的主要步骤，加上可选的机会点。与 `/start`（仅首次使用）和 `/project-stage-detect`（完整审计）不同。

#### 全面 QA 和测试框架

9 个新的 QA/测试技能，覆盖完整测试生命周期：

- **`/test-setup`** — 为你的引擎搭建测试框架和 CI/CD 流水线
- **`/test-helpers`** — 生成引擎专属测试辅助库（GDUnit4、NUnit 等）
- **`/qa-plan`** — 为迭代或功能生成 QA 测试计划，按测试类型对用户故事进行分类
- **`/smoke-check`** — 在移交 QA 前运行关键路径冒烟测试门禁
- **`/soak-test`** — 为长时游戏会话生成浸泡测试协议（稳定性、内存泄漏）
- **`/regression-suite`** — 将测试覆盖率映射到 GDD 关键路径，识别缺少回归测试的已修复 bug
- **`/test-evidence-review`** — 对测试文件和手动测试证据文档进行质量审查
- **`/test-flakiness`** — 通过读取 CI 运行日志检测不稳定测试
- **`/skill-test`** — 验证技能文件的结构合规性和行为正确性（三种模式：lint、spec、catalog）

另有新增：**`/bug-triage`** 重新评估所有未解决 bug 的优先级、严重级别和所有权。

#### 技能验证器（`/skill-test`）

`/skill-test` 是用于验证测试工具本身的元技能。编辑任何技能文件后运行它。三种模式：
- `lint` — 验证 YAML frontmatter 和必填字段
- `spec [skill-name]` — 针对特定技能运行行为规格测试
- `catalog` — 检查 `.claude/skills/` 中的所有技能是否已在目录中被索引

新的 `validate-skill-change.sh` 钩子会在技能文件被修改时自动提醒你运行 `/skill-test`。

#### 团队运营和团队 QA 编排

- **`/team-live-ops`** — 协调运营活动设计师 + 经济系统设计师 + 社区运营 + 数据分析工程师，完成发布后内容规划（赛季活动、战令、留存）
- **`/team-qa`** — 编排 QA 负责人 + QA 测试员 + 游戏玩法程序员 + 制作人，完成完整 QA 周期：策略、执行、覆盖率和签发

#### 模型层级路由

技能现在根据任务复杂度明确分配到 Haiku、Sonnet 或 Opus 层级。只读状态检查使用 Haiku；复杂多文档综合使用 Opus；其余默认为 Sonnet。层级分配记录在 `.claude/docs/coordination-rules.md` 中。

#### 目录 CLAUDE.md 文件

三个新的目录作用域 CLAUDE.md 文件（`design/`、`src/`、`docs/`）为在这些目录中工作的 Agent 提供路径专属指令。当 Claude Code 读取该目录中的文件时，这些文件会自动加载。

---

### 升级后操作

1. **验证新钩子**已在 `.claude/settings.json` 中注册——检查全部四个：`log-agent-stop.sh`、`notify.sh`、`post-compact.sh`、`validate-skill-change.sh`。

2. **测试审计追踪**，启动任意子智能体——启动和停止事件都应出现在 `production/session-logs/` 中。

3. **生成 sprint-status.yaml**（如果你处于活跃生产阶段）：
   ```
   /sprint-plan status
   ```

4. **运行 `/adopt`**（如果你有早于本模板版本的现有 GDD 或 ADR）——它会识别哪些章节需要补充，而不覆盖你的内容。

5. **编辑任何技能后用 `/skill-test` 验证**——新的 `validate-skill-change.sh` 钩子会自动提醒你执行此操作。

---

## v0.2.0 → v0.3.0

**发布时间**：2026-03-09
**提交范围**：`e289ce9..HEAD`
**核心主题**：`/design-system` GDD 撰写、`/map-systems` 重命名、自定义状态栏

### 破坏性变更

#### `/design-systems` 重命名为 `/map-systems`

`/design-systems` 技能已重命名为 `/map-systems`，以提高清晰度（分解 = *映射*，而非 *设计*）。

**需执行的操作**：更新所有引用 `/design-systems` 的文档、笔记或脚本，新的调用方式为 `/map-systems`。

### 变更内容

| 类别 | 变更 |
|------|------|
| **新技能** | `/design-system`（逐节引导式 GDD 撰写） |
| **重命名技能** | `/design-systems` → `/map-systems`（破坏性重命名） |
| **新文件** | `.claude/statusline.sh`、`.claude/settings.json` 状态栏配置 |
| **技能更新** | `/gate-check` — 通过时写入 `production/stage.txt`，新的阶段定义 |
| **技能更新** | `brainstorm`、`start`、`design-review`、`project-stage-detect`、`setup-engine` — 交叉引用修复 |
| **Bug 修复** | `log-agent.sh`、`validate-commit.sh` — 钩子执行修复 |
| **文档** | 新增 `UPGRADING.md`、更新 `README.md`、更新 `WORKFLOW-GUIDE.md` |

---

### 可安全覆盖的文件

**需新增的文件：**
```
.claude/skills/design-system/SKILL.md
.claude/statusline.sh
```

**可直接覆盖的现有文件（无用户内容）：**
```
.claude/skills/map-systems/SKILL.md      ← 原为 design-systems/SKILL.md
.claude/skills/gate-check/SKILL.md
.claude/skills/brainstorm/SKILL.md
.claude/skills/start/SKILL.md
.claude/skills/design-review/SKILL.md
.claude/skills/project-stage-detect/SKILL.md
.claude/skills/setup-engine/SKILL.md
.claude/hooks/log-agent.sh
.claude/hooks/validate-commit.sh
README.md
docs/WORKFLOW-GUIDE.md
UPGRADING.md
```

**需删除（已被重命名替代）：**
```
.claude/skills/design-systems/   ← 整个目录；已被 map-systems/ 替代
```

---

### 需谨慎合并的文件

#### `.claude/settings.json`

新版本添加了指向 `.claude/statusline.sh` 的 `statusLine` 配置块。如果你未自定义 `settings.json`，覆盖是安全的。否则，请手动添加以下块：

```json
"statusLine": {
  "script": ".claude/statusline.sh"
}
```

---

### 新功能详解

#### 自定义状态栏

`.claude/statusline.sh` 在终端状态栏显示 7 阶段生产流水线面包屑导航：

```
ctx: 42% | claude-sonnet-4-6 | Systems Design
```

在生产/精磨/发布阶段，若 `production/session-state/active.md` 中存在 `<!-- STATUS -->` 块，还会显示当前 Epic/功能/任务的详细信息：

```
ctx: 42% | claude-sonnet-4-6 | Production | Combat System > Melee Combat > Hitboxes
```

当前阶段会从项目工件中自动检测，也可以通过向 `production/stage.txt` 写入阶段名称来手动固定。

#### `/gate-check` 阶段推进

当门禁 PASS 裁定被确认时，`/gate-check` 现在会将新的阶段名称写入 `production/stage.txt`。这会立即为所有后续会话更新状态栏，无需手动编辑文件。

---

### 升级后操作

1. **删除旧技能目录：**
   ```bash
   rm -rf .claude/skills/design-systems/
   ```

2. **测试状态栏**，启动一个 Claude Code 会话——你应该在终端页脚看到阶段面包屑导航。

3. **验证钩子执行**仍正常工作：
   ```bash
   bash .claude/hooks/log-agent.sh '{}' '{}'
   bash .claude/hooks/validate-commit.sh '{}' '{}'
   ```

---

## v0.1.0 → v0.2.0

**发布时间**：2026-02-21
**提交范围**：`ad540fe..e289ce9`
**核心主题**：上下文韧性、AskUserQuestion 集成、`/map-systems` 技能

### 变更内容

| 类别 | 变更 |
|------|------|
| **新技能** | `/start`（引导流程）、`/map-systems`（系统分解）、`/design-system`（逐节引导式 GDD 撰写） |
| **新钩子** | `session-start.sh`（会话恢复）、`detect-gaps.sh`（缺口检测） |
| **新模板** | `systems-index.md`、3 个协作协议模板 |
| **上下文管理** | 大幅重写——新增基于文件的状态策略 |
| **Agent 更新** | 14 个设计/创意 Agent — AskUserQuestion 集成 |
| **技能更新** | 全部 7 个 `team-*` 技能 + `brainstorm` — 在阶段过渡时集成 AskUserQuestion |
| **CLAUDE.md** | 从约 159 行精简至约 60 行；5 个文档导入代替 10 个 |
| **钩子更新** | 全部 8 个钩子 — Windows 兼容性修复、新功能 |
| **已删除文档** | `docs/IMPROVEMENTS-PROPOSAL.md`、`docs/MULTI-STAGE-DOCUMENT-WORKFLOW.md` |

---

### 可安全覆盖的文件

以下为纯基础设施文件——你未对其进行自定义。可直接复制新版本，不会有任何项目内容风险。

**需新增的文件：**
```
.claude/skills/start/SKILL.md
.claude/skills/map-systems/SKILL.md
.claude/skills/design-system/SKILL.md
.claude/docs/templates/systems-index.md
.claude/docs/templates/collaborative-protocols/design-agent-protocol.md
.claude/docs/templates/collaborative-protocols/implementation-agent-protocol.md
.claude/docs/templates/collaborative-protocols/leadership-agent-protocol.md
.claude/hooks/detect-gaps.sh
.claude/hooks/session-start.sh
production/session-state/.gitkeep
docs/examples/README.md
.github/ISSUE_TEMPLATE/bug_report.md
.github/ISSUE_TEMPLATE/feature_request.md
.github/PULL_REQUEST_TEMPLATE.md
```

**可直接覆盖的现有文件（无用户内容）：**
```
.claude/skills/brainstorm/SKILL.md
.claude/skills/design-review/SKILL.md
.claude/skills/gate-check/SKILL.md
.claude/skills/project-stage-detect/SKILL.md
.claude/skills/setup-engine/SKILL.md
.claude/skills/team-audio/SKILL.md
.claude/skills/team-combat/SKILL.md
.claude/skills/team-level/SKILL.md
.claude/skills/team-narrative/SKILL.md
.claude/skills/team-polish/SKILL.md
.claude/skills/team-release/SKILL.md
.claude/skills/team-ui/SKILL.md
.claude/hooks/log-agent.sh
.claude/hooks/pre-compact.sh
.claude/hooks/session-stop.sh
.claude/hooks/validate-assets.sh
.claude/hooks/validate-commit.sh
.claude/hooks/validate-push.sh
.claude/rules/design-docs.md
.claude/docs/hooks-reference.md
.claude/docs/skills-reference.md
.claude/docs/quick-start.md
.claude/docs/directory-structure.md
.claude/docs/context-management.md
docs/COLLABORATIVE-DESIGN-PRINCIPLE.md
docs/WORKFLOW-GUIDE.md
README.md
```

**Agent 文件可覆盖**（前提是你未在其中写入自定义提示词）：
```
.claude/agents/art-director.md
.claude/agents/audio-director.md
.claude/agents/creative-director.md
.claude/agents/economy-designer.md
.claude/agents/game-designer.md
.claude/agents/level-designer.md
.claude/agents/live-ops-designer.md
.claude/agents/narrative-director.md
.claude/agents/producer.md
.claude/agents/systems-designer.md
.claude/agents/technical-director.md
.claude/agents/ux-designer.md
.claude/agents/world-builder.md
.claude/agents/writer.md
```

如果你*确实*自定义了 Agent 提示词，请参阅下方"需谨慎合并"部分。

---

### 需谨慎合并的文件

以下文件同时包含模板结构和你的项目专属内容。**请勿覆盖**——请手动合并变更。

#### `CLAUDE.md`

模板版本已从约 159 行精简至约 60 行。核心结构变化：删除了 5 个文档导入，因为 Claude Code 无论如何都会自动加载它们（agent-roster、skills-reference、hooks-reference、rules-reference、review-workflow）。

**从你的版本保留的内容：**
- `## Technology Stack` 章节（你的引擎/语言选择）
- 你所做的任何项目专属添加

**从新版本采纳的内容：**
- 精简的导入列表（如果存在，删除 5 个多余的 `@` 导入）
- 更新的协作协议措辞

#### `.claude/docs/technical-preferences.md`

如果你运行过 `/setup-engine`，这个文件包含你的引擎配置、命名规范和性能预算。请全部保留。模板版本只是空占位符。

#### `.claude/docs/templates/game-concept.md`

次要结构更新——新增了指向 `/map-systems` 的 `## Next Steps` 章节。如果你想获得更新的引导，可将该章节添加到你的副本中，但这不是必须的。

#### `.claude/settings.json`

检查新版本是否添加了你需要的权限规则。变更较小（结构更新）。如果你未自定义 `settings.json`，覆盖是安全的。

#### 自定义 Agent 文件

如果你在任何 Agent `.md` 文件中添加了项目专属知识或自定义行为，请执行 diff 并手动添加新的 AskUserQuestion 集成章节，而不是直接覆盖。每个 Agent 的变更是在系统提示末尾添加了标准化的协作协议块。

---

### 需删除的文件

以下文件在 v0.2.0 中已被移除。如果你的仓库中存在这些文件，可以安全删除——它们已被更好组织的替代品所取代。

```
docs/IMPROVEMENTS-PROPOSAL.md          → 已被 WORKFLOW-GUIDE.md 取代
docs/MULTI-STAGE-DOCUMENT-WORKFLOW.md  → 内容已并入 context-management.md
```

---

### 升级后操作

1. **运行 `/project-stage-detect`** 验证系统能用新的检测逻辑正确读取你的项目。

2. **运行一次 `/start`**（如果你还没用过）——它现在能正确识别你的阶段，并跳过你已完成的引导步骤。

3. **检查 `production/session-state/`** 是否存在且已被 gitignore：
   ```bash
   ls production/session-state/
   cat .gitignore | grep session-state
   ```

4. **测试钩子执行**——如果你在 Windows 上，请验证新钩子在 Git Bash 中无报错运行：
   ```bash
   bash .claude/hooks/detect-gaps.sh '{}' '{}'
   bash .claude/hooks/session-start.sh '{}' '{}'
   ```

---

*后续每个新版本都将在本文件中添加对应章节。*
