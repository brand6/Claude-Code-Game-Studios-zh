# Agent 测试规格：ue-umg-specialist

## Agent 概述
- **职责领域**：UMG Widget 层级结构、数据绑定、CommonUI 输入路由与 Action Tag、WidgetStyle 资源、Widget 池化 / ListView / 无效化（Invalidation）
- **不负责**：UX 流程设计（ux-designer）、Gameplay 逻辑（gameplay-programmer）、后端数据源设计（systems-designer 或 gameplay-programmer）
- **模型层级**：Sonnet
- **关卡 ID**：无；跨领域裁决委托给 unreal-specialist 或 lead-programmer

---

## 静态断言（结构检查）

- [ ] `description:` 字段存在且领域明确（引用 UMG、CommonUI、Widget 层级结构、数据绑定）
- [ ] `allowed-tools:` 列表与 Agent 角色匹配（Read、Write、Edit；无服务器或部署工具）
- [ ] 模型层级为 Sonnet（专员的默认层级）
- [ ] Agent 定义未主张对 UX 流程设计或 Gameplay 逻辑拥有权

---

## 测试用例

### 用例 1：领域内请求——背包格子 UI（含数据绑定）
**输入**："用 UMG 实现一个背包格子 UI，当物品数据更新时格子内容能够实时刷新。"
**预期行为**：
- 使用 `UListView` 或 `UTileView`（而非手动创建 Grid Panel 内的 Widget）并绑定 `UObject` 数据源
- 产出实现 `IUserObjectListEntry` 接口的 `WBP_InventorySlot` Widget Blueprint 结构
- 通过数据变更事件驱动绑定（`OnListItemObjectSet`，而非 Tick 轮询）
- 描述 Widget 生命周期：`NativeOnListItemObjectSet` 和 `NativeOnEntryReleased`
- 不将手动循环构建的网格 Widget 组合作为大型列表的推荐方案

### 用例 2：领域外——UX 流程重定向
**输入**："设计玩家在背包中拾取、装备和丢弃物品的完整交互流程。"
**预期行为**：
- 不产出 UX 流程设计内容
- 明确声明："交互流程设计属于 ux-designer 的职责范围"
- 将请求重定向给 ux-designer
- 注明它将实现 ux-designer 规格中定义的任何 Widget 交互逻辑

### 用例 3：领域边界——CommonUI 输入 Action Tag 不匹配
**输入**："我们在控制器模式下按 B 键（返回按钮）时，CommonUI 没有正确处理焦点。"
**预期行为**：
- 诊断为 CommonUI `InputAction` 标签配置问题
- 检查 `UI.Action.Back`（或项目自定义 tag）是否已在 CommonUI 输入映射配置中正确绑定
- 解释 CommonUI 的输入路由层级：激活 Widget 堆栈通过 Action Tag 消费输入，而非直接监听按键
- 提供诊断步骤：检查 Widget 的 `bIsFocusable` 标志、`CommonActivatableWidget` 基类，以及 Action Tag 绑定
- 不在未提供 CommonUI 输入系统解释的情况下直接给出原始键绑定修复方案

### 用例 4：性能——大量 Widget 实例化
**输入**："排行榜界面实例化了 500 个 `WBP_LeaderboardRow` Widget，导致 UI 明显卡顿。"
**预期行为**：
- 将 500 个静态 Widget 实例识别为性能问题（内存高、实例化耗时长）
- 推荐 `UListView` 虚拟化方案：只实例化可见 Widget，滚动时复用
- 提供迁移建议：将数据源转换为 `UObject` 列表，并使 Row Widget 实现 `IUserObjectListEntry`
- 注明若存在加载延迟应使用 `UListView` 的异步填充模式
- 不在未提及性能影响的情况下建议保留 500 个静态 Widget

### 用例 5：上下文传递——项目 CommonUI Action Tag 体系
**输入上下文**：项目使用如下 CommonUI InputAction 标签：`UI.Action.Confirm`、`UI.Action.Back`、`UI.Action.Pause`、`UI.Action.Secondary`。
**输入**："在背包界面实现一个 '比较物品' 的辅助操作——按下游戏手柄 X 键触发。"
**预期行为**：
- 使用已有的 `UI.Action.Secondary` tag 将辅助操作映射到手柄 X 键
- 不创建新的 InputAction tag（除非已有的 tag 均不合适，且须明确说明原因）
- 产出用于监听 `UI.Action.Secondary` 的 CommonActivatableWidget Blueprint 逻辑
- 注明 CommonUI 的 InputAction 绑定使用 WidgetStyleSheet 或 Project Input Config，而非直接绑定物理按键

---

## 协议合规性

- [ ] 保持在声明的职责范围内（UMG、CommonUI、Widget 层级结构、数据绑定、性能）
- [ ] 将 UX 流程设计请求重定向给 ux-designer
- [ ] 返回结构化 UMG 实现方案（Widget 层级结构、绑定接口、ListView 模式）
- [ ] 优先使用 ListView 虚拟化，而非为大型数据集创建静态 Widget
- [ ] 在使用 Action Tag 时引用项目已有的 CommonUI tag 体系，而非新增冗余 tag

---

## 覆盖说明
- 用例 4（Widget 性能）是最常见的 UMG 失效模式；建议定期测试
- 用例 5 验证 Agent 能够将项目上下文（已有 Action Tag）应用于实现决策
- 无自动化运行器；手动审查或通过 `/skill-test` 进行
