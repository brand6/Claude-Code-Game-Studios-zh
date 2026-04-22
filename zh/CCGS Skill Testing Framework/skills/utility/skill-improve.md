# 技能测试规范：/skill-improve

## 技能概要

`/skill-improve` 对技能文件运行自动化的测试-修复-复测改进循环。它调用
`/skill-test static`（可选地调用 `/skill-test category`）来建立基准分数，
诊断失败的检查项，向 SKILL.md 文件提出有针对性的修复建议，询问
"May I write the improvements to [skill path]?"，应用修复，并重新运行测试以确认改进效果。

如果提议的修复导致技能退步（回归），则修复将被撤销（经用户确认），而不是保留。
如果技能已完美（0 个失败），则技能立即退出而不进行任何修改。
无 director 门控。判定结果：IMPROVED（分数提升）、NO CHANGE（无可改进项或用户拒绝），
或 REVERTED（已应用修复但导致回归，已撤销）。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判定关键词：IMPROVED、NO CHANGE、REVERTED
- [ ] 在应用修复前包含"May I write"协作协议语言
- [ ] 包含下一步交接（例如，运行 `/skill-test spec` 验证行为合规性）

---

## Director 门控检查

无。`/skill-improve` 是元工具技能，不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——技能有 2 个静态失败，均已修复，IMPROVED

**夹具：**
- `.claude/skills/some-skill/SKILL.md` 有 2 个静态失败：
  - 检查项 4：allowed-tools 中包含 Write，但无"May I write"语言
  - 检查项 5：末尾无下一步交接

**输入：** `/skill-improve some-skill`

**预期行为：**
1. 技能运行 `/skill-test static some-skill`——基准：5/7 检查通过
2. 技能诊断 2 个失败的检查项（4 和 5）
3. 技能提出修复建议：
   - 在适当阶段添加"May I write"语言
   - 在末尾添加下一步交接章节
4. 技能询问"May I write improvements to `.claude/skills/some-skill/SKILL.md`?"
5. 应用修复；重新运行 `/skill-test static some-skill`——现在 7/7 通过
6. 判定结果为 IMPROVED（5→7）

**断言：**
- [ ] 在任何修改前建立基准分数（5/7）
- [ ] 2 个失败的检查项均已诊断并在提议的修复中处理
- [ ] 应用修复前询问"May I write"
- [ ] 复测确认改进（7/7）
- [ ] 判定结果为 IMPROVED，并显示修改前后分数

---

### 用例 2：修复导致回归——分数比较显示回归，REVERTED

**夹具：**
- `.claude/skills/some-skill/SKILL.md` 有 1 个静态失败（缺少交接）
- 提议的修复无意中删除了判定关键词章节（引入新失败）

**输入：** `/skill-improve some-skill`

**预期行为：**
1. 基准：6/7 检查通过（1 个失败：缺少交接）
2. 技能提出修复并询问"May I write improvements?"
3. 应用修复；复测运行
4. 复测结果：5/7（修复了交接但破坏了判定关键词）
5. 技能检测到回归：分数下降
6. 技能询问用户："Fix caused a regression (6→5). May I revert the changes?"
7. 用户确认；修改被撤销；判定结果为 REVERTED

**断言：**
- [ ] 在最终确定前将复测分数与基准比较
- [ ] 当分数下降时检测到回归
- [ ] 询问用户确认撤销（非自动）
- [ ] 用户确认后文件被撤销
- [ ] 判定结果为 REVERTED

---

### 用例 3：技能有分类分配——基准捕获两种分数

**夹具：**
- `.claude/skills/gate-check/SKILL.md` 是门控技能，有 1 个静态失败和 2 个分类（G 标准）失败
- `tests/skills/quality-rubric.md` 包含门控技能章节

**输入：** `/skill-improve gate-check`

**预期行为：**
1. 技能运行静态测试和分类测试以建立基准：
   - 静态：6/7 通过
   - 分类：3/5 G 标准通过
2. 综合基准：9/12
3. 技能诊断所有 3 个失败并提出修复
4. "May I write improvements to `.claude/skills/gate-check/SKILL.md`?"
5. 应用修复；两种测试类型均重新运行
6. 复测：静态 7/7，分类 5/5 = 12/12
7. 判定结果为 IMPROVED（9→12）

**断言：**
- [ ] 基准中同时捕获静态和分类分数
- [ ] 使用综合分数进行比较（不仅一种类型）
- [ ] 所有 3 个失败均在提议的修复中处理
- [ ] 复测确认两种分数类型均有改进
- [ ] 判定结果为 IMPROVED，并显示综合前后分数

---

### 用例 4：技能已完美——无需改进

**夹具：**
- `.claude/skills/brainstorm/SKILL.md` 无静态失败
- 分类分数也为 5/5（如适用）

**输入：** `/skill-improve brainstorm`

**预期行为：**
1. 技能运行 `/skill-test static brainstorm`——7/7 通过
2. 如分类适用：5/5 标准通过
3. 技能输出："No improvements needed — brainstorm is fully compliant"
4. 技能退出而不提出任何修改
5. 不询问"May I write"；不修改任何文件
6. 判定结果为 NO CHANGE

**断言：**
- [ ] 确认 0 个失败后技能立即退出
- [ ] 显示"No improvements needed"消息
- [ ] 不提出修改
- [ ] 不询问"May I write"
- [ ] 判定结果为 NO CHANGE

---

### 用例 5：Director 门控检查——无门控；skill-improve 是元工具

**夹具：**
- 至少有 1 个静态失败的技能

**输入：** `/skill-improve some-skill`

**预期行为：**
1. 技能运行测试-修复-复测循环
2. 任何时候都不会生成 director agent
3. 输出中不出现门控 ID

**断言：**
- [ ] 未调用任何 director 门控
- [ ] 不出现门控跳过消息
- [ ] 判定结果为 IMPROVED、NO CHANGE 或 REVERTED——无门控判定

---

## 协议合规性

- [ ] 在提出任何修改前始终建立基准分数
- [ ] 输出中显示修改前后的分数比较
- [ ] 应用任何修复前询问"May I write"
- [ ] 通过将复测分数与基准比较来检测回归
- [ ] 撤销前询问用户确认（非自动）
- [ ] 以 IMPROVED、NO CHANGE 或 REVERTED 判定结束

---

## 覆盖说明

- 改进循环设计为每次调用仅运行一个修复-复测周期；运行多次迭代需要重新调用
  `/skill-improve`。
- 行为合规性（规范模式测试结果）不包含在改进循环中——仅自动化静态和分类分数。
- 技能文件无法读取的情况（权限错误或文件缺失）未经测试；这将在建立基准前导致错误。
