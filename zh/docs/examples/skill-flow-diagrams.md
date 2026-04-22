# 技能流程图

各技能在7个开发阶段中如何衔接的可视化导图。
展示每个技能的前置和后续操作，以及在它们之间流动的工件。

---

## 完整流水线概览（从零到发布）

```
阶段 1：概念
  /start ──────────────────────────────────────────────────────► 路由至 A/B/C/D
  /brainstorm ──────────────────────────────────────────────────► design/gdd/game-concept.md
  /setup-engine ────────────────────────────────────────────────► CLAUDE.md + technical-preferences.md
  /design-review [game-concept.md] ────────────────────────────► 概念验证完成
  /gate-check ─────────────────────────────────────────────────► PASS → 推进至系统设计
        │
        ▼
阶段 2：系统设计
  /map-systems ────────────────────────────────────────────────► design/gdd/systems-index.md
        │
        ▼ （按依赖顺序，逐系统进行）
  /design-system [name] ──────────────────────────────────────► design/gdd/[system].md
  /design-review [system].md ─────────────────────────────────► 每个 GDD 的审查意见
        │
        ▼ （所有 MVP GDD 完成后）
  /review-all-gdds ────────────────────────────────────────────► design/gdd/gdd-cross-review-[date].md
  /gate-check ─────────────────────────────────────────────────► PASS → 推进至技术设置
        │
        ▼
阶段 3：技术设置
  /create-architecture ────────────────────────────────────────► docs/architecture/master.md
  /architecture-decision (×N) ─────────────────────────────────► docs/architecture/[adr-nnn].md
  /architecture-review ────────────────────────────────────────► 审查报告 + docs/architecture/tr-registry.yaml
  /create-control-manifest ────────────────────────────────────► docs/architecture/control-manifest.md
  /gate-check ─────────────────────────────────────────────────► PASS → 推进至预生产
        │
        ▼
阶段 4：预生产
  [UX — 在 Epics 之前，确保写故事时规格已存在]
  /ux-design [screen/hud/patterns] ────────────────────────────► design/ux/*.md
  /ux-review ──────────────────────────────────────────────────► UX 规格已批准（/team-ui 的硬性门）

  [测试基础设施 — 在故事引用测试之前搭建脚手架]
  /test-setup ─────────────────────────────────────────────────► 测试框架 + CI/CD 流水线
  /test-helpers ───────────────────────────────────────────────► tests/helpers/[engine-specific].gd

  [故事 + 原型]
  /create-epics [layer] ───────────────────────────────────────► production/epics/*/EPIC.md
  /create-stories [epic-slug] ─────────────────────────────────► production/epics/*/story-*.md
  /prototype [core-mechanic] ──────────────────────────────────► prototypes/[name]/
  /playtest-report ────────────────────────────────────────────► tests/playtest/vertical-slice.md
  /sprint-plan new ────────────────────────────────────────────► production/sprints/sprint-01.md
  /gate-check ─────────────────────────────────────────────────► PASS → 推进至生产
        │
        ▼
阶段 5：生产（循环冲刺）
  /sprint-status ──────────────────────────────────────────────► 冲刺快照
  /story-readiness [story] ────────────────────────────────────► 故事验证为 READY
        │
        ▼ （认领并实现）
  /dev-story [story] ──────────────────────────────────────────► 路由至正确的程序员智能体
        │
        ▼ （实现期间，按需）
  /code-review ────────────────────────────────────────────────► 代码审查报告
  /scope-check ────────────────────────────────────────────────► 检测到范围蔓延 / 清晰
  /content-audit ──────────────────────────────────────────────► 识别出 GDD 内容差距
  /bug-report ─────────────────────────────────────────────────► production/qa/bugs/bug-NNN.md
  /bug-triage ─────────────────────────────────────────────────► Bug 重新优先级排序并分配

  [功能区域的团队技能 — 处理完整功能时启动]
  /team-combat / /team-narrative / /team-ui / /team-level / /team-audio

  [每冲刺 QA 周期]
  /qa-plan ────────────────────────────────────────────────────► production/qa/qa-plan-sprint-NN.md
  /smoke-check ────────────────────────────────────────────────► 冒烟测试门（PASS/FAIL）
  /regression-suite ───────────────────────────────────────────► 覆盖差距 + 缺少回归测试
  /test-evidence-review ───────────────────────────────────────► 证据质量报告
  /test-flakiness ─────────────────────────────────────────────► 不稳定测试报告
        │
        ▼
  /story-done [story] ─────────────────────────────────────────► 故事关闭 + 浮出下一个
  /sprint-plan [next] ─────────────────────────────────────────► 下一冲刺
        │
        ▼ （生产里程碑后）
  /milestone-review ───────────────────────────────────────────► 里程碑报告
  /gate-check ─────────────────────────────────────────────────► PASS → 推进至打磨
        │
        ▼
阶段 6：打磨
  /perf-profile ───────────────────────────────────────────────► 性能报告 + 修复
  /balance-check ──────────────────────────────────────────────► 平衡报告 + 修复
  /asset-audit ────────────────────────────────────────────────► 资源合规报告
  /tech-debt ──────────────────────────────────────────────────► docs/tech-debt-register.md
  /soak-test ──────────────────────────────────────────────────► 浸泡测试协议 + 结果
  /localize ───────────────────────────────────────────────────► 本地化就绪报告
  /team-polish ────────────────────────────────────────────────► 打磨冲刺统筹编排
  /team-qa ────────────────────────────────────────────────────► 完整 QA 周期签字确认
  /gate-check ─────────────────────────────────────────────────► PASS → 推进至发布
        │
        ▼
阶段 7：发布
  /launch-checklist ───────────────────────────────────────────► 发布就绪报告
  /release-checklist ──────────────────────────────────────────► 平台专属清单
  /changelog ──────────────────────────────────────────────────► CHANGELOG.md
  /patch-notes ────────────────────────────────────────────────► 玩家可见更新说明
  /team-release ───────────────────────────────────────────────► 发布流水线统筹编排
        │
        ▼ （发布后，持续进行）
  /hotfix ─────────────────────────────────────────────────────► 附带审计追踪的紧急修复
  /team-live-ops ──────────────────────────────────────────────► 运营内容计划
```

