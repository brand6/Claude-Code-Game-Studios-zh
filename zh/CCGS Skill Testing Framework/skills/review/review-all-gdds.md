# Skill 测试规范：/review-all-gdds

## Skill 摘要

`/review-all-gdds` 对 `design/gdd/` 中所有系统 GDD 进行整体性跨文档评审。Skill 分两个并行阶段运行：第一阶段（一致性检查）和第二阶段（设计理论检查）。该 Skill 为 Opus 级别操作，需要对整个 GDD 集合的深度理解。

Skill 为只读操作——不写入任何文件，仅生成报告。无 Director 门控。Verdict 为：CONSISTENT、MINOR ISSUES、MAJOR ISSUES。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需 Fixture。

- [ ] 包含必填 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含 ≥2 个阶段标题
- [ ] 包含 verdict 关键词：CONSISTENT、MINOR ISSUES、MAJOR ISSUES
- [ ] 不包含"May I write"语言（只读 Skill）
- [ ] 末尾包含适合对应 verdict 的下一步交接
- [ ] 说明两个阶段并行运行（不是依次运行）
- [ ] 说明无 Director 门控（不读取 review-mode.txt）

---

## Director 门控检查

无 Director 门控——该 Skill 无论审核模式如何均不生成任何 Director 门控代理。该 Skill 本身就是 Opus 级别的跨文档评审。

---

## 测试用例

### 用例 1：正常路径——GDD 集合整洁，两个阶段均通过

**Fixture：**
- `design/gdd/` 包含 ≥3 个已批准系统 GDD
- GDD 之间无规则冲突
- 所有跨文档依赖均有效

**输入：** `/review-all-gdds`

**预期行为：**
1. Skill 读取 `design/gdd/` 中所有 GDD
2. 第一阶段（一致性检查）和第二阶段（设计理论检查）并行生成
3. 两个阶段均返回通过结果
4. Skill 输出完整性说明和通过理由
5. Verdict 为 CONSISTENT

**断言：**
- [ ] 两个阶段并行运行（不是依次运行）
- [ ] Verdict 为 CONSISTENT
- [ ] 不写入任何文件
- [ ] 末尾包含适合对应 verdict 的下一步交接（`/architecture-review` 或 `/create-architecture`）

---

### 用例 2：冲突规则——两个 GDD 有相互矛盾的定义

**Fixture：**
- `design/gdd/combat.md` 定义了一条游戏规则
- `design/gdd/physics.md` 定义了与上述规则相矛盾的规则

**输入：** `/review-all-gdds`

**预期行为：**
1. 第一阶段（一致性检查）检测到规则冲突
2. 报告命名两个冲突的 GDD 文件
3. 报告引用每个文档中相互矛盾的具体规则文本
4. Verdict 为 MAJOR ISSUES

**断言：**
- [ ] Verdict 为 MAJOR ISSUES
- [ ] 两个冲突的 GDD 文件名均在报告中命名
- [ ] 引用了相互矛盾的具体规则
- [ ] 输出提供明确的修复建议

---

### 用例 3：孤立依赖引用

**Fixture：**
- `design/gdd/inventory.md` 引用一个名为 "crafting-system" 的系统
- `design/gdd/crafting.md` 不存在（尚未设计该系统）

**输入：** `/review-all-gdds`

**预期行为：**
1. 第一阶段检测到孤立依赖
2. 报告注明 `inventory.md` 引用了不存在的 `crafting-system`
3. 建议运行 `/design-system crafting`
4. Verdict 为 MINOR ISSUES（依赖缺失，但不是直接规则冲突）

**断言：**
- [ ] Verdict 为 MINOR ISSUES（不是 MAJOR ISSUES 或 CONSISTENT）
- [ ] 报告中命名孤立的依赖引用
- [ ] Skill 建议 `/design-system` 作为下一步
- [ ] 输出区分孤立依赖（MINOR）和规则冲突（MAJOR）

---

### 用例 4：失败路径——未找到 GDD 文件

**Fixture：**
- `design/gdd/` 目录为空或不存在

**输入：** `/review-all-gdds`

**预期行为：**
1. Skill 尝试读取 `design/gdd/` 中的文件
2. 未找到文件——Skill 输出错误并给出指导
3. Skill 建议运行 `/brainstorm` 和 `/design-system` 后再重新运行
4. Skill 不生成 verdict（CONSISTENT / MINOR ISSUES / MAJOR ISSUES）

**断言：**
- [ ] 未找到 GDD 时 Skill 输出明确错误消息
- [ ] 目录为空时不生成 verdict
- [ ] Skill 推荐正确的下一步操作（`/brainstorm` 或 `/design-system`）
- [ ] Skill 不崩溃或生成部分报告

---

### 用例 5：Director 门控——无论审核模式如何均不生成门控

**Fixture：**
- `design/gdd/` 包含 ≥2 个一致的系统 GDD
- `production/session-state/review-mode.txt` 存在，内容为 `full`

**输入：** `/review-all-gdds`

**预期行为：**
1. Skill 读取所有 GDD 并运行两个评审阶段
2. Skill 不读取 `review-mode.txt`
3. Skill 不生成任何 Director 门控代理（无 CD-、TD-、PR-、AD- 前缀）
4. Skill 正常完成并输出 verdict
5. 审核模式设置对该 Skill 行为无影响

**断言：**
- [ ] 全程不生成 Director 门控代理
- [ ] Skill 不读取 `production/session-state/review-mode.txt`
- [ ] 输出不包含任何"Gate: [GATE-ID]"或门控跳过条目
- [ ] 无论审核模式如何 Skill 均生成 verdict
- [ ] R4 指标：该 Skill 在所有模式下门控数量 = 0

---

## 协议合规

- [ ] 第一阶段（一致性）和第二阶段（设计理论）并行生成——不是依次生成
- [ ] 不在无"May I write"批准的情况下写入任何文件
- [ ] 任何写入询问前展示结论表
- [ ] Verdict 严格为以下之一：CONSISTENT、MINOR ISSUES、MAJOR ISSUES
- [ ] 末尾包含适合对应 verdict 的交接：MAJOR ISSUES → 修复后重新运行；MINOR ISSUES → 可继续并知晓问题；CONSISTENT → `/create-architecture`

---

## 覆盖率说明

- 经济平衡分析（来源/汇出循环）需要跨 GDD 的资源数据——通过用例 2 结构性覆盖（冲突检测模式相同）。
- 设计理论阶段（第二阶段）的检查项（包括主导策略检测和认知过载）未独立设计 Fixture 测试——遵循与一致性检查相同的模式，通过支柱漂移用例结构验证。
- `since-last-review` 范围模式未在此测试——这是运行时问题。
