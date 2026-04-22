# Findings — CCGS 汉化项目

## 发布前校对门禁（2026-04-22）
- `auto/validate_translation.py` 的 0 errors / 0 warnings 主要覆盖结构、保护字段、标题、命令保留与缺失翻译，不覆盖全部语义一致性。
- 发布前需要新增“翻译文本校对”阶段，双语对照校准两类问题：语义偏差；不应翻译的文件名、路径、命令、脚本名、frontmatter / YAML 键名、agent / skill 标识符被误翻。
- 语义校对时优先复核职责边界、条件限制、流程顺序、门禁裁定词与例外说明，这些最容易出现“中文通顺但行为变了”的问题。
- 建议执行顺序按风险递减推进：入口主流程文档 → 核心 agents / 核心 skills → 其余 `.claude` 文档 → 模板 / 示例 / 协作文档 → YAML / 引擎参考 → CCGS Skill Testing Framework。
- 高风险目录优先级：zh/docs/WORKFLOW-GUIDE.md、zh/CLAUDE.md、zh/.claude/agents/ 核心角色、zh/.claude/skills/ 核心链路、zh/.claude/rules/、zh/.github/、zh/design/registry/、zh/docs/registry/。
- 阶段 11 结果：批次 1-5 的抽检与定点复核未发现阻塞性的语义漂移或受保护内容误翻。
- 阶段 11 命中的实质问题集中在 `zh/CCGS Skill Testing Framework/skills/analysis/`：5 个测试规范把“可选报告写入、仅在用户选择后才询问 `May I write`”误改成了默认询问或默认写入；`test-flakiness.md` 还把可选报告误改成了登记册写入。
- 这类问题说明发布前校对应额外核对“写入是否可选”与“触发条件是否变化”，不能只检查 `May I write` 关键词是否存在。
- `zh/README.md` 中相对路径从根目录形式调整为 `../` 是 `zh/` 子目录下的预期适配，不属于误翻。

## 项目性质
- 这是 Claude Code Game Studios 游戏开发工作室模板（提示词库），不是游戏运行时项目
- 核心是 agents + skills + templates + docs + rules + hooks 的 Markdown 体系
- 仓库名已经有 `-zh` 后缀（说明用户意图是建立中文版本）

## 完整文件清单（按类别）

### Root（3 文件，必翻）
- README.md
- UPGRADING.md
- CLAUDE.md

### .claude/agents/（49 个 agent md 文件）

Tier 1 — 核心 Directors（最优先，Opus 精修）：
- creative-director.md, technical-director.md, producer.md

Tier 2 — Department Leads（Sonnet 批量 + 核心 Opus 精修）：
- game-designer.md, lead-programmer.md, art-director.md
- audio-director.md, narrative-director.md, qa-lead.md
- release-manager.md, localization-lead.md

Tier 3 — Specialists（Sonnet 批量，23个通用）：
- accessibility-specialist.md, ai-programmer.md, analytics-engineer.md
- community-manager.md, devops-engineer.md, economy-designer.md
- engine-programmer.md, gameplay-programmer.md, level-designer.md
- live-ops-designer.md, network-programmer.md, performance-analyst.md
- prototyper.md, qa-tester.md, security-engineer.md
- sound-designer.md, systems-designer.md, technical-artist.md
- tools-programmer.md, ui-programmer.md, ux-designer.md
- world-builder.md, writer.md

Engine Specialists（15个，用户选引擎后再翻，可暂缓）：
- Godot: godot-specialist, gdscript, gdextension, csharp, shader（5个）
- Unity: unity-specialist, dots, shader, addressables, ui（5个）
- UE5: unreal-specialist, gas, blueprint, replication, umg（5个）

### .claude/skills/（72 个 SKILL.md 文件）

核心链路 Skills（最优先，11个）：
start, help, brainstorm, design-system, dev-story,
create-epics, create-stories, sprint-plan,
gate-check, project-stage-detect, adopt

完整列表（72个）：
adopt, architecture-decision, architecture-review, art-bible, asset-audit,
asset-spec, balance-check, brainstorm, bug-report, bug-triage, changelog,
code-review, consistency-check, content-audit, create-architecture,
create-control-manifest, create-epics, create-stories, day-one-patch,
design-review, design-system, dev-story, estimate, gate-check, help, hotfix,
launch-checklist, localize, map-systems, milestone-review, onboard, patch-notes,
perf-profile, playtest-report, project-stage-detect, propagate-design-change,
prototype, qa-plan, quick-design, regression-suite, release-checklist,
retrospective, reverse-document, review-all-gdds, scope-check, security-audit,
setup-engine, skill-improve, skill-test, smoke-check, soak-test, sprint-plan,
sprint-status, start, story-done, story-readiness, team-audio, team-combat,
team-level, team-live-ops, team-narrative, team-polish, team-qa, team-release,
team-ui, tech-debt, test-evidence-review, test-flakiness, test-helpers,
test-setup, ux-design, ux-review