---

## 技能链：/design-system 详解

单个 GDD 的创作、审查和移交架构的完整流程：

```
systems-index.md（输入）
game-concept.md（输入）
上游 GDDs（输入，如有）
        │
        ▼
/design-system [name]
        │
        ├── 预检：可行性表 + 引擎风险标记
        │
        ├── 章节循环 × 8：
        │     提问 → 选项 → 决策 → 草稿 → 批准 → 写入
        │     [批准后每节立即写入文件]
        │
        └── 输出：design/gdd/[system].md（完整，含全部 8 节）
                │
                ▼
        /design-review design/gdd/[system].md
                │
                ├── APPROVED → 在 systems-index 中标记为 DONE，进入下一系统
                ├── NEEDS REVISION → 智能体展示具体问题，重新进入章节循环
                └── MAJOR REVISION → 进入下一系统前需要大幅重新设计
                        │
                        ▼ （所有 MVP GDD + 交叉审查完成后）
                /review-all-gdds
                        │
                        └── 输出：gdd-cross-review-[date].md
```

---

## 技能链：UX / UI 流水线详解

UX 规格在阶段 4（预生产）创作，在撰写 Epics 之前，
确保故事验收标准能引用具体的 UX 工件。

```
design/gdd/*.md（提取 UI/UX 需求）
design/player-journey.md（情感弧线，如已创作）
        │
        ▼
/ux-design hud              → design/ux/hud.md
/ux-design screen [name]    → design/ux/screens/[name].md
/ux-design patterns         → design/ux/interaction-patterns.md
        │
        ▼
/ux-review design/ux/
        │
        ├── APPROVED → UX 规格就绪，可进入 /create-epics
        ├── NEEDS REVISION → 列出阻塞问题 → 修复 → 重新运行审查
        └── MAJOR REVISION → 存在根本性 UX 问题 → 在创建 Epics 前重新设计
                │
                ▼ （APPROVED 后 — 在阶段 5 实现 UI 功能时）
        /team-ui
                │
                ├── 阶段 1：/ux-design（如有规格缺失）+ /ux-review
                ├── 阶段 2：视觉设计（art-director）
                ├── 阶段 3：布局实现（ui-programmer）
                ├── 阶段 4：无障碍审计（accessibility-specialist）
                └── 阶段 5：最终审查

注意：/ux-design 和 /ux-review 属于阶段 4（预生产）。
      /team-ui 属于阶段 5（生产），在构建 UI 功能时使用。
```

