# Skill 测试规范：/architecture-review

## Skill 摘要

`/architecture-review [architecture-file]` 对架构文档进行 Opus 级别的完整审核。Skill 验证架构文档涵盖所有必需章节，检查与 ADR 的一致性，并交叉核对引擎版本兼容性。该 Skill 为只读操作——不写入任何文件。

在 `full` 审核模式下，TD-ARCHITECTURE（Technical Director）和 LP-FEASIBILITY（Lead Programmer）两个门控并行运行。在 `lean` 或 `solo` 模式下，两个门控均被跳过并注明。Verdict 为：APPROVED、NEEDS REVISION、MAJOR REVISION NEEDED。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需 Fixture。

- [ ] 包含必填 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含 ≥2 个阶段标题
- [ ] 包含 verdict 关键词：APPROVED、NEEDS REVISION、MAJOR REVISION NEEDED
- [ ] 不包含"May I write"语言（只读 Skill）
- [ ] 末尾包含适合对应 verdict 的下一步交接
- [ ] 说明 TD-ARCHITECTURE 和 LP-FEASIBILITY 门控行为（full 模式并行）

---

## Director 门控检查

`full` 模式下：TD-ARCHITECTURE（Technical Director）和 LP-FEASIBILITY（Lead Programmer）并行生成，对架构文档进行审核。

`lean` 模式下：两个门控均被跳过。

`solo` 模式下：两个门控均被跳过，以"solo mode"标签注明。

---

## 测试用例

### 用例 1：正常路径——完整架构文档，full 模式通过两个门控

**Fixture：**
- `docs/architecture/architecture.md` 存在，包含全部 8 个必需章节
- 所有管理 ADR 均为 Accepted 状态
- 无章节与任何 ADR 相矛盾
- `production/session-state/review-mode.txt` 内容为 `full`

**输入：** `/architecture-review docs/architecture/architecture.md`

**预期行为：**
1. Skill 读取架构文档和所有 ADR
2. 验证 8/8 个必需章节均存在
3. TD-ARCHITECTURE 和 LP-FEASIBILITY 并行生成
4. 两个门控均返回 APPROVED
5. Skill 输出完整性检查结果
6. Verdict 为 APPROVED

**断言：**
- [ ] 输出中 8/8 章节均标记为存在
- [ ] TD-ARCHITECTURE 和 LP-FEASIBILITY 均作为已完成门控显示在输出中
- [ ] 两个门控并行生成（不是依次生成）
- [ ] Verdict 为 APPROVED
- [ ] 不写入任何文件
- [ ] 末尾包含 `/create-control-manifest` 或 `/create-epics` 的下一步交接

---

### 用例 2：失败路径——缺少必需章节

**Fixture：**
- `docs/architecture/architecture.md` 存在，但缺少 3 个必需章节

**输入：** `/architecture-review docs/architecture/architecture.md`

**预期行为：**
1. Skill 读取架构文档并检查所有必需章节
2. 检测到缺少 3 个章节
3. 按名称列出缺少的章节
4. Verdict 为 MAJOR REVISION NEEDED

**断言：**
- [ ] Verdict 为 MAJOR REVISION NEEDED（不是 NEEDS REVISION 或 APPROVED）
- [ ] 每个缺少的章节均按名称列出
- [ ] 输出提供明确的修复指导

---

### 用例 3：部分失败——架构与 ADR 相矛盾

**Fixture：**
- `docs/architecture/architecture.md` 存在，包含全部 8 个章节
- 其中一个架构决策与 Accepted ADR 规定的限制相矛盾

**输入：** `/architecture-review docs/architecture/architecture.md`

**预期行为：**
1. Skill 检测到矛盾：架构文档中的决策与 ADR 规定相冲突
2. 命名相互冲突的 ADR
3. Verdict 为 NEEDS REVISION（不是 MAJOR REVISION NEEDED，章节均已存在）

**断言：**
- [ ] Verdict 为 NEEDS REVISION（不是 APPROVED 或 MAJOR REVISION NEEDED）
- [ ] 冲突的 ADR 按名称标注在输出中
- [ ] 输出提供具体的修复建议

---

### 用例 4：边缘情况——文件未找到

**Fixture：**
- 提供的路径在项目中不存在

**输入：** `/architecture-review docs/architecture/nonexistent.md`

**预期行为：**
1. Skill 尝试读取该文件
2. 文件未找到
3. Skill 输出明确错误，指出缺少的文件名
4. Skill 建议检查 `docs/architecture/` 或运行 `/create-architecture`
5. Skill 不生成 verdict

**断言：**
- [ ] 文件未找到时 Skill 输出明确错误
- [ ] 不生成 verdict（APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED）
- [ ] Skill 建议纠正措施
- [ ] Skill 不崩溃或生成部分报告

---

### 用例 5：Director 门控——Full 模式生成两个门控；solo 模式跳过两个

**Fixture（full 模式）：**
- `docs/architecture/architecture.md` 存在，包含全部 8 个章节
- `production/session-state/review-mode.txt` 内容为 `full`

**Full 模式预期行为：**
1. TD-ARCHITECTURE 门控生成
2. LP-FEASIBILITY 门控与 TD-ARCHITECTURE 并行生成
3. 两个门控均完成后才发布 verdict

**断言（full 模式）：**
- [ ] TD-ARCHITECTURE 和 LP-FEASIBILITY 均作为已完成门控显示在输出中
- [ ] 两个门控并行生成
- [ ] Verdict 反映门控反馈

**Fixture（solo 模式）：**
- 相同架构文档
- `production/session-state/review-mode.txt` 内容为 `solo`

**Solo 模式预期行为：**
1. Skill 读取架构文档
2. 不生成任何门控
3. 输出注明："TD-ARCHITECTURE skipped — solo mode"和"LP-FEASIBILITY skipped — solo mode"
4. Verdict 仅基于结构性检查

**断言（solo 模式）：**
- [ ] TD-ARCHITECTURE 和 LP-FEASIBILITY 均不作为活跃门控出现
- [ ] 两个被跳过的门控均在输出中注明
- [ ] Verdict 仍然基于结构性检查生成

---

## 协议合规

- [ ] 不写入任何文件（只读 Skill）
- [ ] 发布 verdict 前展示章节完整性检查结果
- [ ] full 模式下 TD-ARCHITECTURE 和 LP-FEASIBILITY 并行生成
- [ ] lean/solo 输出中按名称和模式注明被跳过的门控
- [ ] Verdict 严格为以下之一：APPROVED、NEEDS REVISION、MAJOR REVISION NEEDED
- [ ] 末尾包含适合对应 verdict 的下一步交接

---

## 覆盖率说明

- 8 个必需架构章节是项目特定的——测试使用 Skill 主体中定义的章节列表，不在此重新列举。
- 引擎版本兼容性检查（交叉引用 `docs/engine-reference/`）是用例 1 正常路径的一部分，未独立设计 Fixture 测试。
- RTM（需求可追溯性矩阵）模式是由 `/architecture-review` Skill 自身的 `rtm` 参数模式处理的独立问题，未在此测试。
