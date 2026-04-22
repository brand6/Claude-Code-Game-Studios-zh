# Godot — 破坏性变更

Last verified: 2026-02-12

各 Godot 版本之间的变更，重点关注 LLM 截止日期之后的变更（4.4+）。

## 4.5 → 4.6（2026 年 1 月 — 截止日期后，高风险）

| 子系统 | 变更 | 详情 |
|--------|------|------|
| 物理 | Jolt 现在是默认的 3D 物理引擎 | 新项目自动使用 Jolt。已有项目保留原设置。部分 HingeJoint3D 属性（如 `damp`）仅在 GodotPhysics 下有效。 |
| 渲染 | 辉光（Glow）在色调映射之前处理 | 原来是在之后处理。场景中有辉光效果的将显示不同。请在 WorldEnvironment 中调整强度/混合值。 |
| 渲染 | Windows 默认使用 D3D12 | 原为 Vulkan，以提升驱动兼容性。 |
| 渲染 | AgX 色调映射器新增控制项 | 新增白点和对比度参数。 |
| 核心 | Quaternion 初始化为单位四元数 | 原为零四元数。大多数代码不受影响，但技术上属于破坏性变更。 |
| UI | 双焦点系统 | 鼠标/触摸焦点现与键盘/手柄焦点分开。不同输入方式的视觉反馈有所不同。 |
| 动画 | IK 系统完整恢复 | 通过 SkeletonModifier3D 节点提供 CCDIK、FABRIK、Jacobian IK、Spline IK、TwoBoneIK。 |
| 编辑器 | 新的"Modern"主题设为默认 | 灰度色调替代蓝色调。恢复方式：Editor Settings → Interface → Theme → Style: Classic |
| 编辑器 | "Select Mode"快捷键变更 | 新增"Select Mode"（`v` 键）防止误操作变换。旧模式更名为"Transform Mode"（`q` 键）。 |
| 2D | TileMapLayer 场景瓦片旋转 | 场景瓦片现在可以像图集瓦片一样旋转。 |
| 本地化 | CSV 复数形式支持 | 不再需要 Gettext 来处理复数形式。新增上下文列。 |
| C# | 自动字符串提取 | 翻译字符串从 C# 代码中自动提取。 |
| 插件 | 新 EditorDock 类 | 专用于插件 dock 的容器，具有布局控制功能。 |

## 4.4 → 4.5（2025 年底 — 截止日期后，高风险）

| 子系统 | 变更 | 详情 |
|--------|------|------|
| GDScript | 可变参数支持 | 函数可以接受 `...` 任意数量参数 — 新语言特性 |
| GDScript | `@abstract` 装饰器 | 现在可强制声明抽象类和方法 |
| GDScript | 脚本回溯 | 即使在发布构建中也可获得详细调用栈 |
| 渲染 | 模板缓冲支持 | 用于高级视觉效果的新功能 |
| 渲染 | SMAA 1x 抗锯齿 | 新的后处理 AA 选项 |
| 渲染 | Shader Baker（着色器预烘焙） | 预编译着色器 — 某些 Demo 启动速度提升约 20 倍 |
| 渲染 | 弯曲法线贴图、镜面遮蔽 | 新增材质特性 |
| 无障碍 | 屏幕阅读器支持 | Control 节点通过 AccessKit 与无障碍工具集成 |
| 编辑器 | 实时翻译预览 | 可在编辑器内测试不同语言的 GUI 布局 |
| 物理 | 3D 插值架构重写 | 从 RenderingServer 迁移到 SceneTree，用户侧 API 不变但内部行为在边缘情况下可能不同。 |
| 动画 | BoneConstraint3D | 新增：AimModifier3D、CopyTransformModifier3D、ConvertTransformModifier3D |
| 资源 | 新增 `duplicate_deep()` | 用于显式深拷贝嵌套资源 |
| 导航 | 独立的 2D 导航服务器 | 不再代理到 3D 导航；2D 游戏导出体积更小 |
| UI | FoldableContainer 节点 | 新增折叠式容器，用于可收起的 UI 区块 |
| UI | 递归 Control 行为 | 可对整个节点层级禁用鼠标/焦点交互 |
| 平台 | visionOS 导出支持 | 新平台目标 |
| 平台 | SDL3 手柄驱动 | 手柄处理委托给 SDL 库 |
| 平台 | Android 16KB 页面支持 | 针对 Android 15+ Google Play 的必要条件 |

## 4.3 → 4.4（2025 年中 — 接近截止日期，建议核实）

| 子系统 | 变更 | 详情 |
|--------|------|------|
| 核心 | `FileAccess.store_*` 返回 `bool` | 原为 `void`。涉及方法：`store_8`、`store_16`、`store_32`、`store_64`、`store_buffer`、`store_csv_line`、`store_double`、`store_float`、`store_half`、`store_line`、`store_pascal_string`、`store_real`、`store_string`、`store_var` |
| 核心 | `OS.execute_with_pipe` | 新增可选 `blocking` 参数 |
| 核心 | `RegEx.compile/create_from_string` | 新增可选 `show_error` 参数 |
| 渲染 | `RenderingDevice.draw_list_begin` | 移除多个参数；新增 `breadcrumb` 参数 |
| 渲染 | 着色器纹理类型 | 参数/返回类型从 `Texture2D` 改为 `Texture` |
| 粒子 | `.restart()` 方法 | 新增可选 `keep_seed` 参数（CPU/GPU 2D/3D 均适用） |
| GUI | `RichTextLabel.push_meta` | 新增可选 `tooltip` 参数 |
| GUI | `GraphEdit.connect_node` | 新增可选 `keep_alive` 参数 |

## 4.2 → 4.3（在训练数据范围内 — 低风险）

| 子系统 | 变更 | 详情 |
|--------|------|------|
| 动画 | `Skeleton3D.add_bone` 返回 `int32` | 原为 `void` |
| 动画 | `bone_pose_updated` 信号 | 已被 `skeleton_updated` 替代 |
| TileMap | `TileMapLayer` 取代 `TileMap` | 每个图层一个节点，而非单节点多图层 |
| 导航 | `NavigationRegion2D` | 移除了 `avoidance_layers`、`constrain_avoidance` 属性 |
| 编辑器 | `EditorSceneFormatImporterFBX` | 更名为 `EditorSceneFormatImporterFBX2GLTF` |
| 动画 | AnimationMixer 基类 | AnimationPlayer 和 AnimationTree 现在都继承自 AnimationMixer |
