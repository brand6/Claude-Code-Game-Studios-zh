# Skill Test Spec: /team-narrative

## Skill 概述

编排五阶段叙事内容流水线：1. 叙事架构（narrative-director）→ 2. 传说 + 初稿并行
（world-builder + writer）→ 3. 叙事评审（narrative-director）→ 4. 本地化合规
（localization-lead）→ 5. 最终整合并行（writer + localization-lead + world-builder）。
裁决：COMPLETE / BLOCKED。
下一步：`/design-review`、`/localize extract`、`/dev-story`。

---

## 静态断言（结构性）

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 明确包含五个阶段
- [ ] 阶段 2 明确并行派生 world-builder 和 writer
- [ ] 阶段 5 明确并行派生 writer、localization-lead 和 world-builder
- [ ] 包含裁决关键字：COMPLETE、BLOCKED
- [ ] 存在文件写入协议；编排者不直接写入文件
- [ ] 子 agent 在任何写入之前强制执行"May I write to [path]?"
- [ ] 存在错误恢复协议
- [ ] 步骤过渡前使用 `AskUserQuestion`
- [ ] 末尾包含下一步交接：`/design-review`、`/localize extract`、`/dev-story`

---

## 测试用例

### 用例 1：正常路径——五个阶段全部完成，裁决 COMPLETE

**测试夹具：**
- 叙事 GDD 位于 `design/gdd/narrative.md`
- 世界圣经位于 `design/narrative/world-bible.md`
- 角色档案位于 `design/narrative/characters/`
- 目标内容：`chapter-2`
- 所有 agent 成功完成任务

**输入：** `/team-narrative chapter-2`

**预期行为：**
1. 上下文收集：读取叙事 GDD、世界圣经、现有角色档案
2. 阶段 1：派生 narrative-director 制定叙事架构（情节节拍、人物弧线、与整体故事的连接点）
3. `AskUserQuestion` 批准叙事架构后进行阶段 2
4. 阶段 2：并行派生 world-builder（场景传说、历史背景、地点细节）和 writer（对话初稿、场景描述、日志条目）
5. `AskUserQuestion` 批准传说和初稿后进行阶段 3
6. 阶段 3：派生 narrative-director 评审——检查一致性、声音质量、叙事节拍是否实现
7. `AskUserQuestion` 批准评审结果后进行阶段 4
8. 阶段 4：派生 localization-lead 进行本地化合规检查（文化敏感性、可译性、字符串长度）
9. `AskUserQuestion` 批准本地化合规后进行阶段 5
10. 阶段 5：并行派生 writer（最终对话润色）、localization-lead（字符串准备）和 world-builder（传说条目最终定稿）
11. 子 agent 询问写入权限后输出保存至相关叙事文档
12. 裁决：COMPLETE；下一步：`/design-review`、`/localize extract`、`/dev-story`

**断言：**
- [ ] 阶段 2 中 world-builder 和 writer 的 Task 调用同时发出
- [ ] 阶段 5 中三个 agent 的 Task 调用同时发出
- [ ] 每次阶段过渡前使用 `AskUserQuestion`
- [ ] 编排者不直接写入任何文件
- [ ] 裁决为 COMPLETE
- [ ] 下一步引用 `/design-review`、`/localize extract`、`/dev-story`

---

### 用例 2：传说矛盾——world-builder 发现内容冲突

**测试夹具：**
- 阶段 2 进行中
- 世界圣经中记录北方森林在 500 年前被诅咒并荒废
- writer 的对话初稿中有一个角色提到"北方森林的古老守护者从未离开那片土地"
- world-builder 在审查 writer 草稿时检测到这一矛盾

**输入：** `/team-narrative chapter-2`（阶段 2 场景）

**预期行为：**
1. 阶段 2 中 world-builder 和 writer 并行工作
2. world-builder 在整合期间审查 writer 的草稿，发现矛盾
3. world-builder 报告矛盾："对话中的'守护者从未离开'与世界圣经中'500 年前诅咒后荒废'的设定相矛盾。"
4. 编排者在 `AskUserQuestion` 之前立即显示此矛盾
5. `AskUserQuestion` 呈现选项：
   - 修改对话中的守护者说法以符合世界圣经
   - 更新世界圣经以纳入守护者持续存在的设定（需要 narrative-director 审批）
   - 在此停止，由 narrative-director 仲裁

