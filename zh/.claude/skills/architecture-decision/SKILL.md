---
name: architecture-decision
description: "创建架构决策记录（ADR），记录重要的技术决策、背景、备选方案及其影响。每个重大技术选型都应有对应的 ADR。"
argument-hint: "[title] [--review full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Task, AskUserQuestion
---

调用本技能时：

## 0. 解析参数 — 检测补录模式

解析评审模式（本次运行期间只解析一次，用于所有门控生成）：
1. 若传入了 `--review [full|lean|solo]` → 使用该值
2. 否则读取 `production/review-mode.txt` → 使用其中的值
3. 否则 → 默认使用 `lean`

完整检测模式说明参见 `.claude/docs/director-gates.md`。

**若参数以 `retrofit` 开头，后跟文件路径**
（例如 `/architecture-decision retrofit docs/architecture/adr-0001-event-system.md`）：

进入**补录模式**：

1. 完整读取现有 ADR 文件。
2. 通过扫描标题识别模板中哪些章节已存在：
   - `## Status` — **阻塞项，缺失则阻塞**：`/story-readiness` 无法在没有 ADR 接受状态时完成检查
   - `## ADR Dependencies` — 高优先级缺失项：依赖排序会失效
   - `## Engine Compatibility` — 高优先级缺失项：截止日期后的风险未知
   - `## GDD Requirements Addressed` — 中优先级缺失项：可追溯性丢失
3. 向用户展示：
   ```
   ## 补录：[ADR 标题]
   文件：[路径]

   已存在的章节（不会修改）：
   ✓ Status: [当前值，或"缺失 — 将补充"]
   ✓ [章节名]

   缺失需补充的章节：
   ✗ Status — 阻塞项（没有此字段，story 无法验证 ADR 接受状态）
   ✗ ADR Dependencies — 高优先级
   ✗ Engine Compatibility — 高优先级
   ```
4. 询问："是否要补充这 [N] 个缺失章节？我不会修改任何已有内容。"
5. 若确认：
   - 对于 **Status**：询问用户——"此决策的当前状态是什么？"
     选项："Proposed"、"Accepted"、"Deprecated"、"Superseded by ADR-XXXX"
   - 对于 **ADR Dependencies**：询问——"此决策是否依赖其他任何 ADR？它是否启用或阻塞其他 ADR 或 epic？"每个字段接受"None"。
   - 对于 **Engine Compatibility**：读取引擎参考文档（同下方步骤 0），并请用户确认所属领域，然后使用验证后的数据生成表格。
   - 对于 **GDD Requirements Addressed**：询问——"哪些 GDD 系统促成了此决策？每个 GDD 中哪项具体需求由本 ADR 解决？"
   - 使用 Edit 工具将每个缺失章节追加到 ADR 文件。
   - **绝不修改任何已有章节。** 仅追加或填充缺失章节。
6. 补充所有缺失章节后，若 ADR 中无 `## Date` 字段，则补充该字段。
7. 建议："运行 `/architecture-review` 以重新验证覆盖范围，现在该 ADR 已包含 Status 和 Dependencies 字段。"

若**不处于**补录模式，则继续执行下方步骤 0（正常 ADR 编写流程）。

**无参数保护**：若未提供参数（标题为空），在执行阶段 0 之前先询问：

> "您要记录哪项技术决策？请提供一个简短标题
> （例如 `event-system-architecture`、`physics-engine-choice`）。"

使用用户的回复作为标题，然后继续步骤 0。

---

## 0. 加载引擎上下文（始终最先执行）

在执行其他任何操作之前，先确定引擎环境：

1. 读取 `docs/engine-reference/[engine]/VERSION.md`，获取：
   - 引擎名称与版本
   - LLM 知识截止日期
   - 截止日期后的版本风险等级（LOW / MEDIUM / HIGH）

2. 从标题或用户描述中识别本次架构决策的**领域**。常见领域：Physics、Rendering、UI、Audio、Navigation、Animation、Networking、Core、Input、Scripting。

3. 若对应模块参考文档存在，则读取：
   `docs/engine-reference/[engine]/modules/[domain].md`

4. 读取 `docs/engine-reference/[engine]/breaking-changes.md`——标记相关领域中晚于 LLM 训练截止日期的变更。

5. 读取 `docs/engine-reference/[engine]/deprecated-apis.md`——标记相关领域中不应使用的 API。

6. 若该领域风险等级为 MEDIUM 或 HIGH，则在继续执行前**显示知识缺口警告**：

   ```
   ⚠️  引擎知识缺口警告
   引擎：[名称 + 版本]
   领域：[领域]
   风险等级：HIGH — 此版本已超出 LLM 知识截止日期。

   已从 engine-reference 文档中验证的关键变更：
   - [与本领域相关的变更 1]
   - [变更 2]

   本 ADR 将与引擎参考库交叉验证。
   仅使用已验证的信息继续编写——不要仅凭训练数据判断。
   ```

   若尚未配置引擎，提示："未配置引擎。请先运行 `/setup-engine`，或告知您使用的引擎。"

