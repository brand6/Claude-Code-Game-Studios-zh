# Skill Test Spec: /team-audio

## Skill 概述

编排音频团队完成四步流水线：音频指导（audio-director）→ 音效设计 + 无障碍审查并行
（sound-designer + accessibility-specialist）→ 技术实现 + 引擎验证并行
（technical-artist + 主引擎专项 agent）→ 代码集成（gameplay-programmer）。
在派生 agent 之前读取相关 GDD、音效圣经（如存在）以及现有音频素材列表。
将所有输出汇总为保存至 `design/gdd/audio-[feature].md` 的音频设计文档。
每次步骤过渡时使用 `AskUserQuestion`。所有输出写入均为 COMPLETE 时视为完成。
当没有配置引擎时，引擎专项 agent 的派生步骤将被优雅跳过。

---

## 静态断言（结构性）

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 至少包含 2 个步骤/阶段标题
- [ ] 包含裁决关键字：COMPLETE、BLOCKED
- [ ] 包含"文件写入协议"部分
- [ ] 文件写入委托给子 agent——编排者不直接写入文件
- [ ] 子 agent 在任何写入之前强制执行"May I write to [path]?"
- [ ] 末尾包含下一步交接（引用 `/dev-story`、`/asset-audit`）
- [ ] 存在错误恢复协议部分
- [ ] 步骤过渡前使用 `AskUserQuestion`
- [ ] 步骤 2 明确并行派生 sound-designer 和 accessibility-specialist
- [ ] 步骤 3 在引擎已配置时明确并行派生 technical-artist 和引擎专项 agent
- [ ] Skill 在上下文收集期间（若存在）读取 `design/gdd/sound-bible.md`
- [ ] 输出文档保存至 `design/gdd/audio-[feature].md`

---

## 测试用例

### 用例 1：正常路径——所有步骤完成，音频设计文档已保存

**测试夹具：**
- 目标功能的 GDD 位于 `design/gdd/combat.md`
- 音效圣经位于 `design/gdd/sound-bible.md`
- 现有音频素材列于 `assets/audio/`
- 引擎已在 `.claude/docs/technical-preferences.md` 中配置
- 计划音频事件列表中不存在无障碍缺口

**输入：** `/team-audio combat`

**预期行为：**
1. 上下文收集：编排者在派生任何 agent 之前读取 `design/gdd/combat.md`、`design/gdd/sound-bible.md` 以及 `assets/audio/` 素材列表
2. 步骤 1：派生 audio-director；为战斗定义声音身份、情感基调、自适应音乐指导、混音目标和自适应音频规则
3. `AskUserQuestion` 呈现音频指导；用户批准后开始步骤 2
4. 步骤 2：并行派生 sound-designer 和 accessibility-specialist；sound-designer 生成 SFX 规格、带触发条件的音频事件列表和混音组；accessibility-specialist 识别关键游戏玩法音频事件并指定视觉备用方案和字幕要求
5. `AskUserQuestion` 呈现 SFX 规格和无障碍要求；用户批准后开始步骤 3
6. 步骤 3：并行派生 technical-artist 和主引擎专项 agent；technical-artist 设计总线结构、中间件集成、内存预算和流式策略；引擎专项 agent 验证集成方式是否符合所配引擎的惯用法
7. `AskUserQuestion` 呈现技术方案；用户批准后开始步骤 4
8. 步骤 4：派生 gameplay-programmer；将音频事件连接到游戏玩法触发器，实现自适应音乐，设置遮挡区域，为音频事件触发器编写单元测试
9. 编排者将所有输出汇总为单一音频设计文档
10. 子 agent 在写入之前询问"May I write the audio design document to `design/gdd/audio-combat.md`?"
11. 摘要输出列出：音频事件数量、预计素材数量、实现任务和所有未解决问题
12. 裁决：COMPLETE

