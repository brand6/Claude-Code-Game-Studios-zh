# Skill Test Spec: /ux-review

## Skill 概述

只读 UX 规格验证。
检查项：4 个必需章节、5 种交互状态（正常/悬停/聚焦/禁用/错误）、无障碍合规性、美术圣经一致性。
无导演门控，不写入任何文件。
裁决：APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需 Fixture。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 明确检查 4 个必需章节：用户流程、交互状态、线框描述、无障碍说明
- [ ] 明确检查 5 种交互状态：正常、悬停、聚焦、禁用、错误
- [ ] 明确检查无障碍覆盖（键盘导航、对比度、屏幕阅读器）
- [ ] 不写入任何文件（只读模式）
- [ ] 无导演门控（`/ux-review` 本身就是审查 Skill）
- [ ] 裁决关键字：APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED
- [ ] 非 APPROVED 时提供具体可操作的改进建议
- [ ] 末尾包含下一步交接：修订回 `/ux-design` 或继续推进实现

---

## 导演门控检查

无。`/ux-review` 本身就是 UX 规格的审查门控。该 Skill 内部不调用任何额外的导演门控。

---

## 测试用例

### 用例 1：正常路径——APPROVED，所有章节和状态完整

**测试夹具：**
- `design/ux/hud-main.md` 存在，包含：
  - ✅ 用户流程（完整）
  - ✅ 交互状态（5 种状态均定义：正常/悬停/聚焦/禁用/错误）
  - ✅ 线框描述（完整）
  - ✅ 无障碍说明（含键盘导航、WCAG AA 对比度比值、屏幕阅读器标签）

**输入：** `/ux-review hud-main`

**预期行为：**
1. 读取 `design/ux/hud-main.md`
2. 检查所有 4 个必需章节：均存在 ✅
3. 检查交互状态：5 种状态均已定义 ✅
4. 检查无障碍覆盖：键盘导航、对比度比值、屏幕阅读器支持均已描述 ✅
5. 检查美术圣经一致性：视觉规格与 `design/art-bible.md` 一致 ✅
6. 裁决：APPROVED
7. 下一步：继续推进 `/dev-story` 或 UI 实现

**断言：**
- [ ] 所有 4 个章节均检查
- [ ] 所有 5 种交互状态均检查
- [ ] 无障碍覆盖经过检查（键盘/对比度/屏幕阅读器）
- [ ] 裁决为 APPROVED
- [ ] 不写入任何文件

---

### 用例 2：缺少无障碍章节——NEEDS REVISION

**测试夹具：**
- `design/ux/inventory-screen.md` 存在，但：
  - ✅ 用户流程（完整）
  - ✅ 交互状态（5 种状态）
  - ✅ 线框描述（完整）
  - ❌ 无障碍说明章节缺失（完全空白）

**输入：** `/ux-review inventory-screen`

**预期行为：**
1. 读取 `design/ux/inventory-screen.md`
2. 检查章节：3 个章节完整，1 个缺失
3. 裁决：NEEDS REVISION
4. 具体、可操作的反馈：
   ```
   NEEDS REVISION
   
   缺失内容：
   - 无障碍说明章节为空。请添加：
     * 键盘导航说明（Tab 顺序、快捷键）
     * WCAG AA 对比度比值
     * 屏幕阅读器标签和 ARIA 属性
   
   建议：运行 /ux-design inventory-screen 补充无障碍章节后重新提交审查。
   ```
5. 不写入任何文件
6. 裁决：NEEDS REVISION

**断言：**
- [ ] 缺失章节准确识别（无障碍说明）
- [ ] 反馈具体且可操作（列出所需内容）
- [ ] 裁决为 NEEDS REVISION
- [ ] 不写入任何文件
- [ ] 下一步指向 `/ux-design` 进行修订

---

### 用例 3：交互状态不完整（缺少"禁用"状态）——NEEDS REVISION

**测试夹具：**
- `design/ux/settings-menu.md` 存在，交互状态章节仅定义 4 种状态：正常、悬停、聚焦、错误
- 缺少"禁用"状态定义

**输入：** `/ux-review settings-menu`

**预期行为：**
1. 读取 `design/ux/settings-menu.md`
2. 检查 4 个章节：均存在 ✅
3. 检查交互状态：发现缺少"禁用"状态 ❌
4. 裁决：NEEDS REVISION
5. 具体反馈：
   ```
   NEEDS REVISION
   
   交互状态不完整：
   - 缺少"禁用"状态定义。
   - 当前已定义：正常、悬停、聚焦、错误
   - 缺失状态：禁用（Disabled）
   
   请在交互状态章节中补充"禁用"状态的视觉和行为定义。
   ```
6. 不写入任何文件

**断言：**
- [ ] 识别出缺少"禁用"状态
- [ ] 反馈列出已有状态和缺失状态
- [ ] 裁决为 NEEDS REVISION
- [ ] 不写入任何文件

---

### 用例 4：文件不存在——提示运行 /ux-design

**输入：** `/ux-review shop-ui`（`design/ux/shop-ui.md` 不存在）

**预期行为：**
1. Skill 尝试读取 `design/ux/shop-ui.md`
2. 文件不存在
3. 输出：
   ```
   UX 规格未找到：design/ux/shop-ui.md
   
   请先运行 /ux-design shop-ui 创建 UX 规格，然后再进行审查。
   ```
4. 不执行审查，不发出裁决

**断言：**
- [ ] 文件不存在时不执行审查
- [ ] 输出包含规格文件路径
- [ ] 不发出任何裁决（APPROVED/NEEDS REVISION/MAJOR REVISION NEEDED）
- [ ] 引导用户先运行 `/ux-design shop-ui`

---

### 用例 5：门控检查——无导演门控，裁决为 APPROVED/NEEDS REVISION/MAJOR REVISION NEEDED

**测试夹具：**
- 完整模式：`production/session-state/review-mode.txt` 为 `full`
- `design/ux/pause-menu.md` 存在且完整（通过所有检查）

**输入：** `/ux-review pause-menu`

**预期行为：**
1. 读取 `design/ux/pause-menu.md`
2. 执行所有检查（章节、交互状态、无障碍、美术圣经一致性）
3. 全程无任何导演 agent 派生
4. 无门控跳过消息（因为此 Skill 设计为无导演门控——它本身就是审查）
5. 裁决：APPROVED（规格完整）

**断言：**
- [ ] 不派生任何导演 agent（不派生 art-director、creative-director 等）
- [ ] 无门控跳过消息
- [ ] 裁决为 APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED（由实际内容决定）
- [ ] 不写入任何文件

---

## 协议合规性

- [ ] 检查所有 4 个必需章节（用户流程、交互状态、线框描述、无障碍说明）
- [ ] 检查所有 5 种交互状态（正常、悬停、聚焦、禁用、错误）
- [ ] 检查无障碍覆盖（键盘导航、对比度、屏幕阅读器）
- [ ] 不写入任何文件（只读）
- [ ] 非 APPROVED 时提供具体可操作的改进建议
- [ ] 末尾包含下一步交接：修订回 `/ux-design` 或继续推进实现

---

## 覆盖率说明

- MAJOR REVISION NEEDED 触发条件：整个结构性章节完全缺失
  （而非仅内容不完整，后者触发 NEEDS REVISION）——未独立测试此场景。
- 美术圣经/设计系统一致性检查在 Skill 描述中提及，但未为其独立设计夹具测试——
  通过用例 1 中的"一致 ✅"隐式覆盖。
- 以不同路径命名的界面（例如重命名）不会影响审查——
  Skill 按文件路径进行审查，路径变更不纳入测试范围。