---

## 1. 确定下一个 ADR 编号

扫描 `docs/architecture/` 中已有的 ADR，确定下一个编号。

---

## 2. 收集上下文

读取相关代码、现有 ADR 以及 `design/gdd/` 中的相关 GDD。

### 2a：架构注册表检查（阻塞门控）

读取 `docs/registry/architecture.yaml`，提取与本 ADR 领域和决策相关的条目（按系统名称、领域关键词或被修改的状态值进行 grep）。

在开始协作设计（步骤 3）之前，将所有相关立场作为锁定约束展示给用户：

```
## 现有架构立场（不得矛盾）

状态所有权：
  player_health → 由 health-system 拥有（ADR-0001）
  接口：HealthComponent.current_health（只读 float）
  → 若本 ADR 读取或写入玩家血量，必须使用此接口。

接口约定：
  damage_delivery → 信号模式（ADR-0003）
  信号：damage_dealt(amount, target, is_crit)
  → 若本 ADR 传递或接收伤害事件，必须使用此信号。

禁止模式：
  ✗ autoload_singleton_coupling（ADR-0001）
  ✗ direct_cross_system_state_write（ADR-0000）
```

若用户提出的决策与任何已注册立场矛盾，立即提示冲突：

> "⚠️ 冲突：本 ADR 提议 [X]，但 ADR-[NNNN] 已将 [Y] 确立为此用途的接受模式。不解决此冲突则会产生相互矛盾的 ADR 和不一致的 story。
> 选项：（1）与现有立场对齐；（2）明确用新决策取代 ADR-[NNNN]；（3）说明为何此情形属于例外。"

在冲突解决或被明确接受为例外之前，不得继续执行步骤 3（协作设计）。

---

## 3. 协作引导决策

开始提问前，先从已收集的上下文（已读取的 GDD、已加载的引擎参考、已扫描的现有 ADR）中推导技能的最佳假设。然后使用 `AskUserQuestion` 提供一个**确认/调整**提示——不要开放式提问。

**先推导假设：**
- **问题**：从标题 + GDD 上下文推断需要做出什么决策
- **备选方案**：从引擎参考 + GDD 需求中提出 2-3 个具体选项
- **依赖关系**：扫描现有 ADR 中的上游依赖；若不明确则假设为 None
- **GDD 关联**：提取标题直接关联的 GDD 系统
- **状态**：新 ADR 始终为 `Proposed`——不要询问用户状态

**假设范围**：假设仅涵盖：问题框架、备选方案、上游依赖、GDD 关联和状态。模式设计问题（例如"派生时机如何处理？"、"数据应内联还是外部存储？"）不属于假设——它们是设计决策，应在假设被确认后单独提问。不要在假设的 AskUserQuestion 组件中包含模式设计问题。

**假设确认后**，若 ADR 涉及模式或数据设计选择，请使用单独的多标签 `AskUserQuestion` 独立提问每个设计问题，再起草 ADR。

**使用 `AskUserQuestion` 展示假设：**

```
以下是起草前的假设：

问题：[从上下文推导的一句话问题陈述]
将考虑的备选方案：
  A) [来自引擎参考的选项]
  B) [来自 GDD 需求的选项]
  C) [来自常见模式的选项]
驱动此决策的 GDD 系统：[从上下文推导的列表]
依赖关系：[上游 ADR（若有），否则为"None"]
状态：Proposed

[A] 继续——使用这些假设起草
[B] 修改备选方案列表
[C] 调整 GDD 关联
[D] 添加性能预算约束
[E] 需要先改变其他内容
```

在用户确认假设或提供修正之前，不要生成 ADR。

**引擎专家和 TD 评审返回后**（步骤 4.5/4.6），若仍有未解决的决策，对每个未解决点单独展示一个 `AskUserQuestion`，将提议的选项作为选择项，并附加自由文本出口：

```
决策：[具体未解决的问题]
[A] [来自专家评审的选项]
[B] [备选方案]
[C] 不同方案——我来描述
```

**ADR 依赖关系** — 从现有 ADR 推导，然后确认：
- 此决策是否依赖尚未 Accepted 的其他 ADR？
- 它是否解锁或解除对其他 ADR 或 epic 的阻塞？
- 它是否阻止某个特定 epic 启动？

将答案记录到 **ADR Dependencies** 章节。若无约束，每个字段写"None"。

---

## 4. 生成 ADR

遵循以下格式：

