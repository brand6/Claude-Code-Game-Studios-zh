# Skill Test Spec: /team-level

## Skill 概述

编排五步关卡设计流水线：1. 关卡概念（level-designer + narrative-director + world-builder）→
2. 系统规格（systems-designer）→ 3. 区块规划（level-designer）→ 4. 视觉 + 无障碍
并行（art-director + accessibility-specialist）→ 5. QA 验证（qa-tester）。
输出为 `design/levels/[level-name].md`。
裁决：COMPLETE / BLOCKED。

---

## 静态断言（结构性）

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 明确包含五个步骤/阶段
- [ ] 步骤 4 明确并行派生 art-director 和 accessibility-specialist
- [ ] 包含裁决关键字：COMPLETE、BLOCKED
- [ ] 存在文件写入协议；编排者不直接写入文件
- [ ] 子 agent 在任何写入之前强制执行"May I write to [path]?"
- [ ] 存在错误恢复协议
- [ ] 步骤过渡前使用 `AskUserQuestion`
- [ ] 输出文档路径遵循 `design/levels/[level-name].md` 模式

---

## 测试用例

### 用例 1：正常路径——所有五步完成，关卡文档已保存

**测试夹具：**
- 项目 GDD 位于 `design/gdd/`
- 世界圣经位于 `design/narrative/world-bible.md`
- 引擎已配置
- 关卡名称：`forest-village`
- 所有 agent 成功完成任务

**输入：** `/team-level forest-village`

**预期行为：**
1. 上下文收集：读取相关 GDD、世界圣经、现有关卡文档（如有）
2. 步骤 1：并行派生 level-designer（空间流程和遭遇布局）、narrative-director（叙事目的、情感节奏）和 world-builder（环境叙事、派系存在）
3. `AskUserQuestion` 批准关卡概念后进行步骤 2
4. 步骤 2：派生 systems-designer 定义关卡特定系统规格（拾取物分布、敌人刷新、谜题机制）
5. `AskUserQuestion` 批准系统规格后进行步骤 3
6. 步骤 3：派生 level-designer 制作详细区块规划图（房间/区域布局、连接通道、遭遇触发点）
7. `AskUserQuestion` 批准区块规划后进行步骤 4
8. 步骤 4：并行派生 art-director（视觉指导、灯光方案、素材需求列表）和 accessibility-specialist（导航清晰度、视觉对比度、替代路径）
9. `AskUserQuestion` 批准视觉和无障碍规格后进行步骤 5
10. 步骤 5：派生 qa-tester 验证关卡设计的可测试性和完整性
11. 子 agent 询问"May I write the level design document to `design/levels/forest-village.md`?"
12. 文档写入，裁决：COMPLETE

**断言：**
- [ ] 步骤 1 中 level-designer、narrative-director 和 world-builder 同时派生
- [ ] 步骤 4 中 art-director 和 accessibility-specialist 同时派生
- [ ] 每次步骤过渡前使用 `AskUserQuestion`
- [ ] 关卡文档写入 `design/levels/forest-village.md`
- [ ] 编排者不直接写入任何文件
- [ ] 裁决为 COMPLETE

---

### 用例 2：阻塞 world-builder——部分报告生成

**测试夹具：**
- 步骤 1 进行中
- world-builder 返回 BLOCKED："缺少森林村庄派系信息——world-bible.md 中没有关于该地区控制派系的记录，无法确定环境叙事细节。"
- level-designer 和 narrative-director 正常完成步骤 1

**输入：** `/team-level forest-village`（步骤 1 场景）

**预期行为：**
1. 步骤 1 中三个 agent 并行派生
2. world-builder 返回 BLOCKED，明确说明阻塞原因
3. 编排者立即在对话中显示 BLOCKED 状态
4. level-designer 和 narrative-director 的结果仍被收集和展示
5. `AskUserQuestion` 呈现部分步骤 1 结果，提供选项：
   - 停止并更新世界圣经后重新继续（推荐）
   - 继续进行步骤 2–5，将世界构建部分标记为待完成
6. 生成部分报告，记录已完成内容（level-designer + narrative-director）和缺失内容（world-builder）
7. 裁决：BLOCKED

**断言：**
- [ ] world-builder 明确引用阻塞原因（缺失派系信息）
- [ ] level-designer 和 narrative-director 的结果不因 world-builder 阻塞而丢失
- [ ] `AskUserQuestion` 提供停止或继续的清晰选项
- [ ] 部分报告列出已完成和被阻塞的内容
- [ ] 裁决为 BLOCKED

