---
name: skill-improve
description: "使用测试-修复-复测循环改进技能。运行静态检查，提出针对性修复方案，重写技能，复测后根据分数变化决定保留或回滚。"
argument-hint: "[skill-name]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Bash
---

# 技能改进

对单个技能运行改进循环：
测试 → 修复 → 复测 → 保留或回滚。

---

## 阶段 1：解析参数

从第一个参数读取技能名称。若未提供，输出用法说明并停止：

```
用法：/skill-improve [skill-name]
示例：/skill-improve tech-debt
```

验证 `.claude/skills/[name]/SKILL.md` 是否存在。若不存在，停止并输出：
"技能 '[name]' 未找到。"

---

## 阶段 2：基准测试

运行 `/skill-test static [name]` 并记录基准分数：
- FAIL 数量
- WARN 数量
- 具体哪些检查失败（检查 1-7）

向用户展示：
```
静态基准：   [N] 个失败，[M] 个警告
失败项：检查 4（无写入前询问），检查 5（无交接说明）
```

若基准为 0 个 FAIL 且 0 个 WARN，记录此情况并继续进行阶段 2b。

### 阶段 2b：类别基准

在 `CCGS Skill Testing Framework/catalog.yaml` 中查找该技能的 `category:` 字段。

若未找到 `category:` 字段，显示：
"类别：尚未分配——跳过类别检查。"
并跳至阶段 3。

若找到类别，运行 `/skill-test category [name]` 并记录类别基准：
- FAIL 数量
- WARN 数量
- 具体哪些类别规范指标失败

向用户展示：
```
类别基准：   [N] 个失败，[M] 个警告（[category] 规范）
```

若**静态和类别基准均为** 0 个 FAIL 且 0 个 WARN，停止：
"此技能已通过所有静态和类别检查，无需改进。"

---

## 阶段 3：诊断

读取 `.claude/skills/[name]/SKILL.md` 的完整内容。

对每个失败或警告的**静态**检查，定位具体缺陷：

- **检查 1 失败** → 缺少哪个 frontmatter 字段
- **检查 2 失败** → 发现的阶段数与最低要求的对比
- **检查 3 失败** → 技能正文中没有任何裁定关键词
- **检查 4 失败** → allowed-tools 中包含 Write 或 Edit，但无写入前询问的表述
- **检查 5 警告** → 结尾没有后续步骤或交接说明章节
- **检查 6 警告** → 设置了 `context: fork` 但发现的阶段少于 5 个
- **检查 7 警告** → argument-hint 为空或与文档中的模式不匹配

对每个失败或警告的**类别**检查（若在阶段 2b 中分配了类别），定位技能文本中的具体缺陷。例如：
- 若 G2 失败（门禁模式，未派遣全部总监）：技能正文从未引用所有 4 个 PHASE-GATE 总监提示
- 若 A2 失败（创作模式，无逐节写入询问）：技能只在结尾询问一次，而不是在每节写入前询问
- 若 T3 失败（团队模式，未暴露 BLOCKED 状态）：技能在智能体被阻塞时不会暂停相关工作

在提出任何修改方案之前，向用户展示完整的综合诊断结果。

---

## 阶段 4：提出修复方案

针对每个失败和警告，编写有针对性的修复方案。以清晰标注的"修改前/修改后"代码块展示建议的变更。**只修改失败的部分——不要重写通过检查的章节。**

询问："May I write this improved version to `.claude/skills/[name]/SKILL.md`？"

若用户拒绝，停止执行。

---

## 阶段 5：写入并复测

记录技能文件的当前内容（如需回滚备用）。

将改进后的技能写入 `.claude/skills/[name]/SKILL.md`。

重新运行 `/skill-test static [name]` 并记录新的静态分数。
若已分配类别，同时重新运行 `/skill-test category [name]` 并记录新的类别分数。

展示对比结果：
```
静态：   修改前 [N] 个失败，[M] 个警告  →  修改后 [N'] 个失败，[M'] 个警告
类别：   修改前 [N] 个失败，[M] 个警告  →  修改后 [N'] 个失败，[M'] 个警告（如适用）
综合变化：已改善 / 无变化 / 变差
```

---

## 阶段 6：裁定

统计综合失败总数：静态 FAIL + 类别 FAIL + 静态 WARN + 类别 WARN。

**若综合分数改善（综合失败数低于基准）：**
报告："分数已改善。保留变更。"
展示每个维度修复内容的摘要。

**若综合分数相同或变差：**
报告："综合分数未改善。"
展示变更内容及可能未能改善的原因。
询问："May I revert `.claude/skills/[name]/SKILL.md` using git checkout？"
若同意：运行 `git checkout -- .claude/skills/[name]/SKILL.md`

---

## 阶段 7：后续步骤

- 运行 `/skill-test static all` 查找下一个有失败的技能。
- 运行 `/skill-improve [next-name]` 对另一个技能继续执行循环。
- 运行 `/skill-test audit` 查看整体覆盖率进度。
