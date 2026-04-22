# Godot — 已废弃 API

Last verified: 2026-02-12

如果 Agent 建议使用"已废弃"列中的任何 API，必须替换为"替代方案"列中的内容。

## 节点与类

| 已废弃 | 替代方案 | 自版本 | 说明 |
|--------|---------|--------|------|
| `TileMap` | `TileMapLayer` | 4.3 | 每个图层一个节点，而非多图层单节点 |
| `VisibilityNotifier2D` | `VisibleOnScreenNotifier2D` | 4.0 | 重命名以提高清晰度 |
| `VisibilityNotifier3D` | `VisibleOnScreenNotifier3D` | 4.0 | 重命名以提高清晰度 |
| `YSort` | `Node2D.y_sort_enabled` | 4.0 | Node2D 上的属性，不再是独立节点 |
| `Navigation2D` / `Navigation3D` | `NavigationServer2D` / `NavigationServer3D` | 4.0 | 基于服务器的 API |
| `EditorSceneFormatImporterFBX` | `EditorSceneFormatImporterFBX2GLTF` | 4.3 | 重命名 |

## 方法与属性

| 已废弃 | 替代方案 | 自版本 | 说明 |
|--------|---------|--------|------|
| `yield()` | `await signal` | 4.0 | GDScript 2.0 协程语法 |
| `connect("signal", obj, "method")` | `signal.connect(callable)` | 4.0 | 基于 Callable 的连接方式 |
| `instance()` | `instantiate()` | 4.0 | 重命名 |
| `PackedScene.instance()` | `PackedScene.instantiate()` | 4.0 | 重命名 |
| `get_world()` | `get_world_3d()` | 4.0 | 明确区分 2D/3D |
| `OS.get_ticks_msec()` | `Time.get_ticks_msec()` | 4.0 | 优先使用 Time 单例 |
| 嵌套资源的 `duplicate()` | `duplicate_deep()` | 4.5 | 显式深拷贝控制 |
| `Skeleton3D` 信号 `bone_pose_updated` | `skeleton_updated` | 4.3 | 重命名 |
| `AnimationPlayer.method_call_mode` | `AnimationMixer.callback_mode_method` | 4.3 | 移至基类 |
| `AnimationPlayer.playback_active` | `AnimationMixer.active` | 4.3 | 移至基类 |

## 模式（不仅仅是 API）

| 已废弃模式 | 替代方案 | 原因 |
|-----------|---------|------|
| 基于字符串的 `connect()` | 类型安全的信号连接 | 类型安全，便于重构 |
| 在 `_process()` 中使用 `$NodePath` | `@onready var` 缓存引用 | 性能：每帧路径查找开销大 |
| 无类型的 `Array` / `Dictionary` | `Array[Type]`、类型化变量 | GDScript 编译器优化 |
| 着色器参数中使用 `Texture2D` | `Texture` 基类型 | 自 4.4 起已更改 |
| 手动后处理视口链 | `Compositor` + `CompositorEffect` | 结构化后处理（4.3+） |
| 新项目使用 GodotPhysics3D | Jolt Physics 3D | 自 4.6 起为默认；稳定性更好 |