```markdown
# ADR-[NNNN]: [标题]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXXX]

## Date
[决策日期]

## Engine Compatibility

| 字段 | 值 |
|------|----|
| **Engine** | [例如 Godot 4.6] |
| **Domain** | [Physics / Rendering / UI / Audio / Navigation / Animation / Networking / Core / Input] |
| **Knowledge Risk** | [LOW / MEDIUM / HIGH — 来自 VERSION.md] |
| **References Consulted** | [已读取的引擎参考文档列表，例如 `docs/engine-reference/godot/modules/physics.md`] |
| **Post-Cutoff APIs Used** | [本决策依赖的任何截止日期后版本 API，或"None"] |
| **Verification Required** | [发布前需测试的具体行为，或"None"] |

## ADR Dependencies

| 字段 | 值 |
|------|----|
| **Depends On** | [ADR-NNNN（必须在本决策实现之前 Accepted），或"None"] |
| **Enables** | [ADR-NNNN（本 ADR 解锁该决策），或"None"] |
| **Blocks** | [Epic/Story 名称——在本 ADR Accepted 之前无法启动，或"None"] |
| **Ordering Note** | [上方未涵盖的任何排序约束] |

## Context

### Problem Statement
[我们在解决什么问题？为何现在必须做出此决策？]

### Constraints
- [技术约束]
- [时间约束]
- [资源约束]
- [兼容性要求]

### Requirements
- [必须支持 X]
- [必须在 Y 预算内运行]
- [必须与 Z 集成]

## Decision

[所做的具体技术决策，详细程度足以让他人据此实现。]

### Architecture Diagram
[ASCII 图或此决策所创建系统架构的描述]

### Key Interfaces
[此决策创建的 API 约定或接口定义]

## Alternatives Considered

### 备选方案 1：[名称]
- **描述**：[如何运作]
- **优点**：[优势]
- **缺点**：[劣势]
- **未选择原因**：[为何未选此方案]

### 备选方案 2：[名称]
- **描述**：[如何运作]
- **优点**：[优势]
- **缺点**：[劣势]
- **未选择原因**：[为何未选此方案]

## Consequences

### Positive
- [此决策的良好结果]

### Negative
- [已接受的权衡与代价]

### Risks
- [可能出错的事项]
- [每项风险的缓解措施]

## GDD Requirements Addressed

| GDD 系统 | 需求 | 本 ADR 如何满足 |
|---------|------|----------------|
| [system-name].md | [该 GDD 中的具体规则、公式或性能约束] | [此决策如何满足该需求] |

## Performance Implications
- **CPU**：[预期影响]
- **Memory**：[预期影响]
- **Load Time**：[预期影响]
- **Network**：[预期影响（若适用）]

## Migration Plan
[若此决策改变了现有代码，如何从现状迁移到目标状态？]

## Validation Criteria
[如何验证此决策是正确的？使用哪些指标或测试？]

## Related Decisions
- [相关 ADR 链接]
- [相关设计文档链接]
```

4.5. **引擎专家验证** — 保存之前，生成**主要引擎专家** Task 来验证 ADR 草稿：
   - 读取 `.claude/docs/technical-preferences.md` 中的 `Engine Specialists` 章节，获取主要专家信息
   - 若未配置引擎（`[TO BE CONFIGURED]`），跳过此步骤
   - 生成 `subagent_type: [主要专家]`，提供：ADR 的 Engine Compatibility 章节、Decision 章节、Key Interfaces 以及 engine-reference 文档路径。要求其：
     1. 确认所提方案对锁定的引擎版本是否符合惯用法
     2. 标记任何在训练数据截止后已废弃或已变更的 API 或模式
     3. 识别 ADR 草稿中未捕获的引擎特定风险或注意事项
   - 若专家发现**阻塞性问题**（错误 API、已废弃方案、引擎版本不兼容）：相应修改 Decision 和 Engine Compatibility 章节，并在继续之前向用户确认变更
   - 若专家仅发现**小问题**：将其纳入 ADR 的 Risks 子章节

**评审模式检查** — 在生成 TD-ADR 之前执行：
- `solo` → 跳过。注记："TD-ADR 已跳过——Solo 模式。"继续步骤 4.7（GDD 同步检查）。
- `lean` → 跳过（非 PHASE-GATE）。注记："TD-ADR 已跳过——Lean 模式。"继续步骤 4.7（GDD 同步检查）。
- `full` → 正常生成。

4.6. **技术总监战略评审** — 引擎专家验证后，使用门控 **TD-ADR**（`.claude/docs/director-gates.md`）生成 `technical-director` Task：
   - 提供：ADR 文件路径（或草稿内容）、引擎版本、领域、同一领域中的现有 ADR
   - TD 验证架构一致性（此决策与整体系统是否一致？）——与引擎专家的 API 级检查不同
   - 若 CONCERNS 或 REJECT：在继续之前相应修改 Decision 或 Alternatives 章节

