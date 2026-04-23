# 示例会话：/adopt — 存量项目接入

**背景：** 开发者在发现此智能体系统之前，已构建游戏 3 个月。他们有代码、部分设计文档和粗略笔记——但没有符合技能所需格式的任何内容。

**初始状态：**
- `src/gameplay/` — 约 4000 行 Godot 4.6 GDScript
- `design/` — 3 个 Markdown 文件，内含粗略设计笔记（非 GDD 模板格式）
- 无 `design/gdd/` 目录
- 无 `docs/architecture/` 目录
- 无 `production/` 目录
- 无 `design/gdd/systems-index.md`
- CLAUDE.md 存在（引擎已配置：Godot 4.6）

**会话时长：** 约 30 分钟
**轮数：** 8
**结果：** 接入计划已写入，最紧急的差距（缺少系统索引）立即修复

---

## 第 1 轮：用户调用 /adopt

**用户：**
> /adopt

## 第 2 轮：智能体检测项目状态

**智能体（technical-director，通过 /adopt，上下文：fork）：**
> 正在运行存量项目审计……
>
> **阶段 1：项目状态检测**
>
> | 工件类别 | 是否存在 | 备注 |
> |---------|---------|------|
> | 引擎配置 | ✅ | CLAUDE.md 中已配置 Godot 4.6 |
> | 源代码 | ✅ | `src/gameplay/` 中约 4000 行 |
> | 设计文档 | ⚠️ | `design/` 中有 3 个文件，非 GDD 格式 |
> | 架构文档 | ❌ | `docs/architecture/` 缺失 |
> | 系统索引 | ❌ | `design/gdd/systems-index.md` 缺失 |
> | 生产追踪 | ❌ | `production/` 目录缺失 |
> | 冲刺/故事文件 | ❌ | 无 |
>
> **阶段 2：格式审计（现有文件）**
>
> 检查 3 个设计文件的内部结构……
>
> *`design/combat-notes.md`：*
> - 内含非正式笔记，无 GDD 模板章节
> - 包含：部分规则描述、伤害公式、粗略平衡数字
> - 缺少 GDD 模板中的：概述、玩家幻想、边缘情况、依赖关系、调节旋钮、验收标准（8 节中缺 6 节）
>
> *`design/crafting-ideas.md`：*
> - 头脑风暴式笔记，无结构
> - 无公式，无验收标准
> - 代表早期概念思考——可作为 GDD 的输入，但尚非 GDD
>
> *`design/inventory.md`：*
> - 最接近 GDD——有概述和规则章节
> - 缺少：玩家幻想、公式、边缘情况、调节旋钮、验收标准（8 节中缺 5 节）
>
> **阶段 3：差距分类**
>
> | 差距 | 严重程度 | 原因 |
> |------|---------|------|
> | 无系统索引 | BLOCKING | `/design-system`、`/create-stories`、`/gate-check` 均需要它 |
> | GDD 文件非模板格式 | HIGH | 技能无法从格式错误的 GDD 中引用 TR-ID |
> | 无架构文档 | HIGH | 无法运行 `/architecture-review` 或 `/create-control-manifest` |
> | 无生产追踪 | MEDIUM | 冲刺和故事技能无法工作，但在生产阶段之前不需要 |
> | `design/crafting-ideas.md` — GDD 前期内容 | LOW | 可作为输入使用；在阻塞任何内容之前，需要完整 GDD 创作 |

## 第 3 轮：智能体呈现迁移计划

**智能体：**
> **阶段 4：迁移计划**
>
> 7 个有序步骤，让你的项目完全符合要求。**绝不覆盖你的现有内容**——每一步仅填补差距。
>
> | # | 步骤 | 技能 | 优先级 | 备注 |
> |---|------|------|--------|------|
> | 1 | 创建 `design/gdd/systems-index.md` | `/map-systems` 或 `/adopt` 内联 | BLOCKING | 解锁所有下游技能 |
> | 2 | 改造 `design/inventory.md` → GDD 格式 | `/design-system retrofit design/inventory.md` | HIGH | 补充 5 个缺失章节，保留现有内容 |
> | 3 | 改造 `design/combat-notes.md` → GDD 格式 | `/design-system retrofit design/combat-notes.md` | HIGH | 补充 6 个缺失章节 |
> | 4 | 将 `design/crafting-ideas.md` 转换为完整 GDD | `/design-system crafting`（全新创作，使用想法文件作为输入） | MEDIUM | 非改造——内容太非正式，无法改造 |
> | 5 | 从现有代码创建架构 ADR | `/reverse-document` + `/architecture-decision` | HIGH | 捕获代码中已做出的决策 |
> | 6 | 创建主架构文档 | `/create-architecture` | HIGH | 在 ADR 之后 |
> | 7 | 设置生产追踪 | `/sprint-plan new` | MEDIUM | 在架构阶段之后 |
>
> **重要提示：** 步骤 1 必须在所有其他步骤之前完成。其他步骤可以并行完成或根据你的优先级重新排序。
>
> 我可以将此计划写入 `docs/adoption-plan-2026-03-12.md` 吗？