---

## 技能链：Dev Story 流程详解

故事从待办事项到关闭的完整流程：

```
/story-readiness [story]
        │
        ├── READY → 状态：ready-for-dev → 认领进行实现
        ├── NEEDS WORK → 智能体展示具体差距 → 解决 → 重新运行就绪检查
        └── BLOCKED → ADR 仍为提议中，或上游故事未完成
                │
                ▼ （READY 后）
        /dev-story [story]
                │
                ├── 读取：故事文件、关联的 GDD 需求、ADR 决策、控制清单
                ├── 路由至：gameplay-programmer / engine-programmer / ui-programmer / 等
                │
                └── 实现开始
                        │
                        ▼ （可选，实现期间/之后）
                /code-review          → 变更集的架构审查
                /scope-check          → 验证与原始故事标准相比是否有范围蔓延
                /test-evidence-review → 验证测试文件和手动证据的质量
                        │
                        ▼
                /story-done [story]
                        │
                        ├── COMPLETE → 状态：Complete，更新 sprint-status.yaml，浮出下一个故事
                        ├── COMPLETE WITH NOTES → 已完成但部分标准延迟（已记录）
                        └── BLOCKED → 无法验证验收标准 → 调查阻塞原因
```

---

## 技能链：故事生命周期（从待办到关闭）

故事从待办事项到关闭的概览视图：

```
/create-epics [layer]
        │
        └── 输出：production/epics/[slug]/EPIC.md
                │
                ▼
        /create-stories [epic-slug]
                │
                └── 输出：production/epics/[slug]/story-NNN-[slug].md
                            （状态：Ready 或 Blocked，若 ADR 为提议中）
                │
                ▼
        /story-readiness [story]
                │
                ├── READY → /dev-story → 实现 → /story-done
                ├── NEEDS WORK → 解决差距 → 重新运行
                └── BLOCKED → 先修复上游依赖
```

---

## 技能链：QA 流水线详解

```
[阶段 4 — 一次性基础设施设置]
/test-setup ────────────────────────────────────────────────────► 测试框架搭建 + CI/CD 接入
/test-helpers ──────────────────────────────────────────────────► tests/helpers/[engine].gd（GDUnit4、NUnit 等）

[阶段 5 — 每冲刺 QA 周期]
/qa-plan [sprint or feature]
        │
        ├── 读取：故事文件、GDDs、验收标准
        ├── 按测试类型分类每个故事：
        │     逻辑类 → 自动化单元测试（阻塞性）
        │     集成类 → 集成测试或有文档的试玩（阻塞性）
        │     视觉/体感类 → 截图 + 负责人签字（建议性）
        │     UI 类 → 手动流程测试或交互测试（建议性）
        │     配置/数据类 → 冒烟测试（建议性）
        └── 输出：production/qa/qa-plan-sprint-NN.md
                │
                ▼
        /smoke-check
                │
                ├── PASS → QA 交接放行
                └── FAIL → 阻塞冲刺关闭 → 优先修复关键路径
                        │
                        ▼
                /regression-suite
                        │
                        └── 覆盖差距 + 已修复 Bug 但缺少回归测试的列表
                                │
                                ▼
                        /test-evidence-review
                                │
                                └── 验证证据质量，而非仅检查是否存在
                                        │
                                        ▼ （如有 CI 运行历史）
                        /test-flakiness
                                │
                                └── 不稳定测试报告 + 修复建议

[阶段 6 — 扩展稳定性测试]
/soak-test ─────────────────────────────────────────────────────► 浸泡测试协议 + 观测结果
/team-qa ───────────────────────────────────────────────────────► 发布门的完整 QA 周期签字确认

[持续进行 — Bug 管理]
/bug-report ────────────────────────────────────────────────────► production/qa/bugs/bug-NNN.md
/bug-triage ────────────────────────────────────────────────────► 开放 Bug 重新优先级排序并分配

[元级别 — 测试框架验证]
/skill-test [lint|spec|catalog] ────────────────────────────────► 技能文件结构 + 行为检查
```

