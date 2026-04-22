# Unreal Engine 5.7 — 破坏性变更

**最后验证：** 2026-02-13

本文档记录 Unreal Engine 5.3（模型训练数据可能包含）与 Unreal Engine 5.7（当前版本）之间的 API 破坏性变更和行为差异。按风险等级分类。

## 高风险 — 会破坏现有代码

### Substrate 材质系统（5.7 生产就绪）
**版本：** UE 5.5+（实验性），5.7（生产就绪）

Substrate 以模块化、物理精确的框架替代旧版材质系统。

```cpp
// ❌ 旧版：旧式材质节点（仍可用，但已废弃）
// 标准材质图：Base Color、Metallic、Roughness 等

// ✅ 新版：Substrate 材质层
// 使用 Substrate 节点：Substrate Slab、Substrate Blend 等
// 模块化材质制作，具有真实的物理精度
```

**迁移：** 在 `项目设置 > 引擎 > Substrate` 中启用 Substrate，并用 Substrate 节点重建材质。

---

### PCG（程序化内容生成）API 大改
**版本：** UE 5.7（生产就绪）

PCG 框架在 API 重大变更后达到生产就绪状态。

```cpp
// ❌ 旧版：实验性 PCG API（5.7 之前）
// 旧节点类型，API 不稳定

// ✅ 新版：生产级 PCG API（5.7+）
// 使用 FPCGContext、IPCGElement、新节点类型
// 稳定 API，生产就绪工作流
```

**迁移：** 参阅 5.7 文档中的 PCG 迁移指南。实验性 PCG 代码需要较大重构。

---

### Megalights 渲染系统
**版本：** UE 5.5+

新光照系统支持数百万动态灯光。

```cpp
// ❌ 旧版：动态灯光数量有限（聚类前向着色）
// 动态灯光超过约 100-200 个后性能急剧下降

// ✅ 新版：Megalights（5.5+）
// 数百万动态灯光，性能成本极低
// 启用：项目设置 > 引擎 > 渲染 > Megalights
```

**迁移：** 无需代码改动，但光照行为可能有所不同。启用后请测试场景。

---

## 中风险 — 行为变更

### Enhanced Input 系统（现为默认）
**版本：** UE 5.1+（推荐），5.7（默认）

Enhanced Input 现在是默认输入系统。

```cpp
// ❌ 旧版：旧式输入绑定（已废弃）
InputComponent->BindAction("Jump", IE_Pressed, this, &ACharacter::Jump);

// ✅ 新版：Enhanced Input
SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) {
    UEnhancedInputComponent* EIC = Cast<UEnhancedInputComponent>(PlayerInputComponent);
    EIC->BindAction(JumpAction, ETriggerEvent::Started, this, &ACharacter::Jump);
}
```

**迁移：** 将旧式输入绑定替换为 Enhanced Input 动作。

---

### Nanite 默认启用
**版本：** UE 5.0+（可选），5.7（推荐）

Nanite 虚拟化几何体现在是静态网格体的推荐工作流。

```cpp
// 在静态网格体上启用 Nanite：
// 静态网格编辑器 > 细节 > Nanite 设置 > 启用 Nanite 支持
```

**迁移：** 将高精度网格转换为 Nanite。在目标平台上测试性能。

---

## 低风险 — 废弃项（仍可使用）

### 旧版材质系统
**状态：** 已废弃，但仍受支持
**替代方案：** Substrate 材质系统

旧版材质仍然可用，但新项目推荐使用 Substrate。

---

### 旧版 World Partition（UE4 风格）
**状态：** 已废弃
**替代方案：** World Partition（UE5+）

大型世界请使用 UE5 的 World Partition 系统。

---

## 平台特定破坏性变更

### Windows
- **UE 5.7**：DirectX 12 现为默认（旧版本默认 DX11）
- 更新着色器以兼容 DX12

### macOS
- **UE 5.5+**：需要 Metal 3（最低 macOS 13）

### 移动端
- **UE 5.7**：最低 Android API 等级提升至 26（Android 8.0）
- 最低 iOS 部署目标提升至 iOS 14

---

## 迁移检查清单

从 UE 5.3 升级到 UE 5.7 时：

- [ ] 检查 Substrate 材质（如果准备好迁移到新系统则转换）
- [ ] 审计 PCG 用法（如果使用了实验性 API，升级到生产级 API）
- [ ] 测试 Megalights 性能（启用并做基准测试）
- [ ] 将旧版输入迁移到 Enhanced Input
- [ ] 将高精度网格转换为 Nanite
- [ ] 更新着色器以兼容 DX12（Windows）或 Metal 3（macOS）
- [ ] 验证最低平台版本要求（Android 8.0，iOS 14）
- [ ] 在目标硬件上测试 Lumen 和 Nanite 性能

---

**来源：**
- https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-7-release-notes
- https://dev.epicgames.com/documentation/en-us/unreal-engine/upgrading-projects-to-newer-versions-of-unreal-engine
