# /planning-with-files-zh 将阶段6批次4的skill翻译.

# 规则：不翻斜杠命令名，翻译 description + 正文任务计划 — CCGS 项目全量汉化

## 目标

将 Claude-Code-Game-Studios 模板项目完整汉化为中文版，
产出独立中文仓库（Claude-Code-Game-Studios-cn）。
所有翻译文件放入 `zh/` 子目录（保持原结构），发布前移出成独立仓库。

## 总策略

Sonnet 4.6 批量翻译 + Opus 4.6 精修核心 + 人工抽检

## 阶段划分

### 阶段 0：术语表 & 翻译规则制定

状态：`complete`

- 输出：zh/GLOSSARY.md ✅（已创建）
- 内容：120+ 核心术语的固定中文译法
- 绝对不翻列表已最终化
- 翻译规则文档已建立

### 阶段 1：结构扫描 & 优先级清单

状态：`complete`

- 项目结构全量盘点完成
- 总文件数：约 305 个
- 核心链路已识别
- 优先级矩阵已建立

### 阶段 2：入口文档汉化

状态：`complete`（8/8 完成）
模型：Sonnet 4.6
文件（8个）：

- zh/README.md ✅
- zh/UPGRADING.md ✅
- zh/CLAUDE.md ✅
- zh/docs/WORKFLOW-GUIDE.md ✅
- zh/docs/COLLABORATIVE-DESIGN-PRINCIPLE.md ✅
- zh/docs/CLAUDE.md ✅
- zh/.claude/docs/quick-start.md ✅
- zh/.claude/docs/skills-reference.md ✅

验证：中文可读，链接正确，命令名未被翻译

### 阶段 3：核心 Agents 精修

状态：`complete`（11/11 完成）
模型：**Opus 4.6**（最关键步骤）
文件（11个，Tier 1 + 核心 Tier 2）：

- zh/.claude/agents/creative-director.md ✅
- zh/.claude/agents/technical-director.md ✅
- zh/.claude/agents/producer.md ✅
- zh/.claude/agents/game-designer.md ✅
- zh/.claude/agents/lead-programmer.md ✅
- zh/.claude/agents/narrative-director.md ✅
- zh/.claude/agents/qa-lead.md ✅
- zh/.claude/agents/art-director.md ✅
- zh/.claude/agents/audio-director.md ✅
- zh/.claude/agents/release-manager.md ✅
- zh/.claude/agents/localization-lead.md ✅

要求：不简单翻译，重写为更适合中文语境的结构化指令
验收：2026-04-20 复核通过，未发现阻塞性翻译质量问题；保留后续一致性优化建议

### 阶段 4：核心 Skills 翻译

状态：`complete`（11/11 完成）
模型：Sonnet 4.6
文件（11个核心链路 SKILL.md）：

- zh/.claude/skills/start/SKILL.md ✅
- zh/.claude/skills/help/SKILL.md ✅
- zh/.claude/skills/brainstorm/SKILL.md ✅
- zh/.claude/skills/design-system/SKILL.md ✅
- zh/.claude/skills/dev-story/SKILL.md ✅
- zh/.claude/skills/create-epics/SKILL.md ✅
- zh/.claude/skills/create-stories/SKILL.md ✅
- zh/.claude/skills/sprint-plan/SKILL.md ✅
- zh/.claude/skills/gate-check/SKILL.md ✅
- zh/.claude/skills/project-stage-detect/SKILL.md ✅
- zh/.claude/skills/adopt/SKILL.md ✅

规则：不翻斜杠命令名，翻译 description + 正文

### 阶段 5：剩余 Agents 批量翻译

状态：`complete`（23/23 完成）
模型：Sonnet 4.6
文件（23个通用 agents）：

- accessibility-specialist.md ✅
- ai-programmer.md ✅
- analytics-engineer.md ✅
- community-manager.md ✅
- devops-engineer.md ✅
- economy-designer.md ✅
- engine-programmer.md ✅
- gameplay-programmer.md ✅
- level-designer.md ✅
- live-ops-designer.md ✅
- network-programmer.md ✅
- performance-analyst.md ✅
- prototyper.md ✅
- qa-tester.md ✅
- security-engineer.md ✅
- sound-designer.md ✅
- systems-designer.md ✅
- technical-artist.md ✅
- tools-programmer.md ✅
- ui-programmer.md ✅
- ux-designer.md ✅
- world-builder.md ✅
- writer.md ✅

