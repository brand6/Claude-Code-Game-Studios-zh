# Skill 测试规范：/dev-story

## Skill 摘要

`/dev-story [story-file]` 读取 Story 文件，加载全部上下文（TR-ID、ADR、控制清单、引擎设置），并将实现工作委派给合适的专家程序员代理。Skill 本身不直接编写源代码——而是编排专家代理来实现。

在 `full` 审核模式下，LP-CODE-REVIEW 门控（Lead Programmer）在实现完成后运行。在 `lean` 或 `solo` 模式下，LP-CODE-REVIEW 被跳过并注明。实现完成且门控通过（或被跳过）后，Skill 请求"May I write"以更新 Story 状态为 Complete。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需 Fixture。

- [ ] 包含必填 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含 ≥2 个阶段标题
- [ ] 包含 verdict 关键词：COMPLETE、BLOCKED、IN PROGRESS、NEEDS CHANGES
- [ ] 包含"May I write"协作协议语言（更新 Story 状态和写入代码文件）
- [ ] 末尾包含下一步交接（`/story-done`）
- [ ] 说明 LP-CODE-REVIEW 门控行为：full 模式运行，lean/solo 跳过
- [ ] 说明委派给专家代理，而非直接编写代码

---

## Director 门控检查

`full` 模式下：LP-CODE-REVIEW（Lead Programmer）门控在实现完成后运行。若门控返回 NEEDS CHANGES，Story 状态保持 In Progress，不标记为 Complete。

`lean` 模式下：LP-CODE-REVIEW 被跳过。输出注明："LP-CODE-REVIEW skipped — lean mode"。

`solo` 模式下：LP-CODE-REVIEW 被跳过，注明方式相同。

---

## 测试用例

### 用例 1：正常路径——Full 模式实现并通过 LP-CODE-REVIEW

**Fixture：**
- Story 文件存在，Status: Ready，含 3 个验收标准
- 管理 ADR 为 Accepted 状态
- `docs/architecture/control-manifest.md` 存在
- `production/session-state/review-mode.txt` 内容为 `full`

**输入：** `/dev-story production/epics/[layer]/story-[name].md`

**预期行为：**
1. Skill 读取 Story 文件，加载 TR-ID、ADR 和控制清单
2. 将实现委派给合适的专家程序员代理
3. 专家代理实现功能，输出代码文件路径
4. LP-CODE-REVIEW 门控生成并审核实现
5. LP-CODE-REVIEW 返回 APPROVED
6. Skill 询问"May I write"以更新 Story 状态和写入代码文件
7. 批准后 Story 状态更新为 Complete

**断言：**
- [ ] Skill 不直接编写源代码——委派给专家代理
- [ ] LP-CODE-REVIEW 门控在任何写入 Story 状态前运行
- [ ] LP-CODE-REVIEW APPROVED 后才标记 Story 为 Complete
- [ ] 写入代码文件和更新 Story 状态前询问"May I write"
- [ ] 写入后 Verdict 为 COMPLETE

---

### 用例 2：失败路径——管理 ADR 为 Proposed 状态

**Fixture：**
- Story 文件存在，Status: Ready
- 管理 ADR 状态为 Proposed（尚未 Accepted）

**输入：** `/dev-story production/epics/[layer]/story-[name].md`

**预期行为：**
1. Skill 读取 Story 文件并检查管理 ADR 状态
2. 检测到 ADR 为 Proposed 状态
3. Skill 输出："Implementation blocked: [ADR name] is still Proposed. Finalize the ADR before implementing this story."
4. Skill 退出，不开始实现
5. Verdict 为 BLOCKED

**断言：**
- [ ] 检测到 Proposed ADR 时 Skill 以明确消息退出
- [ ] 不开始实现（不委派给专家代理）
- [ ] Skill 推荐 `/architecture-decision` 作为下一步
- [ ] Verdict 为 BLOCKED

---

### 用例 3：澄清需求——验收标准不明确

