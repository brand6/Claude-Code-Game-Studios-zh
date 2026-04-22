---
name: gate-check
description: "验证推进到下一个开发阶段的就绪状态。生成包含具体阻塞项和必需制品的 PASS/CONCERNS/FAIL 裁定结果。当用户说\"我们准备好进入 X 了吗\"、\"我们可以推进到生产阶段了吗\"、\"检查我们是否可以开始下一阶段\"、\"通过门禁\"时使用。"
argument-hint: "[target-phase: systems-design | technical-setup | pre-production | production | polish | release] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Write, Task, AskUserQuestion
model: opus
---

# 阶段门禁验证

本技能验证项目是否已准备好推进到下一个开发阶段。它检查必需制品、质量标准和阻塞项。

**与 `/project-stage-detect` 的区别**：该技能是诊断性的（"我们在哪里？"）。本技能是规定性的（"我们准备好推进了吗？"并给出正式裁定）。

## 生产阶段（7 个）

项目按以下阶段推进：

1. **概念** —— 头脑风暴、游戏概念文档
2. **系统设计** —— 映射系统、撰写 GDD
3. **技术设置** —— 引擎配置、架构决策
4. **预制作** —— 原型验证、垂直切片验证
5. **生产** —— 功能开发（功能模块/故事跟踪激活）
6. **打磨** —— 性能优化、游戏测试、修复 bug
7. **发布** —— 发布准备、平台认证

**门禁通过时**，将新阶段名称写入 `production/stage.txt`（单行，例如 `Production`）。这将立即更新状态行。

---

## 1. 解析参数

**目标阶段：** `$ARGUMENTS[0]`（空白 = 自动检测当前阶段，然后验证下一个过渡）

同时解析评审模式（一次性解析，保存供本次运行的所有门禁调用使用）：
1. 若传入了 `--review [full|lean|solo]` → 使用该值
2. 否则读取 `production/review-mode.txt` → 使用其值
3. 否则 → 默认为 `lean`

注意：在 `solo` 模式下，主任生成（CD-PHASE-GATE、TD-PHASE-GATE、PR-PHASE-GATE、AD-PHASE-GATE）被跳过 —— 门禁检查变为仅检查制品存在性。在 `lean` 模式下，所有四位主任仍然运行（阶段门禁是精简模式的目的）。

- **有参数**：`/gate-check production` —— 验证针对该特定阶段的就绪状态
- **无参数**：使用与 `/project-stage-detect` 相同的启发式方法自动检测当前阶段，然后**在运行前向用户确认**：

  使用 `AskUserQuestion`：
  - 提示："检测到阶段：**[当前阶段]**。正在运行 [当前] → [下一个] 过渡的门禁检查。是否正确？"
  - 选项：
    - `[A] 是 —— 运行此门禁`
    - `[B] 否 —— 选择不同的门禁`（若选中，显示第二个控件列出所有门禁选项：概念→系统设计、系统设计→技术设置、技术设置→预制作、预制作→生产、生产→打磨、打磨→发布）
  
  无参数时不跳过此确认步骤。

---

## 2. 阶段门禁定义

### 门禁：概念 → 系统设计

**必需制品：**
- [ ] `design/gdd/game-concept.md` 存在且有内容
- [ ] 已定义游戏支柱（在概念文档或 `design/gdd/game-pillars.md` 中）
- [ ] `design/gdd/game-concept.md` 中存在视觉识别锚点章节（来自 `/brainstorm` 阶段 4 的美术总监输出）

**质量检查：**
- [ ] 游戏概念已审查（`/design-review` 裁定结果不是 MAJOR REVISION NEEDED）
- [ ] 核心循环已描述且已理解
- [ ] 已确定目标受众
- [ ] 视觉识别锚点包含一行视觉规则和至少 2 个辅助视觉原则

---

### 门禁：系统设计 → 技术设置

**必需制品：**
- [ ] `design/gdd/systems-index.md` 中的系统索引存在，且至少列举了 MVP 系统
- [ ] 所有 MVP 级 GDD 存在于 `design/gdd/`，并分别通过 `/design-review`
- [ ] `design/gdd/` 中存在跨 GDD 审查报告（来自 `/review-all-gdds`）

