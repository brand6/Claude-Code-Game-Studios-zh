---
name: ux-review
description: "验证 UX 规格、HUD 设计或交互模式库的完整性、无障碍合规性、GDD 对齐情况及实施就绪状态。生成 APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED 结论，附具体缺口说明。"
argument-hint: "[文件路径 或 'all' 或 'hud' 或 'patterns']"
user-invocable: true
allowed-tools: Read, Glob, Grep
agent: ux-designer
---

## 概述

在 UX 设计文档进入实施流水线之前对其进行验证。
在 `/team-ui` 流水线的 UX 设计与视觉设计/实施之间充当质量门控。

**运行本技能的时机：**
- 用 `/ux-design` 完成 UX 规格后
- 交付给 `ui-programmer` 或 `art-director` 之前
- 预生产到生产门控检查之前（要求关键屏幕有已审阅的 UX 规格）
- 对 UX 规格进行重大修订后

**结论等级：**
- **APPROVED** — 规格完整、一致，可实施
- **NEEDS REVISION** — 发现具体缺口；在交付前修复，但不需要完全重新设计
- **MAJOR REVISION NEEDED** — 范围、玩家需求或完整性存在根本性问题；需要大量返工

---

## 第 1 阶段：解析参数

- **具体文件路径**（如 `/ux-review design/ux/inventory.md`）：验证该文档
- **`all`**：找到 `design/ux/` 中的所有文件并逐一验证
- **`hud`**：专门验证 `design/ux/hud.md`
- **`patterns`**：专门验证 `design/ux/interaction-patterns.md`
- **无参数**：询问用户要验证哪个规格

对于 `all`，先输出摘要表（文件 | 结论 | 主要问题），然后逐个提供详细信息。

---

## 第 2 阶段：加载交叉参考上下文

在验证任何规格之前，加载：

1. **输入与平台配置**：读取 `.claude/docs/technical-preferences.md` 并
   提取 `## Input & Platform`。这是游戏支持哪些输入方式的权威来源——
   用它驱动第 3A 阶段的输入方式覆盖检查，而不是规格自己的标题。
   若未配置，则退回到规格标题。
2. `design/accessibility-requirements.md` 中承诺的无障碍等级（若存在）
3. `design/ux/interaction-patterns.md` 中的交互模式库（若存在）
4. 规格标题中引用的 GDD（读取它们的 UI 需求部分）
5. `design/player-journey.md` 中的玩家旅程地图（若存在）用于情境到达验证

---

## 第 3A 阶段：UX 规格验证清单

对基于 `ux-spec.md` 的文档运行所有检查。

### 完整性（必需部分）

- [ ] 文档标题包含 Status、Author、Platform Target
- [ ] 目的与玩家需求——有玩家视角的需求声明（非开发者视角）
- [ ] 到达时的玩家情境——描述玩家状态和先前活动
- [ ] 导航位置——显示屏幕在层级中的位置
- [ ] 入口与出口——所有入口来源和出口目标已记录
- [ ] 布局规格——区域已定义，组件清单表格已存在
- [ ] 状态与变体——至少记录了加载、空/已填充和错误状态
- [ ] 交互地图——覆盖所有目标输入方式（检查标题中的平台目标）
- [ ] 数据需求——每个显示的数据元素均有来源系统和所有者
- [ ] 触发的事件——每个玩家操作均有对应事件或空解释
- [ ] 过渡与动画——至少指定了进入/退出过渡
- [ ] 无障碍需求——屏幕级需求已存在
- [ ] 本地化注意事项——文字元素的最大字符数
- [ ] 验收标准——至少 5 条具体可测试的标准

### 质量检查

**玩家需求清晰度**
- [ ] 目的从玩家视角撰写，而非系统/开发者视角
- [ ] 玩家到达时的目标明确（"玩家到达时想要 ___"）
- [ ] 玩家到达时的情境具体（不只是"他们打开了背包"）

**状态完整性**
- [ ] 错误状态已记录（不只有理想路径）
- [ ] 空状态已记录（无数据场景）
- [ ] 若屏幕获取异步数据，加载状态已记录
- [ ] 有计时器或自动关闭的状态已记录持续时间

**输入方式覆盖**
- [ ] 若平台包含 PC：纯键盘导航已完整指定
- [ ] 若平台包含主机/手柄：方向键导航和面键映射已记录
- [ ] 手柄上没有需要鼠标精度的交互
- [ ] 焦点顺序已定义（键盘的 Tab 顺序，手柄的方向键顺序）

**数据架构**
- [ ] 没有数据元素将"UI"列为所有者（UI 不能拥有游戏状态）
- [ ] 所有实时数据均指定了更新频率（不只是"实时"——什么触发更新？）
- [ ] 所有数据元素均指定了空处理（数据不可用时显示什么？）

**无障碍**
- [ ] `accessibility-requirements.md` 中承诺的无障碍等级已满足或超出
- [ ] 若为 Basic 等级：没有仅通过颜色传递的信息指示器
- [ ] 若为 Standard 等级以上：焦点顺序已记录，文字对比度已指定
- [ ] 若为 Comprehensive 等级以上：关键状态变化的屏幕阅读器通知
- [ ] 色盲检查：任何颜色编码的元素均有非颜色的替代方案