**断言：**
- [ ] 音效圣经在上下文收集期间（步骤 1 之前）被读取（若存在）
- [ ] audio-director 在 sound-designer 或 accessibility-specialist 之前被派生
- [ ] 步骤 1 输出后且步骤 2 启动前出现 `AskUserQuestion`
- [ ] 步骤 2 中 sound-designer 和 accessibility-specialist 的 Task 调用同时发出
- [ ] 步骤 3 中 technical-artist 和引擎专项 agent 的 Task 调用同时发出
- [ ] 步骤 3 的 `AskUserQuestion` 批准前不启动 gameplay-programmer
- [ ] 音频设计文档写入 `design/gdd/audio-combat.md`（不是其他路径）
- [ ] 摘要包含音频事件数量和预计素材数量
- [ ] 编排者不直接写入任何文件
- [ ] 文档交付后裁决为 COMPLETE

---

### 用例 2：无障碍缺口——关键游戏玩法音频事件没有视觉备用方案

**测试夹具：**
- 步骤 1 和步骤 2 进行中
- sound-designer 的音频事件列表包含"EnemyNearbyAlert"——一个空间音频提示，警告玩家屏幕外有敌人接近
- accessibility-specialist 审查事件列表，发现"EnemyNearbyAlert"没有视觉备用方案（无屏幕指示器、无字幕、无手柄震动规格）

**输入：** `/team-audio stealth`（步骤 2 场景）

**预期行为：**
1. 步骤 1–2 进行；accessibility-specialist 和 sound-designer 并行派生
2. accessibility-specialist 返回带有 BLOCKING 关注点的审查结果："`EnemyNearbyAlert` 是关键游戏玩法音频事件（警告玩家屏幕外威胁），没有视觉备用方案——听力障碍玩家无法检测到此威胁。这是一个 BLOCKING 无障碍缺口。"
3. 编排者在呈现 `AskUserQuestion` 之前立即在对话中显示此关注点
4. `AskUserQuestion` 将无障碍关注点作为 BLOCKING 问题呈现，并提供选项：
   - 为 EnemyNearbyAlert 添加视觉指示器（例如 HUD 上的方向箭头）并继续
   - 添加手柄触觉反馈作为备用方案并继续
   - 在此停止，解决所有无障碍缺口后再进行步骤 3
5. 在用户解决或明确接受缺口之前，步骤 3（technical-artist + 引擎专项 agent）不会启动
6. 如果未解决，无障碍缺口将包含在最终音频设计文档的"未解决无障碍问题"中

**断言：**
- [ ] 无障碍缺口在报告中被标记为 BLOCKING（不是建议性的）
- [ ] 具体事件名称（"EnemyNearbyAlert"）和缺口性质已明确说明
- [ ] `AskUserQuestion` 在步骤 3 启动之前显示缺口
- [ ] 至少提供一个解决方案选项（添加视觉备用方案、添加触觉备用方案）
- [ ] 在未经明确用户授权的情况下，缺口未解决时不启动步骤 3
- [ ] 若缺口未解决就继续，则在音频设计文档中将其记录为未解决问题

---

### 用例 3：无参数——使用指导或设计文档推断

**测试夹具：**
- 任何项目状态

**输入：** `/team-audio`（无参数）

**预期行为：**
1. Skill 检测到未提供参数
2. 输出使用指导：例如"用法：`/team-audio [功能或区域]`——指定要设计音频的功能或区域（例如 `combat`、`main menu`、`forest biome`、`boss encounter`）"
3. Skill 在不派生任何 agent 的情况下退出

**断言：**
- [ ] 无参数时 Skill 不派生任何 agent
- [ ] 使用信息包含带参数示例的正确调用格式
- [ ] Skill 不尝试在没有用户指引的情况下从现有设计文档推断功能
- [ ] 不使用 `AskUserQuestion`——输出为直接指导

---

### 用例 4：缺少音效圣经——Skill 注意到缺口并在没有它的情况下继续

**测试夹具：**
- 目标功能的 GDD 位于 `design/gdd/main-menu.md`
- `design/gdd/sound-bible.md` 不存在
- 引擎已配置；其他上下文文件存在

**输入：** `/team-audio main menu`

