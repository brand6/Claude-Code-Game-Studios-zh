---
name: consistency-check
description: "扫描所有 GDD 文件与实体注册表，检测跨文档不一致：同一实体属性值不同、同一道具数值不同、同一公式变量不同。Grep 优先策略——先读取注册表，再仅针对有冲突的 GDD 段落进行检查，不做全文读取。"
argument-hint: "[full | since-last-review | entity:<name> | item:<name>]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

# 一致性检查

通过将所有 GDD 与实体注册表（`design/registry/entities.yaml`）对比，检测跨文档不一致问题。采用 Grep 优先策略：一次性读取注册表，然后仅针对提及注册名称的 GDD 段落进行检查——除非需要深入调查冲突，否则不做全文读取。

**本技能是写入阶段的安全网。** 它能捕获 `/design-system` 逐节检查可能遗漏的内容，以及 `/review-all-gdds` 整体评审过晚才能发现的问题。

**运行时机：**
- 每写完一个新 GDD 后（在继续下一个系统之前）
- 在运行 `/review-all-gdds` 之前（确保该技能从干净的基准线开始）
- 在运行 `/create-architecture` 之前（不一致问题会污染下游 ADR）
- 按需运行：`/consistency-check entity:[名称]` 专项检查某个实体

**输出：** 冲突报告 + 可选的注册表修正

---

## 阶段 1：解析参数并加载注册表

**模式：**
- 无参数 / `full` — 检查所有已注册条目与所有 GDD
- `since-last-review` — 仅检查上次评审报告以来修改过的 GDD
- `entity:<name>` — 在所有 GDD 中检查特定实体
- `item:<name>` — 在所有 GDD 中检查特定道具

**加载注册表：**

```
Read path="design/registry/entities.yaml"
```

如果文件不存在或没有任何条目：
> "实体注册表为空。请先运行 `/design-system` 编写 GDD——每个 GDD 完成后注册表会自动填充。目前没有内容可检查。"

停止并退出。

从注册表中建立四张查找表：
- **entity_map**：`{ name → { source, attributes, referenced_by } }`
- **item_map**：`{ name → { source, value_gold, weight, ... } }`
- **formula_map**：`{ name → { source, variables, output_range } }`
- **constant_map**：`{ name → { source, value, unit } }`

统计已注册条目总数。输出报告：
```
注册表已加载：[N] 个实体，[N] 个道具，[N] 个公式，[N] 个常量
检查范围：[full | since-last-review | entity:名称]
```

---

## 阶段 2：确定待检查的 GDD 范围

```
Glob pattern="design/gdd/*.md"
```

排除：`game-concept.md`、`systems-index.md`、`game-pillars.md`——这些不是系统 GDD。

`since-last-review` 模式：
```bash
git log --name-only --pretty=format: -- design/gdd/ | grep "\.md$" | sort -u
```
限定为最近一次 `design/gdd/gdd-cross-review-*.md` 文件创建日期之后修改过的 GDD。

扫描前先列出待检查的 GDD 清单。

---

## 阶段 3：Grep 优先冲突扫描

对每个已注册条目，在所有待检查 GDD 中 grep 其名称。
**不做全文读取**——只提取匹配行及其前后上下文（`-C 3` 行）。

这是核心优化：与其逐一全文读取 10 份 GDD × 400 行（共 4000 行），
不如对 50 个实体名 × 10 份 GDD 执行 50 次定向搜索，每次命中约返回 10 行。

### 3a：实体扫描

对 entity_map 中的每个实体：

```
Grep pattern="[entity_name]" glob="design/gdd/*.md" output_mode="content" -C 3
```

对每条 GDD 命中结果，提取实体名称附近提及的值：
- 任何数字属性（数量、费用、持续时间、范围、速率）
- 任何分类属性（类型、层级、类别）
- 任何派生值（总量、输出值、结果）
- 注册在 entity_map 中的其他任何属性

将提取值与注册表条目进行对比。

**冲突检测：**
- 注册表记录 `[entity_name].[attribute] = [value_A]`，GDD 写的是 `[entity_name] 有 [value_B]`。→ **冲突**
- 注册表记录 `[item_name].[attribute] = [value_A]`，GDD 写的是 `[item_name] 是 [value_B]`。→ **冲突**
- GDD 提及 `[entity_name]` 但未指定该属性。→ **注意**（无冲突，仅无法验证）

### 3b：道具扫描

对 item_map 中的每个道具，在所有 GDD 中 grep 道具名称。提取：
- 出售价格 / 价值 / 金币值
- 重量
- 堆叠规则（可堆叠 / 不可堆叠）
- 类别

与注册表条目值进行对比。

### 3c：公式扫描

对 formula_map 中的每个公式，在所有 GDD 中 grep 公式名称。提取：
- 公式附近提及的变量名
- 提及的输出范围或上限值

与注册表条目对比：
- 变量名不同 → **冲突**
- 输出范围表述不同 → **冲突**

### 3d：常量扫描

对 constant_map 中的每个常量，在所有 GDD 中 grep 常量名称。提取：
- 常量名附近提及的任何数值