**质量检查：**
- [ ] 所有 MVP GDD 通过单独的设计审查（8 个必需章节，无 MAJOR REVISION NEEDED 裁定）
- [ ] `/review-all-gdds` 裁定结果不是 FAIL（跨 GDD 一致性和设计理论检查通过）
- [ ] 所有被 `/review-all-gdds` 标记的跨 GDD 一致性问题已解决或明确接受
- [ ] 系统依赖关系在系统索引中已映射，且双向一致
- [ ] 已定义 MVP 优先级层级
- [ ] 未标记过时的 GDD 引用（较早的 GDD 已更新以反映后续 GDD 中的决策）

---

### 门禁：技术设置 → 预制作

**必需制品：**
- [ ] 已选择引擎（CLAUDE.md 技术栈不是 `[CHOOSE]`）
- [ ] 已配置技术偏好（`.claude/docs/technical-preferences.md` 已填写）
- [ ] 美术圣经存在于 `design/art/art-bible.md`，至少包含第 1-4 节（视觉识别基础）
- [ ] `docs/architecture/` 中至少有 3 个架构决策记录，涵盖基础层系统（场景管理、事件架构、存档/读档）
- [ ] 引擎参考文档存在于 `docs/engine-reference/[engine]/`
- [ ] 测试框架已初始化：`tests/unit/` 和 `tests/integration/` 目录存在
- [ ] CI/CD 测试工作流存在于 `.github/workflows/tests.yml`（或同等位置）
- [ ] 至少存在一个示例测试文件，确认框架可正常运行
- [ ] 主架构文档存在于 `docs/architecture/architecture.md`
- [ ] 架构可追踪性索引存在于 `docs/architecture/architecture-traceability.md`
- [ ] `/architecture-review` 已运行（审查报告文件存在于 `docs/architecture/`）
- [ ] `design/accessibility-requirements.md` 存在，已确定无障碍等级
- [ ] `design/ux/interaction-patterns.md` 存在（模式库已初始化，即使内容较少）

**质量检查：**
- [ ] 架构决策涵盖核心系统（渲染、输入、状态管理）
- [ ] 技术偏好已设置命名约定和性能预算
- [ ] 无障碍等级已定义并记录（即使是"基础"也可接受 —— 未定义则不可接受）
- [ ] 至少有一个屏幕的 UX 规格已开始（通常在技术设置期间设计主菜单或核心 HUD）
- [ ] 所有 ADR 在引擎兼容性章节中标注了引擎版本
- [ ] 所有 ADR 在 GDD 需求已解决章节中有明确的 GDD 关联
- [ ] 没有任何 ADR 引用 `docs/engine-reference/[engine]/deprecated-apis.md` 中列出的 API
- [ ] VERSION.md 中所有 HIGH RISK 引擎域已在架构文档中明确解决，或标记为开放问题
- [ ] 架构可追踪性矩阵**基础层零缺口**（所有基础层需求必须在预制作之前有 ADR 覆盖）

**ADR 循环依赖检查**：对于 `docs/architecture/` 中的所有 ADR，读取每个 ADR 的"ADR 依赖项"/"依赖于"章节。构建依赖图（ADR-A → ADR-B 意味着 A 依赖 B）。若检测到任何循环（例如 A→B→A，或 A→B→C→A）：
- 标记为 **FAIL**："循环 ADR 依赖：[ADR-X] → [ADR-Y] → [ADR-X]。在循环存在时两者都无法达到 Accepted 状态。移除一条'依赖于'边以打破循环。"

---

### 门禁：预制作 → 生产

**必需制品：**
- [ ] `prototypes/` 中至少有 1 个原型，包含 README
- [ ] `production/sprints/` 中存在第一个迭代计划
- [ ] 美术圣经已完整（全部 9 节），且 AD-ART-BIBLE 签字裁定已记录在 `design/art/art-bible.md` 中
- [ ] 叙事文档中引用的关键角色存在角色视觉档案
- [ ] 所有系统索引中 MVP 级 GDD 已完整
- [ ] 主架构文档存在于 `docs/architecture/architecture.md`
- [ ] `docs/architecture/` 中至少有 3 个涵盖基础层决策的 ADR
- [ ] 控制清单存在于 `docs/architecture/control-manifest.md`
- [ ] `production/epics/` 中已定义功能模块，至少存在基础层和核心层功能模块
- [ ] 垂直切片构建存在且可游玩（不只是范围定义）
- [ ] 垂直切片已通过至少 3 次游戏测试（内部即可）
- [ ] 垂直切片游戏测试报告存在于 `production/playtests/` 或同等位置
- [ ] 关键屏幕的 UX 规格存在：主菜单、核心游戏 HUD（`design/ux/`）、暂停菜单
- [ ] HUD 设计文档存在于 `design/ux/hud.md`（若游戏有 HUD）
- [ ] 所有关键屏幕 UX 规格已通过 `/ux-review`（裁定结果为 APPROVED 或接受的 NEEDS REVISION）

