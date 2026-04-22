# 技能测试规范：/adopt

## 技能概要

`/adopt` 审查现有项目的制品——GDD、ADR、故事、基础设施文件以及
`technical-preferences.md`——检验其是否符合模板技能流水线的格式规范。
它按严重程度（BLOCKING / HIGH / MEDIUM / LOW）对每个差距进行分类，
生成编号且排序的迁移计划，并在通过 `AskUserQuestion` 获得用户明确批准后，
将计划写入 `docs/adoption-plan-[日期].md`。

此技能有别于 `/project-stage-detect`（后者检查制品是否存在）。
`/adopt` 检查的是现有制品能否实际配合模板技能运作。

不适用 director 门控。本技能不调用任何 director agent。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含严重程度层级关键词：BLOCKING、HIGH、MEDIUM、LOW
- [ ] 在写入采用计划前包含"May I write"或 `AskUserQuestion` 语言
- [ ] 末尾包含下一步交接（例如，提供立即修复最高优先级差距的选项）

---

## Director 门控检查

无。`/adopt` 是一个棕地审查工具。不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——所有 GDD 合规，无差距，COMPLIANT

**夹具：**
- `design/gdd/` 包含 3 个 GDD 文件；每个文件均包含全部 8 个必要章节且有内容
- `docs/architecture/adr-0001.md` 存在，包含 `## Status`、`## Engine Compatibility`
  及所有其他必要章节
- `production/stage.txt` 存在
- `docs/architecture/tr-registry.yaml` 和 `docs/architecture/control-manifest.md` 存在
- `technical-preferences.md` 中已配置引擎

**输入：** `/adopt`

**预期行为：**
1. 技能输出"Scanning project artifacts..."后静默读取所有制品
2. 报告检测到的阶段、GDD 数量、ADR 数量、故事数量
3. 阶段 2 审查：全部 3 个 GDD 包含所有 8 个章节，Status 字段存在且有效
4. ADR 审查：所有必要章节存在
5. 基础设施审查：所有关键文件存在
6. 阶段 3：零个 BLOCKING、零个 HIGH、零个 MEDIUM、零个 LOW 差距
7. 摘要报告："No blocking gaps — this project is template-compatible"
8. 使用 `AskUserQuestion` 询问是否写入计划；用户选择写入
9. 采用计划写入 `docs/adoption-plan-[日期].md`
10. 阶段 7 提供下一步操作：无阻塞差距，提供后续选项

**断言：**
- [ ] 技能在输出任何内容之前先静默读取
- [ ] "Scanning project artifacts..."出现在静默读取阶段之前
- [ ] 差距计数显示 0 BLOCKING、0 HIGH、0 MEDIUM（或仅有 LOW）
- [ ] 在写入采用计划前使用 `AskUserQuestion`
- [ ] 采用计划文件写入 `docs/adoption-plan-[日期].md`
- [ ] 阶段 7 提供具体的下一步操作（不只是列出选项）

---

### 用例 2：不合规文件——GDD 缺少章节，NEEDS MIGRATION

**夹具：**
- `design/gdd/` 包含 2 个 GDD 文件：
  - `combat.md`——缺少 `## Acceptance Criteria` 和 `## Formulas` 章节
  - `movement.md`——包含全部 8 个章节
- 一个 ADR（`adr-0001.md`）缺少 `## Status` 章节
- `docs/architecture/tr-registry.yaml` 不存在

**输入：** `/adopt`

**预期行为：**
1. 技能扫描所有制品
2. 阶段 2 审查发现：
   - `combat.md`：2 个缺失章节（Acceptance Criteria、Formulas）
   - `adr-0001.md`：缺少 `## Status`——BLOCKING 影响
   - `tr-registry.yaml`：缺失——HIGH 影响
3. 阶段 3 分类：
   - BLOCKING：`adr-0001.md` 缺少 `## Status`（story-readiness 会静默通过）
   - HIGH：`tr-registry.yaml` 缺失；`combat.md` 缺少 Acceptance Criteria（无法生成故事）
   - MEDIUM：`combat.md` 缺少 Formulas
4. 阶段 4 生成排序迁移计划：
   - 步骤 1（BLOCKING）：为 `adr-0001.md` 添加 `## Status`——命令：`/architecture-decision retrofit`
   - 步骤 2（HIGH）：运行 `/architecture-review` 以引导生成 tr-registry.yaml
   - 步骤 3（HIGH）：为 `combat.md` 添加 Acceptance Criteria——命令：`/design-system retrofit`
   - 步骤 4（MEDIUM）：为 `combat.md` 添加 Formulas
5. 差距预览将 BLOCKING 项显示为项目符号列表（含实际文件名），HIGH/MEDIUM 显示为计数
6. `AskUserQuestion` 询问是否写入计划；批准后写入
7. 阶段 7 提供立即修复最高优先级差距（ADR Status）的选项

