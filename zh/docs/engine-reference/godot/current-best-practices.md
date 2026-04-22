# Godot — 当前最佳实践

Last verified: 2026-02-12 | Engine: Godot 4.6

本文档记录自模型训练数据（~4.3）以来**新增或已变更**的实践。
这是对 Agent 内置知识的补充，而非替代。

## GDScript（4.5+）

- **可变参数**：函数可接受任意数量的参数
  ```gdscript
  func log_values(prefix: String, values: Variant...) -> void:
      for v in values:
          print(prefix, ": ", v)
  ```

- **抽象类和方法**：使用 `@abstract` 强制继承
  ```gdscript
  @abstract
  class_name BaseEnemy extends CharacterBody3D

  @abstract
  func get_attack_pattern() -> Array[Attack]:
      pass  # 子类必须重写
  ```

- **脚本回溯**：即使在发布构建中也能获得详细调用栈

## 物理（4.6）

- **Jolt Physics 是新项目的默认 3D 引擎**
  - 比 GodotPhysics3D 具有更好的确定性和稳定性
  - 部分 HingeJoint3D 属性（`damp`）仅在 GodotPhysics 下有效
  - 切换方式：项目设置 → 物理 → 3D → 物理引擎
  - 2D 物理不变（仍使用 Godot Physics 2D）

## 渲染（4.6）

- **D3D12 是 Windows 的默认渲染后端**（原为 Vulkan）— 以提升驱动兼容性
- **辉光（Glow）现在在色调映射之前处理**，使用屏幕混合模式 — 已有辉光设置可能显示不同
- **SSR 全面重构** — 真实感、稳定性和性能均有显著提升
- **AgX 色调映射器** — 新增白点和对比度控制项

## 渲染（4.5）

- **Shader Baker（着色器预烘焙）**：预编译着色器以消除启动卡顿
- **SMAA 1x**：新 AA 选项 — 比 FXAA 更清晰，比 TAA 更轻量
- **模板缓冲**：可用于高级遮罩/传送门效果
- **弯曲法线贴图**：在法线贴图纹理中编码方向性遮蔽
- **镜面遮蔽**：环境光遮蔽现在正确影响反射

## 无障碍（4.5+）

- **屏幕阅读器支持**：Control 节点通过 AccessKit 与无障碍工具集成
- **实时翻译预览**：可在编辑器内直接测试不同语言的 GUI 布局
- **FoldableContainer**：新增折叠式 UI 节点，用于可收起区块
- **递归 Control 禁用**：通过单一属性禁用整个节点层级的鼠标/焦点交互

## 动画（4.5+）

- **BoneConstraint3D**：将骨骼绑定到其他骨骼，支持修改器
  - AimModifier3D、CopyTransformModifier3D、ConvertTransformModifier3D

## 动画（4.6）

- **IK 系统完整恢复**：为 3D 完整引入逆运动学
  - 可用修改器：CCDIK、FABRIK、Jacobian IK、Spline IK、TwoBoneIK
  - 通过 `SkeletonModifier3D` 节点应用

## 资源（4.5+）

- **`duplicate_deep()`**：用于嵌套资源树的显式深拷贝
  - 原 `duplicate()` 行为保留，保持向后兼容
  - 需要每个实例各自拥有嵌套资源副本时，使用 `duplicate_deep()`

## 导航（4.5+）

- **独立的 2D 导航服务器**：不再通过 3D NavigationServer 代理
  - 减少纯 2D 游戏的导出二进制体积

## UI（4.6）

- **双焦点系统**：鼠标/触摸焦点现与键盘/手柄焦点分开
  - 不同输入方式的视觉反馈各有不同
  - 设计自定义焦点行为时请考虑这一点

## 编辑器工作流（4.6）

- 灵活的 dock 拖放功能，带蓝色轮廓预览（包括底部面板）
- 大多数面板支持浮动窗口（调试器除外）
- 新键盘快捷键：Alt+O（输出）、Alt+S（着色器）
- 导出变量自动生成：从文件系统将资源拖入脚本编辑器
- 在 Quick Open 对话框中启用"Live Preview"后可即时预览
- 新增"Select Mode"（`v` 键）防止误操作变换；旧模式更名为"Transform Mode"（`q` 键）

## 平台（4.5+）

- **visionOS 导出**：开源后的首个新平台（窗口应用模式）
- **SDL3 手柄驱动**：更好的跨平台手柄支持
- **Android**：边到边显示、摄像头馈流访问、16KB 页面支持（Android 15+）
- **Linux**：Wayland 子窗口支持，实现多窗口能力