**质量检查：**
- [ ] **核心循环乐趣已验证** —— 游戏测试数据确认核心机制有趣，而非仅仅可以运行
- [ ] UX 规格涵盖所有 MVP 级 GDD 的 UI 需求章节
- [ ] 交互模式库记录了关键屏幕中使用的模式
- [ ] `design/accessibility-requirements.md` 中的无障碍等级已在所有关键屏幕 UX 规格中解决
- [ ] 迭代计划引用了 `production/epics/` 中的真实故事文件路径（不只是 GDD —— 故事必须嵌入 GDD 需求 ID + ADR 引用）
- [ ] **垂直切片已完整**，而非只是定了范围 —— 构建展示了完整的核心循环端到端
- [ ] 架构文档在基础层或核心层中无未解决的开放问题
- [ ] 所有 ADR 的引擎兼容性章节已标注引擎版本
- [ ] **核心幻想已交付** —— 至少有一位游戏测试者独立描述了与核心系统 GDD 的玩家幻想章节匹配的体验

**垂直切片验证**（任何项目为否则 FAIL）：
- [ ] 人类在没有开发人员指导的情况下完整游玩了核心循环
- [ ] 游戏在游玩的前 2 分钟内传达了玩家应该做什么
- [ ] 垂直切片构建中不存在关键"乐趣阻塞"bug
- [ ] 核心机制操作感觉良好（这是主观检查 —— 请询问用户）

> **注意**：若任何垂直切片验证项目为 FAIL，无论其他检查结果如何，裁定结果自动为 FAIL。没有经过验证的垂直切片就推进是游戏开发中生产失败的首要原因。

---

### 门禁：生产 → 打磨

**必需制品：**
- [ ] `src/` 中有按子系统组织的活跃代码
- [ ] GDD 中所有核心机制已实现（交叉参考 `design/gdd/` 与 `src/`）
- [ ] 主要游戏路径端到端可游玩
- [ ] `tests/unit/` 和 `tests/integration/` 中存在测试文件，覆盖逻辑和集成故事
- [ ] 本迭代所有逻辑故事在 `tests/unit/` 中有对应的单元测试文件
- [ ] 冒烟测试已运行，裁定结果为 PASS 或 PASS WITH WARNINGS —— 报告存在于 `production/qa/`
- [ ] `production/qa/` 中存在 QA 计划（由 `/qa-plan` 生成），涵盖本迭代或最终生产迭代
- [ ] `production/qa/` 中存在 QA 签字报告（由 `/team-qa` 生成），裁定结果为 APPROVED 或 APPROVED WITH CONDITIONS
- [ ] `production/playtests/` 中记录了至少 3 次不同的游戏测试会话

**质量检查：**
- [ ] 测试通过（通过 Bash 运行测试套件）
- [ ] 没有已知的严重/阻塞 bug
- [ ] 核心循环按设计运行（与 GDD 验收标准对比）
- [ ] 性能在预算范围内（检查 technical-preferences.md 目标）
- [ ] 游戏测试发现已审查，关键乐趣问题已解决（而非仅记录）
- [ ] 未发现"困惑循环" —— 游戏中无超过 50% 的游戏测试者不知原因卡住的点
- [ ] 难度曲线与难度曲线设计文档匹配（若 `design/difficulty-curve.md` 存在）
- [ ] 所有已实现屏幕有对应的 UX 规格（无"代码中设计"的屏幕）
- [ ] 交互模式库已更新，包含实现中使用的所有模式
- [ ] 无障碍合规性已根据 `design/accessibility-requirements.md` 中承诺的等级验证

---

### 门禁：打磨 → 发布