---

### 用例 3：无参数——使用指导

**测试夹具：**
- 任何项目状态

**输入：** `/team-level`（无参数）

**预期行为：**
1. Skill 检测到未提供关卡名称
2. 输出使用指导，包含正确的调用格式和示例（例如 `forest-village`、`dungeon-floor-2`、`boss-arena`）
3. 不派生任何 agent

**断言：**
- [ ] 无参数时不派生任何 agent
- [ ] 使用信息包含带参数示例的正确格式
- [ ] 不使用 `AskUserQuestion`

---

### 用例 4：无障碍 BLOCKING 关注点——步骤 4 中 accessibility-specialist 发现问题

**测试夹具：**
- 步骤 1–3 已成功完成
- 步骤 4 进行中
- accessibility-specialist 在审查区块规划后发现：主要谜题区域只有一条通路，且需要精确跳跃——轮椅用户或运动障碍玩家无法完成

**输入：** `/team-level puzzle-tower`（步骤 4 场景）

**预期行为：**
1. 步骤 4 中 art-director 和 accessibility-specialist 并行派生
2. accessibility-specialist 返回 BLOCKING 关注点："主谜题区（C3 区块）的精确跳跃要求构成 BLOCKING 无障碍问题。运动障碍玩家无法完成此区域——需要替代路径或辅助模式。"
3. 编排者立即显示 BLOCKING 关注点
4. `AskUserQuestion` 在步骤 5 之前呈现选项：
   - 为 C3 区块添加替代路径并继续
   - 添加辅助模式选项（自动跳跃、宽容判定）并继续
   - 在此停止，重新设计关卡布局
5. 步骤 5 在用户解决或明确接受无障碍缺口之前不启动

**断言：**
- [ ] 无障碍关注点在报告中标记为 BLOCKING
- [ ] 具体位置（C3 区块）和问题性质已明确说明
- [ ] 步骤 5 在未经用户明确授权前不启动
- [ ] `AskUserQuestion` 提供至少一个解决方案选项
- [ ] 若缺口未解决就继续，则在关卡文档中记录为未解决问题

---

### 用例 5：循环关卡引用——发现并报告引用冲突

**测试夹具：**
- `design/levels/dungeon-floor-1.md` 引用 dungeon-floor-2 作为前提关卡
- 正在设计 `dungeon-floor-2`，其设计草案引用 dungeon-floor-1 作为前提关卡
- 步骤 1 上下文收集期间发现此循环引用

**输入：** `/team-level dungeon-floor-2`

**预期行为：**
1. 上下文收集：读取 `design/levels/dungeon-floor-1.md`，发现它引用 dungeon-floor-2 作为前提
2. 正在设计的 dungeon-floor-2 也引用 dungeon-floor-1 作为前提——形成循环依赖
3. 编排者在对话中立即报告："检测到循环关卡依赖：dungeon-floor-1 → dungeon-floor-2 → dungeon-floor-1。请在流水线继续之前解决此冲突。"
4. `AskUserQuestion` 呈现选项：
   - 移除其中一个依赖引用并继续
   - 重新设计关卡顺序

**断言：**
- [ ] 循环引用在上下文收集期间（步骤 1 之前）被检测到
- [ ] 循环引用被明确报告，不被静默忽略
- [ ] 不在未解决循环引用的情况下继续派生设计 agent
- [ ] 报告中明确说明涉及的具体关卡名称

---

## 协议合规性

- [ ] 上下文收集（GDD、世界圣经、现有关卡文档）在派生任何 agent 之前运行
- [ ] 步骤 1 中 level-designer、narrative-director、world-builder 并行派生
- [ ] 步骤 4 中 art-director 和 accessibility-specialist 并行派生
- [ ] 每次步骤过渡前使用 `AskUserQuestion`
- [ ] 编排者不直接写入任何文件
- [ ] 子 agent 在任何写入之前强制执行"May I write to [path]?"
- [ ] BLOCKED agent 立即报告并显示部分结果
- [ ] 输出路径遵循 `design/levels/[level-name].md` 模式
- [ ] 裁决为 COMPLETE 或 BLOCKED
- [ ] 末尾包含下一步交接：`/design-review`、`/dev-story`、`/qa-plan`

---

## 覆盖率说明

- 步骤 3 区块规划中 level-designer 对自身步骤 1 工作的重访——
  同一 agent 在不同步骤中被派生两次的情况未独立测试。
- 关卡设计文档内部各区块的命名约定未在此 spec 中独立断言。
