# Skill 测试规范：/story-readiness

## Skill 摘要

`/story-readiness [story-file]` 验证 Story 文件是否满足实现所需的全部条件。Skill 从 4 个维度评估 Story 的就绪状态：设计（TR-ID 存在于注册表中）、架构（管理 ADR 为 Accepted 状态）、范围（验收标准具体可测试）、完成标准（DoD 章节存在）。

该 Skill 为只读操作，不写入任何文件。在 `full` 审核模式下，QL-STORY-READY（QA Lead）门控在 4 维检查完成后运行。Verdict 为：READY、NEEDS WORK、BLOCKED。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需 Fixture。

- [ ] 包含必填 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含 ≥2 个阶段标题
- [ ] 包含 verdict 关键词：READY、NEEDS WORK、BLOCKED
- [ ] 不包含"May I write"语言（只读 Skill）
- [ ] 末尾包含推荐的下一步（修复问题或继续实现）
- [ ] 说明 QL-STORY-READY 门控行为（full 模式运行，lean/solo 跳过）
- [ ] 说明 3 个 verdict 级别之间的区别（READY vs NEEDS WORK vs BLOCKED）

---

## Director 门控检查

`full` 模式下：QL-STORY-READY（QA Lead）门控在 4 维检查完成后运行。若门控返回 INADEQUATE，最终 verdict 为 BLOCKED，即使 4 维检查全部通过。

`lean` 模式下：QL-STORY-READY 被跳过。输出注明："[QL-STORY-READY] skipped — Lean/Solo mode"。

`solo` 模式下：QL-STORY-READY 被跳过，注明方式相同。

---

## 测试用例

### 用例 1：正常路径——完全就绪的 Story，4 个维度全部通过

**Fixture：**
- Story 文件存在，包含完整的 frontmatter
- TR-ID 存在于 TR 注册表中
- 管理 ADR 为 Accepted 状态
- 验收标准具体、可测试（3 个标准）
- DoD 章节存在
- `production/session-state/review-mode.txt` 内容为 `lean`

**输入：** `/story-readiness production/epics/[layer]/story-[name].md`

**预期行为：**
1. Skill 读取 Story 文件并加载相关上下文
2. 从 4 个维度检查 Story
3. 全部 4 个维度通过
4. Verdict 为 READY

**断言：**
- [ ] 输出中全部 4 个维度均标记为通过
- [ ] Verdict 为 READY
- [ ] 不写入任何文件
- [ ] 末尾包含继续进入实现的建议

---

### 用例 2：阻塞路径——管理 ADR 为 Proposed 状态

**Fixture：**
- Story 文件存在
- 管理 ADR 状态为 Proposed（尚未 Accepted）
- 其他条件均满足

**输入：** `/story-readiness production/epics/[layer]/story-[name].md`

**预期行为：**
1. Skill 读取 Story 文件并检查 ADR 状态
2. 检测到 ADR 为 Proposed 状态
3. Skill 输出："Blocked: [ADR name] is Proposed — must be Accepted before implementation."
4. Verdict 为 BLOCKED

**断言：**
- [ ] Verdict 为 BLOCKED（不是 NEEDS WORK 或 READY）
- [ ] 输出中命名相关 ADR
- [ ] Skill 推荐 `/architecture-decision` 作为解除阻塞的步骤
- [ ] Skill 区分 BLOCKED（需要外部操作）和 NEEDS WORK（可在当前修复）

---

### 用例 3：需要工作——缺少验收标准章节

**Fixture：**
- Story 文件存在
- TR-ID 和 ADR 均满足
- Story 文件中缺少验收标准章节

**输入：** `/story-readiness production/epics/[layer]/story-[name].md`

**预期行为：**
1. Skill 读取 Story 文件并核查所有 4 个维度
2. 范围维度：缺少验收标准
3. Skill 输出 NEEDS WORK verdict，指出缺少该章节

**断言：**
- [ ] 缺少验收标准章节时 Verdict 为 NEEDS WORK（不是 BLOCKED 或 READY）
- [ ] 输出中具体标注缺少验收标准章节
- [ ] 输出建议添加可测试/可衡量的标准
- [ ] Skill 区分 NEEDS WORK（可修复，无外部依赖）和 BLOCKED（需要外部操作）

---

### 用例 4：边缘情况——清单版本过期

**Fixture：**
- Story 文件头部有 `Manifest Version: 2026-01-15`
- `docs/architecture/control-manifest.md` 有 `Manifest Version: 2026-03-10`
- 版本不匹配（Story 在清单更新前创建）

**输入：** `/story-readiness production/epics/[layer]/story-[name].md`

**预期行为：**
1. Skill 读取 Story 并提取清单版本 `2026-01-15`
2. Skill 读取控制清单头部并提取当前版本 `2026-03-10`
3. Skill 检测到版本不匹配
4. Skill 将此标记为建议性问题（不阻塞，但值得关注）
5. Verdict 为 NEEDS WORK，注明清单版本过期

**断言：**
- [ ] Skill 读取 `docs/architecture/control-manifest.md` 获取当前版本
- [ ] Skill 将 Story 中嵌入的清单版本与当前清单版本进行比较
- [ ] 清单版本过期时 Verdict 为 NEEDS WORK（不是 BLOCKED，也不是 READY）
- [ ] 输出说明 Story 中嵌入的指南可能已过时

---

### 用例 5：Director 门控——QL-STORY-READY 在各审核模式下的行为

**Fixture：**
- Story 文件存在且就绪（4 个维度全部通过，ADR Accepted，标准存在）
- `production/session-state/review-mode.txt` 存在

**用例 5a——full 模式：**
- `review-mode.txt` 内容为 `full`

**输入：** `/story-readiness production/epics/[layer]/story-[name].md`（full 模式）

**Full 模式预期行为：**
1. Skill 读取审核模式——确定为 `full`
2. 4 维检查完成后 Skill 调用 QL-STORY-READY 门控
3. QA Lead 审核 Story 的就绪状态
4. 若 QA Lead verdict 为 INADEQUATE → Story verdict 为 BLOCKED，即使 4 维检查通过
5. 若 QA Lead verdict 为 ADEQUATE → verdict 正常进行

**断言（5a）：**
- [ ] Skill 在决定是否调用 QL-STORY-READY 前读取审核模式
- [ ] full 模式下 4 维检查完成后调用 QL-STORY-READY 门控
- [ ] QA Lead INADEQUATE verdict 覆盖 READY 的 4 维检查结果 → 最终 verdict 为 BLOCKED
- [ ] 输出中注明门控调用："Gate: QL-STORY-READY — [result]"

**用例 5b——lean 或 solo 模式：**
- `review-mode.txt` 内容为 `lean` 或 `solo`

**预期行为：**
1. Skill 读取审核模式——确定为 `lean` 或 `solo`
2. QL-STORY-READY 门控被跳过
3. 输出注明跳过："[QL-STORY-READY] skipped — Lean/Solo mode"
4. Verdict 仅基于 4 维检查

**断言（5b）：**
- [ ] lean 或 solo 模式下 QL-STORY-READY 门控不生成
- [ ] 输出中明确注明跳过
- [ ] Verdict 仅基于 4 维检查

---

## 协议合规

- [ ] 不使用 Write 或 Edit 工具（只读 Skill）
- [ ] 发布 verdict 前展示完整检查结果
- [ ] 不请求批准（无文件写入需要批准）
- [ ] 末尾包含推荐的下一步（修复问题或继续实现）
- [ ] 清晰区分 3 个 verdict 级别（READY vs NEEDS WORK vs BLOCKED）