**断言：**
- [ ] 差距预览中 BLOCKING 差距以文件名项目符号列出
- [ ] HIGH 和 MEDIUM 在差距预览中显示为计数
- [ ] 迁移计划项按 BLOCKING 优先排序
- [ ] 每个计划项包含修复命令或手动步骤
- [ ] 在写入前使用 `AskUserQuestion`
- [ ] 阶段 7 提供立即修复第一个 BLOCKING 项的选项

---

### 用例 3：混合状态——部分文档合规，部分不合规，生成部分报告

**夹具：**
- 4 个 GDD 文件：2 个完全合规，2 个存在差距（一个缺少 Tuning Knobs，一个缺少 Edge Cases）
- ADR：3 个文件——2 个合规，1 个缺少 `## ADR Dependencies`
- 故事：5 个文件——3 个含 TR-ID 引用，2 个没有
- 基础设施：所有关键文件存在；`technical-preferences.md` 完整配置

**输入：** `/adopt`

**预期行为：**
1. 技能审查所有制品类型
2. 审查摘要显示总计："4 GDDs (2 fully compliant, 2 with gaps); 3 ADRs
   (2 fully compliant, 1 with gaps); 5 stories (3 with TR-IDs, 2 without)"
3. 差距分类：
   - 无 BLOCKING 差距
   - HIGH：1 个 ADR 缺少 `## ADR Dependencies`
   - MEDIUM：2 个 GDD 有缺失章节；2 个故事缺少 TR-ID
   - LOW：无
4. 迁移计划先列 HIGH 差距，再按顺序列 MEDIUM 差距
5. 包含注释："Existing stories continue to work — do not regenerate stories
   that are in progress or done"
6. `AskUserQuestion` 询问是否写入计划；批准后写入

**断言：**
- [ ] 显示每类制品的合规统计（N 个合规，M 个有差距）
- [ ] 计划中包含现有故事兼容性注释
- [ ] 无 BLOCKING 差距时，迁移计划中无 BLOCKING 章节
- [ ] HIGH 差距在计划排序中先于 MEDIUM 差距
- [ ] 在写入前使用 `AskUserQuestion`

---

### 用例 4：无制品——全新项目，提示运行 /start

**夹具：**
- 仓库中 `design/gdd/`、`docs/architecture/`、`production/epics/` 均无文件
- `production/stage.txt` 不存在
- `src/` 目录不存在或文件不足 10 个
- 无 game-concept.md，无 systems-index.md

**输入：** `/adopt`

**预期行为：**
1. 阶段 1 存在性检查发现无制品
2. 技能推断为"全新"项目——无棕地工作需迁移
3. 使用 `AskUserQuestion`：
   - "This looks like a fresh project — no existing artifacts found. `/adopt` is for
     projects with work to migrate. What would you like to do?"
   - 选项："Run `/start`"、"My artifacts are in a non-standard location"、"Cancel"
4. 技能停止——无论用户如何选择都不继续审查

**断言：**
- [ ] 在未发现制品时使用 `AskUserQuestion`（而非纯文本消息）
- [ ] `/start` 作为命名选项呈现
- [ ] 技能在提问后停止——不运行审查阶段
- [ ] 未写入任何采用计划文件

---

### 用例 5：Director 门控检查——无门控；adopt 是工具审查技能

**夹具：**
- 具有合规和不合规混合 GDD 的项目

**输入：** `/adopt`

**预期行为：**
1. 技能完成完整审查并生成迁移计划
2. 未调用任何 director agent
3. 输出中无门控 ID
4. 技能运行期间不调用 `/gate-check`

**断言：**
- [ ] 未调用 director 门控
- [ ] 输出中无门控跳过消息
- [ ] 技能在不经过任何门控检查的情况下完成

---

## 协议合规

- [ ] 在提交任何输出前静默读取所有制品
- [ ] 按 BLOCKING → HIGH → MEDIUM → LOW 对差距进行分类
- [ ] 差距预览：BLOCKING 项以文件名项目符号列出；HIGH/MEDIUM 显示为计数
- [ ] 迁移计划按 BLOCKING 优先排序
- [ ] 在写入计划前使用 `AskUserQuestion`（不是纯文本"May I write"）
- [ ] 阶段 7 提供立即修复最高优先级差距的选项

---

## 覆盖说明

- 所有 GDD 均合规但 ADR 缺失的情况（反之亦然）遵循用例 2 的相同分类模式，
  不单独进行夹具测试。
- "May I write" vs `AskUserQuestion` 的选择是有意的：`/adopt` 使用
  `AskUserQuestion` 而非普通的"May I write"，以便提供写入/跳过/取消等多个选项。
- 故事重新生成风险（用例 3 中的注释）是防止用户意外覆盖进行中故事的保护措施。
