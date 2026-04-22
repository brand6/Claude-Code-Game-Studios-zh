# 技能测试规范：/onboard

## 技能概要

`/onboard` 为加入项目的新团队成员或 agent 生成情境化入职摘要。
它读取 `CLAUDE.md`、`technical-preferences.md`、活跃冲刺、
最近的 git 提交，以及 `production/stage.txt`，将相关信息汇编为
对新成员有帮助的摘要。

本技能接受可选的角色参数（例如 `/onboard artist`、`/onboard programmer`），
并据此定制摘要内容，突出与该角色相关的部分。
运行于 Haiku 模型（只读），不写入任何文件。

不适用 director 门控。判决始终为 ONBOARDING COMPLETE。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判决关键词：ONBOARDING COMPLETE
- [ ] 不包含"May I write"语言（技能为只读）
- [ ] 支持带可选角色参数的调用（`/onboard [role]`）

---

## Director 门控检查

无。`/onboard` 是信息摘要技能。不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——生产阶段，配置完整的项目

**夹具：**
- `CLAUDE.md` 存在，包含：引擎（Godot 4）、语言（GDScript）、项目名称
- `technical-preferences.md` 存在，包含代码规范
- `production/stage.txt` 内容为 `production`
- `production/sprints/sprint-015.md` 为活跃冲刺，包含 4 个未完成的故事
- 最近的 git 提交可读（最近 5 次提交）

**输入：** `/onboard`

**预期行为：**
1. 技能读取 `CLAUDE.md`、`technical-preferences.md`、`production/stage.txt`
2. 技能读取活跃冲刺，找到 sprint-015
3. 技能读取最近的 git 提交
4. 技能生成包含以下内容的入职摘要：
   - 项目概述（名称、引擎、语言）
   - 当前开发阶段：Production
   - 活跃冲刺及未完成故事概述
   - 代码规范概要
   - 最近的活动（git 提交）
   - 下一步建议：`/sprint-status`、`/dev-story`
5. 判决为 ONBOARDING COMPLETE

**断言：**
- [ ] 摘要包含引擎/语言信息
- [ ] 摘要提及活跃冲刺（sprint-015）
- [ ] 摘要提及当前开发阶段（Production）
- [ ] 未写入任何文件
- [ ] 判决为 ONBOARDING COMPLETE

---

### 用例 2：全新项目——无配置，最小化摘要

**夹具：**
- 不存在 `CLAUDE.md`
- 不存在 `production/stage.txt`
- 无冲刺文件
- 无 git 提交

**输入：** `/onboard`

**预期行为：**
1. 技能尝试读取 `CLAUDE.md`——未找到
2. 技能尝试读取 `production/stage.txt`——未找到
3. 技能输出最小化摘要："Project is in initial setup stage, no configuration found"
4. 技能说明入职工作流：`/start` → `/setup-engine` → `/brainstorm`，并建议先运行 `/start` 进行项目初始设置
5. 判决为 ONBOARDING COMPLETE

**断言：**
- [ ] 技能在缺少配置文件时不报错
- [ ] 建议中提及 `/start` 进行初始设置
- [ ] 技能优雅降级——输出有意义的最小化摘要
- [ ] 判决为 ONBOARDING COMPLETE

---

### 用例 3：缺少 CLAUDE.md——错误消息

**夹具：**
- `CLAUDE.md` 不存在
- 存在 `production/stage.txt` 和冲刺文件

**输入：** `/onboard`

**预期行为：**
1. 技能尝试读取 `CLAUDE.md`——未找到
2. 技能输出警告："CLAUDE.md not found — project may not be configured
   with this template"
3. 技能继续生成尽可能完整的摘要（使用可用文件）
4. 判决为 ONBOARDING COMPLETE（附警告说明）

**断言：**
- [ ] 输出中包含"CLAUDE.md not found"警告
- [ ] 技能不完全停止——基于其他可用文件生成摘要
- [ ] 判决为 ONBOARDING COMPLETE（即使文件缺失，也明确注明）

---

### 用例 4：指定角色——为"artist"定制入职内容

**夹具：**
- 配置完整的项目（CLAUDE.md、stage.txt、活跃冲刺、art bible 存在）

**输入：** `/onboard artist`

**预期行为：**
1. 技能识别角色参数为"artist"
2. 技能读取 art bible（若存在）并将相关内容纳入摘要
3. 摘要内容聚焦于与美术相关的部分：美术圣经、资产规范、美术规范
4. 代码规范或编程工作流的讲解比例少于无角色参数的情况
5. 判决为 ONBOARDING COMPLETE

**断言：**
- [ ] 摘要中包含美术相关内容（美术圣经、资产规范等）
- [ ] 摘要不以编程内容为主
- [ ] 内容与"artist"角色的相关性明显高于通用入职摘要
- [ ] 判决为 ONBOARDING COMPLETE

---

### 用例 5：Director 门控检查——无门控；onboard 为信息工具

**夹具：**
- 标准项目设置

**输入：** `/onboard`

**预期行为：**
1. 技能生成入职摘要
2. 未调用任何 director agent
3. 未写入任何文件

**断言：**
- [ ] 未调用 director 门控
- [ ] 未写入任何文件
- [ ] 输出中无门控跳过消息
- [ ] 判决为 ONBOARDING COMPLETE

---

## 协议合规

- [ ] 读取 `CLAUDE.md`、`technical-preferences.md`（若存在）、`production/stage.txt`、活跃冲刺
- [ ] 支持可选角色参数以定制摘要内容
- [ ] 文件缺失时优雅降级（提供最小化摘要）
- [ ] 不写入任何文件
- [ ] 所有情况下判决均为 ONBOARDING COMPLETE

---

## 覆盖说明

- 在此规范中不测试运行于 Haiku 模型的情况——
  这是技能主体中的性能指导，而非可断言的行为。
- 所有可能的角色（programmer、designer、qa 等）不单独测试；
  用例 4 仅验证角色参数会影响摘要内容这一原则。
- Git 提交读取访问失败的情况被视为可选内容缺失，
  技能会继续生成不包含提交历史的摘要。
