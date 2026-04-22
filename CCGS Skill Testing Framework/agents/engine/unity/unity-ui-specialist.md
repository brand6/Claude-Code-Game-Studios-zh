# Agent 测试规格：unity-ui-specialist

## Agent 概述
职责领域：Unity UI Toolkit（UXML/USS）、UGUI（Canvas）、数据绑定、运行时 UI 性能，以及 UI 输入事件处理。
不负责：UX 流程设计（ux-designer）、视觉美术风格（art-director）。
模型层级：Sonnet（默认）。
未分配关卡 ID。

---

## 静态断言（结构检查）

- [ ] `description:` 字段存在且领域明确（引用 UI Toolkit / UGUI / Canvas / 数据绑定）
- [ ] `allowed-tools:` 列表包含 Read、Write、Edit、Bash、Glob、Grep
- [ ] 模型层级为 Sonnet（专员的默认层级）
- [ ] Agent 定义未主张对 UX 流程设计或视觉美术方向拥有权

---

## 测试用例

### 用例 1：领域内请求——合适的输出
**输入**："使用 Unity UI Toolkit 实现一个背包 UI 界面。"
**预期行为**：
- 产出定义背包面板结构的 UXML 文档（ListView、物品模板、详情面板）
- 产出背包布局和物品状态的 USS 样式（默认、悬停、已选中）
- 提供通过 `INotifyValueChanged` 或 `IBindable` 将背包数据模型绑定到 UI 的 C# 代码
- 为可滚动物品列表使用带 `makeItem` / `bindItem` 回调的 `ListView`
- 不产出 UX 流程设计——基于提供的规格进行实现

### 用例 2：领域外重定向
**输入**："设计背包的 UX 流程——玩家装备物品与丢弃物品时应发生什么。"
**预期行为**：
- 不产出 UX 流程设计
- 明确声明交互流程设计属于 `ux-designer` 的职责范围
- 将请求重定向给 `ux-designer`
- 注明它将实现 ux-designer 指定的任何流程

### 用例 3：动态列表的 UI Toolkit 数据绑定
**输入**："当玩家背包中的物品被添加或移除时，背包列表需要实时更新。"
**预期行为**：
- 产出带绑定 `ObservableList<T>` 或事件驱动刷新方案的 `ListView` 模式
- 在数据集合变更事件上使用 `ListView.Rebuild()` 或 `ListView.RefreshItems()`
- 注明大型列表的性能考量（通过 `makeItem`/`bindItem` 模式实现虚拟化）
- 不将 `QuerySelector` 循环用于更新单个元素的列表刷新策略——将此标记为性能反模式

### 用例 4：Canvas 性能——过度绘制
**输入**："主菜单 Canvas 触发了 GPU 过度绘制警告，存在大量重叠面板。"
**预期行为**：
- 识别过度绘制原因：多层堆叠的 Canvas、在不活跃时未被剔除的全屏遮罩面板
- 推荐方案：
  - 为世界空间、屏幕空间覆盖层和屏幕空间摄像机层分别设置独立 Canvas
  - 停用/禁用面板而非将透明度设为 0（alpha 为 0 的不可见面板仍会绘制）
  - 渐变效果使用 Canvas Group + alpha，而非单独修改 Image alpha
- 若项目处于迁移阶段，注明 UI Toolkit 替代方案

### 用例 5：上下文传递——Unity 版本
**输入**：项目上下文：Unity 2022.3 LTS。请求："用数据绑定实现设置面板。"
**预期行为**：
- 使用 2022.3 LTS 版本的 UI Toolkit 运行时绑定系统
- 注明 Unity 2022.3 引入了运行时数据绑定（相对于早期版本的仅编辑器绑定）
- 不使用 Unity 6 增强绑定 API 功能（若在 2022.3 中不可用）
- 产出与所述 Unity 版本兼容的代码，并附有版本专属 API 说明

---

## 协议合规性

- [ ] 保持在声明的职责范围内（UI Toolkit、UGUI、数据绑定、UI 性能）
- [ ] 将 UX 流程设计重定向给 ux-designer
- [ ] 返回结构化输出（UXML、USS、C# 绑定代码）
- [ ] 为项目的 Unity 版本使用正确的 Unity UI 框架版本
- [ ] 将 Canvas 过度绘制标记为性能反模式，并提供具体修复方案
- [ ] 不使用 alpha-0 作为显示/隐藏模式——使用 SetActive() 或 VisualElement.style.display

---

## 覆盖说明
- 背包 UI（用例 1）应在 `production/qa/evidence/` 中有手动演练文档
- 动态列表绑定（用例 3）应有集成测试或自动化交互测试
- Canvas 过度绘制（用例 4）验证 Agent 了解正确的 Unity UI 性能模式