4.7. **GDD 同步检查** — 在展示写入审批之前，扫描"GDD Requirements Addressed"章节中引用的所有 GDD，检查 ADR 的 Key Interfaces 和 Decision 章节中的命名是否与 GDD 保持一致（信号、API 方法或数据类型被重命名）。若有不一致，在写入审批之前立即以**醒目警告块**的形式提示——不要作为脚注：

```
⚠️ 需要 GDD 同步
[gdd-filename].md 使用了本 ADR 已重命名的名称：
  [旧名称] → [ADR 中的新名称]
  [旧名称 2] → [新名称 2]
在写入本 ADR 之前或同时必须更新 GDD，否则读取 GDD 的开发者会实现错误的接口。
```

若无不一致：静默跳过此块。

5. **写入审批** — 使用 `AskUserQuestion`：

若发现 GDD 同步问题：
- "ADR 草稿已完成。您希望如何继续？"
  - [A] 在同一步骤中写入 ADR 并更新 GDD
  - [B] 仅写入 ADR——我会手动更新 GDD
  - [C] 暂不——我需要进一步审阅

若无 GDD 同步问题：
- "ADR 草稿已完成。是否写入？"
  - [A] 写入 ADR 到 `docs/architecture/adr-[NNNN]-[slug].md`
  - [B] 暂不——我需要进一步审阅

若确认写入，则写入文件，必要时创建目录。
对于选项 [A] 含 GDD 更新：同时更新 GDD 文件以使用新名称。

6. **更新架构注册表**

扫描已写入的 ADR，找出应在注册表中登记的新架构立场：
- 它声明所有权的状态
- 它定义的接口约定（信号签名、方法 API）
- 它声明的性能预算
- 它明确做出的 API 选择
- 它禁止的模式（Consequences → Negative 或明确的"不要使用 X"）

展示候选项：
```
此 ADR 的注册表候选项：
  新状态所有权：      player_stamina → stamina-system
  新接口约定：        stamina_depleted 信号
  新性能预算：        stamina-system: 0.5ms/帧
  新禁止模式：        每帧轮询耐力值（使用信号替代）
  已存在（仅更新 referenced_by）：player_health → 已注册 ✅
```

**注册表追加逻辑**：写入 `docs/registry/architecture.yaml` 时，不要假设各章节为空。该文件可能已有来自本会话中之前写入的 ADR 的条目。每次 Edit 调用前：
1. 读取 `docs/registry/architecture.yaml` 的当前状态
2. 找到正确的章节（state_ownership、interfaces、forbidden_patterns、api_decisions）
3. 在该章节最后一个已有条目之后追加新条目——不要尝试替换可能已不存在的 `[]` 占位符
4. 若章节已有条目，使用最后一个条目的结尾内容作为 `old_string` 锚点，并在其后追加新条目

**阻塞——未经用户明确审批，不得写入 `docs/registry/architecture.yaml`。**

使用 `AskUserQuestion` 询问：
- "是否可以用这 [N] 个新立场更新 `docs/registry/architecture.yaml`？"
  - 选项："是——更新注册表"、"暂不——我想先审阅候选项"、"跳过注册表更新"

仅在用户选择"是"后继续。若是：追加新条目。不要修改已有条目——若某立场发生变化，将旧条目设置为 `status: superseded_by: ADR-[NNNN]` 并添加新条目。

---

## 7. 结束下一步建议

ADR 写入（注册表可选更新）后，用 `AskUserQuestion` 结束。

生成组件前：
1. 读取 `docs/registry/architecture.yaml`——检查是否还有优先级 ADR 尚未写入（查看 technical-preferences.md 或 systems-index.md 中标记为前置条件的 ADR）
2. 检查所有前置 ADR 是否已写入。若是，包含"开始编写 GDD"选项。
3. 将所有剩余优先级 ADR 逐一列为选项——不要只列出接下来的一两个。

组件格式：
```
ADR-[NNNN] 已写入，注册表已更新。接下来做什么？
[1] 编写 [下一优先级 ADR 名称] — [来自前置条件列表的简短描述]
[2] 编写 [另一个优先级 ADR] — [简短描述]（列出所有剩余项）
[N] 开始编写 GDD — 运行 `/design-system [第一个未设计的系统]`（仅在所有前置 ADR 写入完成后显示）
[N+1] 本次会话到此结束
```

若没有剩余的优先级 ADR 也没有未设计的 GDD 系统，只提供"到此结束"并建议在新的 Claude Code 会话中运行 `/architecture-review`。

**始终在结束输出中包含以下固定提示（不得省略）：**

> 要验证 ADR 对 GDD 的覆盖范围，请打开**新的 Claude Code 会话**
> 并运行 `/architecture-review`。
>