**必需制品：**
- [ ] 里程碑计划中的所有功能已实现
- [ ] 内容已完整（设计文档中引用的所有关卡、资产、对话均存在）
- [ ] 本地化字符串已外部化（`src/` 中无硬编码的面向玩家文本）
- [ ] QA 测试计划存在（`production/qa/` 中的 `/qa-plan` 输出）
- [ ] QA 签字报告存在（`/team-qa` 输出 —— APPROVED 或 APPROVED WITH CONDITIONS）
- [ ] 所有"必须有"故事的测试证据已存在（逻辑/集成：测试文件通过；视觉/感受/UI：`production/qa/evidence/` 中的签字文档）
- [ ] 发布候选构建上的冒烟测试干净通过（PASS 裁定）
- [ ] 上一迭代无测试回归（测试套件完全通过）
- [ ] 平衡数据已审查（`/balance-check` 已运行）
- [ ] 发布清单已完成（`/release-checklist` 或 `/launch-checklist` 已运行）
- [ ] 商店元数据已准备好（若适用）
- [ ] 更新日志/补丁说明已起草

**质量检查：**
- [ ] 完整 QA 通过，由 `qa-lead` 签字
- [ ] 所有测试通过
- [ ] 所有目标平台上的性能目标已达到
- [ ] 无已知的严重、高或中严重性 bug
- [ ] 无障碍基础已覆盖（若适用：按键重映射、文字缩放）
- [ ] 所有目标语言的本地化已验证
- [ ] 法律要求已满足（EULA、隐私政策、年龄评级等）
- [ ] 构建能干净地编译和打包

---

## 3. 运行门禁检查

**在运行制品检查之前**，若 `docs/consistency-failures.md` 存在，则读取。
提取 Domain 与目标阶段匹配的条目（例如，检查系统设计→技术设置时，提取经济、战斗或任何 GDD 域中的条目；检查技术设置→预制作时，提取架构、引擎域中的条目）。
将这些作为上下文传递 —— 目标域中反复出现的冲突模式需要对这些特定检查增加审查力度。

对于目标门禁中的每个项目：

### 制品检查
- 使用 `Glob` 和 `Read` 验证文件是否存在且有实质内容
- 不只检查存在性 —— 验证文件有真实内容（而非只有模板标题）
- 对于代码检查，验证目录结构和文件数量

**系统设计→技术设置门禁 —— 跨 GDD 审查检查**：
使用 `Glob('design/gdd/gdd-cross-review-*.md')` 查找 `/review-all-gdds` 报告。
若没有文件匹配，将"跨 GDD 审查报告存在"制品标记为 **FAIL**，并醒目提示：
"在 `design/gdd/` 中未找到 `/review-all-gdds` 报告。在推进到技术设置之前运行 `/review-all-gdds`。"
若找到文件，读取并检查裁定行：FAIL 裁定意味着跨 GDD 一致性检查失败，必须在推进前解决。

### 质量检查
- 对于测试检查：若已配置测试运行器，通过 `Bash` 运行测试套件
- 对于设计审查检查：`Read` GDD 并检查 8 个必需章节
- 对于性能检查：`Read` technical-preferences.md，与 `tests/performance/` 或最近的 `/perf-profile` 输出中的性能分析数据对比
- 对于本地化检查：在 `src/` 中 `Grep` 硬编码字符串

### 交叉引用检查
- 将 `design/gdd/` 文档与 `src/` 实现对比
- 检查架构文档中引用的每个系统是否有对应代码
- 验证迭代计划引用了真实工作项

---

## 4. 协作评估

对于无法自动验证的项目，**询问用户**：

- "我无法自动验证核心循环是否好玩。是否已经进行过游戏测试？"
- "未找到游戏测试报告。是否进行过非正式测试？"
- "性能分析数据不可用。您是否想运行 `/perf-profile`？"

**绝不对不可验证的项目假设 PASS。** 将其标记为 MANUAL CHECK NEEDED。

---

## 4b. 主任团队评估

在生成最终裁定之前，通过 Task 作为**并行子智能体**生成所有四位主任，使用 `.claude/docs/director-gates.md` 中的并行门禁协议。同时发出所有四个 Task 调用 —— 不等待一个完成再开始下一个。

**并行生成：**

1. **`creative-director`** —— 门禁 **CD-PHASE-GATE**
2. **`technical-director`** —— 门禁 **TD-PHASE-GATE**
3. **`producer`** —— 门禁 **PR-PHASE-GATE**
4. **`art-director`** —— 门禁 **AD-PHASE-GATE**

向每位传递：目标阶段名称、已存在的制品列表、该门禁定义中列出的上下文字段。

**收集所有四个响应，然后呈现主任团队摘要：**

