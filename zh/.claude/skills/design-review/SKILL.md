---
name: design-review
description: "评审游戏设计文档（GDD）的完整性、内部一致性、可实现性及项目设计标准符合性。在将设计文档移交给程序员之前运行。"
argument-hint: "[doc: path/to/gdd.md] [--depth full|lean|solo]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Task, AskUserQuestion
---

# 设计评审

本技能对单个游戏设计文档（GDD）执行严格评审。目标是在程序员开始实现之前，捕获设计层面的漏洞、不一致之处和可实现性问题。一份通过评审的 GDD 意味着：它是完整的、内部一致的、可实现的，并与项目其他部分保持一致。

**输出：** `design/review-log.md`（追加）+ 即时评审摘要

---

## 阶段 0：解析参数

解析参数：
- `doc:` → 必填。要评审的 GDD 文件路径
- `--depth full|lean|solo` → 可选。默认为 `full`

**深度模式说明：**
- `full` — 完整的多智能体评审，包含专家对抗评审（阶段 3b）
- `lean` — 正式文档评审，不含专家对抗评审
- `solo` — 基础检查清单评审，不含任何智能体生成；适合快速自检

如果未提供 `doc:`，使用 `AskUserQuestion` 提示用户："请提供要评审的 GDD 路径。"

---

## 阶段 1：加载文档

读取目标 GDD，并加载以下上下文：

### 依赖图验证
- 读取 `design/systems-index.md` — 识别此系统的依赖和被依赖方
- 读取所有被列为依赖项的 GDD（仅加载摘要段落和接口章节）

### 世界观与叙事对齐
- 读取 `design/gdd/world-bible.md`（如果存在）— 或主要叙事/世界构建文档
- 检查：机制是否与世界规则存在矛盾

### 先前评审检查
- Grep `design/review-log.md` 查找此文档的先前评审条目
- 如果存在先前评审：读取它并列出在该轮中标记为 BLOCKING 的未解决问题

报告加载内容：
> "已加载：[GDD 标题]  
> 依赖项：[N] 个 GDD  
> 先前评审：[无 / 发现 N 个条目，其中 M 个有 BLOCKING 问题]"

---

## 阶段 2：完整性检查

验证 GDD 是否包含所有必需章节：

| 章节 | 状态 | 说明 |
|------|------|------|
| 概述 / 摘要 | ✅ / ❌ | |
| 设计目标 | ✅ / ❌ | |
| 核心机制 | ✅ / ❌ | |
| 玩家行为与输入 | ✅ / ❌ | |
| 胜败条件 / 反馈循环 | ✅ / ❌ | |
| 进度与难度 | ✅ / ❌ | |
| 依赖系统 | ✅ / ❌ | |
| 范围信号（S/M/L/XL） | ✅ / ❌ | |
| 未解决的设计问题 | ✅ / ❌ | |

如果有任何关键章节缺失（概述、核心机制、玩家行为、胜败条件）：
> "⚠️ 此 GDD 缺少关键章节（列出）。建议在进行全面评审之前先补全这些章节。是否继续进行部分评审？"

使用 `AskUserQuestion` 询问用户是继续还是暂停。

---

## 阶段 3：一致性与可实现性

### 内部一致性
检查 GDD 内部：
- 不同章节之间是否存在相互矛盾的规则（例如：第 2 节说"玩家最多携带 5 件道具"，第 4 节说"背包无限"）
- 在文档中定义了多次但值不同的数字
- 某处引用了但未曾定义的机制

### 可实现性
使用 `Grep` 检查代码库中与此系统相关的内容，判断：
- GDD 假设的功能在技术上是否可行（不超出已知约束）
- GDD 是否需要尚未存在的系统（依赖系统缺失）
- GDD 是否假设了当前引擎/技术栈中已知不支持的某项功能

### 跨系统一致性
与阶段 1 中加载的依赖 GDD 对比：
- 此 GDD 定义的值是否与被依赖 GDD 中的值存在冲突？
- 是否有系统声明了互斥的规则？
- 接口点是否匹配（例如：战斗 GDD 说"每次命中造成 [combat-damage]"，伤害 GDD 是否定义了 `combat-damage`）？

---

## 阶段 3b：专家对抗评审

**仅适用于 `full` 模式。**

`lean` 和 `solo` 模式跳过此阶段，继续进行阶段 4。

通过 Task 工具**并行**生成以下子智能体（仅生成与此 GDD 系统类型相关的智能体）：

| 智能体 | 关注重点 |
|--------|---------|
| `systems-designer` | 数学合理性、可能的霸权策略、经济不平衡 |
| `gameplay-programmer` | 实现复杂性、技术风险、状态机可行性 |
| `ux-designer` | 玩家可理解性、摩擦点、信息过载 |
| `game-designer` | 与核心设计支柱的一致性、乐趣度 |

