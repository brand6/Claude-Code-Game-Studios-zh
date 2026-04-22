<p align="center">
  <h1 align="center">Claude Code Game Studios</h1>
  <p align="center">
    将一次 Claude Code 会话，变成一支完整的游戏开发工作室。
    <br />
    49 个 Agent。72 个技能。一支协同作战的 AI 团队。
  </p>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT 许可证"></a>
  <a href=".claude/agents"><img src="https://img.shields.io/badge/agents-49-blueviolet" alt="49 个 Agent"></a>
  <a href=".claude/skills"><img src="https://img.shields.io/badge/skills-72-green" alt="72 个技能"></a>
  <a href=".claude/hooks"><img src="https://img.shields.io/badge/hooks-12-orange" alt="12 个钩子"></a>
  <a href=".claude/rules"><img src="https://img.shields.io/badge/rules-11-red" alt="11 条规则"></a>
  <a href="https://docs.anthropic.com/en/docs/claude-code"><img src="https://img.shields.io/badge/built%20for-Claude%20Code-f5f5f5?logo=anthropic" alt="基于 Claude Code 构建"></a>
  <a href="https://www.buymeacoffee.com/donchitos3"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-Support%20this%20project-FFDD00?logo=buymeacoffee&logoColor=black" alt="请我喝咖啡"></a>
  <a href="https://github.com/sponsors/Donchitos"><img src="https://img.shields.io/badge/GitHub%20Sponsors-Support%20this%20project-ea4aaa?logo=githubsponsors&logoColor=white" alt="GitHub Sponsors"></a>
</p>

> 这是对原始仓库 [Donchitos/Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios/) 的中文翻译与本地化发布版本。若需对照英文原版或查看上游更新，请参考原仓库。

---

## 为什么要做这个项目

用 AI 独自开发游戏是一种很强大的方式——但单次聊天会话没有任何结构。没有人阻止你硬编码魔法数字、跳过设计文档，或写出面条代码。没有 QA 环节，没有设计评审，也没有人问你"这真的符合游戏的愿景吗？"

**Claude Code Game Studios** 通过赋予你的 AI 会话真实工作室的结构来解决这个问题。你不再只有一个万能助手，而是拥有 49 个专业 Agent，按工作室层级组织——守护愿景的总监层、各司其职的主管层，以及实际动手的专家层。每个 Agent 都有明确的职责范围、上报路径和质量门禁。

结果是：你仍然做每一个决定，但现在你有了一支会问对问题、早期发现错误、并从第一次头脑风暴到发布上线都保持项目条理的团队。

---

## 目录