```
## 主任团队评估

创意总监：  [READY / CONCERNS / NOT READY]
  [反馈]

技术总监：  [READY / CONCERNS / NOT READY]
  [反馈]

制作人：    [READY / CONCERNS / NOT READY]
  [反馈]

美术总监：  [READY / CONCERNS / NOT READY]
  [反馈]
```

**应用于裁定：**
- 任何主任返回 NOT READY → 裁定最低为 FAIL（用户可通过明确确认覆盖）
- 任何主任返回 CONCERNS → 裁定最低为 CONCERNS
- 所有四位 READY → 有资格获得 PASS（仍需满足第 3 节的制品和质量检查）

---

## 5. 输出裁定结果

```
## 门禁检查：[当前阶段] → [目标阶段]

**日期**：[日期]
**检查人**：gate-check 技能

### 必需制品：[X/Y 存在]
- [x] design/gdd/game-concept.md —— 存在，2.4KB
- [ ] docs/architecture/ —— 缺失（未找到 ADR）
- [x] production/sprints/ —— 存在，1 个迭代计划

### 质量检查：[X/Y 通过]
- [x] GDD 有 8/8 个必需章节
- [ ] 测试 —— FAILED（tests/unit/ 中有 3 个失败）
- [?] 核心循环已游戏测试 —— MANUAL CHECK NEEDED

### 阻塞项
1. **无架构决策记录** —— 在进入生产之前运行 `/architecture-decision` 创建一个涵盖核心系统架构的 ADR。
2. **3 个测试失败** —— 在推进之前修复 tests/unit/ 中的失败测试。

### 建议
- [解决阻塞项的优先行动]
- [不阻塞但推荐的可选改进]

### 裁定：[PASS / CONCERNS / FAIL]
- **PASS**：所有必需制品已存在，所有质量检查通过
- **CONCERNS**：存在小的缺口但可以在下一阶段内解决
- **FAIL**：关键阻塞项必须在推进之前解决
```

---

## 5a. 验证链

在阶段 5 中起草裁定结果后，在最终确定前对其提出质疑。

**步骤 1 —— 生成 5 个质疑问题**，旨在反驳裁定结果：

对于 **PASS** 草稿：
- "哪些质量检查是通过实际读取文件验证的，哪些是推断通过的？"
- "是否有 MANUAL CHECK NEEDED 项目我在未得到用户确认的情况下标记为 PASS？"
- "我是否确认了所有列出的制品有真实内容，而非只有空标题？"
- "我认为次要的任何阻塞项实际上是否可能阻止阶段成功？"
- "哪个检查我最不确定，为什么？"

对于 **CONCERNS** 草稿：
- "任何列出的 CONCERN 鉴于项目当前状态是否可以升级为阻塞项？"
- "该顾虑是否在下一阶段内可解决，还是会随时间复合？"
- "我是否为了避免更严重的裁定而将任何 FAIL 条件软化为 CONCERN？"
- "我是否遗漏了可能揭示额外阻塞项的制品？"
- "所有 CONCERNS 合在一起是否造成阻塞问题，即使每个单独来看都是次要的？"

对于 **FAIL** 草稿：
- "我是否准确区分了硬阻塞项和强烈建议？"
- "是否有任何 PASS 项目我过于宽松了？"
- "我是否遗漏了用户应该知道的其他阻塞项？"
- "我能否提供通过 PASS 的最短路径 —— 必须改变的具体 3 件事？"
- "失败条件是否可解决，还是表明存在更深层的设计问题？"

**步骤 2 —— 独立回答每个问题。**
不要引用草稿裁定文本 —— 重新检查特定文件或询问用户。

**步骤 3 —— 若需要则修订：**
- 若任何回答揭示了遗漏的阻塞项 → 升级裁定（PASS→CONCERNS 或 CONCERNS→FAIL）
- 若任何回答揭示了被夸大的阻塞项 → 仅在引用具体证据的情况下降级
- 若回答一致 → 确认裁定不变

**步骤 4 —— 在最终报告输出中注明验证：**
`验证链：已检查 [N] 个问题 —— 裁定 [不变 | 从 X 修订为 Y]`

---

## 6. PASS 时更新阶段

当裁定为 **PASS** 且用户确认要推进时：

1. 将新阶段名称写入 `production/stage.txt`（单行，无尾随换行符）
2. 这会立即为所有未来会话更新状态行

示例：通过"预制作→生产"门禁时：
```bash
echo -n "Production" > production/stage.txt
```

