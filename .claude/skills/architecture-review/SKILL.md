---
name: architecture-review
description: "验证项目架构相对于所有 GDD 的完整性和一致性。建立追溯矩阵，将每条 GDD 技术需求映射到 ADR，识别覆盖缺口，检测跨 ADR 冲突，验证所有决策中引擎兼容性的一致性，并给出 PASS/CONCERNS/FAIL 判定。是 /design-review 的架构等价命令。"
argument-hint: "[focus: full | coverage | consistency | engine | single-gdd path/to/gdd.md]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Task, AskUserQuestion
agent: technical-director
model: opus
---

# 架构评审

架构评审验证完整的架构决策集是否覆盖了所有游戏设计需求，内部是否一致，并正确指向项目锁定的引擎版本。它是技术准备阶段与预制作阶段之间的质量门控。

**参数模式：**
- **无参数 / `full`**：完整评审——所有阶段
- **`coverage`**：仅追溯性——哪些 GDD 需求没有对应 ADR
- **`consistency`**：仅跨 ADR 冲突检测
- **`engine`**：仅引擎兼容性审计
- **`single-gdd [路径]`**：审查某个特定 GDD 的架构覆盖情况
- **`rtm`**：需求追溯矩阵——在标准矩阵基础上扩展 story 文件路径和测试文件路径；输出 `docs/architecture/requirements-traceability.md`，包含完整的 GDD 需求 → ADR → Story → 测试链。在 story 和测试已存在的生产阶段使用。

---

## 阶段 1：加载所有内容

### 阶段 1a — L0：摘要扫描（快速，低 token 消耗）

在读取任何完整文档之前，先使用 Grep 从所有 GDD 和 ADR 中提取 `## Summary` 章节：

```
Grep pattern="## Summary" glob="design/gdd/*.md" output_mode="content" -A 4
Grep pattern="## Summary" glob="docs/architecture/adr-*.md" output_mode="content" -A 3
```

对于 `single-gdd [路径]` 模式：使用目标 GDD 的摘要识别引用了同一系统的 ADR（对 ADR 按系统名称 Grep），然后仅完整读取这些 ADR。完全跳过对无关 GDD 的完整读取。

对于 `engine` 模式：仅完整读取 ADR——引擎检查不需要 GDD。

对于 `coverage` 或 `full` 模式：继续下方的完整文档读取。

### 阶段 1b — L1/L2：完整文档加载

根据模式读取所有适用的输入：

### 设计文档
- 范围内所有 `design/gdd/` 中的 GDD——完整读取每个文件
- `design/gdd/systems-index.md`——系统权威清单

### 架构文档
- 范围内所有 `docs/architecture/` 中的 ADR——完整读取每个文件
- 若存在 `docs/architecture/architecture.md` 则读取

### 引擎参考
- `docs/engine-reference/[engine]/VERSION.md`
- `docs/engine-reference/[engine]/breaking-changes.md`
- `docs/engine-reference/[engine]/deprecated-apis.md`
- `docs/engine-reference/[engine]/modules/` 中的所有文件

### 项目标准
- `.claude/docs/technical-preferences.md`

报告计数："已加载 [N] 个 GDD、[M] 个 ADR，引擎：[名称 + 版本]。"

**同时读取 `docs/consistency-failures.md`**（若存在）。提取 Domain 与当前审查系统匹配的条目（Architecture、Engine 或任何被审查的 GDD 领域）。在阶段 4 冲突检测输出的顶部，将反复出现的模式标注为"已知易冲突区域"。

---

## 阶段 2：从每个 GDD 中提取技术需求

### 预加载 TR 注册表

在提取任何需求之前，若存在 `docs/architecture/tr-registry.yaml`，则先读取。按 `id` 和规范化 `requirement` 文本（小写、去空格）索引现有条目，以防止跨评审运行时 ID 被重新编号。

对于每条提取的需求，匹配规则如下：
1. **与同一系统已有注册表条目完全/近似匹配** → 不变地复用该条目的 TR-ID。仅当 GDD 措辞已变更时更新注册表中的 `requirement` 文本（意图相同，表述更清晰）——添加 `revised: [日期]` 字段。
2. **无匹配** → 分配新 ID：为该系统分配下一个可用的 `TR-[system]-NNN`，从现有最大序号 +1 开始。
3. **模糊**（部分匹配，意图不明确）→ 询问用户：
   > "'[新需求文本]' 是否与 `TR-[system]-NNN: [已有文本]` 指代同一需求，还是一个新需求？"
   用户回答："同一需求"（复用 ID）或"新需求"（新建 ID）。