**GDD 对齐**
- [ ] 标题中引用的每条 GDD UI 需求均在本规格中得到体现
- [ ] 没有 UI 元素在没有对应 GDD 需求的情况下显示或修改游戏状态
- [ ] 本规格中没有遗漏的 GDD UI 需求（与引用的 GDD 部分交叉核查）

**模式库一致性**
- [ ] 所有交互组件引用了模式库（或注明为新模式）
- [ ] 没有模式行为在模式库中已存在的情况下从头重新规格
- [ ] 本规格中发明的任何新模式均已标记为待添加到模式库

**本地化**
- [ ] 所有文字密集元素均存在字符数限制警告
- [ ] 所有布局关键文字均已标记为需要 40% 扩展适应

**验收标准质量**
- [ ] 标准对于未阅读设计文档的 QA 测试员来说足够具体
- [ ] 存在性能标准（屏幕打开时间）
- [ ] 存在分辨率标准
- [ ] 没有需要阅读其他文档才能评估的标准

---

## 第 3B 阶段：HUD 验证清单

对基于 `hud-design.md` 的文档运行所有检查。

### 完整性

- [ ] HUD 哲学已定义
- [ ] 信息架构表涵盖 GDD 中所有有 UI 需求的系统
- [ ] 布局区域已定义，包含所有目标平台的安全区域边距
- [ ] 每个 HUD 元素均有完整规格（区域、可见性触发器、数据来源、优先级）
- [ ] 按游戏情境的 HUD 状态至少涵盖：探索、战斗、对话/过场动画、暂停
- [ ] 视觉预算已定义（最大同时元素数、最大屏幕占比）
- [ ] 平台适应涵盖所有目标平台
- [ ] 玩家可调节元素存在调节旋钮

### 质量检查

- [ ] 没有 HUD 元素在没有可见性规则隐藏它的情况下覆盖中心游戏区域
- [ ] 所有 GDD 中存在的每条信息要么在 HUD 中，要么明确分类为"隐藏/按需"
- [ ] 所有颜色编码的 HUD 元素均有色盲变体
- [ ] 反馈与通知部分的 HUD 元素定义了队列/优先级行为
- [ ] 视觉预算合规：总同时元素在预算内

### GDD 对齐

- [ ] `design/gdd/systems-index.md` 中所有 UI 类别的系统在 HUD 中均有体现
  （或有合理的缺席说明）

---

## 第 3C 阶段：模式库验证清单

- [ ] 模式目录索引是最新的（与文档中的实际模式匹配）
- [ ] 所有标准控件模式均已指定：按钮变体、切换、滑块、下拉菜单、
  列表、网格、模态框、对话框、Toast 提示、工具提示、进度条、
  输入框、标签栏、滚动
- [ ] 当前 UX 规格所需的所有游戏特定模式均存在
- [ ] 每个模式均包含：使用时机、不使用时机、完整状态规格、无障碍规格、实施说明
- [ ] 动画标准表已存在
- [ ] 音效标准表已存在
- [ ] 模式之间没有冲突行为（例如所有导航模式中"返回"行为一致）

---

## 第 4 阶段：输出结论

```markdown
## UX Review: [Document Name]
**Date**: [date]
**Reviewer**: ux-review skill
**Document**: [file path]
**Platform Target**: [from header]
**Accessibility Tier**: [from header or accessibility-requirements.md]

### Completeness: [X/Y sections present]
- [x] Purpose & Player Need
- [ ] States & Variants — MISSING: error state not documented

### Quality Issues: [N found]
1. **[Issue title]** [BLOCKING / ADVISORY]
   - What's wrong: [specific description]
   - Where: [section name]
   - Fix: [specific action to take]

### GDD Alignment: [ALIGNED / GAPS FOUND]
- GDD [name] UI Requirements — [X/Y requirements covered]
- Missing: [list any uncovered GDD requirements]

### Accessibility: [COMPLIANT / GAPS / NON-COMPLIANT]
- Target tier: [tier]
- [list specific accessibility findings]

### Pattern Library: [CONSISTENT / INCONSISTENCIES FOUND]
- [findings]

### Verdict: APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED
**Blocking issues**: [N] — must be resolved before implementation
**Advisory issues**: [N] — recommended but not blocking

[For APPROVED]: This spec is ready for handoff to `/team-ui` Phase 2
(Visual Design).

[For NEEDS REVISION]: Address the [N] blocking issues above, then re-run
`/ux-review`.

[For MAJOR REVISION NEEDED]: The spec has fundamental gaps in [areas].
Recommend returning to `/ux-design` to rework [sections].
```

---

## 第 5 阶段：协作协议

本技能为只读——它永远不会编辑或写入文件。仅报告发现结果。

交付结论后：
- **APPROVED**：建议运行 `/team-ui` 开始实施协调
- **NEEDS REVISION**：提议帮助修复具体缺口（"需要我帮助起草缺失的错误状态吗？"）
  ——但不要自动修复；等待用户指令
- **MAJOR REVISION NEEDED**：建议返回 `/ux-design` 处理需要返工的具体部分

永远不要阻止用户继续——结论是建议性的。记录风险，呈现发现结果，
让用户决定是否在有顾虑的情况下继续。选择在 NEEDS REVISION 规格下继续的用户
承担已记录的风险。
