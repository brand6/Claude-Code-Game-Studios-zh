# 技能测试规范：/skill-test

## 技能概要

`/skill-test` 验证技能文件的结构正确性、行为合规性和分类评分。支持三种模式：

- **static**：检查单个技能文件的结构要求
  （frontmatter 字段、阶段标题、判定关键词、"May I write"语言、下一步交接），
  无需夹具。生成逐项 PASS/FAIL 表格。
- **spec**：读取 `tests/skills/` 中的测试规范文件，并针对每个测试用例断言评估技能，
  生成逐用例判定。
- **audit**：生成 `.claude/skills/` 中所有技能和 `.claude/agents/` 中所有 agent
  的覆盖率表格，显示哪些有规范文件，哪些没有。

另有 **category** 模式，读取技能分类的质量评分标准
（例如门控技能），并根据评分标准给技能评分。各模式的判定系统不同。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判定关键词：COMPLIANT、NON-COMPLIANT、WARNINGS（静态模式）；PASS、FAIL、PARTIAL（规范模式）；COMPLETE（审计模式）
- [ ] 不包含"May I write"语言（技能在所有模式下均为只读）
- [ ] 包含下一步交接（例如 `/skill-improve` 修复发现的问题）

---

## Director 门控检查

无。`/skill-test` 是元工具技能，不适用 director 门控。

---

## 测试用例

### 用例 1：静态模式——格式良好的技能，7 项检查全部通过，COMPLIANT

**夹具：**
- `.claude/skills/brainstorm/SKILL.md` 存在且格式良好：
  - 包含所有必要 frontmatter 字段
  - 包含至少 2 个阶段标题
  - 包含判定关键词
  - 包含"May I write"语言
  - 包含下一步交接
  - 记录了 director 门控
  - 记录了门控模式行为（精简/单人模式跳过）

**输入：** `/skill-test static brainstorm`

**预期行为：**
1. 技能读取 `.claude/skills/brainstorm/SKILL.md`
2. 技能运行全部 7 项结构检查
3. 7 项全部通过
4. 技能输出 PASS/FAIL 表格，7 项均标记为 PASS
5. 判定结果为 COMPLIANT

**断言：**
- [ ] 恰好报告 7 项结构检查
- [ ] 7 项均标记为 PASS
- [ ] 判定结果为 COMPLIANT
- [ ] 不写入任何文件

---

### 用例 2：静态模式——技能在 allowed-tools 中有 Write 但缺少"May I Write"

**夹具：**
- `.claude/skills/some-skill/SKILL.md` 的 frontmatter 中 `allowed-tools` 包含 `Write`
- 技能正文中无"May I write"或"May I update"语言

**输入：** `/skill-test static some-skill`

**预期行为：**
1. 技能读取 `some-skill/SKILL.md`
2. 检查项 4（协作写入协议）失败：allowed-tools 包含 `Write` 但未发现"May I write"语言
3. 其他检查项可能通过
4. 判定结果为 NON-COMPLIANT，检查项 4 为失败断言
5. 输出列出检查项 4 为 FAIL 并附说明

**断言：**
- [ ] 检查项 4 标记为 FAIL
- [ ] 说明指出具体不匹配（Write 工具无"May I write"语言）
- [ ] 判定结果为 NON-COMPLIANT
- [ ] 其他通过的检查项也显示（不仅显示失败项）

---

### 用例 3：规范模式——gate-check 技能针对规范评估

**夹具：**
- `tests/skills/gate-check.md` 存在，包含 5 个测试用例
- `.claude/skills/gate-check/SKILL.md` 存在

**输入：** `/skill-test spec gate-check`

**预期行为：**
1. 技能读取技能文件和规范文件
2. 技能针对规范的每个测试用例断言评估技能行为
3. 每个用例：若技能行为与规范断言匹配则 PASS，否则 FAIL
4. 技能生成逐用例结果表格
5. 总体判定：PASS（全部 5 个通过）、PARTIAL（部分通过）或 FAIL（多数失败）

**断言：**
- [ ] 规范中的所有 5 个测试用例均被评估
- [ ] 每个用例有独立的 PASS/FAIL 结果
- [ ] 总体判定基于用例结果为 PASS、PARTIAL 或 FAIL
- [ ] 不写入任何文件

---

### 用例 4：审计模式——所有技能和 Agent 的覆盖率表格

**夹具：**
- `.claude/skills/` 包含 72 个以上技能目录
- `.claude/agents/` 包含 49 个以上 agent 文件
- `tests/skills/` 包含技能子集的规范文件

**输入：** `/skill-test audit`

**预期行为：**
1. 技能枚举 `.claude/skills/` 中的所有技能和 `.claude/agents/` 中的所有 agent
2. 技能检查 `tests/skills/` 是否有每项对应的规范文件
3. 技能生成覆盖率表格：
   - 列出每个技能/agent
   - "Has Spec"列：YES 或 NO
   - 摘要："X of Y skills have specs; A of B agents have specs"
4. 判定结果为 COMPLETE

**断言：**
- [ ] 枚举所有技能目录（不仅是样本）
- [ ] 每项的"Has Spec"列准确
- [ ] 摘要计数正确
- [ ] 判定结果为 COMPLETE

---

### 用例 5：分类模式——根据质量评分标准评估门控技能

**夹具：**
- `tests/skills/quality-rubric.md` 存在，其"Gate Skills"章节定义了
  标准 G1-G5（例如 G1：有模式守卫，G2：有判定表等）
- `.claude/skills/gate-check/SKILL.md` 是门控技能

**输入：** `/skill-test category gate-check`

**预期行为：**
1. 技能读取 `quality-rubric.md` 并识别门控技能章节
2. 技能根据标准 G1-G5 评估 `gate-check/SKILL.md`
3. 每项标准评分：PASS、PARTIAL 或 FAIL
4. 计算总体分类分数（例如 5 项标准中 4 项通过）
5. 判定结果为 COMPLIANT（全部通过）、WARNINGS（部分通过）或 NON-COMPLIANT（有失败）

**断言：**
- [ ] 评估 quality-rubric.md 中的所有门控标准（G1-G5）
- [ ] 每项标准有独立分数
- [ ] 总体判定反映分数分布
- [ ] 不写入任何文件

---

## 协议合规性

- [ ] 静态模式恰好检查 7 项结构断言
- [ ] 规范模式逐一评估规范文件中的每个测试用例
- [ ] 审计模式覆盖所有技能和 agent（不仅一类）
- [ ] 分类模式读取 quality-rubric.md 获取标准（非硬编码）
- [ ] 在任何模式下均不写入任何文件
- [ ] 发现问题时建议 `/skill-improve` 作为下一步

---

## 覆盖说明

- skill-test 技能具有自引用性（可测试自身）。skill-test 自身 SKILL.md 的静态模式
  用例未单独进行夹具测试，以避免测试设计中的无限递归。
- 具体的 7 项结构检查在技能正文中定义；此处仅单独测试检查项 4（May I write），
  因为其逻辑最为精细。
- 审计模式计数为近似值——随着系统增长，技能和 agent 的确切数量会变化；
  断言使用"所有"而非固定计数。