对于注册表中 `status: deprecated` 的需求——跳过。这是有意从 GDD 中移除的。

对于每个 GDD，读取并提取所有**技术需求**——架构必须提供的内容，以使该系统能够运行。技术需求是任何意味着特定架构决策的陈述。

待提取的类别：

| 类别 | 示例 |
|------|------|
| **数据结构** | "每个实体有血量、最大血量、状态效果" → 需要组件/数据模式 |
| **性能约束** | "碰撞检测必须以 200 个实体 60fps 运行" → 物理预算 ADR |
| **引擎能力** | "角色动画的逆运动学" → IK 系统 ADR |
| **跨系统通信** | "伤害系统同时通知 UI 和音频" → 事件/信号架构 ADR |
| **状态持久化** | "玩家进度在会话间持久保存" → 存档系统 ADR |
| **线程/时序** | "AI 决策在主线程之外进行" → 并发 ADR |
| **平台要求** | "支持键盘、手柄、触控" → 输入系统 ADR |

对于每个 GDD，生成结构化列表：

```
GDD：[文件名]
系统：[系统名称]
技术需求：
  TR-[GDD]-001：[需求文本] → 领域：[Physics/Rendering/等]
  TR-[GDD]-002：[需求文本] → 领域：[...]
```

这将成为**需求基线**——架构必须覆盖的完整内容集。

---

## 阶段 3：建立追溯矩阵

对于阶段 2 中提取的每条技术需求，搜索 ADR：

1. 读取每个 ADR 的"GDD Requirements Addressed"章节
2. 检查是否明确引用了该需求或其 GDD
3. 检查 ADR 的决策文本是否隐含地覆盖了该需求
4. 标记覆盖状态：

| 状态 | 含义 |
|------|------|
| ✅ **Covered** | 某个 ADR 明确解决了此需求 |
| ⚠️ **Partial** | 某个 ADR 部分覆盖了此需求，或覆盖情况模糊 |
| ❌ **Gap** | 没有 ADR 解决此需求 |

建立完整矩阵：

```
## 追溯矩阵

| 需求 ID | GDD | 系统 | 需求 | ADR 覆盖 | 状态 |
|--------|-----|------|------|---------|------|
| TR-combat-001 | combat.md | 战斗 | 命中框检测 < 1 帧 | ADR-0003 | ✅ |
| TR-combat-002 | combat.md | 战斗 | 连击窗口时序 | — | ❌ 缺口 |
| TR-inventory-001 | inventory.md | 背包 | 持久物品存储 | ADR-0005 | ✅ |
```

统计总数：X 已覆盖，Y 部分覆盖，Z 缺口。

---

## 阶段 3b：Story 和测试关联（仅 RTM 模式）

*除非参数为 `rtm` 或 `full` 且 story 已存在，否则跳过此阶段。*

此阶段将阶段 3 矩阵扩展为包含实现每条需求的 story 及其验证测试——生成完整的需求追溯矩阵（RTM）。

### 步骤 3b-1 — 加载 story

Glob `production/epics/**/*.md`（排除 EPIC.md 索引文件）。对每个 story 文件：
- 从 Context 章节提取 `TR-ID`
- 提取 story 文件路径、标题、状态
- 提取 `## Test Evidence` 章节——声明的测试文件路径

### 步骤 3b-2 — 加载测试文件

Glob `tests/unit/**/*_test.*` 和 `tests/integration/**/*_test.*`。
建立索引：系统 → [测试文件路径]。

对于步骤 3b-1 中的每个测试文件路径，通过 Glob 确认文件是否实际存在。若声明路径不存在则标注 MISSING。

### 步骤 3b-3 — 建立扩展 RTM

对于阶段 3 矩阵中的每个 TR-ID，添加：
- **Story**：引用此 TR-ID 的 story 文件路径（可能多个）
- **Test File**：story 的 Test Evidence 章节中声明的测试文件路径
- **Test Status**：COVERED（测试文件存在）/ MISSING（路径已声明但未找到）/ NONE（未声明测试路径，story 类型可能为 Visual/Feel/UI）/ NO STORY（需求尚无 story——预制作缺口）