每个智能体提供：
- 顶级关注项（最多 3 条，需可操作）
- 具体推荐（每项附带建议的 GDD 修改）
- 是否建议批准此 GDD

收集所有结果后，通过 Task 工具生成 `creative-director` 子智能体综合各方意见：
- 解决相互冲突的专家意见
- 确定优先级最高的问题
- 提供最终创意总监判断

---

## 阶段 4：输出评审

综合所有阶段的发现，生成评审摘要：

### 评审摘要格式

```
## 设计评审：[GDD 标题]
**日期**：[日期]
**深度模式**：[full / lean / solo]
**评审人**：[智能体 ID]

### 裁定
[APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED]

### 范围信号
[S — 几天工作量 / M — 1 周 / L — 2–3 周 / XL — 需拆解]

### 完整性
[已通过 / 缺少 N 个章节]

### BLOCKING 问题（如有）
- [问题 1]
- [问题 2]

### 一般问题（非阻断性）
- [问题 1]
- [问题 2]

### 专家关注项（full 模式）
**systems-designer**：[关注项]
**gameplay-programmer**：[关注项]
**ux-designer**：[关注项]
**game-designer**：[关注项]
**creative-director 综合意见**：[综合判断]

### 推荐
- [可操作的修改建议]
```

**裁定标准：**
- **APPROVED** — 无 BLOCKING 问题；少量一般问题是可接受的
- **NEEDS REVISION** — 存在 1–3 个 BLOCKING 问题，需修复后重新评审
- **MAJOR REVISION NEEDED** — 存在 4 个以上 BLOCKING 问题，或核心设计前提有误

---

## 阶段 5：后续步骤

展示评审摘要后：

**询问 1 — 修订：**
使用 `AskUserQuestion`："根据此评审，您想立即修订 GDD 吗？"
选项：`[A] 是——引导我修订` / `[B] 否——我稍后处理`

如果选 [A]：对每个 BLOCKING 问题，展示具体的 GDD 修改建议并请求确认。

**询问 2 — 更新 systems index：**
如果范围信号已更改或发现了新的系统依赖：
"是否允许我用更新后的依赖关系更新 `design/systems-index.md`？"

**询问 2b — 修订后关闭小部件（修订流程 [A] 完成后显示）：**

使用 `AskUserQuestion`：
- 提示："修订完成 —— 已解决 [N] 个阻断项。下一步？"
- 若当前会话上下文较高（~50% 以上），附注："（建议：/clear 后重新评审 —— 完整评审需运行 5 个智能体，需要干净的上下文。）"
- 选项：
  - `[A] 新会话中重新评审 —— 运行 /design-review [doc-path]（/clear 之后）`
  - `[B] 接受修订并标记为已批准 —— 更新系统索引，跳过重新评审`
  - `[C] 进入下一个系统 —— /design-system [next-system]（设计顺序中的第 N 个）`
  - `[D] 到此为止`

**询问 3 — 追加至评审日志：**
使用 `AskUserQuestion`："是否允许我将此评审追加至 `design/gdd/reviews/[doc-name]-review-log.md`？这将创建修订历史，以便未来重新评审时追踪变更。"

如果是：以以下格式追加一条记录：

```markdown
## Review — [YYYY-MM-DD] — Verdict: [APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED]
Scope signal: [S/M/L/XL]
Specialists: [list]
Blocking items: [count] | Recommended: [count]
Summary: [2-3 sentence summary of key findings from creative-director verdict]
Prior verdict resolved: [Yes / No / First review]
```

**最终关闭小部件（所有文件写入完成后显示）：**

读取项目状态，动态构建选项列表（仅包含真正适用的下一步）：

使用 `AskUserQuestion`：
- 提示："[系统名称] 设计评审完成。下一步？"
- 动态选项（仅包含适用项）：
  - `[_] 运行 /design-review [other-gdd-path] —— [系统名] 仍处于 [In Review / NEEDS REVISION]`（若还有其他 GDD 需要评审则包含）
  - `[_] 运行 /consistency-check —— 验证此 GDD 的数值与现有 GDD 不冲突`（若存在至少 1 个其他 GDD 则始终包含）
  - `[_] 运行 /review-all-gdds —— 跨所有已设计系统进行整体设计理论评审`（若存在 ≥ 2 个 GDD 则包含）
  - `[_] 运行 /design-system [next-system] —— 设计顺序中的下一个`（始终包含，注明具体系统名）
  - `[_] 到此为止`

将最能推进流程的选项标注为 `（推荐）`。
