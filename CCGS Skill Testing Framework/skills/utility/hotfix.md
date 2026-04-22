# 技能测试规范：/hotfix

## 技能概要

`/hotfix` 是一个绕过正常冲刺流程的紧急修复工作流，同时保留完整的审计跟踪。
它从主分支创建 hotfix 分支，应用针对性修复，
运行 `/smoke-check` 以验证不发生回归，然后提示用户确认合并回主分支。

每次代码修改均询问"May I write"。Git 操作以 Bash 命令形式展示，
供用户在对话中确认后再在自己的终端执行。技能将修复后的版本标记为
补丁版本升级（例如 v1.0.0 → v1.0.1）。
不适用 director 门控——紧急修复不等待门控批准。
判决为 HOTFIX COMPLETE（smoke 通过）或 HOTFIX BLOCKED（smoke 失败）。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判决关键词：HOTFIX COMPLETE、HOTFIX BLOCKED
- [ ] 代码修改前包含"May I write"协作协议语言
- [ ] git 操作以 Bash 代码块展示（供用户确认后在终端执行）
- [ ] 包含下一步交接（例如，用 `/bug-report` 记录问题，或版本号升级）

---

## Director 门控检查

无。`/hotfix` 是紧急运营技能。不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——崩溃缺陷，smoke 检查通过，HOTFIX COMPLETE

**夹具：**
- `production/bugs/bug-2026-04-06-crash-boss-arena.md` 已存在（CRITICAL 严重程度）
- 当前 git 主分支版本为 v1.0.0
- Smoke 检查通过（无测试失败）

**输入：** `/hotfix`（引用缺陷 slug 或 ID）

**预期行为：**
1. 技能读取缺陷报告并提取问题描述
2. 技能展示以下 Bash 命令以供用户确认：
   `git checkout -b hotfix/crash-boss-arena`
3. 用户确认执行 git 命令
4. 技能分析并提出针对性修复（询问"May I write [修复的文件]?"）
5. 用户批准；修复被写入
6. 技能运行 `/smoke-check`；smoke 检查通过
7. 技能展示合并和版本升级命令：
   `git tag v1.0.1`；`git merge hotfix/crash-boss-arena`
8. 判决为 HOTFIX COMPLETE

**断言：**
- [ ] Git 命令以 Bash 代码块展示（不直接执行）
- [ ] 分支名称与缺陷 slug 相符
- [ ] 修复前询问"May I write"
- [ ] Smoke 检查通过后版本标签从 v1.0.0 升级至 v1.0.1
- [ ] 判决为 HOTFIX COMPLETE

---

### 用例 2：Smoke 检查失败——HOTFIX BLOCKED，不合并

**夹具：**
- 与用例 1 相同的缺陷
- Smoke 检查失败：2 个测试失败，与 hotfix 相关

**输入：** `/hotfix`

**预期行为：**
1. 技能应用修复
2. 技能运行 `/smoke-check`；smoke 检查失败（2 个测试失败）
3. 技能报告失败信息并显示失败的测试
4. 技能不展示合并命令
5. 技能提示用户在再次运行 smoke 检查前调查回归问题
6. 判决为 HOTFIX BLOCKED

**断言：**
- [ ] Smoke 检查失败后不展示合并命令
- [ ] 判决为 HOTFIX BLOCKED
- [ ] 失败的测试名称/详情呈现给用户
- [ ] 明确提示先解决回归问题再继续

---

### 用例 3：已发布版本——标记补丁版本升级

**夹具：**
- 当前 git 标签为 v2.3.0（发布版本）
- 需要修复的缺陷严重程度为 HIGH（非崩溃级，但影响显著）

**输入：** `/hotfix`

**预期行为：**
1. 技能识别当前标签为 v2.3.0
2. 技能展示 hotfix 分支创建命令（`hotfix/[issue-slug]`）
3. 修复完成并通过 smoke 检查后，技能展示版本升级命令：
   v2.3.0 → v2.3.1
4. 技能将版本升级展示为 Bash 代码块，供用户确认后执行
5. 判决为 HOTFIX COMPLETE

**断言：**
- [ ] 补丁版本编号从 v2.3.0 正确升级至 v2.3.1（不升级次版本）
- [ ] 版本升级命令以 Bash 代码块展示
- [ ] 判决为 HOTFIX COMPLETE

---

### 用例 4：缺陷报告无复现步骤——先询问，再开始修复

**夹具：**
- 缺陷报告存在，但复现步骤为"步骤不详"

**输入：** `/hotfix`（引用该缺陷）

**预期行为：**
1. 技能读取缺陷报告并检测到复现步骤缺失
2. 技能暂停，询问："This bug report has no reproduction steps.
   Can you provide the steps to reproduce the issue?"
3. 用户提供步骤
4. 技能继续正常的 hotfix 工作流

**断言：**
- [ ] 复现步骤缺失时，不立即创建分支或实施修复
- [ ] 技能以文字形式询问复现步骤
- [ ] 用户提供步骤后工作流继续
- [ ] 技能不将"步骤不详"作为 HOTFIX BLOCKED 处理——而是追问

---

### 用例 5：Director 门控检查——无门控；hotfix 为紧急工具

**夹具：**
- 存在未关闭的缺陷

**输入：** `/hotfix`

**预期行为：**
1. 技能执行修复工作流
2. 未调用任何 director agent
3. 输出中无门控 ID

**断言：**
- [ ] 未调用 director 门控
- [ ] 输出中无门控跳过消息
- [ ] 技能在不经过任何门控检查的情况下达到 HOTFIX COMPLETE

---

## 协议合规

- [ ] Git 操作以 Bash 代码块展示（不直接执行）
- [ ] 代码修改前询问"May I write [文件路径]?"
- [ ] 修复完成后运行 `/smoke-check`
- [ ] Smoke 通过时展示版本升级和合并命令
- [ ] Smoke 失败时判决为 HOTFIX BLOCKED，不展示合并命令
- [ ] 补丁版本升级格式正确（vX.Y.Z → vX.Y.Z+1）

---

## 覆盖说明

- 多文件修复（hotfix 涉及 3+ 个文件）与每个文件依次询问"May I write"
  的情况不单独作为用例；此规范仅要求每次修改询问一次。
- 向主分支的实际 git 合并在用户的终端中执行——
  技能仅展示命令，不直接执行。
- 需要重新测试（多次 smoke 失败-修复循环）的情况在此不测试；
  用例 2 仅涵盖首次 smoke 失败的情况。