**写入前始终询问**："门禁已通过。我可以将 `production/stage.txt` 更新为 'Production' 吗？"

---

## 7. 结束后续步骤控件

裁定呈现且 stage.txt 更新完成后，使用 `AskUserQuestion` 给出结构化的后续步骤提示。

**根据刚运行的门禁定制选项：**

对于 **systems-design PASS**：
```
门禁已通过。您想做什么？
[A] 运行 /create-architecture —— 生成主架构蓝图和 ADR 工作计划（推荐的下一步）
[B] 先设计更多 GDD —— 所有 MVP 系统完成后再回来
[C] 本次会话到此为止
```

> **注意**：`/create-architecture` 是编写任何 ADR 之前的必需下一步。它生成主架构文档和要编写的 ADR 优先级列表。没有这个步骤就运行 `/architecture-decision` 意味着在没有蓝图的情况下编写 ADR —— 风险自负。

对于 **technical-setup PASS**：
```
门禁已通过。您想做什么？
[A] 开始预制作 —— 开始原型化垂直切片
[B] 先编写更多 ADR —— 运行 /architecture-decision [next-system]
[C] 本次会话到此为止
```

对于其他所有门禁，提供该阶段最合理的两个后续步骤以及"到此为止"。

---

## 8. 后续行动

根据裁定，建议具体的后续步骤：

- **无美术圣经？** → `/art-bible` 创建视觉识别规格
- **美术圣经存在但无资产规格？** → `/asset-spec system:[name]` 从已批准 GDD 生成每个资产的视觉规格和生成提示词
- **无游戏概念？** → `/brainstorm` 创建概念
- **无系统索引？** → `/map-systems` 将概念分解为系统
- **缺少设计文档？** → `/reverse-document` 或委托给 `game-designer`
- **小型设计变更？** → `/quick-design`（跳过完整 GDD 流水线）
- **无 UX 规格？** → `/ux-design [screen name]` 创作规格，或 `/team-ui [feature]` 进行完整流水线
- **UX 规格未审查？** → `/ux-review [file]` 或 `/ux-review all` 进行验证
- **无交互模式库？** → `/ux-design patterns` 进行初始化
- **无无障碍需求文档？** → 使用 `AskUserQuestion` 提议现在创建：
  - 提示："门禁需要 `design/accessibility-requirements.md`。是否现在创建？"
  - 选项：`现在创建 —— 我将选择无障碍等级`、`我自己创建`、`暂时跳过`
- **GDD 未经跨审查？** → `/review-all-gdds`（在所有 MVP GDD 单独批准后运行）
- **跨 GDD 一致性问题？** → 修复标记的 GDD，然后重新运行 `/review-all-gdds`
- **无测试框架？** → `/test-setup` 为你的引擎搭建框架
- **当前迭代无 QA 计划？** → `/qa-plan sprint` 在实现开始前生成
- **缺失 ADR？** → `/architecture-decision` 针对各个决策
- **无主架构文档？** → `/create-architecture` 生成完整蓝图
- **ADR 缺少引擎兼容性章节？** → 重新运行 `/architecture-decision`，或手动为现有 ADR 添加引擎兼容性章节
- **缺失控制清单？** → `/create-control-manifest`（需要已接受的 ADR）
- **缺失功能模块？** → `/create-epics layer: foundation` 然后 `/create-epics layer: core`
- **功能模块缺失故事？** → `/create-stories [epic-slug]`（每个功能模块创建后运行）
- **故事未准备好实现？** → `/story-readiness` 在开发人员开始前验证故事
- **测试失败？** → 委托给 `lead-programmer` 或 `qa-tester`
- **无游戏测试数据？** → `/playtest-report`
- **不足 3 次游戏测试？** → 在推进前进行更多游戏测试。使用 `/playtest-report` 整理发现。
- **需要快速迭代检查？** → `/sprint-status` 获取当前迭代进度快照
- **性能未知？** → `/perf-profile`
- **未本地化？** → `/localize`
- **准备发布？** → `/launch-checklist`

---

## 协作协议

本技能遵循协作设计原则：

1. **先提问**：对不确定的检查询问，不假设
2. **呈现选项**：对不可验证项目，提供具体的验证方式
3. **用户决定**：等待对不可验证制品的方向
4. **展示草稿**：在最终确定前呈现完整裁定
5. **获得批准**：在更新 stage.txt 之前询问
