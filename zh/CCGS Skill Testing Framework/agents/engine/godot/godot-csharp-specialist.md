# Agent 测试规格：godot-csharp-specialist

## Agent 概述
职责领域：Godot 4 中的 C# 模式、应用于 Godot 的 .NET 惯用法、[Export] 特性用法、信号委托，以及 async/await 模式。
不负责：GDScript 代码（gdscript-specialist）、GDExtension C/C++ 绑定（gdextension-specialist）。
模型层级：Sonnet（默认）。
未分配关卡 ID。

---

## 静态断言（结构检查）

- [ ] `description:` 字段存在且领域明确（引用 Godot 4 中的 C# / .NET 模式 / 信号委托）
- [ ] `allowed-tools:` 列表包含 Read、Write、Edit、Bash、Glob、Grep
- [ ] 模型层级为 Sonnet（专员的默认层级）
- [ ] Agent 定义未主张对 GDScript 或 GDExtension 代码拥有权

---

## 测试用例

### 用例 1：领域内请求——合适的输出
**输入**："为敌人生命值创建一个带验证的导出属性，将其限制在 1 到 1000 之间。"
**预期行为**：
- 产出带有 `[Export]` 特性的 C# 属性
- 使用一个支撑字段，属性的 getter/setter 在 setter 中执行值钳制
- 不使用未经验证的原始 `[Export]` 公共字段
- 遵循 Godot 4 的 C# 命名约定（属性用 PascalCase，字段私有加下划线前缀）
- 按编码规范在属性上添加 XML 文档注释

### 用例 2：领域外请求——正确重定向
**输入**："用 GDScript 重写这个敌人生命值系统。"
**预期行为**：
- 不产出 GDScript 代码
- 明确声明 GDScript 编写属于 `godot-gdscript-specialist` 的职责范围
- 将请求重定向给 `godot-gdscript-specialist`
- 可描述 C# 接口，以便 gdscript-specialist 了解期望的 API 形状

### 用例 3：异步信号等待
**输入**："使用 C# async 等待动画播放完毕，再进行游戏状态转换。"
**预期行为**：
- 产出使用 `ToSignal()` 等待 Godot 信号的正确 `async Task` 模式
- 使用 `await ToSignal(animationPlayer, AnimationPlayer.SignalName.AnimationFinished)`
- 不使用 `Thread.Sleep()` 或 `Task.Delay()` 作为轮询替代方案
- 注明调用方法必须是 `async`，且 fire-and-forget 的 `async void` 仅适用于事件处理器
- 处理动画可能无法触发时的取消或超时情况

### 用例 4：线程模型冲突
**输入**："这段 C# 代码从后台 Task 线程访问 Godot Node 以更新其位置。"
**预期行为**：
- 标记为竞争条件风险：Godot 节点非线程安全，必须仅从主线程访问
- 不批准或实现多线程节点访问模式
- 提供正确模式：使用 `CallDeferred()`、`Callable.From().CallDeferred()`，或通过线程安全队列回到主线程
- 解释 Godot 主线程需求与 .NET 线程无关类型之间的区别

### 用例 5：上下文传递——Godot 4.6 API 正确性
**输入**：引擎版本上下文：Godot 4.6。请求："使用新的类型化信号委托模式连接信号。"
**预期行为**：
- 产出使用 Godot 4 C# 类型化委托模式的信号连接代码（信号上的 `+=` 运算符）
- 检查 4.6 上下文，确认 4.4、4.5、4.6 中信号委托 API 无破坏性变更
- 不使用旧式基于字符串的 `Connect("signal_name", callable)` 模式（Godot 4 C# 中已废弃）
- 产出与 VERSION.md 中记录的项目固定版本 4.6 兼容的代码

---

## 协议合规性

- [ ] 保持在声明的职责范围内（Godot 4 中的 C#——模式、导出、信号、异步）
- [ ] 将 GDScript 请求重定向给 godot-gdscript-specialist
- [ ] 将 GDExtension 请求重定向给 godot-gdextension-specialist
- [ ] 返回遵循 Godot 4 约定的 C# 代码（而非 Unity MonoBehaviour 模式）
- [ ] 将多线程 Godot 节点访问标记为不安全并提供正确模式
- [ ] 使用类型化信号委托——不使用已废弃的基于字符串的 Connect() 调用
- [ ] 在产出代码前检查引擎版本参考文件以确认 API 变更

---

## 覆盖说明
- 带验证的导出属性（用例 1）应有一个验证钳制行为的单元测试
- 线程冲突（用例 4）属于安全关键项：Agent 必须在代码写出前主动识别并修复