**断言：**
- [ ] 矛盾被明确报告，包含具体冲突内容
- [ ] `AskUserQuestion` 提供修改对话或更新世界圣经的选项
- [ ] 矛盾在阶段 3 叙事评审之前被识别（阶段 2 内部检查）
- [ ] 不在未解决矛盾的情况下将冲突内容写入文件

---

### 用例 3：无参数——使用指导

**测试夹具：**
- 任何项目状态

**输入：** `/team-narrative`（无参数）

**预期行为：**
1. Skill 检测到未提供内容标识符
2. 输出使用指导，包含正确调用格式和示例（例如 `chapter-2`、`prologue`、`side-quest-forest`）
3. 不派生任何 agent

**断言：**
- [ ] 无参数时不派生任何 agent
- [ ] 使用信息包含带参数示例的正确格式
- [ ] 不使用 `AskUserQuestion`

---

### 用例 4：本地化合规——硬编码日期格式被标记为 BLOCKING

**测试夹具：**
- 阶段 4 进行中
- writer 的对话中包含"公告板上写着：活动于 12/25/2024 截止报名"
- localization-lead 识别出日期格式 MM/DD/YYYY 是美国特定格式

**输入：** `/team-narrative holiday-event`（阶段 4 场景）

**预期行为：**
1. 阶段 4 中 localization-lead 审查所有叙事文本
2. 发现硬编码日期格式"12/25/2024"：MM/DD/YYYY 格式在大多数欧洲和亚洲地区被误读
3. localization-lead 报告 BLOCKING 本地化问题："发现硬编码日期格式（MM/DD/YYYY）——这是 BLOCKING 本地化问题。必须使用相对日期（'活动还有 3 天'）、本地化日期格式占位符，或系统日期格式变量。"
4. 编排者显示 BLOCKING 标记
5. `AskUserQuestion` 提供解决方案选项
6. 阶段 5 在未解决此问题之前不启动

**断言：**
- [ ] 日期格式问题在报告中标记为 BLOCKING
- [ ] 具体问题文本（"12/25/2024"）被引用
- [ ] `AskUserQuestion` 提供具体解决方案（相对日期、占位符等）
- [ ] 阶段 5 在解决之前不启动

---

### 用例 5：writer 被阻塞——缺少声音档案

**测试夹具：**
- 阶段 2 进行中
- writer 尝试为角色 Commander Kael 写对话
- `design/narrative/characters/commander-kael.md` 不存在
- 没有既有对话可参考声音风格

**输入：** `/team-narrative boss-confrontation`（阶段 2 场景）

**预期行为：**
1. 阶段 2 中 writer 尝试为 Commander Kael 写对话
2. writer 发现缺少角色档案，无法建立一致的角色声音
3. writer 返回 BLOCKED："缺少 Commander Kael 的角色档案（`design/narrative/characters/commander-kael.md`）——无法在没有声音参考的情况下写出一致的对话。"
4. world-builder 的工作继续正常进行
5. 编排者显示 BLOCKED 状态
6. `AskUserQuestion` 提供选项：
   - 先创建 Commander Kael 角色档案再继续
   - 为 writer 提供临时声音指导并继续（创建最终档案前的占位方案）

**断言：**
- [ ] writer 明确引用缺失的档案路径
- [ ] world-builder 的工作不因 writer 阻塞而停止
- [ ] `AskUserQuestion` 提供创建档案或使用临时指导的选项
- [ ] 裁决在 writer 完成之前不为 COMPLETE

---

## 协议合规性

- [ ] 上下文收集（叙事 GDD、世界圣经、角色档案）在派生任何 agent 之前运行
- [ ] 阶段 2 中 world-builder 和 writer 并行派生
- [ ] 阶段 5 中 writer、localization-lead 和 world-builder 并行派生
- [ ] 每次阶段过渡前使用 `AskUserQuestion`
- [ ] 编排者不直接写入任何文件
- [ ] 子 agent 在任何写入之前强制执行"May I write to [path]?"
- [ ] BLOCKED agent 立即报告并显示其他 agent 的部分结果
- [ ] 裁决为 COMPLETE 或 BLOCKED
- [ ] 末尾包含下一步交接：`/design-review`、`/localize extract`、`/dev-story`

---

## 覆盖率说明

- 阶段 3 叙事评审中 narrative-director 返回 MAJOR REVISION 的情况——
  此路径暗示阶段 4–5 不应继续，但未独立测试。
- 语音配音本地化（需要 VO 脚本的特殊格式）超出当前 spec 范围。
