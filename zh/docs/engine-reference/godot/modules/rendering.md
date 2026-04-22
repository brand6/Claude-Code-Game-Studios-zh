# Godot 渲染 — 快速参考

Last verified: 2026-02-12 | Engine: Godot 4.6

## 自 ~4.3（LLM 截止版本）以来的变更

### 4.6 变更
- **D3D12 是 Windows 上的默认渲染后端**（原为 Vulkan）
- **辉光（Glow）在色调映射之前处理**（原为之后）— 使用屏幕混合模式
- **AgX 色调映射器**：新增白点和对比度控制项
- **SSR 全面重构**：真实感、视觉稳定性和性能均有显著提升

### 4.5 变更
- **Shader Baker（着色器预烘焙）**：预编译着色器以减少启动时间
- **SMAA 1x**：新抗锯齿选项（比 FXAA 更清晰，比 TAA 更轻量）
- **模板缓冲支持**：支持选择性几何体遮罩/传送门效果
- **弯曲法线贴图**：在法线贴图纹理中编码方向性遮蔽
- **镜面遮蔽**：环境光遮蔽现在正确影响反射

### 4.4 变更
- **`RenderingDevice.draw_list_begin`**：移除多个参数；新增可选 `breadcrumb` 参数
- **着色器纹理类型**：从 `Texture2D` 改为 `Texture` 基类型
- **粒子 `.restart()`**：新增可选 `keep_seed` 参数

### 4.3 变更（在训练数据范围内）
- **Compositor 节点**：使用 `Compositor` + `CompositorEffect` 构建后处理链

## 当前 API 模式

### 后处理（4.3+）
```gdscript
# 使用 Compositor 节点 — 不要使用手动视口着色器链
# 将 Compositor 添加为 WorldEnvironment 或 Camera3D 的子节点
# 为每个后处理步骤创建 CompositorEffect 资源
```

### 抗锯齿选项（4.6）
```
项目设置 → 渲染 → 抗锯齿：
- MSAA 2D/3D：硬件 MSAA（质量好但开销大）
- 屏幕空间 AA：FXAA（快速但模糊）或 SMAA（清晰，中等开销）  # SMAA 在 4.5 新增
- TAA：时间性（质量最佳，快速运动有残影）
```

### 渲染后端选择（4.6）
```
项目设置 → 渲染 → 渲染器：
- Forward+（默认）：功能完整，面向桌面
- Mobile：针对移动/低端设备优化，功能有限
- Compatibility：OpenGL 3.3 / WebGL 2，硬件兼容性最广

Windows 默认后端：D3D12（4.6 之前为 Vulkan）
```

## 常见错误
- 假设 Vulkan 是 Windows 的默认后端（4.6 起已改为 D3D12）
- 使用手动视口链而非 Compositor 处理后处理
- 着色器 uniform 类型使用 `Texture2D`（4.4 起应改用 `Texture`）
- 有大量着色器变体的项目未使用 Shader Baker
