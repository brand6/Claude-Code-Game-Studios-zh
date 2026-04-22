# 技能质量评分标准

由 `/skill-test category [name|all]` 使用，用于在结构合规性之外对技能进行评估。
每个分类定义 4–5 个针对该技能工作的二元 通过/失败 指标。

当技能的书面指令明确满足标准时，指标为 通过（PASS）。
当指令缺失、模糊或相互矛盾时，指标为 失败（FAIL）。
当指令部分满足标准时，指标为 警告（WARN）。

---

## 技能分类

### `gate`

**技能**：gate-check

Gate 技能控制阶段转换。它们必须在不自动推进阶段的情况下保证正确性，
并遵守三种评审模式。

| 指标 | 通过标准 |
|------|---------|
| **G1 — 读取评审模式** | 技能在决定启动哪些 directors 之前，读取 `production/session-state/review-mode.txt`（或等效文件） |
| **G2 — 完整模式：所有 4 个 directors 启动** | 在 `full` 模式下，全部 4 个 Tier-1 directors（CD、TD、PR、AD）的 PHASE-GATE 提示均被并行调用 |
| **G3 — 精简模式：仅 PHASE-GATE** | 在 `lean` 模式下，只运行 `*-PHASE-GATE` 关卡；内联关卡（CD-PILLARS、TD-ARCHITECTURE 等）跳过 |
| **G4 — 单机模式：无 directors** | 在 `solo` 模式下，不启动 director 关卡；每个均标注"已跳过 — 单机模式" |
| **G5 — 禁止自动推进** | 未经用户通过"May I write"明确确认，技能绝不写入 `production/stage.txt` |

---

### `review`

**技能**：design-review、architecture-review、review-all-gdds

Review 技能读取文档并生成结构化裁决。它们主要为只读操作，
在分析阶段不得触发 director 关卡。

| 指标 | 通过标准 |
|------|---------|
| **R1 — 只读强制** | 技能不在未经用户明确批准的情况下修改被审查文档；任何写入操作（评审日志、索引更新）均须通过"May I write"把关 |
| **R2 — 8 节检查** | 技能明确评估全部 8 个必需的 GDD 节（或等效架构节） |
| **R3 — 正确裁决词汇** | 裁决恰好为以下之一：APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED（设计）或 PASS / CONCERNS / FAIL（架构） |
| **R4 — 分析期间无 director 关卡** | 技能在分析阶段不启动 director 关卡；分析后的 director 评审（如 architecture-review 中）在技能范围和风险等级确实需要时可以接受 |
| **R5 — 结构化发现** | 输出在最终裁决前包含逐节状态表或检查清单 |

> **例外情况：**
> - `design-review`：允许的工具中包含 Write、Edit，以支持可选的"立即修订"路径（所有写入须经用户批准）和写入评审日志。R1 已满足，因为被审查文档不会被静默修改。
> - `architecture-review`：在分析完成后启动 TD-ARCHITECTURE 和 LP-FEASIBILITY 关卡。这是有意为之 —— 架构评审风险高，需要 director 签字确认。R4 已满足，因为关卡在分析后运行，而非分析期间。

---

### `authoring`

**技能**：design-system、quick-design、architecture-decision、ux-design、ux-review、art-bible、create-architecture

Authoring 技能以协作方式创建或更新设计文档。完整的 GDD/UX 编写技能
采用逐节循环；轻量级编写技能采用适合其较小范围的单次草稿模式。

| 指标 | 通过标准 |
|------|---------|
| **A1 — 逐节循环** | 完整编写技能（design-system、ux-design、art-bible）每次编写一节，在推进到下一节之前呈现内容供审批。轻量级技能（quick-design、architecture-decision、create-architecture）可以起草完整文档后再请求审批 —— 对于实现范围在约 4 小时以内的文档，单次草稿是可接受的。 |
| **A2 — 每节 May-I-write** | 完整编写技能在每次节写入前询问"May I write this to [filepath]?"。轻量级技能针对完整文档询问一次。 |
| **A3 — 改造模式** | 技能检测目标文件是否已存在，并提供更新特定节而非覆盖整个文档的选项。总是创建新文件的轻量级技能（quick-design）豁免此要求。 |
| **A4 — 正确层级的 director 关卡** | 如果为此技能定义了 director 关卡（如 CD-GDD-ALIGN、TD-ADR），它在正确的模式阈值（full/lean）下运行 —— 在 solo 模式下不运行 |
| **A5 — 骨架优先** | 完整编写技能在填充内容前创建包含所有节标题的文件骨架，以在会话中断时保留进度。轻量级技能豁免此要求。 |