扩展矩阵格式：

```
## 需求追溯矩阵（RTM）

| TR-ID | GDD | 需求 | ADR | Story | 测试文件 | 测试状态 |
|-------|-----|------|-----|-------|---------|---------|
| TR-combat-001 | combat.md | 命中框 < 1 帧 | ADR-0003 | story-001-hitbox.md | tests/unit/combat/hitbox_test.gd | COVERED |
| TR-combat-002 | combat.md | 连击窗口 | — | story-002-combo.md | — | NONE (Visual/Feel) |
| TR-inventory-001 | inventory.md | 持久存储 | ADR-0005 | — | — | NO STORY |
```

RTM 覆盖摘要：
- COVERED：[N] — 需求含 ADR + story + 通过测试
- MISSING test：[N] — story 存在但测试文件未找到
- NO STORY：[N] — ADR 存在但 story 尚未存在
- NO ADR：[N] — 需求无架构覆盖（来自阶段 3 缺口）
- 完整链路完成（COVERED）：[N/total]（[%]）

---

## 阶段 4：跨 ADR 冲突检测

将每个 ADR 与其他所有 ADR 对比，检测矛盾。以下情况视为冲突：

- **数据所有权冲突**：两个 ADR 声称对同一数据拥有独占所有权
- **集成约定冲突**：ADR-A 假设系统 X 具有接口 Y，但 ADR-B 将系统 X 定义为不同接口
- **性能预算冲突**：ADR-A 为物理分配 N ms，ADR-B 为 AI 分配 N ms，合计超出总帧预算
- **依赖循环**：ADR-A 要求系统 X 在 Y 之前初始化；ADR-B 要求 Y 在 X 之前初始化
- **架构模式冲突**：ADR-A 对某子系统使用事件驱动通信；ADR-B 对同一子系统使用直接函数调用
- **状态管理冲突**：两个 ADR 都声称对同一游戏状态拥有权威（例如战斗 ADR 和角色 ADR 都声称拥有血量值）

对于发现的每个冲突：

```
## 冲突：[ADR-NNNN] vs [ADR-MMMM]
类型：[数据所有权 / 集成 / 性能 / 依赖 / 模式 / 状态]
ADR-NNNN 声明：[...]
ADR-MMMM 声明：[...]
影响：[若两者都按原样实现，会造成什么问题]
解决选项：
  1. [选项 A]
  2. [选项 B]
```

### ADR 依赖排序

冲突检测后，分析所有 ADR 的依赖图：

1. **收集所有 ADR "ADR Dependencies" 章节中的 `Depends On` 字段**
2. **拓扑排序**：确定正确的实现顺序——无依赖的 ADR 优先（Foundation），依赖它们的 ADR 次之，依此类推
3. **标记未解决的依赖**：若 ADR-A 的"Depends On"字段引用了仍为 `Proposed` 或不存在的 ADR，标记如下：
   ```
   ⚠️  ADR-0005 依赖 ADR-0002——但 ADR-0002 仍为 Proposed。
       ADR-0002 Accepted 之前，ADR-0005 无法安全实现。
   ```
4. **循环检测**：若 ADR-A 依赖 ADR-B 且 ADR-B 依赖 ADR-A（直接或间接），标记为 `DEPENDENCY CYCLE`：
   ```
   🔴 依赖循环：ADR-0003 → ADR-0006 → ADR-0003
      必须打破此循环，两者才能实现。
   ```
5. **输出推荐实现顺序**：
   ```
   ### 推荐 ADR 实现顺序（拓扑排序）
   Foundation（无依赖）：
     1. ADR-0001：[标题]
     2. ADR-0003：[标题]
   依赖 Foundation：
     3. ADR-0002：[标题]（需要 ADR-0001）
     4. ADR-0005：[标题]（需要 ADR-0003）
   特性层：
     5. ADR-0004：[标题]（需要 ADR-0002、ADR-0005）
   ```

---

## 阶段 5：引擎兼容性交叉检查

在所有 ADR 中检查引擎一致性：

### 版本一致性
- 所有提及引擎版本的 ADR 是否指向同一版本？
- 若有 ADR 是针对旧版本引擎编写的，标记为可能已过时