### .claude/docs/（参考文档，16个 md + 1个 yaml）
agent-coordination-map.md, agent-roster.md,
coding-standards.md, context-management.md,
coordination-rules.md, director-gates.md, directory-structure.md,
hooks-reference.md, quick-start.md, review-workflow.md,
rules-reference.md, setup-requirements.md, skills-reference.md,
CLAUDE-local-template.md, settings-local-template.md, technical-preferences.md,
workflow-catalog.yaml（翻 description 字段值）

### .claude/docs/templates/（35个模板文件）
accessibility-requirements.md, architecture-decision-record.md, architecture-doc-from-code.md,
architecture-traceability.md, art-bible.md, changelog-template.md,
concept-doc-from-prototype.md, design-doc-from-implementation.md, difficulty-curve.md,
economy-model.md, faction-design.md, game-concept.md, game-design-document.md,
game-pillars.md, hud-design.md, incident-response.md, interaction-pattern-library.md,
level-design-document.md, milestone-definition.md, narrative-character-sheet.md,
pitch-document.md, player-journey.md, post-mortem.md, project-stage-report.md,
release-checklist-template.md, release-notes.md, risk-register-entry.md,
skill-test-spec.md, sound-bible.md, sprint-plan.md, systems-index.md,
technical-design-document.md, test-evidence.md, test-plan.md, ux-spec.md

### .claude/docs/templates/collaborative-protocols/（3个）
design-agent-protocol.md, implementation-agent-protocol.md, leadership-agent-protocol.md

### .claude/docs/hooks-reference/（6个）
hook-input-schemas.md, post-merge-asset-validation.md, post-sprint-retrospective.md,
pre-commit-code-quality.md, pre-commit-design-check.md, pre-push-test-gate.md

### .claude/rules/（11个规则文件）
ai-code.md, data-files.md, design-docs.md, engine-code.md, gameplay-code.md,
narrative.md, network-code.md, prototype-code.md, shader-code.md,
test-standards.md, ui-code.md
⚠️ frontmatter 中的 paths: 字段不要翻译

### docs/（主文档）
- CLAUDE.md
- COLLABORATIVE-DESIGN-PRINCIPLE.md
- WORKFLOW-GUIDE.md（最长，分节翻译）

### 目录级 CLAUDE 文档（2个）
- design/CLAUDE.md
- src/CLAUDE.md

### docs/examples/（11个示例文件）
README.md, reverse-document-workflow-example.md, session-adopt-brownfield.md,
session-design-crafting-system.md, session-design-system-skill.md,
session-gate-check-phase-transition.md, session-implement-combat-damage.md,
session-scope-crisis-decision.md, session-story-lifecycle.md,
session-ux-pipeline.md, skill-flow-diagrams.md

### 注册表与架构索引 YAML（3个）
- design/registry/entities.yaml
- docs/registry/architecture.yaml
- docs/architecture/tr-registry.yaml
⚠️ 只翻注释、示例说明，不翻键名、状态值、路径

### .github 协作模板（3个 md）
- .github/PULL_REQUEST_TEMPLATE.md
- .github/ISSUE_TEMPLATE/bug_report.md
- .github/ISSUE_TEMPLATE/feature_request.md

### docs/engine-reference/（引擎参考文档，可选，46个 md）
- README.md
- godot/：VERSION.md, breaking-changes.md, current-best-practices.md, deprecated-apis.md
  + modules/（8个）：animation, audio, input, navigation, networking, physics, rendering, ui
- unity/：VERSION.md, breaking-changes.md, current-best-practices.md, deprecated-apis.md, PLUGINS.md
  + plugins/（3个）：addressables, cinemachine, dots-entities
  + modules/（8个）
- unreal/：VERSION.md, breaking-changes.md, current-best-practices.md, deprecated-apis.md, PLUGINS.md
  + plugins/（4个）：common-ui, gameplay-ability-system, gameplay-camera-system, pcg
  + modules/（8个）

### CCGS Skill Testing Framework（127个文件）
- 126个 md + 1个 catalog.yaml
- 包含 README、CLAUDE、quality-rubric、templates、agents、skills

## 翻译规则（不变量）

### 绝对不翻
- name: 字段的值（所有 agent/skill 标识符）
- 斜杠命令：/start、/brainstorm 等
- YAML 键名：description:、tools:、model: 等
- paths: 字段的值（规则文件路径绑定）
- 注册表 YAML 的状态值、路径、字段键名
- Hooks 脚本文件（.sh 文件）内容
- settings.json 等配置文件
- 裁定词：PASS / FAIL / CONCERNS / BLOCKED / COMPLETE / APPROVED
- 引擎专属 API 名称

### 需保留英文键名的协作文档
- GitHub Issue / PR 模板的 frontmatter 键名：name, about, title, labels, assignees

### 保留英文但可加括注
- GDD（游戏设计文档）
- ADR（架构决策记录）
- QA（质量保证）
- VFX / SFX / HUD / UI / UX

## Agent 文件结构（参考）
```yaml
---
name: creative-director           # 不可翻译
description: "..."                # 可翻译
tools: Read, Glob, Grep, Write
model: opus
maxTurns: 30
memory: user
disallowedTools: Bash
skills: [brainstorm, design-review]
---
```

