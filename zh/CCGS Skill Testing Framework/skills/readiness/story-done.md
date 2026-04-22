# Skill 测试规范：/story-done

## Skill 摘要

`/story-done [story-file]` 在 Story 实现后执行完成验证。Skill 读取 Story 文件，逐条核对每个验收标准是否已在实现中得到满足，提示代码审查，并在批准后将 Story 状态更新为 Complete。

在 `full` 审核模式下，LP-CODE-REVIEW 门控（Lead Programmer）在实现核查后运行。在 `lean` 或 `solo` 模式下，LP-CODE-REVIEW 被跳过并注明。在更新 Story 状态或添加技术债务条目前询问"May I write"。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需 Fixture。

- [ ] 包含必填 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含 ≥2 个阶段标题
- [ ] 包含 verdict 关键词：COMPLETE、COMPLETE WITH NOTES、BLOCKED
- [ ] 包含"May I write"协作协议语言（更新 Story 状态前）
- [ ] 末尾包含显示 sprint 中下一个就绪 Story 的交接
- [ ] 说明 LP-CODE-REVIEW 门控行为（full 模式运行，lean/solo 跳过）

---

## Director 门控检查

`full` 模式下：LP-CODE-REVIEW（Lead Programmer）门控在实现验证完成后运行。若门控返回 NEEDS CHANGES，Story 状态不更新为 Complete。

`lean` 模式下：LP-CODE-REVIEW 被跳过。输出注明："[LP-CODE-REVIEW] skipped — Lean/Solo mode"。

`solo` 模式下：LP-CODE-REVIEW 被跳过，注明方式相同。

---

## 测试用例

### 用例 1：正常路径——所有验收标准满足

**Fixture：**
- Story 文件存在，Status: In Progress，含 3 个验收标准
- 实现文件存在，可核实每个标准
- `production/session-state/review-mode.txt` 内容为 `lean`

**输入：** `/story-done production/epics/[layer]/story-[name].md`

**预期行为：**
1. Skill 读取 Story 文件和实现
2. 逐条核对 3 个验收标准
3. 全部 3 个标准均已满足
4. 提示代码审查
5. 询问"May I write"以更新 Story 状态
6. 批准后 Story 状态更新为 Complete

**断言：**
- [ ] 输出中每个验收标准均显示为已验证
- [ ] 更新 Story 状态前询问"May I write"
- [ ] Verdict 为 COMPLETE
- [ ] 末尾显示 sprint 中下一个就绪 Story

---

### 用例 2：部分满足——某标准无法直接核实

**Fixture：**
- Story 文件存在，含 3 个验收标准
- 标准 1 和 2 已满足
- 标准 3 需要游玩测试（无法通过自动检查核实）

**输入：** `/story-done production/epics/[layer]/story-[name].md`

**预期行为：**
1. Skill 核实标准 1 和 2——两者均通过
2. 标准 3 无法自动核实——标记为需延期验证
3. Skill 输出"Criterion 3 deferred: requires playtesting. Will be noted in completion log."
4. 询问"May I write"以更新 Story 状态
5. 批准后 Story 更新为 Complete，附完成注记（包含延期标准）
6. Verdict 为 COMPLETE WITH NOTES

**断言：**
- [ ] Verdict 为 COMPLETE WITH NOTES（不是 COMPLETE 或 BLOCKED）
- [ ] 延期标准在完成注记中明确记录
- [ ] 更新状态前询问"May I write"
- [ ] 末尾显示 sprint 中下一个就绪 Story

---

### 用例 3：GDD 偏差检测——实现与 GDD 要求不一致

**Fixture：**
- Story 文件引用一个最大值为 3 的 GDD 要求
- 实现使用了不同的值（5）
- 这是一个有意为之的偏差

**输入：** `/story-done production/epics/[layer]/story-[name].md`

