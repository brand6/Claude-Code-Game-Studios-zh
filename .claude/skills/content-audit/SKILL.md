---
name: content-audit
description: "对照 GDD 规划的内容数量与已实现内容进行审计。识别已规划但尚未构建的内容。"
argument-hint: "[system-name | --summary | (无参数 = 全量审计)]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write
agent: producer
---

调用本技能时：

解析参数：
- 无参数 → 对所有系统执行全量审计
- `[system-name]` → 仅审计该单个系统
- `--summary` → 仅输出汇总表格，不写入文件

---

## 阶段 1 — 收集上下文

1. **读取 `design/gdd/systems-index.md`**，获取系统完整列表、各系统所属类别及 MVP/优先级层级。

2. **L0 预扫描**：在全文读取任何 GDD 之前，先对所有 GDD 文件执行 Grep，查找 `## Summary` 章节及常见内容计数关键词：
   ```
   Grep pattern="(## Summary|N enemies|N levels|N items|N abilities|enemy types|item types)" glob="design/gdd/*.md" output_mode="files_with_matches"
   ```
   单系统审计：跳过此步骤，直接全文读取。
   全量审计：仅全文读取命中内容计数关键词的 GDD。
   没有内容计数描述的 GDD（纯机制类 GDD）标注为"无可审计的内容计数"，无需全文读取。

3. **全文读取待审计的 GDD 文件**（如指定了系统名，则读取该系统对应的单个 GDD）。

4. **从每个 GDD 中提取明确的内容计数或列表。** 关注以下模式：
   - "N 个敌人" / "敌人类型：" / 已命名敌人列表
   - "N 个关卡" / "N 个区域" / "N 张地图" / "N 个阶段"
   - "N 个道具" / "N 种武器" / "N 件装备"
   - "N 个技能" / "N 个能力" / "N 个法术"
   - "N 段对话" / "N 次交谈" / "N 段过场动画"
   - "N 个任务" / "N 个使命" / "N 个目标"
   - 任何显式枚举列表（已命名内容的项目符号列表）

4. **根据提取数据建立内容清单表格**：

   | 系统 | 内容类型 | 规划数量/列表 | 来源 GDD |
   |------|---------|--------------|---------|

   注意：如果某个 GDD 对内容有定性描述但未给出数量，记录为"未指定"并标注——未指定的数量是值得关注的设计缺口。

---

## 阶段 2 — 实现扫描

对阶段 1 中发现的每种内容类型，扫描相关目录，统计已实现的数量。使用 Glob 和 Grep 定位文件。

**关卡 / 区域 / 地图：**
- Glob `assets/**/*.tscn`、`assets/**/*.unity`、`assets/**/*.umap`
- Glob `src/**/*.tscn`、`src/**/*.unity`
- 在名为 `levels/`、`areas/`、`maps/`、`worlds/`、`stages/` 的子目录中查找场景文件
- 统计看起来是关卡/场景定义（非 UI 场景）的唯一文件数

**敌人 / 角色 / NPC：**
- Glob `assets/data/**/enemies/**`、`assets/data/**/characters/**`
- Glob `src/**/enemies/**`、`src/**/characters/**`
- 查找定义实体属性的 `.json`、`.tres`、`.asset`、`.yaml` 数据文件
- 查找角色子目录中的场景/预制体文件

**道具 / 装备 / 战利品：**
- Glob `assets/data/**/items/**`、`assets/data/**/equipment/**`、`assets/data/**/loot/**`
- 查找 `.json`、`.tres`、`.asset` 数据文件

**技能 / 能力 / 法术：**
- Glob `assets/data/**/abilities/**`、`assets/data/**/skills/**`、`assets/data/**/spells/**`
- 查找 `.json`、`.tres`、`.asset` 数据文件

**对话 / 交谈 / 过场动画：**
- Glob `assets/**/*.dialogue`、`assets/**/*.csv`、`assets/**/*.ink`
- 在 `assets/data/` 中 Grep 对话数据文件

