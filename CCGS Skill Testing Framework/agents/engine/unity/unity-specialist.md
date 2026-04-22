# Agent 测试规格：unity-specialist

## Agent 概述
职责领域：Unity 专属架构模式、MonoBehaviour vs DOTS 技术选型，以及子系统选择（Addressables、新输入系统、UI Toolkit、Cinemachine 等）。
不负责：特定语言的深度实现（委托给 unity-dots-specialist、unity-ui-specialist 等）。
模型层级：Sonnet（默认）。
未分配关卡 ID。

---

## 静态断言（结构检查）

- [ ] `description:` 字段存在且领域明确（引用 Unity 模式 / MonoBehaviour / 子系统决策）
- [ ] `allowed-tools:` 列表包含 Read、Write、Edit、Bash、Glob、Grep
- [ ] 模型层级为 Sonnet（专员的默认层级）
- [ ] Agent 定义包含子专员路由表（DOTS、UI、Shader、Addressables）

---

## 测试用例

### 用例 1：领域内请求——合适的输出
**输入**："存储敌人配置数据应使用 MonoBehaviour 还是 ScriptableObject？"
**预期行为**：
- 产出涵盖以下内容的模式决策树：
  - MonoBehaviour：用于运行时行为，需附加到 GameObject，具有 Update() 生命周期
  - ScriptableObject：用于纯数据/配置，以资源文件形式存在，可跨实例共享，无场景依赖
- 推荐为敌人配置数据使用 ScriptableObject（无状态、可复用、对设计师友好）
- 注明 MonoBehaviour 可在运行时引用 ScriptableObject
- 提供 ScriptableObject 类定义的具体示例（不产出完整代码——将实现引用给 engine-programmer 或 gameplay-programmer）

### 用例 2：错误引擎重定向
**输入**："为这个敌人系统建立带信号的 Node 场景树。"
**预期行为**：
- 不产出 Godot Node/signal 代码
- 识别为 Godot 模式
- 说明 Unity 中的等价方案是 GameObject 层级结构 + UnityEvent 或 C# 事件
- 进行概念映射：Godot Node → Unity MonoBehaviour，Godot Signal → C# event / UnityEvent
- 在继续之前确认项目基于 Unity

### 用例 3：Unity 版本 API 标记
**输入**："使用 Unity 6 的新 GPU Resident Drawer 进行批量渲染。"
**预期行为**：
- 识别 Unity 6 功能（GPU Resident Drawer）
- 标记该 API 在早期 Unity 版本中可能不可用
- 在提供实现指导前询问或检查项目的 Unity 版本
- 指引参照官方 Unity 6 文档进行验证
- 不在未经确认的情况下假设项目使用 Unity 6

### 用例 4：DOTS vs MonoBehaviour 冲突
**输入**："战斗系统使用 MonoBehaviour 管理状态，但我们想添加基于 DOTS 的投射物系统，两者可以共存吗？"
**预期行为**：
- 识别为混合架构场景
- 说明混合方案：MonoBehaviour 可通过 SystemAPI、IComponentData 和托管组件与 DOTS 交互
- 注明混合两种模式的性能与复杂度权衡
- 建议将架构决策上报给 `lead-programmer` 或 `technical-director`
- 将 DOTS 侧的实现细节委托给 `unity-dots-specialist`

### 用例 5：上下文传递——Unity 版本
**输入**：提供项目上下文：Unity 2023.3 LTS。请求："为本项目配置新输入系统。"
**预期行为**：
- 应用 Unity 2023.3 LTS 上下文：使用新输入系统包（com.unity.inputsystem）
- 不产出旧版 Input Manager 代码（`Input.GetKeyDown()`、`Input.GetAxis()`）
- 注明任何 2023.3 特定的输入系统行为或包版本约束
- 引用项目版本以确认 Burst/Jobs 兼容性（如果输入系统与 DOTS 存在交互）

---

## 协议合规性

- [ ] 保持在声明的职责范围内（Unity 架构决策、模式选择、子系统路由）
- [ ] 将 Godot 模式重定向给相应 Godot 专员，或标记为错误引擎
- [ ] 将 DOTS 实现重定向给 unity-dots-specialist
- [ ] 将 UI 实现重定向给 unity-ui-specialist
- [ ] 标记 Unity 版本限定的 API，并在推荐之前要求版本确认
- [ ] 返回结构化的模式决策指南，而非随意表达的意见

---

## 覆盖说明
- MonoBehaviour vs ScriptableObject（用例 1）若导致项目级决策，应记录为 ADR
- 版本标记（用例 3）确认 Agent 不会在没有上下文的情况下假设最新 Unity 版本
- DOTS 混合（用例 4）验证 Agent 会上报架构冲突，而非单方面解决
