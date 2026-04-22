# Skill 测试规范：/gate-check

## Skill 摘要

`/gate-check` 验证项目是否就绪，可以进入下一个开发阶段。Skill 检查必要制品、运行质量检查、就无法自动核实的事项询问用户，并生成 PASS/CONCERNS/FAIL verdict。在 PASS 且用户确认后，Skill 将新阶段名称写入 `production/stage.txt`。该 Skill 负责所有 6 个阶段转换的把关，是流水线中最关键的质量门控 Skill。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需 Fixture。

- [ ] 包含必填 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含 ≥2 个阶段标题（编号的 Phase N 或 ## 节）
- [ ] 包含 verdict 关键词：PASS、CONCERNS、FAIL
- [ ] 包含"May I write"协作协议语言
- [ ] 末尾包含下一步交接（后续行动章节）

---

## 测试用例

### 用例 1：正常路径——所有概念制品存在，进入系统设计阶段

**Fixture：**
- `design/gdd/game-concept.md` 存在，包含所有必需章节的内容
- `design/gdd/game-pillars.md` 存在（或支柱定义在概念文档中）
- 尚无系统索引（对该阶段而言正确）

**输入：** `/gate-check systems-design`

**预期行为：**
1. Skill 读取 `design/gdd/game-concept.md` 并核实其有内容
2. Skill 检查游戏支柱（在概念文档中或单独文件中）
3. Skill 检查质量项（核心循环已描述、目标受众已确定）
4. Skill 输出结构化检查清单，每项均标注状态
5. Skill 呈现 PASS/CONCERNS/FAIL verdict
6. 若 PASS：Skill 询问"May I update `production/stage.txt` to 'Systems Design'?"

**断言：**
- [ ] Skill 使用 Glob 或 Read 在标记已检查前核实 `design/gdd/game-concept.md` 存在
- [ ] 输出包含"必要制品"章节，每项均有检查状态
- [ ] 输出包含"质量检查"章节，每项均有检查状态
- [ ] 输出包含"Verdict"行，为 PASS / CONCERNS / FAIL 之一
- [ ] Skill 就无法核实的质量项向用户询问（例如"此文档是否经过评审？"），而非假定通过
- [ ] Skill 在更新 `production/stage.txt` 前询问"May I write"
- [ ] 未经用户明确确认 Skill 不写入 `production/stage.txt`

---

### 用例 2：失败路径——概念→系统设计所需制品缺失

**Fixture：**
- `design/gdd/game-concept.md` 不存在
- 无游戏支柱文档
- `design/gdd/` 目录为空或不存在

**输入：** `/gate-check systems-design`

**预期行为：**
1. Skill 尝试读取 `design/gdd/game-concept.md`——文件未找到
2. Skill 将必要制品标记为缺失
3. Skill 输出 FAIL verdict
4. Skill 列出阻塞项："No game concept document found"
5. Skill 建议修复措施：运行 `/brainstorm` 创建

**断言：**
- [ ] 必要制品缺失时 Verdict 为 FAIL（不是 PASS 或 CONCERNS）
- [ ] 输出中明确将 `design/gdd/game-concept.md` 标注为缺失
- [ ] 输出包含"阻塞项"章节，至少包含 1 个条目
- [ ] 输出推荐 `/brainstorm` 作为修复措施
- [ ] Verdict 为 FAIL 时 Skill 不写入 `production/stage.txt`

---

### 用例 3：无参数——自动检测当前阶段

**Fixture：**
- `production/stage.txt` 内容为 `Concept`
- `design/gdd/game-concept.md` 存在并有内容
- 尚无系统索引

**输入：** `/gate-check`（无参数）

**预期行为：**
1. Skill 读取 `production/stage.txt` 以确定当前阶段
2. Skill 确定下一个门控为"概念 → 系统设计"
3. Skill 使用系统设计门控检查继续
4. 输出清楚说明正在验证的阶段转换

**断言：**
- [ ] Skill 读取 `production/stage.txt`（或使用项目阶段检测启发式方法）以确定当前阶段
- [ ] 输出标题命名当前和目标阶段（例如"Gate Check: Concept → Systems Design"）
- [ ] 若当前阶段可确定，Skill 不向用户询问应检查哪个门控

