# Agent 测试规格：godot-specialist

## Agent 概述
职责领域：Godot 专属模式、节点/场景架构、信号、资源，以及 GDScript vs C# vs GDExtension 技术选型。
不负责：特定语言的代码编写（委托给各语言子专员）。
模型层级：Sonnet（默认）。
未分配关卡 ID。

---

## 静态断言（结构检查）

- [ ] `description:` 字段存在且领域明确（引用 Godot 架构 / 节点模式 / 引擎决策）
- [ ] `allowed-tools:` 列表包含 Read、Write、Edit、Bash、Glob、Grep
- [ ] 模型层级为 Sonnet（专员的默认层级）
- [ ] Agent 定义将 `docs/engine-reference/godot/VERSION.md` 列为权威 API 来源

---

## 测试用例

### 用例 1：领域内请求——合适的输出
**输入**："Godot 中何时应用信号（signal），何时应直接调用方法？"
**预期行为**：
- 产出包含决策依据的模式指南：
  - 信号：解耦通信、父节点无需了解子节点、事件驱动的 UI 更新、一对多通知
  - 直接调用：调用方需要返回值的紧耦合系统，或性能敏感的热路径
- 在项目具体情境中提供各模式的代码示例
- 不会为两种模式直接生成原始代码——将实现工作引用给 gdscript-specialist 或 csharp-specialist
- 注明"禁止向上信号"约定（子节点不直接调用父节点方法——改用信号）

### 用例 2：错误引擎重定向
**输入**："写一个 MonoBehaviour，在 Start() 中运行并订阅 UnityEvent。"
**预期行为**：
- 不产出 Unity MonoBehaviour 代码
- 明确指出这是 Unity 模式而非 Godot 模式
- 提供 Godot 等价方案：使用 `_ready()` 代替 `Start()`，用 Godot 信号代替 UnityEvent
- 确认项目基于 Godot 并进行概念映射重定向

### 用例 3：后截止 API 风险
**输入**："使用 Godot 4.5 新增的 @abstract 注解定义一个抽象基类。"
**预期行为**：
- 识别 `@abstract` 为后截止功能（Godot 4.5 引入，晚于 LLM 知识截止日）
- 标记版本风险：LLM 对此注解的了解可能不完整或有误
- 引导用户参照 `docs/engine-reference/godot/VERSION.md` 及官方 4.5 迁移指南进行验证
- 基于版本参考文件中的迁移说明提供尽力而为的指导，同时明确标注"未验证"

### 用例 4：热路径语言选型
**输入**："物理查询循环每帧处理 500 个对象，应使用 GDScript 还是 C#？"
**预期行为**：
- 提供平衡的分析：
  - GDScript：更简单、团队熟悉，但紧循环下速度较慢
  - C#：CPU 密集循环下更快，需要 .NET 运行时，团队需具备 C# 知识
- 不单方面做出最终决策
- 将分析结果提交给 `lead-programmer` 作为决策输入
- 注明 GDExtension（C++）是极端性能需求下的第三选项，并建议 C# 不足时上报评估

### 用例 5：上下文传递——引擎版本 4.6
**输入**：提供引擎版本上下文：Godot 4.6，Jolt 为默认物理引擎。请求："为玩家角色配置 RigidBody3D。"
**预期行为**：
- 读取 4.6 上下文并应用 Jolt 默认知识（来自 VERSION.md 迁移说明）
- 推荐与 Jolt 兼容的 RigidBody3D 配置（如注明在 Jolt 下行为不同的 GodotPhysics 专属设置）
- 引用 4.6 迁移说明中关于 Jolt 成为默认引擎的内容，而非依赖 LLM 训练数据
- 标记在 GodotPhysics 和 Jolt 之间行为发生变化的 RigidBody3D 属性

---

## 协议合规性

- [ ] 保持在声明的职责范围内（Godot 架构决策、节点/场景模式、语言选型）
- [ ] 将语言专属实现重定向给 godot-gdscript-specialist 或 godot-csharp-specialist
- [ ] 返回结构化结果（决策树、含依据的模式推荐）
- [ ] 以 `docs/engine-reference/godot/VERSION.md` 为权威来源，优先于 LLM 训练数据
- [ ] 标记后截止 API 用法（4.4、4.5、4.6）并要求验证
- [ ] 存在权衡时，将语言选型决策委托给 lead-programmer

---

## 覆盖说明
- 信号 vs 直接调用指南（用例 1）应写入 `docs/architecture/`，作为可复用的模式文档