### 截止日期后 API 一致性
- 收集所有 ADR 中的"Post-Cutoff APIs Used"字段
- 对每个字段，与相关模块参考文档核对
- 检查是否有两个 ADR 对同一截止日期后 API 做出了矛盾假设

### 已废弃 API 检查
- 在所有 ADR 中 Grep `deprecated-apis.md` 中列出的 API 名称
- 标记引用了已废弃 API 的 ADR

### 缺失引擎兼容性章节
- 列出所有完全缺失 Engine Compatibility 章节的 ADR
- 这些是盲点——其引擎假设未知

输出格式：
```
### 引擎审计结果
引擎：[名称 + 版本]
含 Engine Compatibility 章节的 ADR：X / Y 总数

已废弃 API 引用：
  - ADR-0002：使用了 [已废弃 API] — 自 [版本] 起废弃

过时版本引用：
  - ADR-0001：针对 [旧版本] 编写 — 当前项目版本为 [版本]

截止日期后 API 冲突：
  - ADR-0004 和 ADR-0007 对 [API] 使用了不兼容的假设
```

---

### 引擎专家咨询

完成上述引擎审计后，生成**主要引擎专家** Task，获取领域专家的第二意见：
- 读取 `.claude/docs/technical-preferences.md` 中的 `Engine Specialists` 章节，获取主要专家
- 若未配置引擎，跳过此咨询
- 生成 `subagent_type: [主要专家]`，提供：所有含引擎特定决策或 `Post-Cutoff APIs Used` 字段的 ADR、engine-reference 文档以及阶段 5 审计结果。要求其：
  1. 确认或质疑每条审计发现——专家可能了解参考文档中未记录的引擎细节
  2. 识别审计可能遗漏的 ADR 中的引擎特定反模式（例如使用了错误的 Godot 节点类型、Unity 组件耦合、Unreal 子系统误用）
  3. 标记对引擎行为做出与实际锁定版本不同假设的 ADR

在阶段 5 输出中的 `### 引擎专家发现` 下纳入额外发现。这些发现与审计发现具有同等权重，都会影响最终判定。

---

## 阶段 5b：设计修订标记（架构 → GDD 反馈）

对于阶段 5 中的每个**高风险引擎发现**，检查是否有 GDD 做出了与已验证引擎现实相矛盾的假设。

需检查的具体情况：

1. **截止日期后 API 行为与训练数据假设不同**：若 ADR 记录了与 LLM 默认假设不同的已验证 API 行为，检查引用相关系统的所有 GDD，查找基于旧（假设）行为编写的设计规则。

2. **ADR 中记录的已知引擎限制**：若 ADR 记录了已知引擎限制（例如"Jolt 忽略 HingeJoint3D damp"、"D3D12 现为默认后端"），检查设计了受影响特性机制的 GDD。

3. **已废弃 API 冲突**：若阶段 5 标记了 ADR 中使用的已废弃 API，检查是否有 GDD 包含假定了该已废弃 API 行为的机制。

对于发现的每个冲突，记录到 GDD 修订标记表：

```
### GDD 修订标记（架构 → 设计反馈）
这些 GDD 假设与已验证的引擎行为或已 Accepted 的 ADR 相冲突。
相关系统进入实现阶段之前应先修订 GDD。

| GDD | 假设 | 实际情况（来自 ADR/engine-reference） | 操作 |
|-----|------|--------------------------------------|------|
| combat.md | "使用 HingeJoint3D damp 实现武器后坐力" | Jolt 忽略 damp — ADR-0003 | 修订 GDD |
```

若无修订标记，写："无 GDD 修订标记——所有 GDD 假设与已验证引擎行为一致。"

询问："是否要在 systems index 中标记这些 GDD 待修订？"
- 若是：将相关系统的 Status 字段更新为"Needs Revision"，并在相邻的 Notes/Description 列中添加简短内联说明解释冲突。在写入前请求审批。
  （不要使用括号注释，如"Needs Revision (Architecture Feedback)"——其他技能匹配精确字符串"Needs Revision"，括号注释会破坏该匹配。）

---

## 阶段 6：架构文档覆盖检查

若 `docs/architecture/architecture.md` 存在，对照 GDD 进行验证：

- `systems-index.md` 中的每个系统是否都出现在架构层中？
- 数据流章节是否覆盖了 GDD 中定义的所有跨系统通信？
- API 边界是否支持 GDD 中所有集成需求？
- 架构文档中是否有无对应 GDD 的系统（孤立架构）？