---

### 用例 4：边缘情况——手动检查项正确标记

**Fixture：**
- 概念→系统设计所有必要制品均存在
- 无游玩测试或评审记录（无法自动核实质量检查项）

**输入：** `/gate-check systems-design`

**预期行为：**
1. Skill 核实所有制品文件存在
2. Skill 遇到质量检查："游戏概念已评审（非 MAJOR REVISION NEEDED）"
3. 由于无评审记录，Skill 将该项标记为"MANUAL CHECK NEEDED"
4. Skill 向用户询问："Has the game concept been reviewed for design quality?"
5. Skill 在用户回答前等待，再确定最终 verdict

**断言：**
- [ ] 无法自动核实的项目标记为 `[?] MANUAL CHECK NEEDED`，而非假定通过
- [ ] Skill 就至少一个无法核实的质量项向用户提问
- [ ] Skill 不将无法核实的项目默认标记为 PASS

---

### 用例 5：Director 门控——lean vs full vs solo 模式

**Fixture：**
- `production/session-state/review-mode.txt` 存在
- 目标门控所有必要制品均存在
- `design/gdd/game-concept.md` 存在

**用例 5a——full 模式：**
- `review-mode.txt` 内容为 `full`

**输入：** `/gate-check systems-design`（full 模式活跃）

**Full 模式预期行为：**
1. Skill 读取审核模式——确定为 `full`
2. Skill 并行生成所有 4 个 PHASE-GATE Director 提示：
   - CD-PHASE-GATE（creative-director）
   - TD-PHASE-GATE（technical-director）
   - PR-PHASE-GATE（producer）
   - AD-PHASE-GATE（art-director）
3. 任何一个 Director 返回 CONCERNS → 整体门控 verdict 至少为 CONCERNS
4. 生成最终输出前收集全部 4 个 verdict

**断言（5a）：**
- [ ] Skill 在决定生成哪些 Director 前读取 review-mode
- [ ] 全部 4 个 PHASE-GATE Director 提示均被生成（不是只生成 1 或 2 个）
- [ ] Director 并行生成（同时，不是依次）
- [ ] 任何一个 Director 返回 CONCERNS 或 REJECT，verdict 不自动为 PASS
- [ ] 任何 Director 返回 CONCERNS 时 Verdict 不自动为 PASS

**用例 5b——solo 模式：**
- `review-mode.txt` 内容为 `solo`

**输入：** `/gate-check systems-design`（solo 模式活跃）

**Solo 模式预期行为：**
1. Skill 读取审核模式——确定为 `solo`
2. 每个 Director 均注明跳过："[CD-PHASE-GATE] skipped — Solo mode"
3. 门控 verdict 仅来源于制品/质量检查
4. 不生成 Director 门控

**断言（5b）：**
- [ ] solo 模式下不生成 Director 门控
- [ ] 每个被跳过的门控均在输出中明确注明："[GATE-ID] skipped — Solo mode"
- [ ] Verdict 仅基于制品和质量检查

---

## 协议合规

- [ ] 更新 `production/stage.txt` 前使用"May I write"
- [ ] 请求写入批准前展示完整检查清单报告
- [ ] 末尾包含"后续行动"章节，按 verdict 列出下一步
- [ ] 未经用户明确确认不推进阶段
- [ ] 若 `production/stage.txt` 不存在，不在未询问的情况下自动创建

---

## 覆盖范围说明

- Production → Polish 和 Polish → Release 门控此处未涵盖，因为它们需要复杂的多制品设置（Sprint 计划、游玩测试数据、QA 签核）；推迟至专项后续规范。
- "CONCERNS" Verdict 路径（存在轻微差距，但不阻塞）未在此处明确测试；它介于用例 1 和用例 2 之间，遵循相同模式。
- Vertical Slice 验证块（Pre-Production → Production 门控）未涵盖，因为它需要无法以文档 Fixture 表达的可游玩构建上下文。