- [包含内容](#包含内容)
- [工作室层级](#工作室层级)
- [斜杠命令](#斜杠命令)
- [快速开始](#快速开始)
- [升级迁移](#升级迁移)
- [项目结构](#项目结构)
- [运作原理](#运作原理)
- [设计哲学](#设计哲学)
- [自定义配置](#自定义配置)
- [平台支持](#平台支持)
- [社区](#社区)
- [支持本项目](#支持本项目)
- [许可证](#许可证)

---

## 包含内容

| 类别                | 数量  | 说明                                                                                                       |
| ----------------- | --- | -------------------------------------------------------------------------------------------------------- |
| **Agent（智能体）**    | 49  | 覆盖设计、编程、美术、音频、叙事、QA 和生产管理的专业子智能体                                                                         |
| **技能（Skill）**     | 72  | 每个工作流阶段对应的斜杠命令（`/start`、`/design-system`、`/create-epics`、`/create-stories`、`/dev-story`、`/story-done` 等） |
| **钩子（Hook）**      | 12  | 在提交、推送、资产变更、会话生命周期、Agent 审计追踪和缺口检测时自动触发的验证逻辑                                                             |
| **规则（Rules）**     | 11  | 按路径作用域划分的编码规范，在编辑游戏玩法、引擎、AI、UI、网络代码等时自动执行                                                                |
| **模板（Templates）** | 39  | GDD（游戏设计文档）、UX 规格、ADR（架构决策记录）、迭代计划、HUD 设计、无障碍等文档模板                                                       |

## 工作室层级

Agent 按照真实工作室的运作方式组织为三个层级：

```
第一层 — 总监层（Opus）
  creative-director    technical-director    producer

第二层 — 主管层（Sonnet）
  game-designer        lead-programmer       art-director
  audio-director       narrative-director    qa-lead
  release-manager      localization-lead

第三层 — 专家层（Sonnet/Haiku）
  gameplay-programmer  engine-programmer     ai-programmer
  network-programmer   tools-programmer      ui-programmer
  systems-designer     level-designer        economy-designer
  technical-artist     sound-designer        writer
  world-builder        ux-designer           prototyper
  performance-analyst  devops-engineer       analytics-engineer
  security-engineer    qa-tester             accessibility-specialist
  live-ops-designer    community-manager
```

### 引擎专家 Agent

模板包含三大主流引擎的 Agent 集合，按你的项目选择对应的那套：

| 引擎 | 负责 Agent | 子专家 |
|------|-----------|--------|
| **Godot 4** | `godot-specialist` | GDScript、着色器、GDExtension |
| **Unity** | `unity-specialist` | DOTS/ECS、Shader/VFX、Addressables、UI Toolkit |
| **Unreal Engine 5** | `unreal-specialist` | GAS、Blueprints、网络同步、UMG/CommonUI |

## 斜杠命令

在 Claude Code 中输入 `/` 即可使用全部 72 个技能：

**入门与导航**
`/start` `/help` `/project-stage-detect` `/setup-engine` `/adopt`

**游戏设计**
`/brainstorm` `/map-systems` `/design-system` `/quick-design` `/review-all-gdds` `/propagate-design-change`

**美术与资产**
`/art-bible` `/asset-spec` `/asset-audit`

**UX 与界面设计**
`/ux-design` `/ux-review`

**架构**
`/create-architecture` `/architecture-decision` `/architecture-review` `/create-control-manifest`

**用户故事与迭代**
`/create-epics` `/create-stories` `/dev-story` `/sprint-plan` `/sprint-status` `/story-readiness` `/story-done` `/estimate`

**评审与分析**
`/design-review` `/code-review` `/balance-check` `/content-audit` `/scope-check` `/perf-profile` `/tech-debt` `/gate-check` `/consistency-check`

**QA 与测试**
`/qa-plan` `/smoke-check` `/soak-test` `/regression-suite` `/test-setup` `/test-helpers` `/test-evidence-review` `/test-flakiness` `/skill-test` `/skill-improve`

**生产管理**
`/milestone-review` `/retrospective` `/bug-report` `/bug-triage` `/reverse-document` `/playtest-report`

**发布**
`/release-checklist` `/launch-checklist` `/changelog` `/patch-notes` `/hotfix`

**创意与内容**
`/prototype` `/onboard` `/localize`

**团队协调**（多 Agent 协同处理单个功能）
`/team-combat` `/team-narrative` `/team-ui` `/team-release` `/team-polish` `/team-audio` `/team-level` `/team-live-ops` `/team-qa`

## 快速开始

### 前置条件

- [Git](https://git-scm.com/)
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code)（`npm install -g @anthropic-ai/claude-code`）
- **推荐安装**：[jq](https://jqlang.github.io/jq/)（用于钩子验证）和 Python 3（用于 JSON 验证）

所有钩子在缺少可选工具时都会优雅降级——不会报错，只是不进行验证。

### 安装步骤

1. **克隆仓库或将其作为模板使用**：
   ```bash
   git clone https://github.com/Donchitos/Claude-Code-Game-Studios.git my-game
   cd my-game
   ```

2. **打开 Claude Code** 并启动会话：
   ```bash
   claude
   ```

3. **运行 `/start`** — 系统会询问你目前处于哪个阶段（毫无头绪、有模糊概念、有清晰设计、已有项目），然后引导你进入对应的工作流。不做任何假设。

   也可以直接跳转到你需要的技能：
   - `/brainstorm` — 从零开始探索游戏创意
   - `/setup-engine godot 4.6` — 如果已知引擎，直接配置
   - `/project-stage-detect` — 分析现有项目状态

## 升级迁移

已在使用旧版本模板？请参阅 [UPGRADING.md](UPGRADING.md)，其中包含逐步迁移说明、各版本变更说明，以及哪些文件可以直接覆盖、哪些需要手动合并。

## 项目结构

```
CLAUDE.md                           # 主配置文件
.claude/
  settings.json                     # 钩子、权限、安全规则
  agents/                           # 49 个 Agent 定义（Markdown + YAML frontmatter）
  skills/                           # 72 个斜杠命令（每个技能一个子目录）
  hooks/                            # 12 个钩子脚本（bash，跨平台）
  rules/                            # 11 条按路径作用域划分的编码规范
  statusline.sh                     # 状态行脚本（上下文占比、模型、阶段、功能模块面包屑）
  docs/
    workflow-catalog.yaml           # 7 阶段流水线定义（由 /help 读取）
    templates/                      # 39 个文档模板
src/                                # 游戏源代码
assets/                             # 美术、音频、VFX、着色器、数据文件
design/                             # GDD、叙事文档、关卡设计
docs/                               # 技术文档和 ADR
tests/                              # 测试套件（单元测试、集成测试、性能测试、试玩测试）
tools/                              # 构建和流水线工具
prototypes/                         # 一次性原型（与 src/ 隔离）
production/                         # 迭代计划、里程碑、发布跟踪
```

## 运作原理

### Agent 协调机制

Agent 遵循结构化的委派模型：

1. **纵向委派** — 总监层委派给主管层，主管层委派给专家层
2. **横向协商** — 同层 Agent 可以相互咨询，但不能就跨领域事项做出有约束力的决策
3. **冲突解决** — 分歧会逐级上报给共同的上级（设计冲突报 `creative-director`，技术冲突报 `technical-director`）
4. **变更传播** — 跨部门的变更由 `producer` 统筹协调
5. **领域边界** — Agent 在未获明确授权时不得修改其领域以外的文件

### 协作而非自主

这**不是**一个自动驾驶系统。每个 Agent 都遵循严格的协作协议：

1. **提问** — Agent 在提出方案之前会先提问
2. **展示选项** — Agent 会给出 2–4 个选项并说明各自的利弊
3. **由你决定** — 最终决策权始终在用户手中
4. **起草** — Agent 在定稿前会展示工作成果
5. **审批** — 未经你签字同意，任何内容都不会被写入

你始终掌握主导权。Agent 提供的是结构和专业能力，而非自主决策。

### 自动化安全保障

**钩子**在每次会话中自动运行：

| 钩子 | 触发时机 | 作用 |
|------|---------|------|
| `validate-commit.sh` | PreToolUse（Bash） | 检查硬编码值、TODO 格式、JSON 有效性、设计文档章节——命令不是 `git commit` 时提前退出 |
| `validate-push.sh` | PreToolUse（Bash） | 推送到受保护分支时发出警告——命令不是 `git push` 时提前退出 |
| `validate-assets.sh` | PostToolUse（Write/Edit） | 验证命名规范和 JSON 结构——文件不在 `assets/` 下时提前退出 |
| `session-start.sh` | 会话打开时 | 显示当前分支和近期提交，帮助快速定向 |
| `detect-gaps.sh` | 会话打开时 | 检测全新项目（建议运行 `/start`），以及在已有代码或原型时检测缺失的设计文档 |
| `pre-compact.sh` | 压缩前 | 保存会话进度笔记 |
| `post-compact.sh` | 压缩后 | 提醒 Claude 从 `active.md` 恢复会话状态 |
| `notify.sh` | 通知事件 | 通过 PowerShell 显示 Windows 系统弹窗通知 |
| `session-stop.sh` | 会话关闭时 | 将 `active.md` 归档到会话日志，并记录 git 活动 |
| `log-agent.sh` | Agent 启动时 | 审计追踪开始——记录子智能体调用信息 |
| `log-agent-stop.sh` | Agent 停止时 | 审计追踪结束——完善子智能体记录 |
| `validate-skill-change.sh` | PostToolUse（Write/Edit） | 在 `.claude/skills/` 下发生变更后，建议运行 `/skill-test` |

> **注意**：`validate-commit.sh`、`validate-assets.sh` 和 `validate-skill-change.sh` 会在每次 Bash/写入工具调用时触发，当命令或文件路径不相关时立即退出（exit 0）。这是正常的钩子行为，不会造成性能问题。

**`settings.json` 中的权限规则**会自动放行安全操作（git status、测试运行），并拦截危险操作（强制推送、`rm -rf`、读取 `.env` 文件）。

### 按路径作用域的规则

编码规范会根据文件路径自动执行：

| 路径 | 执行规范 |
|------|---------|
| `src/gameplay/**` | 数据驱动的数值、使用增量时间、禁止 UI 引用 |
| `src/core/**` | 热路径零内存分配、线程安全、API 稳定性 |
| `src/ai/**` | 性能预算、可调试性、数据驱动参数 |
| `src/networking/**` | 服务器权威架构、版本化消息、安全性 |
| `src/ui/**` | 不持有游戏状态、本地化就绪、无障碍支持 |
| `design/gdd/**` | 必须包含 8 个章节、公式格式、边界情况 |
| `tests/**` | 测试命名、覆盖率要求、fixture 模式 |
| `prototypes/**` | 放宽标准，但必须有 README 和假设说明文档 |

## 设计哲学

本模板以专业游戏开发实践为基础：

- **MDA 框架** — 机制（Mechanics）、动态（Dynamics）、美感（Aesthetics）的游戏设计分析方法
- **自我决定理论** — 以自主性、胜任感、归属感驱动玩家动机
- **心流状态设计** — 通过挑战与技能的平衡维持玩家沉浸感
- **Bartle 玩家类型** — 目标受众定位与验证
- **验证驱动开发** — 先写测试，再实现功能

## 自定义配置

这是一个**模板**，不是锁死的框架。一切都可以按需定制：

- **增减 Agent** — 删除不需要的 Agent 文件，为你的领域添加新的
- **编辑 Agent 提示词** — 调整 Agent 行为，加入项目特有的知识
- **修改技能** — 调整工作流以匹配你的团队流程
- **添加规则** — 为你的项目目录结构创建新的按路径作用域的规则
- **调整钩子** — 修改验证严格程度，添加新的检查项
- **选择引擎** — 使用 Godot、Unity 或 Unreal 的 Agent 集（或都不用）
- **设置评审强度** — `full`（所有总监门禁）、`lean`（仅阶段门禁）或 `solo`（无门禁）。在 `/start` 时设置，或编辑 `production/review-mode.txt`。也可在任意技能命令后附加 `--review solo` 覆盖单次设置。

## 平台支持

在 **Windows 10** 配合 Git Bash 上测试通过。所有钩子使用 POSIX 兼容的模式（`grep -E`，非 `grep -P`），并内置缺失工具的降级处理。在 macOS 和 Linux 上无需修改即可使用。

## 社区

- **讨论区** — [GitHub Discussions](https://github.com/Donchitos/Claude-Code-Game-Studios/discussions)，欢迎提问、分享想法，以及展示你用这个模板做出来的作品
- **问题追踪** — [Bug 报告和功能请求](https://github.com/Donchitos/Claude-Code-Game-Studios/issues)

---

## 支持本项目

Claude Code Game Studios 是免费的开源项目。如果它为你节省了时间或帮助你发布了游戏，欢迎支持持续开发：

<p>
  <a href="https://www.buymeacoffee.com/donchitos3"><img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="请我喝咖啡"></a>
  &nbsp;
  <a href="https://github.com/sponsors/Donchitos"><img src="https://img.shields.io/badge/GitHub%20Sponsors-ea4aaa?style=for-the-badge&logo=githubsponsors&logoColor=white" alt="GitHub Sponsors"></a>
</p>

- **[Buy Me a Coffee](https://www.buymeacoffee.com/donchitos3)** — 一次性支持
- **[GitHub Sponsors](https://github.com/sponsors/Donchitos)** — 通过 GitHub 进行持续赞助

赞助资金将用于维护技能更新、添加新 Agent、跟进 Claude Code 和各引擎 API 变更，以及回应社区问题。

---

*基于 Claude Code 构建。持续维护和扩展中——欢迎通过 [GitHub Discussions](https://github.com/Donchitos/Claude-Code-Game-Studios/discussions) 贡献。*

## 许可证

MIT 许可证。详见 [LICENSE](LICENSE)。