---

## 阶段 7：输出评审报告

```
## 架构评审报告
日期：[日期]
引擎：[名称 + 版本]
已审查 GDD：[N]
已审查 ADR：[M]

---

### 追溯摘要
总需求数：[N]
✅ 已覆盖：[X]
⚠️ 部分覆盖：[Y]
❌ 缺口：[Z]

### 覆盖缺口（无对应 ADR）
对每个缺口：
  ❌ TR-[id]：[GDD] → [系统] → [需求]
     建议 ADR："/architecture-decision [建议标题]"
     领域：[Physics/Rendering/等]
     引擎风险：[LOW/MEDIUM/HIGH]

### 跨 ADR 冲突
[阶段 4 中的所有冲突列表]

### ADR 依赖顺序
[来自阶段 4 依赖排序章节的拓扑排序实现顺序]
[未解决的依赖和循环（若有）]

### GDD 修订标记
[与已验证引擎行为冲突的 GDD 假设——来自阶段 5b]
[或："无——所有 GDD 假设与已验证引擎行为一致"]

### 引擎兼容性问题
[阶段 5 中的所有引擎问题列表]

### 架构文档覆盖
[阶段 6 中缺失的系统和孤立架构列表]

---

### 判定：[PASS / CONCERNS / FAIL]

PASS：所有需求已覆盖，无冲突，引擎一致
CONCERNS：部分缺口或部分覆盖，但无阻塞性冲突
FAIL：关键缺口（Foundation/Core 层需求未覆盖），
      或检测到阻塞性跨 ADR 冲突

### 阻塞项（PASS 前必须解决）
[必须解决的条目列表——仅 FAIL 判定时]

### 需要创建的 ADR
[按优先级排列的 ADR 创建清单，最基础的优先]
```

---

## 阶段 8：写入并更新追溯索引

使用 `AskUserQuestion` 获取写入审批：
- "评审完成。您希望写入哪些内容？"
  - [A] 写入全部三个文件（评审报告 + 追溯索引 + TR 注册表）
  - [B] 仅写入评审报告——`docs/architecture/architecture-review-[date].md`
  - [C] 暂不写入——我需要先审阅发现内容

### RTM 输出（仅 rtm 模式）

对于 `rtm` 模式，额外询问："是否可以将完整需求追溯矩阵写入 `docs/architecture/requirements-traceability.md`？"

RTM 文件格式：

```markdown
# 需求追溯矩阵（RTM）

> 最后更新：[日期]
> 模式：/architecture-review rtm
> 覆盖率：[N]% 完整链路完成（GDD → ADR → Story → 测试）

## 如何阅读此矩阵

| 列名 | 含义 |
|------|------|
| TR-ID | 来自 tr-registry.yaml 的稳定需求 ID |
| GDD | 来源设计文档 |
| ADR | 管理实现的架构决策 |
| Story | 实现此需求的 story 文件 |
| Test File | 自动化测试文件路径 |
| Test Status | COVERED / MISSING / NONE / NO STORY |

## 完整追溯矩阵

| TR-ID | GDD | 需求 | ADR | Story | 测试文件 | 状态 |
|-------|-----|------|-----|-------|---------|------|
[来自阶段 3b 的完整矩阵行]

## 覆盖摘要

| 状态 | 数量 | % |
|------|------|---|
| COVERED — 完整链路完成 | [N] | [%] |
| MISSING test — story 存在，无测试 | [N] | [%] |
| NO STORY — ADR 存在，尚未实现 | [N] | [%] |
| NO ADR — 架构缺口 | [N] | [%] |
| **总需求数** | **[N]** | **100%** |

## 未覆盖需求（优先修复清单）

链路断裂的需求，按层级优先排序：

### Foundation 层缺口
[按缺口列出并提供建议操作]

### Core 层缺口
[列表]

### Feature / Presentation 层缺口
[列表——低优先级]

## 历史

| 日期 | 完整链路 % | 备注 |
|------|-----------|------|
| [日期] | [%] | 初始 RTM |
```

### TR 注册表更新

同时询问："是否可以用本次评审中的新需求 ID 更新 `docs/architecture/tr-registry.yaml`？"

