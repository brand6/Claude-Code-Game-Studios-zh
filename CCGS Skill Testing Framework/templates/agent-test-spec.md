# Agent 规格：[agent-name]

> **层级**：[directors | leads | specialists | godot | unity | unreal | operations | creative]
> **分类**：[director | lead | specialist | engine | operations | creative]
> **规格编写日期**：[YYYY-MM-DD]

## Agent 摘要

[用一段话描述该 agent 的领域、其拥有的决策权，以及它委派给下级与自行处理的内容。包括其触发的关卡（如有）。]

**领域**：[该 agent 拥有的文件/目录]
**升级至**：[上级 agent — 例如设计冲突升级至 creative-director]
**委派至**：[该 agent 通常启动的子 agents]

---

## 静态断言

- [ ] Agent 文件位于 `.claude/agents/[name].md`
- [ ] Frontmatter 包含 `name`、`description`、`model`、`tools` 字段
- [ ] 领域明确声明
- [ ] 升级路径已记录
- [ ] 不做领域外决策

---

## 测试用例

### 用例 1：领域内请求 — [简短名称]

**场景**：明确属于该 agent 领域范围的请求。

**测试夹具**：
- [相关项目状态]
- [提供给 agent 的输入]

**预期行为**：
1. Agent 接受请求
2. Agent 产出[特定输出类型]
3. Agent 在写入文件前征询意见（如适用）

**断言**：
- [ ] Agent 在其领域内处理请求，不升级
- [ ] 输出格式符合预期结构
- [ ] 遵循协作协议（询问 → 草稿 → 批准）

**用例裁决**：PASS / FAIL / PARTIAL

---

### 用例 2：领域外重定向 — [简短名称]

**场景**：超出该 agent 领域范围的请求。

**测试夹具**：
- [属于其他 agent 的请求]

**预期行为**：
1. Agent 识别请求超出其领域
2. Agent 重定向至正确的 agent
3. Agent 不尝试处理该请求

**断言**：
- [ ] Agent 拒绝并重定向（不静默处理跨领域工作）
- [ ] 重定向中指出了正确的 agent 名称

**用例裁决**：PASS / FAIL / PARTIAL

---

### 用例 3：关卡裁决 — [简短名称]

**场景**：Agent 作为 director 关卡检查的一部分被调用。

**测试夹具**：
- [提交审查的项目状态]
- [关卡 ID：例如 CD-PHASE-GATE]

**预期行为**：
1. Agent 读取相关文档
2. Agent 产出 PASS / CONCERNS / FAIL 裁决
3. Agent 在 CONCERNS 或 FAIL 时不自动推进

**断言**：
- [ ] 输出中包含裁决关键字（PASS、CONCERNS、FAIL）
- [ ] 提供裁决理由
- [ ] CONCERNS/FAIL 时：工作被阻塞，不静默继续

**用例裁决**：PASS / FAIL / PARTIAL

---

### 用例 4：冲突升级 — [简短名称]

**场景**：该 agent 的领域与另一 agent 的决策发生冲突。

**测试夹具**：
- [同级两个 agent 的冲突决策]

**预期行为**：
1. Agent 识别冲突
2. Agent 升级至共同上级（或 creative-director / technical-director）
3. Agent 不单方面解决跨领域冲突

**断言**：
- [ ] 明确浮现冲突
- [ ] 遵循正确的升级路径
- [ ] 未单方面做出跨领域变更

**用例裁决**：PASS / FAIL / PARTIAL

---

### 用例 5：上下文传递 — [简短名称]

**场景**：Agent 从上级 agent 接收包含完整上下文的任务。

**测试夹具**：
- [从上级传递的上下文块]
- [要执行的具体子任务]

**预期行为**：
1. Agent 读取并使用所提供的上下文
2. Agent 完成子任务
3. Agent 将结果返回给上级（不不必要地向用户提问）

**断言**：
- [ ] Agent 使用所提供的上下文，而非重新询问
- [ ] 结果范围限于子任务，不超出
- [ ] 输出格式适合上级 agent 消费

**用例裁决**：PASS / FAIL / PARTIAL

---

## 协议合规性

- [ ] 严守声明领域 — 不单方面做出跨领域变更
- [ ] 冲突升级至正确上级
- [ ] 文件写入前使用 `"May I write"`（或为只读则跳过）
- [ ] 在请求批准前呈现发现
- [ ] 不跳过委派层级

---

## 覆盖说明

[任何覆盖缺口、已知的未测试边界情况，或需要实际调用 agent 才能验证的行为。]
