# Skill Test Spec: /team-release

## Skill 概述

编排七阶段发布流水线：1. 发布前检查（release-manager + qa-lead）→ 2. 构建验证
（devops-engineer）→ 3. 多方并行验证（qa-lead + devops-engineer + 条件：security-engineer
[若有网络功能] + network-programmer [若多人游戏]）→ 4. Go/No-Go 决策
（release-manager）→ 5. 发布部署（devops-engineer）[仅 GO 时执行] → 6. 上线验证
（qa-lead + devops-engineer）→ 7. 发布确认（release-manager）。
阶段 5 仅在 GO 裁决时执行。
裁决：COMPLETE / BLOCKED。
下一步：发布后监控、`/retrospective`，更新 `production/stage.txt` 为 `Live`。

---

## 静态断言（结构性）

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 明确包含七个阶段
- [ ] 阶段 3 明确并行派生 qa-lead 和 devops-engineer
- [ ] security-engineer 仅在有网络/在线功能时条件派生
- [ ] network-programmer 仅在多人游戏时条件派生
- [ ] 阶段 5 仅在 GO 裁决时执行
- [ ] 包含裁决关键字：COMPLETE、BLOCKED
- [ ] 存在文件写入协议；编排者不直接写入文件
- [ ] 子 agent 在任何写入之前强制执行"May I write to [path]?"
- [ ] 存在错误恢复协议
- [ ] 步骤过渡前使用 `AskUserQuestion`
- [ ] 末尾包含下一步交接：`/retrospective`，更新 `production/stage.txt`

---

## 测试用例

### 用例 1：正常路径——单人游戏，所有阶段完成，裁决 COMPLETE

**测试夹具：**
- 单人游戏（无网络功能，无多人游戏）
- 所有 QA 测试通过
- 构建已签名且未修改
- 发布里程碑：`v1.0.0`

**输入：** `/team-release v1.0.0`

**预期行为：**
1. 上下文收集：读取发布清单、QA 报告、里程碑文档
2. 阶段 1：release-manager 和 qa-lead 进行发布前检查（开放 bug 清零、调用 `/release-checklist`）
3. `AskUserQuestion` 批准预检结果后进行阶段 2
4. 阶段 2：devops-engineer 验证构建（哈希校验、代码签名、构建可重现性）
5. `AskUserQuestion` 批准构建验证后进行阶段 3
6. 阶段 3：并行派生 qa-lead（最终 QA 检查）和 devops-engineer（部署配置验证）
   - 单人游戏：security-engineer 和 network-programmer 均不派生
7. `AskUserQuestion` 批准阶段 3 后进行阶段 4
8. 阶段 4：release-manager 发出 Go/No-Go 决策——**GO**
9. `AskUserQuestion` 确认 GO 决策后进行阶段 5（部署）
10. 阶段 5：devops-engineer 执行部署（平台上传、CDN 更新、触发发布）
11. 阶段 6：qa-lead + devops-engineer 并行验证上线状态
12. 阶段 7：release-manager 确认发布成功；`production/stage.txt` 更新为 `Live`
13. 裁决：COMPLETE；下一步：`/retrospective`、发布后监控

**断言：**
- [ ] 单人游戏时 security-engineer 和 network-programmer 不被派生
- [ ] 阶段 3 中 qa-lead 和 devops-engineer 的 Task 调用同时发出
- [ ] 阶段 5 仅在 GO 裁决后执行
- [ ] `production/stage.txt` 更新为 `Live`
- [ ] 编排者不直接写入任何文件
- [ ] `/changelog` 由 release-manager 在阶段 6 调用（不直接写入）
- [ ] `/patch-notes v1.0.0` 由 community-manager 在阶段 6 调用
- [ ] 裁决为 COMPLETE

---

### 用例 2：NO-GO S1 级 Bug——阶段 5 部署被跳过

**测试夹具：**
- 阶段 3 进行中
- qa-lead 在最终检查中发现：一个 S1 级 bug（玩家进度可能被损坏）从 QA 报告中漏网
- 该 bug 在当前构建中存在但未修复

**输入：** `/team-release v1.0.0`（阶段 3–4 场景）

**预期行为：**
1. 阶段 3：qa-lead 发现未修复的 S1 级 bug
2. 编排者立即显示：发现阻塞 bug——qa-lead 报告 S1 级未修复 bug
3. 阶段 4：release-manager 基于 S1 bug 报告发出 **NO-GO** 裁决
4. 阶段 5（部署）被**跳过**——NO-GO 时不执行部署
5. 编排者显示：**NO-GO——部署已跳过。在修复 S1 bug 并重新完成 QA 循环之前不会发布。**
6. `AskUserQuestion` 呈现选项：
   - 提交紧急修复，重新运行 QA，重新发布
   - 推迟发布到下一里程碑
