# Agent 测试规格：godot-gdscript-specialist

## Agent 概述
职责领域：GDScript 静态类型、GDScript 设计模式、信号架构、协程/await 模式，以及 GDScript 性能优化。
不负责：着色器代码（godot-shader-specialist）、GDExtension 绑定（godot-gdextension-specialist）。
模型层级：Sonnet（默认）。
未分配关卡 ID。

---

## 静态断言（结构检查）

- [ ] `description:` 字段存在且领域明确（引用 GDScript / 静态类型 / 信号 / 协程）
- [ ] `allowed-tools:` 列表包含 Read、Write、Edit、Bash、Glob、Grep
- [ ] 模型层级为 Sonnet（专员的默认层级）
- [ ] Agent 定义未主张对着色器代码或 GDExtension 拥有权

---

## 测试用例

### 用例 1：领域内请求——合适的输出
**输入**："审查这个 GDScript 文件的类型注解覆盖率。"
**预期行为**：
- 读取提供的 GDScript 文件
- 标记每个缺少静态类型注解的变量、参数和返回类型
- 产出逐行具体发现列表：`var speed = 5.0` → `var speed: float = 5.0`
- 注明 Godot 4 中静态类型对性能和工具链的优势
- 不会在未经请求的情况下重写整个文件——产出发现列表供开发者自行应用

### 用例 2：领域外请求——正确重定向
**输入**："编写一个在世界空间中使网格变形的顶点着色器。"
**预期行为**：
- 不产出 GDScript 或 Godot 着色语言中的着色器代码
- 明确声明着色器编写属于 `godot-shader-specialist` 的职责范围
- 将请求重定向给 `godot-shader-specialist`
- 可注明：GDScript 侧（将 uniform 传递给着色器、设置着色器参数）在其职责范围内

### 用例 3：使用协程的异步加载
**输入**："异步加载一个场景，并在加载完成后再生成它。"
**预期行为**：
- 产出 Godot 4 的 `await` + `ResourceLoader.load_threaded_request` 模式
- 全程使用静态类型（`var scene: PackedScene`）
- 使用 `ResourceLoader.load_threaded_get_status()` 处理完成状态检查
- 注明加载失败的错误处理方式
- 不使用已废弃的 Godot 3 `yield()` 语法

### 用例 4：性能问题——推荐使用类型化数组
**输入**："实体更新循环很慢，每帧遍历一个包含 1000 个节点的无类型 Array。"
**预期行为**：
- 指出无类型 `Array` 会使 GDScript 无法进行编译器优化
- 推荐转换为类型化数组（`Array[Node]` 或具体类型）以启用 JIT 提示
- 注明若仍不满足需求，则升级为 C# 迁移建议
- 将类型化数组重构作为立即可行的修复方案
- 在没有性能剖析数据的情况下，不推荐将整个代码库迁移到 C#

### 用例 5：上下文传递——Godot 4.6 后截止功能
**输入**：提供引擎版本上下文：Godot 4.6。请求："使用 @abstract 为所有敌人类型创建抽象基类。"
**预期行为**：
- 识别 `@abstract` 为 Godot 4.5+ 功能（后截止）
- 在输出中注明：该功能于 4.5 引入，已根据 VERSION.md 迁移说明验证
- 使用迁移说明中记录的正确语法，产出使用 `@abstract` 的 GDScript 类
- 由于后截止状态，将输出标记为需要对照官方 4.5 发行说明进行验证
- 抽象类中的所有方法签名均使用静态类型

---

## 协议合规性

- [ ] 保持在声明的职责范围内（GDScript——类型、模式、信号、协程、性能）
- [ ] 将着色器请求重定向给 godot-shader-specialist
- [ ] 将 GDExtension 请求重定向给 godot-gdextension-specialist
- [ ] 返回带有完整静态类型的结构化 GDScript 输出
- [ ] 仅使用 Godot 4 API——不使用已废弃的 Godot 3 模式（yield、用字符串 connect 等）
- [ ] 标记后截止功能（4.4、4.5、4.6）并要求文档验证

---

## 覆盖说明
- 类型注解审查（用例 1）的输出适合作为代码审查清单
