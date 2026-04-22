# Skill Test Spec: /quick-design

## Skill 概述

轻量级 3 节设计规格（概述、规则、验收标准），用于设计时间小于 4 小时的功能。
无导演门控。
输出：`design/quick-notes/[name].md`。
裁决：CREATED / BLOCKED / REDIRECTED。
范围检查：若功能过大，重定向至 `/design-system`。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需 Fixture。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 格式为 3 节（概述、规则、验收标准）——不使用 8 节 GDD 格式
- [ ] 无导演门控（不读取 review-mode.txt，不派生任何 CD-/TD-/PR-/AD- 前缀 agent）
- [ ] 写入前询问"May I write `design/quick-notes/[name].md`?"
- [ ] 裁决关键字：CREATED / BLOCKED / REDIRECTED
- [ ] 支持重定向至 `/design-system`

---

## 导演门控检查

无导演门控——该 Skill 不派生任何导演门控代理。Quick Design 的轻量级设计意味着导演门控开销是刻意省略的。单系统、4 小时以内的功能不需要完整的 GDD 审查。

---

## 测试用例

### 用例 1：正常路径——小型 UI 调整

**测试夹具：**
- 无现有文件 `design/quick-notes/ammo-counter-display.md`

**输入：** `/quick-design ammo-counter-display`

**预期行为：**
1. Skill 进行范围判断：弹药计数器 UI 调整——单系统，预估设计时间 < 4 小时
2. 范围通过，继续起草
3. 起草 3 节草稿：
   - **概述：** 在 HUD 右下角显示弹药计数器，格式为"当前/最大"
   - **规则：** 弹药为 0 时显示为红色；倒数第 5 发时闪烁；换弹时显示"装弹中..."
   - **验收标准：** 弹药正确显示；颜色状态按规则变化；动画帧率达标
4. 向用户展示完整草稿
5. 询问"May I write `design/quick-notes/ammo-counter-display.md`?"
6. 用户批准后写入文件
7. 裁决：CREATED
8. 下一步建议：继续推进实现或创建关联 Story

**断言：**
- [ ] 范围检查在起草之前运行
- [ ] 使用 3 节格式（概述/规则/验收标准）
- [ ] 询问"May I write"之前展示完整草稿
- [ ] 裁决为 CREATED
- [ ] 输出路径为 `design/quick-notes/ammo-counter-display.md`

---

### 用例 2：范围超阈值——重定向至 /design-system

**测试夹具：**
- 用户请求设计"完整制作系统，含配方、材料等级、合成站、质量随机性"

**输入：** `/quick-design crafting-system`

**预期行为：**
1. Skill 进行范围判断：完整制作系统——多子系统、配方管理、UI 流程、数据设计，预估 > 4 小时
2. 范围超阈值
3. 不起草 Quick Design
4. 输出：
   ```
   REDIRECTED → /design-system
   
   此功能的设计规模超出 Quick Design 范围（预估 > 4 小时设计时间）。
   建议使用 /design-system crafting 创建完整 GDD。
   ```
5. 裁决：REDIRECTED
6. 明确指向 `/design-system crafting`

**断言：**
- [ ] 范围检查在起草之前运行
- [ ] 超阈值时不起草任何内容
- [ ] 裁决为 REDIRECTED
- [ ] 输出明确指向 `/design-system`（含系统名参数）
- [ ] 不询问"May I write"

---

### 用例 3：文件已存在——更新还是新建

**测试夹具：**
- `design/quick-notes/crosshair-style.md` 已存在

**输入：** `/quick-design crosshair-style`

**预期行为：**
1. Skill 检测到 `design/quick-notes/crosshair-style.md` 已存在
2. 读取现有文件内容
3. `AskUserQuestion` 提供：
   - **更新现有文件：** 修改现有规格的特定部分
   - **创建新版本：** 覆盖整个文件（`crosshair-style.md`）
4. 根据用户选择继续处理
5. 最终裁决：CREATED（无论是更新还是重写）

**断言：**
- [ ] 检测到现有文件不被静默覆盖
- [ ] `AskUserQuestion` 提供更新或新建的选项
- [ ] 用户选择后继续处理

---

### 用例 4：无参数——使用说明报错

**输入：** `/quick-design`（无参数）

**预期行为：**
1. Skill 检测到缺少功能名称参数
2. 不进入设计流程
3. 输出使用说明报错：
   ```
   用法：/quick-design [功能名]
   
   示例：
     /quick-design ammo-counter-display
     /quick-design crosshair-style
     /quick-design pause-menu-button
   
   [功能名] 是必需参数。
   ```
4. 裁决：BLOCKED（缺少参数）

**断言：**
- [ ] 无参数时不进入设计流程
- [ ] 使用说明报错含示例
- [ ] 裁决为 BLOCKED

---

### 用例 5：门控检查——完整模式下不派生任何门控

**测试夹具：**
- 完整模式：`production/session-state/review-mode.txt` 为 `full`

**输入：** `/quick-design sprint-button`

**预期行为：**
1. Skill 读取范围（小型功能，通过）
2. 起草 3 节规格
3. 展示草稿给用户
4. 询问"May I write `design/quick-notes/sprint-button.md`?"
5. 写入文件
6. 裁决：CREATED
7. **全程无任何门控派生**，无 creative-director、technical-director、producer、art-director 调用

**断言：**
- [ ] 不读取 review-mode.txt（或读取但忽略门控逻辑）
- [ ] 不派生任何带 CD-/TD-/PR-/AD- 前缀的 agent
- [ ] 完整模式下裁决仍为 CREATED（无门控）
- [ ] 无门控跳过消息（因为此 Skill 设计为无门控）

---

## 协议合规性

- [ ] 范围检查在起草之前运行（超阈值则重定向到 `/design-system`）
- [ ] 使用 3 节格式（概述、规则、验收标准）——不使用 8 节 GDD 格式
- [ ] 向用户展示完整草稿后，再询问"May I write `design/quick-notes/[name].md`?"
- [ ] 询问"May I write"之前先展示草稿
- [ ] 无导演门控——不读取 review-mode.txt，不派生任何 CD-/TD-/PR-/AD- 前缀 agent
- [ ] 末尾包含下一步交接（例如：继续推进实现或 `/dev-story`）

---

## 覆盖率说明

- 范围阈值启发式（单系统、< 4 小时设计时间）是判断性判断——
  没有精确的机器可验证测试，依赖 agent 的合理判断。
- `design/quick-notes/` 目录不存在时自动创建——未独立测试此行为。
- 与 Story 流程的集成（Quick Design 嵌入 Story 文件）不在本 Skill spec 测试范围内。
