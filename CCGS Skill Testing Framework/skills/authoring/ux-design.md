# Skill Test Spec: /ux-design

## Skill 概述

引导骨架优先的 UX 规格逐节编写。
必需章节：用户流程（User Flows）、交互状态（Interaction States）、线框描述（Wireframe Description）、无障碍说明（Accessibility Notes）。
无内联导演门控（由独立的 `/ux-review` 负责）。
按章节询问"May I write?"。
支持改造模式。
裁决：COMPLETE。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需 Fixture。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 明确包含 4 个必需章节：用户流程、交互状态、线框描述、无障碍说明
- [ ] 无导演门控（`/ux-review` 是独立的审查 Skill）
- [ ] 骨架文件优先创建（含 4 个章节标题，内容为空）
- [ ] 逐节讨论和起草，按章节询问"May I write section [N]?"
- [ ] 裁决：COMPLETE
- [ ] 末尾包含下一步交接至 `/ux-review`

---

## 导演门控检查

无。`/ux-design` 无内联导演门控。`/ux-review` 是该 Skill 完成后独立调用的审查 Skill。

---

## 测试用例

### 用例 1：正常路径——新建 HUD 规格，所有 4 个章节完成

**测试夹具：**
- 无现有 `design/ux/hud-main.md`
- 所有相关 GDD 可用

**输入：** `/ux-design hud-main`

**预期行为：**
1. 立即创建包含 4 个章节标题的骨架文件 `design/ux/hud-main.md`（内容为空）
2. 询问"May I write the skeleton to `design/ux/hud-main.md`?"
3. 逐节引导：
   - **用户流程：** 引导问题（例如："玩家在 HUD 中的主要目标是什么？流程入口和出口在哪里？"）→ 讨论 → 起草 → "May I write section [用户流程]?"
   - **交互状态：** 逐一覆盖 5 种状态（正常/悬停/聚焦/禁用/错误）→ 讨论 → 起草 → "May I write section [交互状态]?"
   - **线框描述：** 仅文字描述（不使用图像）→ 讨论 → 起草 → "May I write section [线框描述]?"
   - **无障碍说明：** 键盘导航、对比度、屏幕阅读器支持 → 讨论 → 起草 → "May I write section [无障碍说明]?"
4. 所有 4 个章节写入完成
5. 裁决：COMPLETE
6. 下一步：`/ux-review hud-main`

**断言：**
- [ ] 骨架文件在内容讨论之前立即创建
- [ ] 逐节起草，每节有独立的"May I write"询问
- [ ] 无导演门控派生
- [ ] 裁决为 COMPLETE
- [ ] 末尾引用 `/ux-review hud-main`

---

### 用例 2：改造模式——现有规格检测

**测试夹具：**
- `design/ux/inventory-screen.md` 已存在，包含 2 个完整章节

**输入：** `/ux-design inventory-screen`

**预期行为：**
1. Skill 读取现有 `design/ux/inventory-screen.md`
2. 编排者注明："发现现有 UX 规格——进入改造模式"
3. 分析现有内容，识别已完整章节（2 个）和缺失章节（2 个）
4. `AskUserQuestion` 提供：
   - 仅补充缺失的 2 个章节
   - 修订特定章节（用户指定）
5. 改造过程中仍逐节询问"May I write section [N]?"

**断言：**
- [ ] 检测到现有规格不被静默覆盖
- [ ] 编排者识别已完整章节和缺失章节
- [ ] `AskUserQuestion` 提供改造选项

---

### 用例 3：依赖缺失——GDD 不存在，添加占位符后继续

**测试夹具：**
- `design/gdd/shop-ui.md` 不存在
- 用户请求设计商店 UI

**输入：** `/ux-design shop-ui`

**预期行为：**
1. 骨架文件创建 `design/ux/shop-ui.md`
2. 编写"用户流程"章节时，Skill 检测到关联 GDD 不存在
3. 编排者注明缺口："⚠ 依赖缺失：`design/gdd/shop-ui.md` 未找到。相关章节将使用占位符。"
4. Skill 不因此停止——在缺口处添加占位符：
   `[待补充：商店 UI GDD 中的用户流程待确认]`
5. 继续完成其他章节
6. 会话末尾列出所有依赖缺口
7. 裁决：COMPLETE（注明有未解决的依赖缺口）

**断言：**
- [ ] 依赖缺失时不停止流程
- [ ] 缺口处添加占位符（含说明性文字）
- [ ] 编排者注明所有依赖缺口
- [ ] Skill 继续完成剩余章节
- [ ] 裁决为 COMPLETE（含缺口注明）

---

### 用例 4：无参数——使用说明报错

**输入：** `/ux-design`（无参数）

**预期行为：**
1. Skill 检测到缺少界面名称参数
2. 不进入 UX 设计流程
3. 输出使用说明报错：
   ```
   用法：/ux-design [界面名]

   示例：
     /ux-design hud-main
     /ux-design inventory-screen
     /ux-design pause-menu

   [界面名] 是必需参数。
   ```
4. 裁决：BLOCKED（缺少参数）

**断言：**
- [ ] 无参数时不进入 UX 设计流程
- [ ] 使用说明报错含示例
- [ ] 裁决为 BLOCKED

---

### 用例 5：门控检查——无门控派生，裁决 COMPLETE

**测试夹具：**
- 完整模式：`production/session-state/review-mode.txt` 为 `full`

**输入：** `/ux-design settings-menu`

**预期行为：**
1. 骨架文件创建
2. 逐节引导完成所有 4 个章节
3. 全程无任何导演 agent 派生
4. 无门控跳过消息（因为此 Skill 设计为无导演门控）
5. 裁决：COMPLETE
6. 下一步：`/ux-review settings-menu`（这是 UX 审查 Skill，而非内联门控）

**断言：**
- [ ] 完整模式下不派生任何导演 agent
- [ ] 无门控跳过消息
- [ ] 裁决为 COMPLETE
- [ ] 末尾引用 `/ux-review`（独立 Skill）而非内联门控

---

## 协议合规性

- [ ] 骨架文件在任何章节内容讨论之前创建
- [ ] 逐节讨论和起草，每节一次
- [ ] 每节起草后询问"May I write section [N]?"
- [ ] 发现现有规格时提供改造路径
- [ ] 末尾交接至 `/ux-review`
- [ ] 裁决为 COMPLETE（所有章节写入后）

---

## 覆盖率说明

- 交互状态枚举（正常/悬停/聚焦/禁用/错误）由 `/ux-review` 独立验证——
  本 Skill 负责引导编写，`/ux-review` 负责验证完整性。
- 线框描述为纯文字格式——不包含图像或视觉资源。
- 响应式布局说明为可选内容——未在此 spec 中独立测试。
