# 技能测试规范：/help

## 技能概要

`/help` 分析项目当前状态，为用户提供工作流导航。
它读取 `production/stage.txt`（若存在）、活跃冲刺和会话状态，
生成情境化指导，说明下一步应运行哪些技能以及原因。

本技能运行于 Haiku 模型（读取速度快，只读），不写入任何文件。
它接受可选的上下文查询（例如 `/help testing`、`/help narrative`），
缩小建议范围。若未找到 `stage.txt`，则显示所有阶段的完整工作流概述。

本技能不适用 director 门控——始终提供帮助，不受门控约束。
判决始终为 HELP COMPLETE。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判决关键词：HELP COMPLETE
- [ ] 不包含"May I write"语言（技能为只读）
- [ ] 支持带可选参数的调用（`/help [topic]`）

---

## Director 门控检查

无。`/help` 是导航/信息技能。不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——生产阶段，活跃冲刺

**夹具：**
- `production/stage.txt` 内容为 `production`
- `production/sprints/sprint-012.md` 存在，状态为 `active`，含部分未完成的故事

**输入：** `/help`

**预期行为：**
1. 技能读取 `production/stage.txt` → `production`
2. 技能读取活跃冲刺，找到 sprint-012 及未完成的故事
3. 技能生成针对生产阶段的情境化指导
4. 建议内容以当前冲刺焦点为主：`/dev-story`、`/story-done`、`/sprint-status`
5. 提及冲刺中正在进行的工作
6. 判决为 HELP COMPLETE

**断言：**
- [ ] 建议内容与生产阶段相符（不推荐 `/brainstorm` 或 `/setup-engine`）
- [ ] 建议中提及活跃冲刺（sprint-012）
- [ ] 未写入任何文件
- [ ] 判决为 HELP COMPLETE

---

### 用例 2：概念阶段——推荐早期工作流技能

**夹具：**
- `production/stage.txt` 内容为 `concept`
- 无活跃冲刺
- 不存在 GDD

**输入：** `/help`

**预期行为：**
1. 技能读取 `production/stage.txt` → `concept`
2. 技能检查 GDD 状态——未找到
3. 技能建议概念阶段的技能：`/brainstorm`、`/art-bible`（可选）、`/map-systems`
4. 技能解释每项技能在工作流中的作用
5. 判决为 HELP COMPLETE

**断言：**
- [ ] 建议中包含 `/brainstorm`
- [ ] 不建议生产阶段的技能（如 `/dev-story`、`/sprint-plan`）
- [ ] 建议数量合理（3-5 个技能，而非列出所有技能）
- [ ] 判决为 HELP COMPLETE

---

### 用例 3：无 stage.txt——显示完整工作流概述

**夹具：**
- 不存在 `production/stage.txt`
- 无其他项目文件

**输入：** `/help`

**预期行为：**
1. 技能尝试读取 `production/stage.txt`——文件未找到
2. 技能输出完整工作流概述，涵盖所有 7 个阶段
3. 技能建议运行 `/project-stage-detect` 以确定当前位置
4. 技能建议运行 `/start` 开始新项目

**断言：**
- [ ] 所有 7 个开发阶段的概述均呈现
- [ ] 建议中提及 `/project-stage-detect` 或 `/start`
- [ ] 技能不报错——在无上下文的情况下能优雅降级
- [ ] 判决为 HELP COMPLETE

---

### 用例 4：带上下文查询——缩小范围：/help testing

**夹具：**
- `production/stage.txt` 内容为 `production`

**输入：** `/help testing`

**预期行为：**
1. 技能读取 `production/stage.txt` → `production`
2. 技能将建议范围缩小到测试相关技能
3. 建议内容：`/qa-plan`、`/smoke-check`、`/regression-suite`、
   `/test-setup`、`/test-evidence-review`
4. 不显示不相关的技能（如 `/brainstorm`、`/world-builder`）
5. 判决为 HELP COMPLETE

**断言：**
- [ ] 至少提及 3 个测试相关技能
- [ ] 不显示无关的非测试技能
- [ ] 响应内容聚焦于测试主题（而非通用工作流）
- [ ] 判决为 HELP COMPLETE

---

### 用例 5：Director 门控检查——无门控；help 始终可用

**夹具：**
- 任意或无项目状态

**输入：** `/help`

**预期行为：**
1. 技能生成帮助输出
2. 未调用任何 director agent
3. 未写入任何文件
4. 任何审查模式下判决均为 HELP COMPLETE

**断言：**
- [ ] 未调用 director 门控
- [ ] 未写入任何文件
- [ ] 输出中无门控跳过消息
- [ ] 判决为 HELP COMPLETE

---

## 协议合规

- [ ] 读取 `production/stage.txt`（若存在）以提供情境化建议
- [ ] 若提供上下文查询，则缩小建议范围
- [ ] 若未找到 `stage.txt`，则呈现完整工作流概述
- [ ] 不写入任何文件
- [ ] 所有情况下判决均为 HELP COMPLETE

---

## 覆盖说明

- `stage.txt` 内容为无效阶段名称（例如 `alpha`）的情况被视为无 `stage.txt` 处理：
  技能回退到完整概述模式。
- 建议列表在整个技能目录中可能随时更新；此规范不对具体技能名称进行硬编码，
  仅对类别（测试、设计、冲刺等）进行断言。
- 运行 Haiku 模型是性能指导，而非可测试的断言——不包含模型检查用例。
