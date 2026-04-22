---
name: skill-test
description: "验证技能文件的结构合规性与行为正确性。三种模式：static（静态检查），spec（行为验证），audit（覆盖率报告）。"
argument-hint: "static [skill-name | all] | spec [skill-name] | category [skill-name | all] | audit"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write
---

# 技能测试

验证 `.claude/skills/*/SKILL.md` 文件的结构合规性和行为正确性。无外部依赖——完全在现有技能/钩子/模板架构内运行。

**四种模式：**

| 模式 | 命令 | 用途 | Token 消耗 |
|------|------|----|-----------|
| `static` | `/skill-test static [name\|all]` | 结构检查——每个技能 7 项合规性检查 | 低（约 1k/技能）|
| `spec` | `/skill-test spec [name]` | 行为验证——评估测试规格中的断言 | 中（约 5k/技能）|
| `category` | `/skill-test category [name\|all]` | 类别规范——根据类别专属指标检查技能 | 低（约 2k/技能）|
| `audit` | `/skill-test audit` | 覆盖率报告——技能、智能体规格、最后测试日期 | 低（约 3k 总计）|

---

## 阶段 1：解析参数

根据第一个参数确定运行模式：

- `static [name]` → 对单个技能运行 7 项结构检查
- `static all` → 对所有技能运行 7 项结构检查（Glob `.claude/skills/*/SKILL.md`）
- `spec [name]` → 读取技能 + 测试规格，评估断言
- `category [name]` → 从 `CCGS Skill Testing Framework/quality-rubric.md` 运行类别专属规范
- `category all` → 对目录中所有有 `category:` 字段的技能运行类别规范
- `audit`（或无参数）→ 读取目录，列出所有技能和智能体，展示覆盖率

若参数缺失或无法识别，输出用法说明并停止。

---

## 阶段 2A：静态模式——结构检查

对每个被测试的技能，完整读取其 `SKILL.md` 并运行全部 7 项检查：

### 检查 1 — 必要的 Frontmatter 字段
文件必须在 YAML frontmatter 块中包含以下所有字段：
- `name:`
- `description:`
- `argument-hint:`
- `user-invocable:`
- `allowed-tools:`

若有任何字段缺失，则 **FAIL**。

### 检查 2 — 多阶段结构
技能必须有 ≥2 个编号阶段标题。查找以下模式：
- `## Phase N` 或 `## Phase N:`
- `## N.`（编号的顶层章节）
- 若未明确编号阶段，至少有 2 个不同的 `##` 标题

若找到的类阶段标题少于 2 个，则 **FAIL**。

### 检查 3 — 裁定关键词
技能必须包含以下至少一个关键词：`PASS`、`FAIL`、`CONCERNS`、`APPROVED`、`BLOCKED`、`COMPLETE`、`READY`、`COMPLIANT`、`NON-COMPLIANT`

若一个都没有，则 **FAIL**。

### 检查 4 — 协作规程表述
技能必须包含写入前询问的表述。查找：
- `"May I write"`（标准形式）
- `"before writing"` 或 `"approval"` 出现在文件写入指令附近
- `"ask"` 和 `"write"` 在临近位置（同一章节内）

若缺失，则 **WARN**（部分只读技能可合理跳过此项）。
若 `allowed-tools` 包含 `Write` 或 `Edit` 但未找到写入前询问表述，则 **FAIL**。

### 检查 5 — 下一步交接说明
技能必须以推荐的后续行动或跟进路径结尾。查找：
- 末尾章节提到其他技能（如 `/story-done`、`/gate-check`）
- "Recommended next" 或 "next step" 等表述
- "Follow-Up" 或 "After this" 等章节

若缺失，则 **WARN**。

### 检查 6 — Fork 上下文复杂度
若 frontmatter 包含 `context: fork`，技能应有 ≥5 个阶段标题（`##` 级别或编号的 Phase N 标题）。Fork 上下文用于复杂的多阶段技能；简单技能不应使用它。

若设置了 `context: fork` 但找到的阶段少于 5 个，则 **WARN**。

### 检查 7 — 参数提示合理性
`argument-hint` 必须非空。若技能正文提及多种模式（如"模式 A | 模式 B"），提示应反映这些模式。将提示与第一个阶段的"解析参数"章节进行交叉验证。

若提示为 `""` 或文档中的模式与提示不匹配，则 **WARN**。

---

### 静态模式输出格式

单个技能的输出：
```
=== 技能静态检查：/[name] ===

检查 1 — Frontmatter 字段：    PASS
检查 2 — 多阶段结构：           PASS（发现 7 个阶段）
检查 3 — 裁定关键词：           PASS（PASS, FAIL, CONCERNS）
检查 4 — 协作规程：             PASS（找到 "May I write"）
检查 5 — 下一步交接：           WARN（未找到后续步骤章节）
检查 6 — Fork 上下文复杂度：    PASS（8 个阶段，已设置 context: fork）
检查 7 — 参数提示：             PASS

裁定：WARNINGS（1 个警告，0 个失败）
建议：在技能末尾添加"后续行动"章节。
```

