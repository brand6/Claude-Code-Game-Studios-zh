---
name: create-stories
description: "将单个功能模块拆分为可实现的用户故事文件。读取功能模块、GDD、治理 ADR 和控制清单。每个用户故事嵌入 GDD 需求 TR-ID、ADR 指南、验收标准、故事类型和测试证据路径。在 /create-epics 之后为每个功能模块运行。"
argument-hint: "[epic-slug | epic-path] [--review full|lean|solo]"
user-invocable: true
agent: lead-programmer
allowed-tools: Read, Glob, Grep, Write, Task, AskUserQuestion
---

调用本技能时：

## 步骤 1：解析参数

解析评审模式（一次性解析，保存供本次运行的所有门禁调用使用）：
1. 若传入了 `--review [full|lean|solo]` → 使用该值
2. 否则读取 `production/review-mode.txt` → 使用其值
3. 否则 → 默认为 `lean`

若未提供功能模块参数，使用 `AskUserQuestion`：
- "要为哪个功能模块创建故事？"提供 Glob `production/epics/*/EPIC.md` 中找到的功能模块列表（显示 slug + 状态）

将功能模块 slug 保存为 **EPIC_SLUG**。功能模块路径：`production/epics/[EPIC_SLUG]/EPIC.md`。

---

## 步骤 2：加载此功能模块的所有内容

读取所有这些内容后再进行任何分析：

1. **功能模块文件**：`production/epics/[epic-slug]/EPIC.md`
   - 提取：层级、GDD 路径、架构模块、治理 ADR 列表、GDD 需求表、完成定义、范围外边界
2. **完整 GDD**：来自功能模块的 GDD 路径
   - 提取：核心规则、状态转换、公式、边界情况、验收标准
3. **治理 ADR**：功能模块中列出的每个 ADR
   - 提取：决策、实现指南章节（这是程序员逐字遵循的）、引擎兼容性注意事项
4. **ADR 存在性验证**：对于功能模块中列出的每个 ADR 路径，验证文件是否存在。
   若任何 ADR 缺失：
   > "缺失 ADR：[path] 未找到。在创建故事之前，通过 `/architecture-decision` 创建 ADR，或纠正功能模块文件中的 ADR 引用。"
   **停止。** 不要在没有所有治理 ADR 存在的情况下创建故事。
5. **控制清单**：`docs/architecture/control-manifest.md`
   - 提取：该层级的规则（功能模块层级字段）

---

## 步骤 3：按类型分类故事

在将 GDD 分解为故事之前，分类该功能模块故事所属的类型。这决定了在 `/story-done` 关闭故事之前需要哪些测试证据。

| 故事类型 | 标准 | 测试要求 |
|---------|------|---------|
| 逻辑 | 纯代码逻辑 —— 公式、规则、状态机、算法 | 自动化单元测试 + 集成测试 |
| 集成 | 跨系统边界 —— 信号/事件、API 调用、数据持久化 | 自动化集成测试 |
| 视觉/感受 | 动画、移动手感、粒子、屏幕效果 | 手动 QA 证据文档 |
| UI | HUD、菜单、对话框、玩家反馈显示 | 手动 UI 测试证据 |
| 配置/数据 | 调整旋钮、平衡值、数据文件更改 | 冒烟测试 |

---

## 步骤 4：将 GDD 分解为故事

识别从 GDD 到故事的映射。规则：

- 每个故事 = ~2-4 小时的实现工作
- 每个故事必须有且仅有一个所有者（由类型决定，在 `/dev-story` 中路由）
- 每个故事必须可独立测试
- 每个故事必须对应至少一个 GDD TR-ID
- 若一个 GDD 功能需要 > 4 小时 → 拆分为多个故事（方法 A + 方法 B + 集成）
- 不为"超出范围"功能模块边界中列出的内容创建故事

生成故事候选清单（暂不写入文件）：

```
## 候选故事：[epic-slug]

[LOGIC] STORY-001：[标题]
  TR-ID：TR-[system]-001
  估计工作量：[1-4] 小时
  验收标准：[标准数量]

[INTEGRATION] STORY-002：[标题]
  TR-ID：TR-[system]-002
  估计工作量：[1-4] 小时
  验收标准：[标准数量]

[VISUAL-FEEL] STORY-003：[标题]
  TR-ID：TR-[system]-003
  估计工作量：[1-4] 小时
  验收标准：[标准数量]
...
```

---

## 步骤 4b：QA 负责人故事就绪性门禁

**评审模式检查** —— 在生成 QL-STORY-READY 之前应用：
- `solo` → 跳过。注明："QL-STORY-READY 已跳过 —— 单人模式。"进入步骤 5。
- `lean` → 跳过。注明："QL-STORY-READY 已跳过 —— 精简模式。"进入步骤 5。
- `full` → 生成门禁。

若评审模式为 `full`：通过 Task 使用门禁 **QL-STORY-READY** 生成 `qa-lead`。

传递：故事候选清单、GDD（核心规则 + 验收标准章节）、控制清单层级规则。

QA 负责人为每个故事生成测试用例规格：
- 对于**逻辑/集成**故事：每个验收标准给出 Given/When/Then + 边界情况
- 对于**视觉/感受/UI**故事：设置/验证/通过条件（描述性的，非代码）

处理裁定结果（来自 `director-gates.md`）：
- `QL-STORY-READY PASS` → 继续步骤 5，将测试用例规格嵌入故事文件
- `QL-STORY-READY CONCERNS(qa-lead)` → 呈现顾虑，询问"调整故事还是继续并记录这些顾虑？"
- `QL-STORY-READY FAIL` → 停止。重新修订故事分解。