**Fixture：**
- Story 文件存在，但其中一个验收标准措辞模糊（例如"系统应该感觉响应灵敏"）
- 管理 ADR 为 Accepted

**输入：** `/dev-story production/epics/[layer]/story-[name].md`

**预期行为：**
1. Skill 读取 Story 文件并识别模糊的验收标准
2. 在开始实现前向用户提出澄清问题
3. 不自动解读模糊标准
4. 用户提供澄清后开始实现
5. 澄清后的标准用于测试（不使用原始模糊版本）

**断言：**
- [ ] Skill 在开始实现前提出模糊标准的澄清问题
- [ ] Skill 请求用户澄清（而非自动解读）
- [ ] 仅在用户提供澄清后开始实现
- [ ] 澄清后的标准用于测试中

---

### 用例 4：边缘情况——无参数；从会话状态读取

**Fixture：**
- 未提供参数
- `production/session-state/active.md` 引用一个活跃 Story 文件
- 该 Story 文件存在，Status: In Progress

**输入：** `/dev-story`（无参数）

**预期行为：**
1. Skill 检测到未提供参数
2. Skill 读取 `production/session-state/active.md`
3. Skill 找到活跃 Story 引用
4. Skill 向用户确认："Continuing work on [story title] — is that correct?"
5. 确认后 Skill 继续处理该 Story

**断言：**
- [ ] 未提供参数时 Skill 读取会话状态
- [ ] Skill 在继续前向用户确认活跃 Story
- [ ] Skill 不在无确认的情况下静默假设活跃 Story
- [ ] 若会话状态无活跃 Story，Skill 询问应实现哪个 Story

---

### 用例 5：Director 门控——LP-CODE-REVIEW 返回 NEEDS CHANGES；lean 模式跳过门控

**Fixture（full 模式）：**
- Story 已实现，全部标准表面上已满足
- `production/session-state/review-mode.txt` 内容为 `full`
- LP-CODE-REVIEW 门控返回带 2 个具体问题的 NEEDS CHANGES

**Full 模式预期行为：**
1. 实现后生成 LP-CODE-REVIEW 门控
2. 门控返回带 2 个具体问题的 NEEDS CHANGES
3. Story 状态保持 In Progress——不标记为 Complete
4. 向用户展示门控反馈并询问如何处理

**断言（full 模式）：**
- [ ] LP-CODE-REVIEW 返回 NEEDS CHANGES 时 Story 不标记为 Complete
- [ ] 门控反馈原文展示给用户
- [ ] 问题解决且门控通过前 Story 状态保持 In Progress

**Fixture（lean 模式）：**
- 相同 Story，`production/session-state/review-mode.txt` 内容为 `lean`

**Lean 模式预期行为：**
1. 实现完成
2. LP-CODE-REVIEW 门控被跳过——在输出中注明
3. 请求用户确认全部标准已满足
4. 用户确认后 Story 标记为 Complete

**断言（lean 模式）：**
- [ ] 输出中出现"LP-CODE-REVIEW skipped — lean mode"
- [ ] 用户确认标准后（无需门控）Story 标记为 Complete
- [ ] Skill 不在被跳过的门控上阻塞

---

## 协议合规

- [ ] 不直接编写源代码——委派给专家代理
- [ ] 开始实现前读取全部上下文（Story、TR-ID、ADR、清单、引擎设置）
- [ ] 更新 Story 状态和写入代码文件前询问"May I write"
- [ ] 跳过的门控在输出中按名称和模式注明
- [ ] Story 完成后更新 `production/session-state/active.md`
- [ ] 末尾包含下一步交接：`/story-done`

---

## 覆盖范围说明

- 引擎路由逻辑（Godot vs Unity vs Unreal）不按引擎测试——路由模式是一致的；引擎选择是配置事实。
- Visual/Feel 和 UI Story 类型（无需自动测试）有不同的证据要求，这些用例中未涵盖。
- Integration Story 类型遵循与 Logic 相同的模式，但证据路径不同——不单独进行 Fixture 测试。