7. `production/stage.txt` 不被更新（保持当前状态）

**断言：**
- [ ] NO-GO 时阶段 5（部署）被跳过——不执行任何部署操作
- [ ] 编排者输出明确的 NO-GO 信息和阻塞原因
- [ ] `production/stage.txt` 在 NO-GO 时不被更新
- [ ] `AskUserQuestion` 提供紧急修复或推迟的选项
- [ ] 裁决为 BLOCKED（非 COMPLETE）

---

### 用例 3：在线游戏——条件派生 security-engineer

**测试夹具：**
- 游戏包含在线多人功能
- `.claude/docs/technical-preferences.md` 中标记有网络/在线功能

**输入：** `/team-release v2.0.0`

**预期行为：**
1. 上下文收集：编排者检测到游戏有在线/多人功能
2. 阶段 3：并行派生 qa-lead + devops-engineer + **security-engineer** + **network-programmer**
3. security-engineer 进行安全审查（通信加密、输入验证、漏洞扫描）
4. network-programmer 验证网络层（延迟容限、断线重连、数据包完整性）
5. 报告中说明 security-engineer 和 network-programmer 因在线功能而被派生

**断言：**
- [ ] 在线/多人游戏时 security-engineer 被派生
- [ ] 在线/多人游戏时 network-programmer 被派生
- [ ] 两者与 qa-lead 和 devops-engineer 并行执行（同时发出四个 Task）
- [ ] 报告说明派生这些 agent 的条件原因

---

### 用例 4：本地化遗漏——阻塞发布

**测试夹具：**
- 阶段 1 发布前检查：release-manager 审查发布清单
- 发现：游戏说明已提交英语版本，但简体中文版本的平台商店页面文字仍为空——而该版本明确包含简体中文本地化

**输入：** `/team-release v1.0.0`（阶段 1 场景）

**预期行为：**
1. 阶段 1：release-manager 检查发布清单
2. 发现本地化缺口：简体中文商店页面文字缺失
3. 编排者报告为 BLOCKING 问题：本地化商店页面文字缺失会导致平台驳回发布申请
4. `AskUserQuestion` 提供选项：
   - 补充简体中文商店页面文字后继续
   - 推迟发布直到本地化完成
5. 在本地化缺口解决之前，流水线在阶段 1 阻塞

**断言：**
- [ ] 本地化缺口在阶段 1 被发现并标记为 BLOCKING
- [ ] 在缺口解决之前流水线不推进到阶段 2
- [ ] `AskUserQuestion` 提供补充本地化或推迟的选项

---

### 用例 5：无参数——从里程碑或会话状态推断

**测试夹具：**
- 场景 A：`production/session-state/current-milestone.txt` 存在，内容为 `v1.2.0`
- 场景 B：无会话状态文件

**输入：** `/team-release`（无参数）

**预期行为（场景 A）：**
1. 编排者读取会话状态文件，推断目标里程碑为 `v1.2.0`
2. `AskUserQuestion`："检测到当前里程碑为 v1.2.0。是否对 v1.2.0 启动发布流水线？"

**预期行为（场景 B）：**
1. 无法推断，`AskUserQuestion`："请指定发布版本或里程碑（如 v1.0.0）"
2. 不猜测或假设版本

**断言：**
- [ ] 有会话状态时尝试推断版本并通过 `AskUserQuestion` 确认
- [ ] 无法推断时通过 `AskUserQuestion` 明确请求输入
- [ ] 不在确认之前派生任何 agent

---

## 协议合规性

- [ ] 上下文收集（发布清单、QA 报告、里程碑文档）在派生任何 agent 之前运行
- [ ] 阶段 3 并行：qa-lead + devops-engineer（+ 条件 agent）同时派生
- [ ] security-engineer 仅在有网络/在线功能时派生
- [ ] network-programmer 仅在多人游戏时派生
- [ ] 阶段 5 仅在 GO 裁决后执行
- [ ] NO-GO 时阶段 5 被跳过且明确报告
- [ ] 每次阶段过渡前使用 `AskUserQuestion`
- [ ] 编排者不直接写入任何文件
- [ ] 发布成功后 `production/stage.txt` 更新为 `Live`
- [ ] 裁决为 COMPLETE 或 BLOCKED
- [ ] 末尾包含下一步交接：`/retrospective`、发布后监控

---

## 覆盖率说明

- 多平台同步发布（PC + 主机同时发布）的协调逻辑超出当前 spec 范围。
- 回滚流程（发布后发现严重问题需要回滚）在此 spec 中未独立测试；
  错误恢复协议的存在是唯一的断言。