---

## 步骤 5：呈现故事供审阅

在写入任何文件之前，呈现完整故事列表：

> **[epic-slug] 的故事分解**
>
> [每个故事的表格：编号、类型、标题、TR-ID、估计工作量]
>
> **总计：** [N] 个故事，约 [总小时数] 小时实现工作
> **未追踪的需求：** [若任何 TR 没有对应故事，列出它们]

使用 `AskUserQuestion`：
- "批准故事分解？"
  - 选项：
    - `[A] 批准 —— 写入所有故事文件`
    - `[B] 修改故事分解 —— 描述需要更改的内容`
    - `[C] 仅写入特定故事 —— 指定编号`
    - `[D] 取消`

---

## 步骤 6：写入故事文件

对每个批准的故事，询问："我可以将故事 [N] 写入 `production/epics/[epic-slug]/story-[NNN]-[slug].md` 吗？"

使用此完整模板（逐字保留字段名，用内容替换括号内的文字）：

```markdown
# 故事：[故事标题]

> **故事 ID**：[epic-slug]-[NNN]（例如 combat-001）
> **层级**：[Foundation/Core/Feature/Presentation]
> **类型**：[逻辑/集成/视觉-感受/UI/配置-数据]
> **功能模块**：production/epics/[epic-slug]/EPIC.md
> **状态**：就绪
> **清单版本**：[控制清单中的日期]

## GDD 需求

**TR-ID**：TR-[system]-[NNN]
**需求**：[来自 GDD 或 TR 注册表的逐字需求文本]
**GDD 章节**：design/gdd/[system-name].md#[章节名]

## 用户故事

作为一名玩家，我希望 [行为]，以便 [效益]。

（配置/数据故事："作为一名设计师，我希望 [数值] 配置为 [值]，以便 [游戏效果]。"）

## 验收标准

- [ ] **GIVEN** [初始状态]，**WHEN** [动作]，**THEN** [可度量的结果]
- [ ] **GIVEN** [初始状态]，**WHEN** [动作]，**THEN** [可度量的结果]
（至少 2 个标准，最多 5 个；每个必须可独立测试）

## 超出范围

- [本故事**不**包含的内容 —— 防止蔓延]

## ADR 指南

**治理 ADR**：docs/architecture/[adr-file].md
**关键决策**：[来自 ADR 决策章节的一句话]
**实现指南**：
> [来自 ADR 实现章节的关键规则 —— 逐字引用，用于防止误解的规则]

**引擎注意事项**（若来自 ADR）：[HIGH/MEDIUM/无 —— 带说明]

## 技术说明

**层级规则（来自控制清单）**：
- 必需：[该层级的相关规则]
- 禁止：[违反的关键禁止规则]

**依赖项**：
- [此故事之前必须完成的故事（epic-slug-NNN 格式）或"无"]

## 测试证据

**类型**：[自动化 / 手动证据 / 冒烟测试]
**路径**：`tests/[system]/test_[feature]_[NNN].[ext]`

（视觉-感受/UI：`production/qa/evidence/[slug]-[NNN]-evidence.md`）
（配置/数据：`production/qa/evidence/[slug]-[NNN]-smoke.md`）

**测试用例规格**（由 QA 负责人验证，若评审模式为 full）：
```
Given: [前提条件]
When: [触发器或动作]
Then: [可验证的结果]
Edge cases: [若存在]
```
```

---

## 步骤 7：写入后

**更新功能模块文件**

写入故事后，用已创建的故事列表更新 `EPIC.md` 的"用户故事"字段：

```markdown
## 用户故事

| 故事 | 类型 | 状态 |
|------|------|------|
| [story-NNN-slug] | 逻辑 | 就绪 |
| [story-NNN-slug] | 集成 | 就绪 |
```

询问："我可以更新 `production/epics/[epic-slug]/EPIC.md` 的用户故事列表吗？"

---

**完成摘要**

> **已为 [epic-slug] 创建 [N] 个故事**
>
> | 故事 | 类型 | 测试要求 |
> |------|------|---------|
> | [标题] | 逻辑 | 自动化测试 |
> | [标题] | 视觉/感受 | 手动证据 |
>
> **未追踪的 TRs**：[列表或"无"]

使用 `AskUserQuestion`：
- "接下来怎么做？"
  - 选项：
    - `[A] 开始实现 —— 运行 /story-readiness story-001 然后 /dev-story`
    - `[B] 为下一个功能模块创建故事 —— 运行 /create-stories [next-epic]`
    - `[C] 规划迭代 —— 运行 /sprint-plan 在实现前安排故事`
    - `[D] 停止`

---

## 协作协议

1. **先读后展示** —— 静默加载所有输入，再展示故事列表
2. **一次性询问** —— 在一个摘要中呈现所有故事，而不是逐一呈现
3. **标注阻塞故事** —— 在写入前标出所有包含 Proposed ADR 的故事
4. **写前获批** —— 在写入文件前，获得完整故事集的批准
5. **不得凭空编造** —— 验收标准来自 GDD，实现说明来自 ADR，规则来自控制清单
6. **绝不启动实现** —— 本技能止步于故事文件层级

写入完成后（或用户拒绝后）：

- **Verdict: COMPLETE** —— 已将 [N] 个故事写入 `production/epics/[epic-slug]/`。运行 `/story-readiness` → `/dev-story` 开始实现。
- **Verdict: BLOCKED** —— 用户拒绝。未写入任何故事文件。