**任务 / 使命：**
- Glob `assets/data/**/quests/**`、`assets/data/**/missions/**`
- 查找 `.json`、`.yaml` 定义文件

**引擎特定说明（在报告中注明）：**
- 统计数量为近似值——本技能无法完美解析所有引擎格式，也无法区分编辑器专用文件与发布内容
- 场景文件可能同时包含玩法内容和系统/UI 场景；扫描会统计所有匹配项并附注此说明

---

## 阶段 3 — 缺口报告

生成缺口表格：

```
| 系统 | 内容类型 | 规划数量 | 已实现 | 缺口 | 状态 |
|------|---------|---------|-------|------|------|
```

**状态分类：**
- `COMPLETE` — 已实现 ≥ 规划数量（完成度 100% 及以上）
- `IN PROGRESS` — 已实现为规划数量的 50–99%
- `EARLY` — 已实现为规划数量的 1–49%
- `NOT STARTED` — 已实现为 0

**优先级标注：**
满足以下条件的系统标注为 `HIGH PRIORITY`：
- 状态为 `NOT STARTED` 或 `EARLY`，且
- 在 systems index 中被标记为 MVP 或 Vertical Slice，或
- systems index 显示该系统正在阻塞下游系统

**汇总行：**
- 规划内容总量（Specified 列所有值之和）
- 已实现内容总量（Found 列所有值之和）
- 总体缺口百分比：`(规划数量 - 已实现数量) / 规划数量 * 100`

---

## 阶段 4 — 输出

### 全量审计与单系统模式

向用户展示缺口表格和汇总。询问："是否允许我将完整报告写入 `docs/content-audit-[YYYY-MM-DD].md`？"

如果同意，写入文件：

```markdown
# 内容审计 — [日期]

## 汇总
- **规划总量**：[M] 个系统共 [N] 项内容
- **已实现总量**：[N]
- **缺口**：[N] 项（[X%] 尚未实现）
- **审计范围**：[全量审计 | 系统：名称]

> 注意：数量为基于文件扫描的近似值。
> 审计无法区分发布内容与编辑器/测试资产。
> 建议对任何 HIGH PRIORITY 缺口进行人工核实。

## 缺口表格

| 系统 | 内容类型 | 规划数量 | 已实现 | 缺口 | 状态 |
|------|---------|---------|-------|------|------|

## HIGH PRIORITY 缺口

[列出标注为 HIGH PRIORITY 的系统及其理由]

## 各系统详情

### [系统名称]
- **GDD**：`design/gdd/[file].md`
- **已审计的内容类型**：[列表]
- **备注**：[该系统扫描精度的任何注意事项]

## 建议

优先将实现资源集中在：
1. [缺口最大的 HIGH PRIORITY 系统]
2. [第二个系统]
3. [第三个系统]

## 未指定内容数量

以下 GDD 对内容有定性描述，但未给出具体数量。
建议添加数量以提升可审计性：
[列出 GDD 和内容类型，标注"未指定"]
```

写入报告后，询问：

> "是否要为任何内容缺口创建待办用户故事？"

如果是：对用户选择的每个系统，建议用户故事标题，并根据缺口大小引导其运行 `/create-stories [epic-slug]` 或 `/quick-design`。

### --summary 模式

直接在对话中输出缺口表格和汇总。不写入文件。
最后输出："运行不带 `--summary` 的 `/content-audit` 可写入完整报告。"

---

## 阶段 5 — 后续步骤

审计完成后，推荐最有价值的后续行动：

- 如果某系统状态为 `NOT STARTED` 且被标记为 MVP → "运行 `/design-system [名称]`，在实现开始前为 GDD 补充缺失的内容数量。"
- 如果总缺口 > 50% → "运行 `/sprint-plan`，将内容工作分配到后续迭代中。"