`static all` 的输出：先展示汇总表，再列出不合规的技能：
```
=== 技能静态检查：全部 52 个技能 ===

技能                   | 结果         | 问题
-----------------------|--------------|-------
gate-check             | COMPLIANT    |
design-review          | COMPLIANT    |
story-readiness        | WARNINGS     | 检查 5：无交接说明
...

摘要：48 个 COMPLIANT，3 个 WARNINGS，1 个 NON-COMPLIANT
综合裁定：N 个 WARNINGS / N 个 FAILURES
```

---

## 阶段 2B：Spec 模式——行为验证

### 步骤 1 — 定位文件

在 `.claude/skills/[name]/SKILL.md` 找到技能。
从 `CCGS Skill Testing Framework/catalog.yaml` 查找规格文件路径——使用匹配技能条目的 `spec:` 字段。

若缺失：
- 技能不存在："在 `.claude/skills/` 中未找到技能 '[name]'。"
- 目录中无规格文件路径："catalog.yaml 中未为 '[name]' 设置规格路径。"
- 规格文件在路径不存在："规格文件在 [path] 缺失。运行 `/skill-test audit` 查看覆盖率缺口。"

### 步骤 2 — 完整读取两个文件

完整读取技能文件和测试规格文件。

### 步骤 3 — 评估断言

对规格中的每个**测试用例**：

1. 读取**场景设置**描述（项目文件的假定状态）
2. 读取**预期行为**步骤
3. 读取每个**断言**复选框

对每个断言，评估：在给定场景状态下，若正确遵循技能的书面指令，是否能满足该断言。这是 Claude 评估的推理检查，而非代码执行。

标记每个断言：
- **PASS** — 技能指令能清晰满足此断言
- **PARTIAL** — 技能指令部分满足，但存在歧义
- **FAIL** — 在给定场景状态下，技能指令**无法**满足此断言

对**协作规程**断言（始终存在）：
- 检查技能在写入文件前是否要求"May I write"
- 检查技能是否在请求批准前展示发现结果
- 检查技能是否以推荐的下一步结尾
- 检查技能是否避免在未经批准的情况下自动创建文件

### 步骤 4 — 生成报告

```
=== 技能 Spec 测试：/[name] ===
日期：[日期]
规格：CCGS Skill Testing Framework/skills/[category]/[name].md

用例 1：[正常路径——名称]
  场景：[摘要]
  断言：
    [PASS] [断言文字]
    [FAIL] [断言文字]
       原因：技能阶段 3 中说"……"，但场景状态意味着"……"
  用例裁定：FAIL

用例 2：[边缘情况——名称]
  ...
  用例裁定：PASS

协作规程合规性：
  [PASS] 写入文件前使用 "May I write"
  [PASS] 请求批准前展示发现结果
  [WARN] 结尾没有明确的下一步交接说明

总体裁定：FAIL（1 个用例失败，1 个警告）
```

### 步骤 5 — 提议写入结果

"May I write these results to `CCGS Skill Testing Framework/results/skill-test-spec-[name]-[date].md` and update `CCGS Skill Testing Framework/catalog.yaml`？"

若同意：
- 将结果文件写入 `CCGS Skill Testing Framework/results/`
- 更新 `CCGS Skill Testing Framework/catalog.yaml` 中该技能的条目：
  - `last_spec: [日期]`
  - `last_spec_result: PASS|PARTIAL|FAIL`

---

## 阶段 2D：类别模式——规范评估

### 步骤 1 — 定位技能和类别

在 `.claude/skills/[name]/SKILL.md` 找到技能。
在 `CCGS Skill Testing Framework/catalog.yaml` 中查找 `category:` 字段。

若技能不存在："未找到技能 '[name]'。"
若无 `category:` 字段："catalog.yaml 中未为 '[name]' 分配类别。先在技能条目中添加 `category: [name]`。"

`category all` 模式：收集所有有 `category:` 字段的技能并逐一处理。
`category: utility` 的技能仅针对 U1（静态检查通过）和 U2（如适用，门禁模式正确）进行评估——直接使用静态模式处理 U1。

### 步骤 2 — 读取规范章节

读取 `CCGS Skill Testing Framework/quality-rubric.md`。
提取与技能类别匹配的章节（如 `### gate`、`### team`）。

### 步骤 3 — 读取技能

完整读取技能的 `SKILL.md`。

### 步骤 4 — 评估规范指标