---

## 技能链：UX 流水线详解（遗留参考）

```
design/gdd/*.md（提取 UX 需求）
design/player-journey.md（情感弧线）
        │
        ▼
/ux-design hud              → design/ux/hud.md
/ux-design screen [name]    → design/ux/screens/[name].md
/ux-design patterns         → design/ux/interaction-patterns.md
        │
        ▼
/ux-review design/ux/
        │
        ├── APPROVED → 所有规格就绪，可交 /team-ui
        ├── NEEDS REVISION → 列出阻塞问题 → 修复 → 重新运行审查
        └── MAJOR REVISION → 存在根本性 UX 问题 → 需要大幅重新设计
                │
                ▼ （APPROVED 后）
        /team-ui
                │
                ├── 阶段 1：context load + /ux-design（如有规格缺失）
                ├── 阶段 2：视觉设计（art-director）
                ├── 阶段 3：布局实现（ui-programmer）
                ├── 阶段 4：无障碍审计（accessibility-specialist）
                └── 阶段 5：最终审查
```

---

## 棕地项目引导流程

适用于已有现有工作的项目（使用 `/start` 选项 D 或直接运行）：

```
/project-stage-detect    → 阶段检测报告
        │
        ▼
/adopt
        │
        ├── 阶段 1：检测已有内容
        ├── 阶段 2：格式审计（而非仅检查是否存在）
        ├── 阶段 3：按类别划分差距（BLOCKING / HIGH / MEDIUM / LOW）
        ├── 阶段 4：有序迁移计划
        ├── 阶段 5：写入 docs/adoption-plan-[date].md
        └── 阶段 6：内联修复最紧迫的差距（可选）
                │
                ▼
        /design-system retrofit [path]    → 填充缺失的 GDD 章节
        /architecture-decision retrofit [path] → 填充缺失的 ADR 章节
        /gate-check                       → 你在流水线中的哪个位置？
```

---

## 如何阅读这些图

| 符号 | 含义 |
|--------|---------|
| `──►` | 产出此工件 |
| `│ ▼` | 流入下一步 |
| `├──` | 分支（多种可能的结果） |
| `×N` | 运行 N 次（每个系统、故事等各一次） |
| `(input)` | 被技能读取但不在此处产出 |
| `[optional]` | 不是通过门禁的必要条件 |
| `WRITE`（大写） | 文件立即写入磁盘 |

---

## 常见入口

| 所处位置 | 运行此命令 |
|---------------|---------|
| 全新项目，无思路 | `/start` → `/brainstorm` |
| 有概念，无引擎 | `/setup-engine` |
| 有概念 + 引擎 | `/map-systems` |
| 系统设计进行中 | `/design-system [next system]` 或 `/map-systems next` |
| 所有 GDD 已完成 | `/review-all-gdds` → `/gate-check` |
| 技术设置阶段 | `/create-architecture` → `/architecture-decision` |
| 开始 UX 设计 | `/ux-design screen [name]` 或 `/ux-design hud` |
| 搭建测试脚手架 | `/test-setup` → `/test-helpers` |
| 有故事，准备编码 | `/story-readiness [story]` → `/dev-story [story]` |
| 故事完成 | `/story-done [story]` |
| 为冲刺运行 QA | `/qa-plan` → `/smoke-check` → `/regression-suite` |
| Bug 待办需要整理 | `/bug-triage` |
| 扩展稳定性测试 | `/soak-test` |
| 不确定 | `/help` |
| 已有项目 | `/adopt` |
