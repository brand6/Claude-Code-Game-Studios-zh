# 技能测试规范：/start

## 技能概要

`/start` 是首次引导技能。当项目尚未配置引擎或游戏概念时，它会引导用户
完成初始项目设置：命名项目、选择游戏引擎（Godot 4、Unity 或 Unreal Engine 5），
以及创建基础文件（`CLAUDE.md` 占位符更新、`technical-preferences.md` 框架）。
完成后，它会将用户引导至 `/setup-engine [引擎]` 进行详细配置。

`/start` 会检测现有配置：若已配置，则提供跳过或重新配置选项。
它还会检测中断的设置（部分完成）并提供恢复或重新开始。
每个文件写入均需"May I write"批准。无 director 门控。
判定结果：COMPLETE（成功完成配置）或 BLOCKED（发生无法解决的冲突）。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判定关键词：COMPLETE、BLOCKED
- [ ] 在写入项目文件前包含"May I write"协作协议语言
- [ ] 包含下一步交接（写入文件后交接至 `/setup-engine [引擎]`）

---

## Director 门控检查

无。`/start` 是引导技能，不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——全新仓库，完整引导至 /setup-engine 交接

**夹具：**
- 全新仓库：`CLAUDE.md` 为通用占位符，无 `technical-preferences.md`
- 无引擎配置
- 无游戏名称

**输入：** `/start`

**预期行为：**
1. 技能读取 `CLAUDE.md`，检测到占位符（无项目名称或引擎配置）
2. 技能询问项目名称："What is your game's name?"
3. 用户回答："Epic Quest"
4. 技能询问引擎："Which engine? Godot 4 / Unity / Unreal Engine 5"
5. 用户选择"Godot 4"
6. 技能起草 `CLAUDE.md` 更新（项目名称、引擎占位符）并询问"May I write to `CLAUDE.md`?"
7. 技能起草 `technical-preferences.md` 框架并询问"May I write to `technical-preferences.md`?"
8. 两个写入均获批准
9. 技能输出交接消息："Project 'Epic Quest' initialized. Run `/setup-engine godot` to complete configuration."
10. 判定结果为 COMPLETE

**断言：**
- [ ] 写入前询问项目名称（不使用硬编码名称）
- [ ] 提供恰好 3 个引擎选项（Godot 4、Unity、Unreal Engine 5）
- [ ] CLAUDE.md 更新前询问"May I write"
- [ ] technical-preferences.md 创建前询问"May I write"
- [ ] 交接消息引用正确的引擎（`/setup-engine godot`）
- [ ] 判定结果为 COMPLETE

---

### 用例 2：引擎已配置——提供跳过或重新配置选项

**夹具：**
- `CLAUDE.md` 已包含项目名称"Dragon Forge"并配置 Unity 引擎
- `technical-preferences.md` 已完整填充

**输入：** `/start`

**预期行为：**
1. 技能读取 `CLAUDE.md`，检测到配置已存在（Unity，Dragon Forge）
2. 技能报告："Project already configured: Dragon Forge (Unity)"
3. 技能提供选项：
   - 跳过——项目已就绪，继续开发
   - 重新配置引擎/名称
   - 重新运行 `/setup-engine unity` 更新技术偏好
4. 用户选择"跳过"
5. 技能退出，不修改任何文件
6. 判定结果为 COMPLETE（现有配置被识别）

**断言：**
- [ ] 检测到现有配置并报告
- [ ] 不默认覆盖现有配置
- [ ] 向用户提供 3 种操作选项
- [ ] 选择"跳过"时不写入任何文件
- [ ] 判定结果为 COMPLETE

---

### 用例 3：Godot 4 引擎选择——正确路由至 /setup-engine godot

**夹具：**
- 全新仓库
- 用户在引导过程中选择"Godot 4"

**输入：** `/start`（用户在提示中选择 Godot 4）

**预期行为：**
1. 完整的引导流程完成
2. 交接消息明确指定 Godot 4：
   "Run `/setup-engine godot` to configure Godot-specific settings"
3. 不生成 `/setup-engine unity` 或 `/setup-engine unreal` 的引用

**断言：**
- [ ] 交接消息包含 `/setup-engine godot`（非通用 `/setup-engine`）
- [ ] 不出现其他引擎名称
- [ ] CLAUDE.md 中的引擎字段写入"Godot 4"

---

### 用例 4：中断的设置——恢复或重新开始

**夹具：**
- CLAUDE.md 已用项目名称更新
- `technical-preferences.md` 不存在（设置中途中断）
- 之前的会话已中断

**输入：** `/start`

**预期行为：**
1. 技能读取 `CLAUDE.md`——有项目名称，但没有引擎
2. 技能读取 `technical-preferences.md`——文件不存在
3. 技能检测到部分配置状态
4. 技能报告："Partial setup detected: project name set but engine not configured.
   Resume from engine selection, or restart from the beginning?"
5. 用户选择"从引擎选择继续"
6. 技能从引擎选择步骤继续（跳过名称询问）
7. 完成后续步骤；判定结果为 COMPLETE

**断言：**
- [ ] 检测到部分配置状态
- [ ] 向用户提供恢复与重新开始的选项
- [ ] 恢复时不会重复已完成的步骤
- [ ] 完成后判定结果为 COMPLETE

---

### 用例 5：Director 门控检查——无门控；start 是引导技能

**夹具：**
- 全新仓库

**输入：** `/start`

**预期行为：**
1. 完成完整引导流程
2. 任何时候都不会生成 director agent
3. 输出中不出现门控 ID

**断言：**
- [ ] 未调用任何 director 门控
- [ ] 不出现门控跳过消息
- [ ] 判定结果为 COMPLETE 或 BLOCKED——无门控判定

---

## 协议合规性

- [ ] 写入任何文件前询问项目名称（不使用占位符）
- [ ] 提供恰好 3 个引擎选项（Godot 4、Unity、Unreal Engine 5）
- [ ] 每个文件写入均获"May I write"批准
- [ ] 交接消息指定所选引擎（`/setup-engine [引擎]`）
- [ ] 检测现有配置并提供跳过/重新配置选项

---

## 覆盖说明

- 第四个引擎选项（自定义/其他引擎）未经测试；`/start` 设计为仅支持
  Godot 4、Unity 和 Unreal Engine 5。
- 在多根工作区（多个游戏项目并排放置）中运行的行为此处未测试。
- Unreal Engine 5 引擎选择遵循与用例 3（Godot 4）相同的模式；
  此处作为覆盖说明而非单独用例记录。