**预期行为：**
1. 上下文收集：编排者读取 `design/gdd/main-menu.md` 并检查 `design/gdd/sound-bible.md`
2. 未找到音效圣经；编排者在对话中注意到缺口："注意：未找到 `design/gdd/sound-bible.md`——音频指导将在没有项目级声音身份参考的情况下进行。如果这是持续项目，请考虑创建音效圣经。"
3. 流水线在没有音效圣经作为输入的情况下正常继续完成所有四个步骤
4. 步骤 1 中的 audio-director 被告知不存在音效圣经，必须仅从功能 GDD 建立声音身份
5. 最终摘要中提到缺少音效圣经作为推荐的下一步

**断言：**
- [ ] 编排者在上下文收集期间（步骤 1 之前）检查音效圣经
- [ ] 缺少音效圣经在对话中明确注明——不被静默忽略
- [ ] 因缺少音效圣经，流水线不会停止
- [ ] audio-director 在其提示上下文中被告知不存在音效圣经
- [ ] 摘要或下一步部分推荐创建音效圣经
- [ ] 如果所有其他步骤成功，裁决仍为 COMPLETE

---

### 用例 5：引擎未配置——引擎专项 agent 步骤优雅跳过

**测试夹具：**
- 引擎未在 `.claude/docs/technical-preferences.md` 中配置（显示 `[TO BE CONFIGURED]`）
- 目标功能的 GDD 存在
- 音效圣经可能存在也可能不存在

**输入：** `/team-audio boss encounter`

**预期行为：**
1. 上下文收集：编排者读取 `.claude/docs/technical-preferences.md` 并检测到引擎未配置
2. 步骤 1–2 正常进行（audio-director、sound-designer、accessibility-specialist）
3. 步骤 3：technical-artist 正常派生；引擎专项 agent 派生被跳过
4. 编排者在对话中注明："引擎专项 agent 未派生——technical-preferences.md 中未配置引擎。引擎集成验证将推迟到选定引擎后进行。"
5. 步骤 4：gameplay-programmer 继续进行，并注明引擎特定音频集成模式无法被验证
6. 引擎专项 agent 缺口包含在音频设计文档的"推迟验证"中
7. 裁决：COMPLETE（跳过是优雅的，不是阻塞器）

**断言：**
- [ ] 引擎未配置时不派生引擎专项 agent
- [ ] 因缺少引擎配置，Skill 不会报错退出
- [ ] 跳过在对话中明确注明——不被静默省略
- [ ] 步骤 3 中 technical-artist 仍被派生（跳过仅适用于引擎专项 agent）
- [ ] gameplay-programmer 在步骤 4 中继续进行，并注明推迟验证
- [ ] 推迟的引擎验证记录在音频设计文档中
- [ ] 裁决为 COMPLETE（引擎未配置是已知的优雅情况）

---

## 协议合规性

- [ ] 上下文收集（GDD、音效圣经、素材列表）在派生任何 agent 之前运行
- [ ] 每次步骤输出后且下一步启动前使用 `AskUserQuestion`
- [ ] 并行派生：步骤 2（sound-designer + accessibility-specialist）和步骤 3（technical-artist + 引擎专项 agent）在等待结果之前发出所有 Task 调用
- [ ] 编排者不直接写入任何文件——所有写入均委托给子 agent
- [ ] 每个子 agent 在任何写入之前强制执行"May I write to [path]?"协议
- [ ] 任何 agent 的 BLOCKED 状态立即显示——不被静默跳过
- [ ] 当某些 agent 完成而其他 agent 阻塞时，始终生成部分报告
- [ ] 音频设计文档路径遵循 `design/gdd/audio-[feature].md` 模式
- [ ] 裁决恰好为 COMPLETE 或 BLOCKED——不使用其他裁决值
- [ ] 下一步交接引用 `/dev-story` 和 `/asset-audit`

---

## 覆盖率说明

- 错误恢复协议中的"缩小范围重试"和"跳过此 agent"解决路径在
  用例 2 中通过断言进行了隐式测试。