**预期行为：**
1. Skill 读取 GDD 要求文本（最大值为 3）
2. Skill 检测到要求值与实现值（5）的差异
3. Skill 标记此为 GDD 偏差并请用户分类：
   - INTENTIONAL：记录偏差及原因
   - ERROR：在 Story 标记为 Complete 前必须修复实现
   - OUT OF SCOPE：要求已更改，GDD 需要更新
4. INTENTIONAL 情形：在完成注记中记录偏差，Verdict 为 COMPLETE WITH NOTES
5. ERROR 情形：Verdict 为 BLOCKED，直到实现修正

**断言：**
- [ ] Skill 检测到 GDD 要求与实现值的不匹配
- [ ] Skill 请用户分类偏差（不自动假定任何一种情况）
- [ ] INTENTIONAL 偏差 → COMPLETE WITH NOTES（不是 BLOCKED）
- [ ] ERROR 偏差 → BLOCKED verdict，直到修复
- [ ] 检测到的偏差记录在完成注记或技术债务登记中

---

### 用例 4：边缘情况——无参数，自动检测当前 Story

**Fixture：**
- `production/session-state/active.md` 包含对某个活跃 Story 文件的引用
- 该 Story 文件存在，Status: In Progress

**输入：** `/story-done`（无参数）

**预期行为：**
1. Skill 读取 `production/session-state/active.md`
2. Skill 找到活跃 Story 引用
3. Skill 读取该 Story 文件并正常继续
4. 输出确认自动检测到的 Story

**断言：**
- [ ] 未提供参数时 Skill 读取 `production/session-state/active.md`
- [ ] Skill 在继续前识别并确认自动检测到的 Story
- [ ] 若会话状态中未找到 Story，Skill 请求用户提供路径

---

### 用例 5：Director 门控——LP-CODE-REVIEW 在各审核模式下的行为

**Fixture：**
- Story 文件存在，所有验收标准均已核实，无 GDD 偏差
- `production/session-state/review-mode.txt` 存在

**用例 5a——full 模式：**
- `review-mode.txt` 内容为 `full`

**输入：** `/story-done production/epics/[layer]/story-[name].md`（full 模式）

**Full 模式预期行为：**
1. Skill 读取审核模式——确定为 `full`
2. 实现核实后 Skill 调用 LP-CODE-REVIEW 门控
3. Lead Programmer 审核实现
4. 若 LP verdict 为 NEEDS CHANGES → Story 不能标记为 Complete
5. 若 LP verdict 为 APPROVED → Skill 继续标记 Story 为 Complete

**断言（5a）：**
- [ ] Skill 在决定是否调用 LP-CODE-REVIEW 前读取审核模式
- [ ] full 模式下实现核查后调用 LP-CODE-REVIEW 门控
- [ ] LP NEEDS CHANGES verdict 阻止 Story 标记为 Complete
- [ ] 输出中注明门控结果："Gate: LP-CODE-REVIEW — [result]"
- [ ] 即使 LP 批准，更新 Story 状态前仍询问"May I write"

**用例 5b——lean 或 solo 模式：**
- `review-mode.txt` 内容为 `lean` 或 `solo`

**预期行为：**
1. Skill 读取审核模式——确定为 `lean` 或 `solo`
2. LP-CODE-REVIEW 门控被跳过
3. 输出注明跳过："[LP-CODE-REVIEW] skipped — Lean/Solo mode"
4. Story 完成流程仅基于验收标准核查进行

**断言（5b）：**
- [ ] lean 或 solo 模式下 LP-CODE-REVIEW 门控不生成
- [ ] 输出中明确注明跳过
- [ ] 标记 Story 为 Complete 前仍需要"May I write"批准

---

## 协议合规

- [ ] 更新 Story 文件前使用"May I write"
- [ ] 向 `docs/tech-debt-register.md` 添加条目前使用"May I write"
- [ ] 请求批准前展示完整结论（标准核查、偏差检查）
- [ ] 末尾显示 sprint 计划中下一个就绪 Story
- [ ] 若有任何标准处于 ERROR 状态，不将 Story 标记为 Complete
- [ ] 不跳过代码审查提示