引擎 agents（15个）拆为后续子批次，按用户选引擎后翻译，不计入本阶段数量

### 阶段 6：剩余 Skills 批量翻译

状态：`complete` ✅
模型：Sonnet 4.6
文件（61个 SKILL.md，除核心11个外的剩余）
分批：共6批

#### 批次1（10个）— 状态：`complete` ✅

architecture-decision ✅, architecture-review ✅, art-bible ✅, asset-audit ✅, asset-spec ✅,
balance-check ✅, bug-report ✅, bug-triage ✅, changelog ✅, code-review ✅

#### 批次2（10个）— 状态：`complete` ✅

consistency-check ✅, content-audit ✅, create-architecture ✅, create-control-manifest ✅,
day-one-patch ✅, design-review ✅, estimate ✅, hotfix ✅, launch-checklist ✅, localize ✅

#### 批次3（10个）— 状态：`complete` ✅

map-systems ✅, milestone-review ✅, onboard ✅, patch-notes ✅, perf-profile ✅,
playtest-report ✅, propagate-design-change ✅, prototype ✅, qa-plan ✅, quick-design ✅

#### 批次4（11个）— 状态：`complete` ✅

regression-suite ✅, release-checklist ✅, retrospective ✅, reverse-document ✅,
review-all-gdds ✅, scope-check ✅, security-audit ✅, setup-engine ✅,
skill-improve ✅, skill-test ✅, smoke-check ✅

#### 批次5（10个）— 状态：`complete` ✅

soak-test ✅, sprint-status ✅, story-done ✅, story-readiness ✅, team-audio ✅,
team-combat ✅, team-level ✅, team-live-ops ✅, team-narrative ✅, team-polish ✅

#### 批次6（10个）— 状态：`complete` ✅

team-qa ✅, team-release ✅, team-ui ✅, tech-debt ✅, test-evidence-review ✅,
test-flakiness ✅, test-helpers ✅, test-setup ✅, ux-design ✅, ux-review ✅

### 阶段 7：Rules 翻译