**用户：**
> 可以。写入它。

**智能体写入接入计划。**

## 第 4 轮：智能体提议修复最紧急的差距

**智能体：**
> BLOCKING 差距是缺少 `design/gdd/systems-index.md`。
>
> 我可以现在通过读取你的现有代码和设计文档来推断你已构建了哪些系统，来立即创建它。这比从头运行 `/map-systems` 更快——我会根据现有内容填充它，然后你确认或调整。
>
> 你希望我现在这样做吗？

**用户：**
> 是的，做吧。

## 第 5 轮：智能体读取代码库并起草系统索引

**智能体：**
> 读取 `src/gameplay/` 以推断系统……
>
> 在代码中发现了以下系统边界：
>
> - `src/gameplay/combat/` — 伤害计算、命中检测、状态效果
> - `src/gameplay/inventory/` — 物品管理、重量、堆叠
> - `src/gameplay/crafting/` — 配方查找、结果生成（引用背包）
> - `src/gameplay/movement/` — CharacterBody2D，地形修正器（被战斗引用，用于定位）
> - `src/gameplay/ui/` — HUD、背包界面、对话框
> - `src/gameplay/world/` — 瓦片地图、地形类型、区块加载
>
> **系统索引草稿：**
>
> | 系统 | 类别 | 优先级 | 依赖关系 | GDD 状态 |
> |------|------|--------|---------|---------|
> | 移动 | 基础 | MVP | 无 | ❌ 缺失 |
> | 世界/地形 | 基础 | MVP | 移动 | ❌ 缺失 |
> | 战斗 | 核心 | MVP | 移动 | ⚠️ 需要改造 |
> | 背包 | 核心 | MVP | 无 | ⚠️ 需要改造 |
> | 合成 | 功能 | MVP | 背包 | ❌ 仅有前期内容 |
> | UI / HUD | 呈现 | MVP | 战斗、背包、移动 | ❌ 缺失 |
>
> 这看起来正确吗？我是否遗漏或误分类了什么？

**用户：**
> 看起来正确。添加一个耐力系统——它在 combat/ 中，但应该是独立的系统。

**智能体：**
> 已将耐力作为核心 / MVP 系统添加：
>
> | 耐力 | 核心 | MVP | 移动、战斗 | ❌ 缺失 |
>
> 依赖关系更新：移动依赖耐力（移动消耗耐力）。
>
> 我可以将此写入 `design/gdd/systems-index.md` 吗？

## 第 6 轮：用户批准

**用户：**
> 可以

**智能体写入 `design/gdd/systems-index.md`。**

## 第 7 轮：智能体展示现已解锁的内容

**智能体：**
> `design/gdd/systems-index.md` 已创建。
>
> **BLOCKING 差距已解决。** 以下技能现在可以运行：
>
> - ✅ `/design-system [name]` — 任何系统的引导式 GDD 创作
> - ✅ `/design-system retrofit [path]` — 填补现有文档中缺失的章节
> - ✅ `/gate-check` — 现在有系统索引可以验证
> - ✅ `/help` — 现在可以显示正确的阶段工作流
>
> **推荐的后续步骤（来自接入计划）：**
>
> 1. 运行 `/design-system retrofit design/inventory.md` — 你最完整的现有文档，最容易获得进展
> 2. 运行 `/design-system retrofit design/combat-notes.md`
> 3. 运行 `/design-system crafting` — 使用你的想法文件作为输入，创作合成 GDD
>
> 完成这 3 步后，你将有 7 个系统中的 5 个具备完整 GDD。然后运行 `/review-all-gdds` 在开始架构工作之前发现跨系统一致性问题。

## 第 8 轮：用户确认计划

**用户：**
> 完美。我先从背包改造开始。

**智能体：**
> 运行：
> ```
> /design-system retrofit design/inventory.md
> ```
>
> 技能将检测你现有的概述和规则章节，向你展示 8 个章节中哪些缺失，并仅对缺口运行章节循环。你现有的内容不会被触动。

---

## 本示例展示了什么

- **格式审计，而非存在性审计**：`/adopt` 不仅检查文件是否存在——还检查其内部结构是否符合技能期望。一个名为 `gdd.md` 但没有模板章节的文件会被标记为差距。
- **迁移，而非替换**：现有内容永远不会被覆盖。计划只填补差距。
- **BLOCKING 差距优先浮出**：缺少系统索引被识别为 BLOCKING，因为它阻止了最多技能运行。
- **紧急差距的内联创建**：智能体不仅仅报告差距，还在同一会话中提议立即修复它。
- **从代码推断**：系统索引从代码库结构引导，而非从头撰写——存量项目代码本身就包含答案。
- **改造 vs. 全新创作**：`/design-system retrofit` 处理已存在但不完整的文档；完整的 `/design-system` 处理全新文档。接入计划区分了每个文件适用哪种方式。
- **上下文：fork**：`/adopt` 在 forked 上下文中运行，以避免在整个代码库的大量文件读取中污染主会话。