与注册表值对比：
- 数值不同 → **冲突**

---

## 阶段 4：深度调查（仅限冲突项）

对阶段 3 发现的每个冲突，对冲突 GDD 做定向全节读取，以获取精确上下文：

```
Read path="design/gdd/[conflicting_gdd].md"
```
（如果文件较大，可用更宽上下文的 Grep）

结合完整上下文确认冲突。判断：
1. **哪份 GDD 是正确的？** 查看注册表中的 `source:` 字段——source GDD 是权威来源，与其矛盾的其他 GDD 需要更新。
2. **注册表本身是否过时？** 如果 source GDD 在注册表条目写入后有所更新（查看 git log），注册表可能已过期。
3. **这是否是有意为之的设计变更？** 如果冲突代表一个蓄意的设计决策，解决方案是：更新 source GDD、更新注册表，再修正所有其他 GDD。

对每个冲突进行分类：
- **🔴 CONFLICT** — 同名实体/道具/公式/常量在不同 GDD 中有不同值。必须在架构开始前解决。
- **⚠️ STALE REGISTRY** — source GDD 值已更改但注册表未更新。注册表需要更新；其他 GDD 可能已是正确的。
- **ℹ️ UNVERIFIABLE** — 实体被提及但没有可比对的属性。不是冲突，仅做记录。

---

## 阶段 5：输出报告

```
## 一致性检查报告
日期：[日期]
已检查的注册表条目：[N 个实体，N 个道具，N 个公式，N 个常量]
已扫描的 GDD：[N] 个（[列出名称]）

---

### 发现的冲突（架构开始前必须解决）

🔴 [实体/道具/公式/常量名称]
   注册表（来源：[gdd]）：[属性] = [值]
   [other_gdd].md 中有冲突：[属性] = [不同的值]
   → 需要解决：[应修改哪份文档及修改内容]

---

### 过期的注册表条目（注册表落后于 GDD）

⚠️ [条目名称]
   注册表记录：[值]（写入于 [日期]）
   Source GDD 当前值：[新值]
   → 更新注册表条目以匹配 source GDD，然后检查 referenced_by 文档。

---

### 无法验证的引用（无冲突，仅供参考）

ℹ️ [gdd].md 提及了 [entity_name]，但未说明可比对的属性。
   未检测到冲突。无需采取行动。

---

### 无问题条目（未发现问题）

✅ [N] 个注册表条目已在所有 GDD 中验证，未发现冲突。

---

结论：PASS | CONFLICTS FOUND
```

**结论：**
- **PASS** — 无冲突。注册表与 GDD 在所有已检查值上保持一致。
- **CONFLICTS FOUND** — 发现一个或多个冲突。列出解决步骤。

---

## 阶段 6：注册表修正

如果发现过期的注册表条目，询问：
> "是否允许我更新 `design/registry/entities.yaml` 以修复 [N] 个过期条目？"

对每个过期条目：
- 更新 `value` / 属性字段
- 将 `revised:` 设置为今日日期
- 在 YAML 注释中记录旧值：`# was: [old_value] before [date]`

如果在 GDD 中发现未收录于注册表的新条目，询问：
> "在 GDD 中发现了 [N] 个实体/道具，尚未收录到注册表中。是否允许我将它们添加到 `design/registry/entities.yaml`？"

只添加出现在两份或以上 GDD 中的条目（真正的跨系统事实）。

**绝不删除注册表条目。** 如果某条目已从所有 GDD 中移除，将其 `status` 设置为 `deprecated`。

写入完成后：结论：**COMPLETE** — 一致性检查完毕。
如果冲突仍未解决：结论：**BLOCKED** — [N] 个冲突需要手动解决，方可开始架构设计。

### 6b：追加到 Reflexion 日志

如果发现任何 🔴 CONFLICT 条目（无论是否已解决），将条目追加到 `docs/consistency-failures.md`：

```markdown
### [YYYY-MM-DD] — /consistency-check — 🔴 CONFLICT
**Domain**：[涉及的系统领域]
**Documents involved**：[source GDD] 与 [conflicting GDD]
**What happened**：[具体冲突——实体名称、属性、不同值]
**Resolution**：[修复方式，或"未解决——需要手动处理"]
**Pattern**：[归纳出的规律，例如"战斗 GDD 中定义的道具值在编写经济 GDD 时未被参照——始终先检查 entities.yaml"]
```

仅当 `docs/consistency-failures.md` 存在时才追加。如果该文件不存在，静默跳过本步骤——不得从本技能创建该文件。

---

## 下一步

- **若 PASS**：运行 `/review-all-gdds` 进行整体设计理论评审；如果所有 MVP GDD 均已完成，可运行 `/create-architecture`。
- **若 CONFLICTS FOUND**：修复标记的 GDD，然后重新运行 `/consistency-check` 确认解决情况。
- **若 STALE REGISTRY**：更新注册表（阶段 6），然后重新运行以验证。
- 每写完一个新 GDD 后运行 `/consistency-check`，尽早发现问题，不要等到架构阶段。