对类别规范表中的每个指标：
1. 检查技能的书面指令是否清晰满足该标准
2. 标记 PASS、FAIL 或 WARN
3. 对 FAIL/WARN，定位技能文本中的确切缺陷（引用相关章节或说明其缺失）

### 步骤 5 — 输出报告

```
=== 技能类别检查：/[name]（[category]）===

指标 G1 — 审查模式读取：    PASS
指标 G2 — 完整模式总监：    FAIL
  缺陷：阶段 3 仅派遣 CD-PHASE-GATE；缺少 TD-PHASE-GATE、PR-PHASE-GATE、AD-PHASE-GATE
指标 G3 — 精简模式：仅 PHASE-GATE：  PASS
指标 G4 — 独奏模式：无总监：         PASS
指标 G5 — 无自动推进：              PASS

裁定：FAIL（1 个失败，0 个警告）
修复方案：在阶段 3 的完整模式总监面板中添加 TD-PHASE-GATE、PR-PHASE-GATE 和 AD-PHASE-GATE。
```

### 步骤 6 — 提议更新目录

"May I update `CCGS Skill Testing Framework/catalog.yaml` to record this category check (`last_category`, `last_category_result`) for [name]？"

---

## 阶段 2C：审计模式——覆盖率报告

### 步骤 1 — 读取目录

读取 `CCGS Skill Testing Framework/catalog.yaml`。若缺失，说明目录尚不存在（首次运行状态）。

### 步骤 2 — 枚举所有技能和智能体

Glob `.claude/skills/*/SKILL.md` 获取完整技能列表。
从每个路径提取技能名称（目录名）。

同时从 `CCGS Skill Testing Framework/catalog.yaml` 的 `agents:` 章节读取完整的智能体列表。

### 步骤 3 — 生成技能覆盖率表

对每个技能：
- 检查规格文件是否存在（使用目录中的 `spec:` 路径，或 Glob `CCGS Skill Testing Framework/skills/*/[name].md`）
- 从目录中查找 `last_static`、`last_static_result`、`last_spec`、`last_spec_result`、`last_category`、`last_category_result`、`category`（若不在目录中则标记为"从未" / "—"）
- 优先级来自目录的 `priority:` 字段（critical/high/medium/low）

### 步骤 3b — 生成智能体覆盖率表

对目录 `agents:` 章节中的每个智能体：
- 检查规格文件是否存在（使用目录中的 `spec:` 路径，或 Glob `CCGS Skill Testing Framework/agents/*/[name].md`）
- 从目录中查找 `last_spec`、`last_spec_result`、`category`

### 步骤 4 — 输出报告

```
=== 技能测试覆盖率审计 ===
日期：[日期]

技能（共 72 个）
已编写规格：72 个（100%）| 从未做静态测试：72 | 从未做类别测试：72

技能                   | 类别     | 有规格 | 上次静态 | S.结果 | 上次类别 | C.结果 | 优先级
-----------------------|----------|--------|---------|--------|---------|--------|-------
gate-check             | gate     | YES    | 从未    | —      | 从未    | —      | critical
design-review          | review   | YES    | 从未    | —      | 从未    | —      | critical
...

智能体（共 49 个）
已编写智能体规格：49 个（100%）

智能体                 | 类别       | 有规格 | 上次规格 | 结果
-----------------------|------------|--------|---------|------
creative-director      | director   | YES    | 从未    | —
technical-director     | director   | YES    | 从未    | —
...

前 5 个优先级缺口（无规格、critical/high 优先级的技能）：
（若所有规格均已编写则为空）

技能覆盖率：72/72 规格（100%）
智能体覆盖率：49/49 规格（100%）
```

审计模式下不写入任何文件。

提示："是否运行 `/skill-test static all` 检查所有技能的结构合规性？运行 `/skill-test category all` 执行类别规范检查？或运行 `/skill-test spec [name]` 运行特定的行为测试？"

---

## 阶段 3：建议的后续步骤

任何模式完成后，提供上下文相关的跟进建议：

- `static [name]` 后："若存在测试规格，运行 `/skill-test spec [name]` 验证行为正确性。"
- `static all` 有失败后："优先解决 NON-COMPLIANT 的技能。单独运行 `/skill-test static [name]` 获取详细修复指导。"
- `spec [name]` PASS 后："更新 `CCGS Skill Testing Framework/catalog.yaml` 记录本次通过日期。考虑运行 `/skill-test audit` 找出下一个规格缺口。"
- `spec [name]` FAIL 后："审查失败的断言，更新技能或测试规格以解决不匹配问题。"
- `audit` 后："从 critical 优先级的缺口开始。使用 `CCGS Skill Testing Framework/templates/skill-test-spec.md` 中的规格模板创建新规格。"