> **完整编写技能**（必须通过全部 5 个指标）：`design-system`、`ux-design`、`art-bible`
> **轻量级编写技能**（A1、A2、A5 使用单次草稿模式；仅创建新文件的技能豁免 A3）：`quick-design`、`architecture-decision`、`create-architecture`
> **评审模式技能**（按 review 指标评估）：`ux-review`

---

### `readiness`

**技能**：story-readiness、story-done

Readiness 技能在实现前后验证 stories。它们必须产生多维裁决，
并与 director 关卡模式正确集成。

| 指标 | 通过标准 |
|------|---------|
| **RD1 — 多维检查** | 技能检查 ≥3 个独立维度（如设计、架构、范围、完成定义），并分别报告每个维度 |
| **RD2 — 三级裁决** | 裁决层级明确定义：READY/COMPLETE > NEEDS WORK/COMPLETE WITH NOTES > BLOCKED |
| **RD3 — BLOCKED 需要外部行动** | BLOCKED 裁决仅用于 story 作者单独无法解决的问题（如提议的 ADR、不可解决的依赖关系） |
| **RD4 — 正确模式下的 director 关卡** | QL-STORY-READY 或 LP-CODE-REVIEW 关卡在 `full` 模式下启动，在 `lean`/`solo` 模式下跳过并附注跳过说明 |
| **RD5 — 下一个 story 交接** | 完成后，技能从当前冲刺中浮现下一个 READY story |

---

### `pipeline`

**技能**：create-epics、create-stories、dev-story、create-control-manifest、propagate-design-change、map-systems

Pipeline 技能生成其他技能消费的制品。它们必须按正确的 schema 写入文件，
遵守层级/优先级排序，并在写入前把关。

| 指标 | 通过标准 |
|------|---------|
| **P1 — 正确输出 schema** | 每个产出文件遵循项目模板（EPIC.md、story frontmatter 等）；技能引用模板路径 |
| **P2 — 层级/优先级排序** | 产出 epics 或 stories 的技能遵守层级排序（core → extended → meta）和优先级字段 |
| **P3 — 每个制品前 May-I-write** | 技能在创建每个输出文件前询问"May I write [artifact]?"，而非批量批准所有文件 |
| **P4 — 正确层级的 director 关卡** | 范围内的关卡（PR-EPIC、QL-STORY-READY、LP-CODE-REVIEW 等）在 `full` 模式运行，在 `lean`/`solo` 模式跳过并附注说明 |
| **P5 — 写入前先读取** | 技能在产出制品前读取相关的 GDD/ADR/清单，以确保对齐 |

---

### `analysis`

**技能**：consistency-check、balance-check、content-audit、code-review、tech-debt、
scope-check、estimate、perf-profile、asset-audit、security-audit、test-evidence-review、test-flakiness

Analysis 技能扫描项目并浮现发现。它们在分析期间为只读，
并在推荐任何文件写入前询问用户。

| 指标 | 通过标准 |
|------|---------|
| **AN1 — 只读扫描** | 分析阶段仅使用 Read/Glob/Grep 工具；扫描本身期间不进行 Write 或 Edit |
| **AN2 — 结构化发现表** | 输出包含发现表或检查清单（而非纯文本），每条发现附严重程度/优先级 |
| **AN3 — 禁止自动写入** | 任何建议的文件写入（如技术债务注册表、修复补丁）均须通过"May I write"把关 |
| **AN4 — 分析期间无 director 关卡** | Analysis 技能不启动 director 关卡；它们产出发现供人工审查 |

---

### `team`