若是：
- **追加**本次评审之前不在注册表中的所有新 TR-ID
- **更新** GDD 措辞有变化的条目的 `requirement` 文本和 `revised` 日期（ID 保持不变）
- **标记** `status: deprecated`：GDD 需求已不存在的注册表条目（标记前需与用户确认）
- **不要**重新编号或删除现有条目
- 更新顶部的 `last_updated` 和 `version` 字段

这确保所有后续 story 文件都能引用在每次架构评审中持久存在的稳定 TR-ID。

### 反思日志更新

写入评审报告后，将阶段 4 中发现的所有 🔴 CONFLICT 条目追加到 `docs/consistency-failures.md`（若文件存在）：

```markdown
### [YYYY-MM-DD] — /architecture-review — 🔴 CONFLICT
**Domain**: Architecture / [具体领域，如 State Ownership、Performance]
**Documents involved**: [ADR-NNNN] vs [ADR-MMMM]
**What happened**: [具体冲突——每个 ADR 的声明内容]
**Resolution**: [已解决或应如何解决]
**Pattern**: [针对该领域未来 ADR 作者的通用教训]
```

仅追加 CONFLICT 条目——不记录 GAP 条目（架构完成前出现缺失 ADR 是正常现象）。若文件不存在，不创建——仅在已存在时追加。

### 会话状态更新

写入所有已批准文件后，静默追加到 `production/session-state/active.md`：

    ## Session Extract — /architecture-review [日期]
    - Verdict: [PASS / CONCERNS / FAIL]
    - Requirements: [N] total — [X] covered, [Y] partial, [Z] gaps
    - New TR-IDs registered: [N, or "None"]
    - GDD revision flags: [逗号分隔的 GDD 名称，或"None"]
    - Top ADR gaps: [报告中前 3 条缺口标题，或"None"]
    - Report: docs/architecture/architecture-review-[date].md

若 `active.md` 不存在，以此块作为初始内容创建文件。
在对话中确认："Session state updated。"

追溯索引格式：

```markdown
# Architecture Traceability Index
Last Updated: [日期]
Engine: [名称 + 版本]

## Coverage Summary
- Total requirements: [N]
- Covered: [X] ([%])
- Partial: [Y]
- Gaps: [Z]

## Full Matrix
[来自阶段 3 的完整追溯矩阵]

## Known Gaps
[所有 ❌ 条目及建议的 ADR]

## Superseded Requirements
[GDD 在 ADR 编写后有变更的需求]
```

---

## 阶段 9：交接

完成评审并写入已批准文件后，展示：

1. **即时行动**：列出优先级最高的 3 个待创建 ADR（影响最大的缺口优先，Foundation 层优先于 Feature 层）
2. **门控指引**："当所有阻塞问题解决后，运行 `/gate-check pre-production` 推进到下一阶段"
3. **重新运行触发器**："每写完一个新 ADR 后重新运行 `/architecture-review`，以验证覆盖率是否提升"

然后通过 `AskUserQuestion` 收尾：
- "架构评审完成。接下来你想做什么？"
  - [A] 补写缺失的 ADR — 开启新会话并运行 `/architecture-decision [系统]`
  - [B] 运行 `/gate-check pre-production` — 若所有阻塞缺口已解决
  - [C] 本次会话到此结束

---

## 错误恢复协议

若任何被召唤的代理返回 BLOCKED、报错或未能完成：

1. **立即呈报**：在继续之前报告"[AgentName]: BLOCKED — [原因]"
2. **评估依赖**：若被阻塞代理的输出是后续阶段的必要条件，在未获得用户输入的情况下不要推进到该阶段之后
3. 通过 AskUserQuestion **提供三种选项**：
   - 跳过该代理，在最终报告中记录缺口
   - 以更小范围重试（更少的 GDD、单系统聚焦）
   - 停止并先解决阻塞问题
4. **始终生成部分报告** — 输出所有已完成的内容，确保工作不丢失

---

## 协作协议

1. **静默读取** — 不要旁白每一个文件读取过程
2. **展示矩阵** — 在请求任何操作之前先呈现完整的追溯矩阵；让用户看到当前状态
3. **不要猜测** — 如果某个需求含义模糊，询问："[X] 是技术需求还是设计偏好？"
4. **写入前询问** — 写入报告文件前始终确认
5. **非阻塞性** — 判定仅供参考；用户决定是否在 CONCERNS 甚至 FAIL 情况下继续推进