## 核心调用链（已识别）
/start → 检测项目状态 → 路由
→ /brainstorm（creative-director）→ 概念文档
→ /map-systems（game-designer）→ 系统索引
→ /design-system（game-designer）→ GDD
→ /create-architecture（technical-director）→ 架构文档
→ /create-epics（producer）→ Epic 文件
→ /create-stories（lead-programmer）→ Story 文件
→ /dev-story（各专家）→ 实现
→ /story-done（qa-lead）→ 验收
→ /smoke-check → /gate-check → /sprint-plan（下一迭代）

## 工作流缺口（本次新增）

- 当前 `review / QA / check` 类命令在发现问题后，普遍只给出“修复后重跑”的建议，没有统一的显式修复命令。
- `.claude/skills/code-review/SKILL.md` 已写明“fix the issues and re-run `/code-review`”，但没有对应的 `/code-fix` 命令定义。
- `.claude/skills/design-review/SKILL.md` 虽支持同会话内直接修订，但缺少跨会话、可复用的 `/design-fix` 命令。
- `test-evidence-review`、`smoke-check` 这类 QA 环节会发现问题，但并不总是 QA 工件自身的问题，必须先做责任归因，不能默认交给 QA 修。
- 最小可行闭环应先补 3 个修复命令：`/code-fix`、`/design-fix`、`/qa-fix`。
- 修复命令的设计原则：谁输出，谁管理；主 Agent 负责从自然语言 blocker 中检索相关上下文、裁剪问题范围、将问题交给正确的生产者 Agent。
- 若问题不属于当前工件责任边界，则 fix 命令应明确拒绝修复，并重定向到正确命令，而不是越权修改。

## 已生成文件
- zh/GLOSSARY.md（120+条术语对照表）
- zh/docs/ARCHITECTURE.md（系统架构文档，12章）
- zh/ 目录结构（含 .gitkeep 占位）

## 阶段 2 验收发现（2026-04-20）

- 阶段 2 的 8 个入口文档中，7 个文件通过结构与命令保留检查：zh/README.md、zh/UPGRADING.md、zh/CLAUDE.md、zh/docs/COLLABORATIVE-DESIGN-PRINCIPLE.md、zh/docs/CLAUDE.md、zh/.claude/docs/quick-start.md、zh/.claude/docs/skills-reference.md
- 更正：经 read_file 直接核对，zh/docs/WORKFLOW-GUIDE.md 实际包含 Workflow 6、Workflow 7、Workflow 8 与 Tips for Getting the Most Out of the System
- 上一轮“文件缺尾”的判断来自 PowerShell 行数/尾部检查误导，不应作为验收结论
- 阶段 2 的 8 个入口文档均通过当前已执行的结构与命令保留检查
- 对 zh/UPGRADING.md 的核查显示，主要是目录锚点链接；未发现之前子代理声称的 Markdown 外链损坏问题

## 阶段 3 验收发现（2026-04-20）

- 验收范围：11 个核心 Agent 文件
  - zh/.claude/agents/creative-director.md
  - zh/.claude/agents/technical-director.md
  - zh/.claude/agents/producer.md
  - zh/.claude/agents/game-designer.md
  - zh/.claude/agents/lead-programmer.md
  - zh/.claude/agents/narrative-director.md
  - zh/.claude/agents/qa-lead.md
  - zh/.claude/agents/art-director.md
  - zh/.claude/agents/audio-director.md
  - zh/.claude/agents/release-manager.md
  - zh/.claude/agents/localization-lead.md
- 结构与标识符检查：对 zh/.claude/agents/*.md 执行 frontmatter 与门禁裁定词扫描，未发现 `name/tools/skills/model/memory/disallowedTools` 被误翻，也未发现 `[GATE-ID]:` 后接中文裁定词的情况
- 人工复核样本：creative-director、lead-programmer、qa-lead、audio-director、release-manager、localization-lead
- 复核结果：未发现阻塞性问题；斜杠命令、Agent 标识符、工具名、路径、PASS/FAIL/CONCERNS/APPROVE/REJECT 等固定词均保持可用
- 中文质量：整体达到“精修”目标，不是简单直译；多个文件通过表格化、分层结构和本地语境表达增强了可读性，且未改变原有职责边界
- 样本确认：
  - creative-director 的战略决策工作流与 MDA/玩家心理学框架保真，且中文组织更清晰
  - lead-programmer 保留了写文件前询问批准、架构先行、委托边界等关键约束
  - qa-lead 正确保留了 Story 类型 → 测试证据 → 门禁级别的硬约束逻辑
  - audio-director、release-manager、localization-lead 通过新增结构化表格提升了中文可执行性，未见语义漂移
- 残余建议（非阻塞）：
  - 后续翻译其余 agents 时，尽量统一“协作原则/协作心态”等通用章节的命名与视觉结构
  - qa-lead 中复用的“实现工作流”更像通用协作模板，翻译本身无误，但后续可单独评估原文是否需要按 QA 角色再定制
