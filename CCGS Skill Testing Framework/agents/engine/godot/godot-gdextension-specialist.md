# Agent 测试规格：godot-gdextension-specialist

## Agent 概述
职责领域：GDExtension API、godot-cpp C++ 绑定、godot-rust 绑定、原生库集成，以及原生性能优化。
不负责：GDScript 代码（gdscript-specialist）、着色器代码（godot-shader-specialist）。
模型层级：Sonnet（默认）。
未分配关卡 ID。

---

## 静态断言（结构检查）

- [ ] `description:` 字段存在且领域明确（引用 GDExtension / godot-cpp / 原生绑定）
- [ ] `allowed-tools:` 列表包含 Read、Write、Edit、Bash、Glob、Grep
- [ ] 模型层级为 Sonnet（专员的默认层级）
- [ ] Agent 定义未主张对 GDScript 或着色器编写拥有权

---

## 测试用例

### 用例 1：领域内请求——合适的输出
**输入**："通过 GDExtension 将一个 C++ 刚体物理模拟库暴露给 GDScript。"
**预期行为**：
- 产出使用 godot-cpp 的 GDExtension 绑定模式：
  - 继承自 `godot::Object` 或适当 Godot 基类的类
  - `GDCLASS` 宏注册
  - `_bind_methods()` 实现，将物理 API 暴露给 GDScript
  - `GDExtension` 入口点（`gdextension_init`）设置
- 注明所需的 `.gdextension` 清单文件格式
- 不产出 GDScript 使用代码（属于 gdscript-specialist 的职责）

### 用例 2：领域外重定向
**输入**："编写调用用例 1 中物理模拟的 GDScript 代码。"
**预期行为**：
- 不产出 GDScript 代码
- 明确声明 GDScript 编写属于 `godot-gdscript-specialist` 的职责范围
- 将请求重定向给 `godot-gdscript-specialist`
- 可以描述 GDScript 应调用的 API 接口（方法名、参数类型）作为交接规格

### 用例 3：ABI 兼容性风险——次版本升级
**输入**："我们要从 Godot 4.5 升级到 4.6，现有的 GDExtension 还能用吗？"
**预期行为**：
- 标记 ABI 兼容性问题：GDExtension 二进制可能在次版本间不具备 ABI 兼容性
- 指引查看 4.5→4.6 迁移指南中的 GDExtension API 变更
- 建议针对 4.6 版本的 godot-cpp 头文件重新编译扩展，而非假设二进制兼容性
- 注明 `.gdextension` 清单可能需要更新 `compatibility_minimum` 版本
- 提供重新编译检查清单

### 用例 4：内存管理——Godot 对象的 RAII
**输入**："在 C++ GDExtension 代码中创建的 Godot 对象，其生命周期应如何管理？"
**预期行为**：
- 产出 GDExtension 中 Godot 对象的 RAII 生命周期模式：
  - 引用计数对象使用 `Ref<T>`（Ref 离开作用域时自动释放）
  - 非引用计数对象使用 `memnew()` / `memdelete()`
  - 警告：不得对 Godot 对象使用 `new`/`delete`——会导致未定义行为
- 注明对象所有权规则：谁负责释放添加到场景树中的节点
- 提供在 C++ 中创建 `CollisionShape3D` 的具体内存管理示例

### 用例 5：上下文传递——Godot 4.6 GDExtension API 检查
**输入**：引擎版本上下文：Godot 4.6（从 4.5 升级）。请求："检查 4.5 到 4.6 之间是否有 GDExtension API 变更。"
**预期行为**：
- 引用 VERSION.md 验证来源列表中的 4.5→4.6 迁移指南
- 报告 4.6 发行版中记录的 GDExtension API 变更
- 若 4.6 中无 GDExtension 相关破坏性变更，则明确声明，并附上对照官方变更日志验证的注意事项
- 将 D3D12 成为 Windows 默认渲染器（4.6 变更）标记为可能与 GDExtension 渲染代码相关
- 提供升级后的验证清单

---

## 协议合规性

- [ ] 保持在声明的职责范围内（GDExtension、godot-cpp、godot-rust、原生绑定）
- [ ] 将 GDScript 编写重定向给 godot-gdscript-specialist
- [ ] 将着色器编写重定向给 godot-shader-specialist
- [ ] 返回结构化输出（绑定模式、RAII 示例、ABI 检查清单）
- [ ] 在次版本升级时标记 ABI 兼容性风险——绝不假设二进制兼容性
- [ ] 使用 Godot 专属内存管理（`memnew`/`memdelete`、`Ref<T>`），不使用原始 C++ new/delete
- [ ] 在确认兼容性前检查引擎版本参考文件中的 GDExtension API 变更

---

## 覆盖说明
- 绑定模式（用例 1）应包含一个冒烟测试，验证扩展可加载且方法可从 GDScript 调用
- ABI 风险（用例 3）是关键的上报路径——Agent 不得在未验证的情况下批准发布扩展二进制
- 内存管理（用例 4）验证 Agent 应用了 Godot 专属模式，而非通用 C++ RAII