**技能**：team-combat、team-narrative、team-audio、team-level、team-ui、team-qa、
team-release、team-polish、team-live-ops

Team 技能为某个部门编排多个专家 agents。它们必须
启动正确的 agents，对独立的并行运行，并立即浮现阻塞项。

| 指标 | 通过标准 |
|------|---------|
| **T1 — 命名 agent 列表** | 技能明确指明启动哪些 agents 及其顺序 |
| **T2 — 独立时并行** | 输入互不依赖的 agents 并行启动（单条消息，多个 Task 调用） |
| **T3 — BLOCKED 浮现** | 若任何启动的 agent 返回 BLOCKED 或失败，技能立即浮现，并暂停依赖工作 —— 绝不静默跳过 |
| **T4 — 推进前收集所有裁决** | 依赖阶段等待所有并行 agents 完成后再继续 |
| **T5 — 无参数时报错** | 如果缺少必需参数（如功能名称），技能输出用法提示并停止，不启动任何 agents |

---

### `sprint`

**技能**：sprint-plan、sprint-status、milestone-review、retrospective、changelog、patch-notes

Sprint 技能读取生产状态并产出报告或规划制品。
它们在特定模式阈值下有 PR-SPRINT 或 PR-MILESTONE 关卡。

| 指标 | 通过标准 |
|------|---------|
| **SP1 — 读取冲刺/里程碑状态** | 技能在产出输出前读取 `production/sprints/` 或 `production/milestones/` |
| **SP2 — 正确的冲刺关卡** | PR-SPRINT（用于规划）或 PR-MILESTONE（用于里程碑评审）关卡在 `full` 模式运行，在 `lean`/`solo` 模式跳过 |
| **SP3 — 结构化输出** | 输出使用一致的结构（速度表、风险列表、行动项），而非自由散文 |
| **SP4 — 禁止自动提交** | 技能绝不在未经"May I write"的情况下写入冲刺文件或里程碑记录 |

---

### `utility`

**技能**：start、help、brainstorm、onboard、adopt、hotfix、prototype、localize、
launch-checklist、release-checklist、smoke-check、soak-test、test-setup、test-helpers、
regression-suite、qa-plan、bug-triage、bug-report、playtest-report、asset-spec、
reverse-document、project-stage-detect、setup-engine、skill-test、skill-improve、
day-one-patch，以及其他不属于上述分类的技能

Utility 技能通过 7 项标准静态检查。如果它们恰好启动 director 关卡，
关卡模式逻辑也必须正确。

| 指标 | 通过标准 |
|------|---------|
| **U1 — 通过全部 7 项静态检查** | `/skill-test static [name]` 返回 COMPLIANT，0 个 FAIL |
| **U2 — 关卡模式正确（若适用）** | 如果技能启动任何 director 关卡，它正确读取 review-mode 并应用 full/lean/solo 逻辑 |

---

## Agent 分类

用于验证 `tests/agents/` 中的 agent 规格文件。

### `director`

**Agents**：creative-director、technical-director、art-director、producer

| 指标 | 通过标准 |
|------|---------|
| **D1 — 正确裁决词汇** | 返回 APPROVE / CONCERNS / REJECT（或领域等效词：producer 使用 REALISTIC/CONCERNS/UNREALISTIC） |
| **D2 — 领域边界遵守** | 不在声明领域之外做出约束性决策 |
| **D3 — 冲突升级** | 当两个部门发生冲突时，升级至正确的上级（creative-director 或 technical-director），而非单方面决定 |
| **D4 — Opus 模型层级** | Agent 按 coordination-rules.md 分配 Opus 模型 |

### `lead`

**Agents**：lead-programmer、qa-lead、narrative-director、audio-director、game-designer、
systems-designer、level-designer

| 指标 | 通过标准 |
|------|---------|
| **L1 — 领域裁决** | 返回领域专属裁决（如 lead-programmer 使用 FEASIBLE/INFEASIBLE，qa-lead 使用 PASS/FAIL） |
| **L2 — 升级至共同上级** | 跨领域冲突升级至 creative-director（设计）或 technical-director（技术） |
