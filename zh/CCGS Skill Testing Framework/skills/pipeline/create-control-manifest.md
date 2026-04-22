# Skill 测试规范：/create-control-manifest

## Skill 摘要

`/create-control-manifest` 读取 `docs/architecture/` 中所有已接受（Accepted）的 ADR，并生成控制清单——一份汇总所有架构约束、必须遵循的模式和禁止模式的参考文档。该清单供 Story 编写者参考，确保 Story 继承正确的架构规则，而无需逐一阅读所有 ADR。

该 Skill 仅包含 Accepted 状态的 ADR；Proposed 状态的 ADR 被排除并注明。无 Director 门控。Skill 在写入 `docs/architecture/control-manifest.md` 前询问"May I write"。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需 Fixture。

- [ ] 包含必填 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含 ≥2 个阶段标题
- [ ] 包含 verdict 关键词：CREATED、BLOCKED
- [ ] 包含"May I write"协作协议语言（针对 control-manifest.md）
- [ ] 末尾包含下一步交接（`/create-epics` 或 `/create-stories`）
- [ ] 说明只包含 Accepted ADR（不包含 Proposed）

---

## Director 门控检查

无 Director 门控——该 Skill 不生成任何 Director 门控代理。控制清单是从 Accepted ADR 的机械提取；不需要创意或技术审核门控。

---

## 测试用例

### 用例 1：正常路径——4 个 Accepted ADR 生成正确清单

**Fixture：**
- `docs/architecture/` 包含 4 个 ADR 文件，全部 `Status: Accepted`
- 每个 ADR 有"Required Patterns"和/或"Forbidden Patterns"章节
- 不存在 `docs/architecture/control-manifest.md`

**输入：** `/create-control-manifest`

**预期行为：**
1. Skill 读取 `docs/architecture/` 中的所有 ADR 文件
2. 从每个 ADR 中提取 Required Patterns、Forbidden Patterns 和关键约束
3. 起草具有正确章节结构的清单
4. 向用户展示清单草稿
5. 询问"May I write `docs/architecture/control-manifest.md`?"
6. 批准后写入清单

**断言：**
- [ ] 所有 4 个 Accepted ADR 均在清单中体现
- [ ] 清单包含 Required Patterns 和 Forbidden Patterns 的独立章节
- [ ] 清单中每条约束都包含来源 ADR 编号
- [ ] 写入前询问"May I write"
- [ ] 未经批准 Skill 不写入
- [ ] 写入后 Verdict 为 CREATED

---

### 用例 2：失败路径——未找到 ADR

**Fixture：**
- `docs/architecture/` 目录存在但不含任何 ADR 文件

**输入：** `/create-control-manifest`

**预期行为：**
1. Skill 读取 `docs/architecture/`，未找到 ADR 文件
2. Skill 输出："No ADRs found. Run `/architecture-decision` to create ADRs before generating the control manifest."
3. Skill 退出，不创建任何文件
4. Verdict 为 BLOCKED

**断言：**
- [ ] 未找到 ADR 时 Skill 输出明确错误
- [ ] 不写入控制清单文件
- [ ] Skill 推荐 `/architecture-decision` 作为下一步操作
- [ ] Verdict 为 BLOCKED（不是错误崩溃）

---

### 用例 3：ADR 状态混合——仅包含 Accepted ADR

**Fixture：**
- `docs/architecture/` 包含 3 个 Accepted ADR 和 2 个 Proposed ADR

**输入：** `/create-control-manifest`

**预期行为：**
1. Skill 读取所有 ADR 文件并按 `Status: Accepted` 过滤
2. 清单仅从 3 个 Accepted ADR 起草
3. 输出注明："2 Proposed ADRs were excluded: [adr-NNN-name, adr-NNN-name]"
4. 用户在批准写入前看到被排除的 ADR
5. 询问"May I write `docs/architecture/control-manifest.md`?"

**断言：**
- [ ] 清单内容中仅出现 3 个 Accepted ADR
- [ ] 被排除的 Proposed ADR 按名称列出
- [ ] 用户在批准写入前看到排除列表
- [ ] Skill 不静默省略 Proposed ADR 而不加说明

---

### 用例 4：边缘情况——清单已存在

**Fixture：**
- `docs/architecture/control-manifest.md` 已存在（v1 版本，上周日期）
- `docs/architecture/` 中有 Accepted ADR（部分是上次清单生成后新增的）

**输入：** `/create-control-manifest`

**预期行为：**
1. Skill 检测到已有清单并读取其版本号 / 日期
2. Skill 提供重新生成选项："control-manifest.md already exists (v1, [date]). Regenerate with current ADRs?"
3. 用户确认后：Skill 起草更新的清单，递增版本号
4. 询问"May I write `docs/architecture/control-manifest.md`?"（覆盖）
5. 批准后写入更新的清单

**断言：**
- [ ] Skill 在提供重新生成选项前读取并报告现有清单的版本
- [ ] 向用户提供重新生成/跳过选择——不自动覆盖
- [ ] 更新后的清单版本号递增
- [ ] 覆盖已有文件前询问"May I write"

---

### 用例 5：Director 门控——不生成门控；不读取 review-mode.txt

**Fixture：**
- 4 个 Accepted ADR 存在
- `production/session-state/review-mode.txt` 存在，内容为 `full`

**输入：** `/create-control-manifest`

**预期行为：**
1. Skill 读取 ADR 并起草清单
2. Skill 不读取 `production/session-state/review-mode.txt`
3. 全程不生成任何 Director 门控代理
4. Skill 起草后直接进行"May I write"
5. 审核模式设置对该 Skill 行为无影响

**断言：**
- [ ] 不生成 Director 门控代理（无 CD-、TD-、PR-、AD- 前缀的门控）
- [ ] Skill 不读取 `production/session-state/review-mode.txt`
- [ ] 输出不包含任何"Gate: [GATE-ID]"或门控跳过条目
- [ ] 清单仅从 ADR 生成，不经外部门控审核

---

## 协议合规

- [ ] 起草清单前读取所有 ADR 文件
- [ ] 仅包含 Accepted ADR——Proposed ADR 注明为已排除
- [ ] 清单草稿在"May I write"询问前展示给用户
- [ ] 写入前询问"May I write `docs/architecture/control-manifest.md`?"
- [ ] 无 Director 门控——不读取 review-mode.txt
- [ ] 末尾包含下一步交接：`/create-epics` 或 `/create-stories`

---

## 覆盖范围说明

- 生成的清单的精确章节结构（约束表、模式列表）由 Skill 主体定义，不在测试断言中重新列举。
- `version` 字段递增逻辑（v1 → v2）通过用例 4 测试，但确切的版本编号格式未做 Fixture 锁定。
- ADR 解析（提取 Required/Forbidden Patterns）依赖一致的 ADR 结构——通过用例 1 的 Fixture 隐式测试。