状态：`complete` ✅
模型：Sonnet 4.6
文件（11个）：.claude/rules/*.md
⚠️ 保留 frontmatter 中 paths: 字段不变

- zh/.claude/rules/ai-code.md ✅
- zh/.claude/rules/data-files.md ✅
- zh/.claude/rules/design-docs.md ✅
- zh/.claude/rules/engine-code.md ✅
- zh/.claude/rules/gameplay-code.md ✅
- zh/.claude/rules/narrative.md ✅
- zh/.claude/rules/network-code.md ✅
- zh/.claude/rules/prototype-code.md ✅
- zh/.claude/rules/shader-code.md ✅
- zh/.claude/rules/test-standards.md ✅
- zh/.claude/rules/ui-code.md ✅

### 阶段 8：Templates 翻译

状态：`complete` ✅
模型：Sonnet 4.6
文件（44个）：

- .claude/docs/templates/（35个）
- .claude/docs/templates/collaborative-protocols/（3个）
- .claude/docs/hooks-reference/（6个）

保留占位符（[GAME NAME]、[TO BE CONFIGURED] 等）

#### 批次1（11个）— 状态：`complete` ✅

accessibility-requirements.md ✅, architecture-decision-record.md ✅, architecture-doc-from-code.md ✅,
architecture-traceability.md ✅, art-bible.md ✅, changelog-template.md ✅,
collaborative-protocols/design-agent-protocol.md ✅,
collaborative-protocols/implementation-agent-protocol.md ✅,
collaborative-protocols/leadership-agent-protocol.md ✅,
concept-doc-from-prototype.md ✅, design-doc-from-implementation.md ✅

#### 批次2（11个）— 状态：`complete` ✅

difficulty-curve.md ✅, economy-model.md ✅, faction-design.md ✅, game-concept.md ✅,
game-design-document.md ✅, game-pillars.md ✅, hud-design.md ✅, incident-response.md ✅,
interaction-pattern-library.md ✅, level-design-document.md ✅, milestone-definition.md ✅

#### 批次3（11个）— 状态：`complete` ✅

narrative-character-sheet.md ✅, pitch-document.md ✅, player-journey.md ✅, post-mortem.md ✅,
project-stage-report.md ✅, release-checklist-template.md ✅, release-notes.md ✅,
risk-register-entry.md ✅, skill-test-spec.md ✅, sound-bible.md ✅, sprint-plan.md ✅

#### 批次4（11个）— 状态：`complete` ✅

systems-index.md ✅, technical-design-document.md ✅, test-evidence.md ✅, test-plan.md ✅, ux-spec.md ✅,
hooks-reference/hook-input-schemas.md ✅, hooks-reference/post-merge-asset-validation.md ✅,
hooks-reference/post-sprint-retrospective.md ✅, hooks-reference/pre-commit-code-quality.md ✅,
hooks-reference/pre-commit-design-check.md ✅, hooks-reference/pre-push-test-gate.md ✅

### 阶段 9：参考与协作文档翻译

状态：`complete` ✅
模型：Sonnet 4.6
总文件数：80
分批：共7批

规则：YAML 仅翻注释与说明文本；GitHub 模板 frontmatter 键名保留英文

#### 批次1（11个）— 状态：`complete`

`.claude/docs/` 协调与规范类文档（group A）：

- agent-coordination-map.md ✅
- agent-roster.md ✅
- CLAUDE-local-template.md ✅
- coding-standards.md ✅
- context-management.md ✅
- coordination-rules.md ✅
- director-gates.md ✅
- directory-structure.md ✅
- hooks-reference.md ✅
- review-workflow.md ✅
- rules-reference.md ✅

#### 批次2（12个）— 状态：`complete` ✅

`.claude/docs/` 剩余文档 + 杂项特殊文件：

- settings-local-template.md ✅
- setup-requirements.md ✅
- technical-preferences.md ✅
- workflow-catalog.yaml（YAML，仅翻说明性字段值）✅
- design/CLAUDE.md ✅
- src/CLAUDE.md ✅
- design/registry/entities.yaml（YAML，仅翻注释）✅
- docs/registry/architecture.yaml（YAML，仅翻注释）✅
- docs/architecture/tr-registry.yaml（YAML，仅翻注释）✅
- .github/PULL_REQUEST_TEMPLATE.md（frontmatter 键名保留英文）✅
- .github/ISSUE_TEMPLATE/bug_report.md（frontmatter 键名保留英文）✅
- .github/ISSUE_TEMPLATE/feature_request.md（frontmatter 键名保留英文）✅

#### 批次3（11个）— 状态：`complete` ✅

docs/examples/ 全部示例文档：

- docs/examples/README.md ✅
- docs/examples/reverse-document-workflow-example.md ✅
- docs/examples/session-adopt-brownfield.md ✅
- docs/examples/session-design-crafting-system.md ✅
- docs/examples/session-design-system-skill.md ✅
- docs/examples/session-gate-check-phase-transition.md ✅
- docs/examples/session-implement-combat-damage.md ✅
- docs/examples/session-scope-crisis-decision.md ✅
- docs/examples/session-story-lifecycle.md ✅
- docs/examples/session-ux-pipeline.md ✅
- docs/examples/skill-flow-diagrams.md ✅

#### 批次4（13个）— 状态：`complete` ✅

docs/engine-reference/README.md + Godot 全部：

- docs/engine-reference/README.md ✅
- docs/engine-reference/godot/VERSION.md ✅
- docs/engine-reference/godot/breaking-changes.md ✅
- docs/engine-reference/godot/current-best-practices.md ✅
- docs/engine-reference/godot/deprecated-apis.md ✅
- docs/engine-reference/godot/modules/animation.md ✅
- docs/engine-reference/godot/modules/audio.md ✅
- docs/engine-reference/godot/modules/input.md ✅
- docs/engine-reference/godot/modules/navigation.md ✅
- docs/engine-reference/godot/modules/networking.md ✅
- docs/engine-reference/godot/modules/physics.md ✅
- docs/engine-reference/godot/modules/rendering.md ✅
- docs/engine-reference/godot/modules/ui.md ✅

#### 批次5（13个）— 状态：`complete` ✅

Unity 核心 + 模块：

- docs/engine-reference/unity/VERSION.md ✅
- docs/engine-reference/unity/breaking-changes.md ✅
- docs/engine-reference/unity/current-best-practices.md ✅
- docs/engine-reference/unity/deprecated-apis.md ✅
- docs/engine-reference/unity/PLUGINS.md ✅
- docs/engine-reference/unity/modules/animation.md ✅
- docs/engine-reference/unity/modules/audio.md ✅
- docs/engine-reference/unity/modules/input.md ✅
- docs/engine-reference/unity/modules/navigation.md ✅
- docs/engine-reference/unity/modules/networking.md ✅
- docs/engine-reference/unity/modules/physics.md ✅
- docs/engine-reference/unity/modules/rendering.md ✅
- docs/engine-reference/unity/modules/ui.md ✅

#### 批次6（13个）— 状态：`complete` ✅

Unreal 核心 + 模块：

- docs/engine-reference/unreal/VERSION.md ✅
- docs/engine-reference/unreal/breaking-changes.md ✅
- docs/engine-reference/unreal/current-best-practices.md ✅
- docs/engine-reference/unreal/deprecated-apis.md ✅
- docs/engine-reference/unreal/PLUGINS.md ✅
- docs/engine-reference/unreal/modules/animation.md ✅
- docs/engine-reference/unreal/modules/audio.md ✅
- docs/engine-reference/unreal/modules/input.md ✅
- docs/engine-reference/unreal/modules/navigation.md ✅
- docs/engine-reference/unreal/modules/networking.md ✅
- docs/engine-reference/unreal/modules/physics.md ✅
- docs/engine-reference/unreal/modules/rendering.md ✅
- docs/engine-reference/unreal/modules/ui.md ✅

#### 批次7（7个）— 状态：`complete` ✅

所有引擎插件文档（Unity plugins + Unreal plugins）：

- docs/engine-reference/unity/plugins/addressables.md ✅
- docs/engine-reference/unity/plugins/cinemachine.md ✅
- docs/engine-reference/unity/plugins/dots-entities.md ✅
- docs/engine-reference/unreal/plugins/common-ui.md ✅
- docs/engine-reference/unreal/plugins/gameplay-ability-system.md ✅
- docs/engine-reference/unreal/plugins/gameplay-camera-system.md ✅
- docs/engine-reference/unreal/plugins/pcg.md ✅

### 阶段 10：CCGS Skill Testing Framework 翻译（可选）

状态：`complete`（批1 complete，批2 complete，批3 complete，批4 complete，批5 complete，批6 complete，批7 complete）
模型：Sonnet 4.6
文件（127个：126个 md + 1个 yaml）
优先级：低（先保证主体框架运作正常）

#### 批次划分（共 7 批，每批约 15-20 个）

**批1（20个）**：顶层 + agents 头部 — `complete` ✅

- README.md ✅ / CLAUDE.md ✅ / quality-rubric.md ✅ / catalog.yaml ✅
- templates/agent-test-spec.md ✅ / templates/skill-test-spec.md ✅
- agents/directors/（4个）✅
- agents/qa/（3个）✅
- agents/leads/（7个）✅

**批2（20个）**：agents 核心专业 — `complete` ✅

- agents/operations/（7个）✅
- agents/specialists/（13个）✅

**批3（15个）**：agents 引擎专项 — `complete` ✅

- agents/engine/godot/godot-specialist.md ✅
- agents/engine/godot/godot-gdscript-specialist.md ✅
- agents/engine/godot/godot-csharp-specialist.md ✅
- agents/engine/godot/godot-gdextension-specialist.md ✅
- agents/engine/godot/godot-shader-specialist.md ✅
- agents/engine/unity/unity-specialist.md ✅
- agents/engine/unity/unity-addressables-specialist.md ✅
- agents/engine/unity/unity-dots-specialist.md ✅
- agents/engine/unity/unity-shader-specialist.md ✅
- agents/engine/unity/unity-ui-specialist.md ✅
- agents/engine/unreal/unreal-specialist.md ✅
- agents/engine/unreal/ue-blueprint-specialist.md ✅
- agents/engine/unreal/ue-gas-specialist.md ✅
- agents/engine/unreal/ue-replication-specialist.md ✅
- agents/engine/unreal/ue-umg-specialist.md ✅

**批4（18个）**：skills/utility 前半 — `complete` ✅

- skills/utility/ 前18个（按字母序）：
  adopt ✅, asset-spec ✅, brainstorm ✅, bug-report ✅, bug-triage ✅,
  day-one-patch ✅, help ✅, hotfix ✅, launch-checklist ✅, localize ✅,
  onboard ✅, playtest-report ✅, project-stage-detect ✅, prototype ✅,
  qa-plan ✅, regression-suite ✅, release-checklist ✅, reverse-document ✅

**批5（20个）**：skills/utility 后半 + analysis — `complete` ✅

- skills/utility/ 后8个：setup-engine ✅, skill-improve ✅, skill-test ✅, smoke-check ✅, soak-test ✅, start ✅, test-helpers ✅, test-setup ✅
- skills/analysis/（12个）：asset-audit ✅, balance-check ✅, code-review ✅, consistency-check ✅, content-audit ✅, estimate ✅, perf-profile ✅, scope-check ✅, security-audit ✅, tech-debt ✅, test-evidence-review ✅, test-flakiness ✅

**批6（16个）**：skills team + authoring — `complete` ✅

- skills/team/（9个）：team-audio ✅, team-combat ✅, team-level ✅, team-live-ops ✅, team-narrative ✅, team-polish ✅, team-qa ✅, team-release ✅, team-ui ✅
- skills/authoring/（7个）：architecture-decision ✅, art-bible ✅, create-architecture ✅, design-system ✅, quick-design ✅, ux-design ✅, ux-review ✅

**批7（18个）**：skills 剩余分类 — `complete` ✅

- skills/sprint/（6个）：changelog ✅, milestone-review ✅, patch-notes ✅, retrospective ✅, sprint-plan ✅, sprint-status ✅
- skills/pipeline/（6个）：create-control-manifest ✅, create-epics ✅, create-stories ✅, dev-story ✅, map-systems ✅, propagate-design-change ✅
- skills/review/（3个）：architecture-review ✅, design-review ✅, review-all-gdds ✅
- skills/readiness/（2个）：story-done ✅, story-readiness ✅
- skills/gate/（1个）：gate-check ✅

### 阶段 11：翻译文本校对

状态：`complete`
工作规范：主Agent：Gpt-5.4负责校对，有问题的地方调用子Agent：Claude Sonnet 4.6修复后再校验。修复和校验使用不同模型，保证翻译质量。
目标：发布前逐项对照英文原版与中文译文，确认可执行语义一致，且受保护内容未被误翻
校对重点：

- 英文原版和中文的语义是否一致，尤其是职责边界、条件约束、流程顺序、门禁结论与例外条件
- 文件名、路径、命令、斜杠命令、脚本名、frontmatter / YAML 键名、agent / skill 标识符、API 名称等不应翻译的内容是否被误翻

执行方式：

- 以核心链路 docs + skills + agents 为第一优先级，再覆盖其余翻译文件
- 对照英文原文逐文件抽检与定点复核，对自动校验难以发现的语义漂移单独登记
- 对发现的问题按“语义偏差 / 保护内容误翻 / 局部措辞不自然”分类修订
- 每批次完成后更新 findings.md / progress.md，并重新运行 auto/validate_translation.py，确保结果仍为 0 errors / 0 warnings

统一检查清单：

- 语义一致性：核对职责边界、条件强弱（must / should / may）、流程顺序、门禁结论、例外说明、禁止事项是否与英文原文一致
- 保护内容：核对文件名、路径、命令、斜杠命令、脚本名、占位符、frontmatter / YAML 键名、agent / skill 标识符、API 名称、verdict 关键词是否保持英文原样
- 术语一致性：核对中文译法是否与 zh/GLOSSARY.md 一致，避免同一概念多种说法导致执行歧义
- 风险升级规则：若某目录抽检发现语义偏差或保护内容误翻，则该目录从抽检升级为全量复核

#### 批次 1：入口与主流程文档

状态：`complete`
范围：

- zh/ 根目录入口文档：README.md、UPGRADING.md、CLAUDE.md、GLOSSARY.md
- zh/docs/ 顶层主流程文档：WORKFLOW-GUIDE.md、COLLABORATIVE-DESIGN-PRINCIPLE.md、CLAUDE.md、ARCHITECTURE.md
- zh/.claude/docs/ 中直接影响启动与协作理解的入口文档

检查重点：

- 主流程顺序、阶段依赖、斜杠命令、仓库结构说明是否与英文原文一致
- “必须 / 应当 / 可以”这类约束强度是否被弱化或加强

#### 批次 2：核心 agents 与核心 skills

状态：`complete`
范围：

- zh/.claude/agents/ 的核心 directors 与 leads
- zh/.claude/skills/ 的核心链路 skills（start、help、brainstorm、design-system、dev-story、create-epics、create-stories、sprint-plan、gate-check、project-stage-detect、adopt）

检查重点：

- 角色职责边界、委派关系、审批要求、工具限制、门禁裁定词是否与英文原文一致
- 命令路由、输入参数、输出产物、下一步建议是否存在语义漂移

#### 批次 3：其余 .claude agents / skills / rules

状态：`complete`
范围：

- zh/.claude/agents/ 其余 agent 文档
- zh/.claude/skills/ 其余 SKILL.md
- zh/.claude/rules/ 全部规则文件

检查重点：

- frontmatter 中不可翻译字段与规则路径绑定是否保持原样
- review / gate / QA / pipeline 类文档中的固定结论词、条件限制、拒绝边界是否保持准确

#### 批次 4：模板、示例与协作文档

状态：`complete`
范围：

- zh/.claude/docs/templates/、collaborative-protocols/、hooks-reference/
- zh/docs/examples/
- zh/.github/ 协作模板
- zh/design/CLAUDE.md、zh/src/CLAUDE.md

检查重点：

- 模板占位符、示例命令、frontmatter 键名、示例工作流是否被误翻或改义
- 示例文本是否仍能正确示范原始流程，而不是只保留表面中文可读性

#### 批次 5：结构化数据与引擎参考

状态：`complete`
范围：

- zh/design/registry/
- zh/docs/registry/
- zh/docs/architecture/
- zh/docs/engine-reference/

检查重点：

- YAML 仅翻说明文本，不翻键名、路径、枚举值、状态值
- 引擎 API、模块名、版本号、插件名、破坏性变更条目是否保持可检索与可引用

#### 批次 6：CCGS Skill Testing Framework

状态：`complete`
范围：

- zh/CCGS Skill Testing Framework/ 全部译文

检查重点：

- framework 内 agent / skill / catalog 标识符与分类层级是否与英文原版一致
- 测试规范、评分标准、工作流说明中的语义边界与固定术语是否保持一致

执行结果：

- 批次 1-5 通过抽检与定点复核，未发现阻塞性的语义漂移或受保护内容误翻
- 批次 6 抽检命中 `zh/CCGS Skill Testing Framework/skills/analysis/` 目录的系统性问题：5 个测试规范文件把“可选报告写入、仅在用户选择后询问 `May I write`”改写成了默认询问/写入
- 已按风险升级规则对 `zh/CCGS Skill Testing Framework/skills/analysis/` 做全量复核，并修复 `asset-audit.md`、`balance-check.md`、`consistency-check.md`、`content-audit.md`、`test-flakiness.md`
- 2026-04-22 复跑 `auto/validate_translation.py`，结果保持 `0 errors / 0 warnings`

验收：

- 中文与英文原文在可执行语义上保持一致，无职责错配、条件反转、范围缩放或流程断裂
- 文件名、命令、路径等受保护内容保持英文原样，可直接执行或引用
- 修订后重新运行 auto/validate_translation.py，结果保持 0 errors / 0 warnings

### 阶段 12：发布准备

状态：`not_started`

- 写中文版 README（加上是原仓库翻译的说明：https://github.com/Donchitos/Claude-Code-Game-Studios/）
- 把 zh/ 目录 连接到远程仓库：https://github.com/brand6/Claude-Code-Game-Studios-zh.git
- 用中文文件覆盖原英文文件
- 写更新日志

---

## 【仅记录，暂不执行】

### 备选阶段 A：整体精简优化（Opus 4.6）

- 删废话，合并重复指令，压缩 token 用量
- 范围：核心 agents + 核心 skills
- 验收：token 数量下降 ≥20%，功能回归测试通过

### 备选阶段 B：中文增强（Opus 4.6）

- 补充中国国内游戏开发流程习惯（版号、游戏备案节点）
- 参考成熟国产游戏设计方法论
- 加入中文文档规范
- 补充国内常见引擎/工具（Unity China、Cocos Creator）适配说明

### 备选阶段 C：命令完成后推荐下一步与修复回流命令

状态：`not_started`
模型：Sonnet 4.6
目标：在每个 SKILL.md 末尾加入"## 完成后推荐"标准段落，并为评审 / QA 环节补齐明确的修复命令
内容：列出 3 个推荐的下一步命令 + /clear + 上下文压缩提示
范围：所有核心链路 skills（11个），再扩展到全部

第一批修复命令：

- `/code-fix [自然语言问题/阻塞项]`
- `/design-fix [自然语言问题/阻塞项]`
- `/qa-fix [自然语言问题/阻塞项]`

核心逻辑：谁输出，谁管理
路由原则：

- `code-fix`：回调原实现者 agent；默认沿用 `/dev-story` 的 story 路由结果，`lead-programmer` 负责兜底
- `design-fix`：回调原设计产出 agent，如 `game-designer`、`narrative-director`、`ux-designer`
- `qa-fix`：仅修复 QA 工件本身，由 `qa-lead` / `qa-tester` 处理；若问题归因于实现或设计而非 QA 工件，则不修复，改为推荐 `/code-fix` 或 `/design-fix`

主 Agent 职责：

- 解析命令后的自然语言，如“阻塞项”“第2条意见”“修复 save/load fail”
- 检索对应的 review 结果、QA 报告、bug 报告、目标工件与最近产出上下文
- 只提炼与当前责任边界相关的问题并传给修复 agent
- 若问题不属于当前工件责任边界，则明确拒绝修复并重定向到正确命令

实现：

- 新增 zh/.claude/skills/code-fix/SKILL.md、zh/.claude/skills/design-fix/SKILL.md、zh/.claude/skills/qa-fix/SKILL.md
- 在 review / QA / check 类 skills 的 Next Steps 中加入 fix 命令，而不是只写“修复后重跑”
- 为 fix 命令定义统一输入：目标工件路径 + 问题摘要 + 来源报告 / 阻塞项引用
- 建立“评审 -> 修复 -> 复审”闭环模板

数据来源：workflow-catalog.yaml 里的 next_phase + steps 字段，以及 review / QA 报告中的阻塞项

### 备选阶段 D：自动模式开关

状态：`not_started`
模型：Sonnet 4.6
目标：开启后，skill 完成时自动触发下一个命令（无需用户输入）
核心理念：流程 / 开发 / QA 类操作自动化；设计 / 决策类操作需玩家参与
实现方案：
  a. 新建 zh/.claude/skills/auto/SKILL.md（/auto on|off|status）
  b. 运行时写入 production/auto-mode.json（enabled: true/false）
  c. 所有 SKILL.md 读取此文件，若 enabled 则直接执行推荐下一步
  d. 涉及 creative-director 决策的步骤始终要求人工确认
  e. 修复命令默认不自动执行；只有当阻塞项可明确归属到单一生产者且不跨责任边界时，才允许自动模式推荐或半自动触发 fix 命令
自动化白名单：sprint-plan → create-epics → create-stories → dev-story → story-done → smoke-check → gate-check
人工确认保留：brainstorm、design-system、architecture-decision、任何 Opus 精修步骤、责任归属不清的 fix 场景

### 备选阶段 E：联调测试

状态：`not_started`
模型：Sonnet 4.6
测试命令：/start、/brainstorm、/design-system、/dev-story、/code-review、/design-review、/test-evidence-review、/smoke-check、/code-fix、/design-fix、/qa-fix
检查：翻译导致的逻辑断裂、引用错误、格式破坏，以及“评审 -> 修复 -> 复审”闭环是否成立
重点用例：

- `/code-review` 产出阻塞项后，`/code-fix` 能定位正确 story / 文件 / 评审意见，并回调原实现者修复
- `/design-review` 产出修订项后，`/design-fix` 能回调原设计者，仅修复属于设计文档的问题
- `/test-evidence-review` / `/smoke-check` 发现 QA 工件缺陷时，`/qa-fix` 只修 QA 工件；若根因在实现或设计，必须拒绝并改推正确 fix 命令
- 对不属于当前工件责任边界的问题，fix 命令不会越权修改

---

## 决策记录

- 主线阶段重排：原阶段 10-12 调整为备选阶段 C-E；原阶段 13 调整为阶段 10；新增阶段 11“翻译文本校对”；原阶段 14“发布准备”顺延为阶段 12
- 发布前新增双语校对门禁：重点核对英中语义一致性，以及文件名、路径、命令等受保护内容未被误翻
- 阶段 11 采用风险优先的 6 批次校对顺序：入口主流程 → 核心 agents / skills → 其余 .claude 文档 → 模板 / 示例 / 协作文档 → 结构化数据与引擎参考 → CCGS Skill Testing Framework
- zh/ 作为翻译暂存目录，发布时移入独立仓库
- 引擎 agents（15个）按用户选定引擎后再翻译，不阻塞主流程
- CCGS Skill Testing Framework 定为可选（低优先级）
- design/CLAUDE.md、src/CLAUDE.md 纳入参考文档翻译范围
- 注册表 YAML 与 .github 协作模板纳入翻译范围；仅翻说明文本，不翻键名/路径/状态值
- review / QA 环节新增修复回流命令，第一批为 `/code-fix`、`/design-fix`、`/qa-fix`
- fix 命令遵循“谁输出，谁管理”；主 Agent 只负责检索上下文、归因和路由，不越权修复不属于当前工件的问题
- verdict 关键词（PASS/FAIL/CONCERNS）保留英文，旁注中文含义
- agent 的 name: 标识符绝对不翻
- 斜杠命令（/start）在所有上下文中保留

## 风险

- 自动校验清零只说明结构与保护字段通过，不代表英中语义已经完全一致
- 文件名、命令、路径等受保护内容若被误翻，会在发布后造成命令失效、引用断裂或流程误导
- WORKFLOW-GUIDE.md 很长，需分节翻译
- agents 文件中有大量交叉引用（agent名），翻译时须保持一致
- YAML frontmatter 格式破坏会导致 Claude Code 无法识别 agent/skill
- 注册表 YAML 若误改键名、枚举值或路径，会破坏 grep / skill 工作流
- GitHub issue / PR 模板若误改 frontmatter 键名，会影响 GitHub 模板识别
- review / QA 产出的阻塞项若描述不够结构化，主 Agent 可能难以做准确责任归因
- QA 环节发现的问题有些根因在实现或设计，不应被 `/qa-fix` 吞掉，否则会造成错误归属
- skills 里的 verdict 词汇必须保留，否则 gate-check 逻辑失效

## 遇到的错误

| 错误                                                   | 尝试次数 | 解决方案                                                                                 |
| ------------------------------------------------------ | -------- | ---------------------------------------------------------------------------------------- |
| 规划文件存入 session memory 而非项目目录               | 1        | 已迁移到项目根目录（本次修复）                                                           |
| session-catchup 脚本按 `.claude/skills` 路径执行失败 | 1        | 改用 `C:\Users\brand\.agents\skills\planning-with-files-zh\scripts\session-catchup.py` |
| 将 zh/docs/WORKFLOW-GUIDE.md 误判为缺尾                | 1        | 改用 read_file 直接核对文件后半段与结尾，确认 Workflow 6-8 与 Tips 实际存在              |
