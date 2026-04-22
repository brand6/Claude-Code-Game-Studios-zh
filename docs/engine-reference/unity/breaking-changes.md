# Unity 6.3 LTS — 破坏性变更

**最后验证：** 2026-02-13

本文档记录 Unity 2022 LTS（可能在模型训练数据中）与 Unity 6.3 LTS（当前版本）之间的
破坏性 API 变更和行为差异，按风险等级分类。

## 高风险 — 将导致现有代码无法运行

### Entities/DOTS API 完整重构
**影响版本：** Entities 1.0+（Unity 6.0+）

```csharp
// ❌ 旧写法（Unity 6 之前，GameObjectEntity 模式）
public class HealthComponent : ComponentData {
    public float Value;
}

// ✅ 新写法（Unity 6+，IComponentData）
public struct HealthComponent : IComponentData {
    public float Value;
}

// ❌ 旧写法：ComponentSystem
public class DamageSystem : ComponentSystem { }

// ✅ 新写法：ISystem（非托管，兼容 Burst）
public partial struct DamageSystem : ISystem {
    public void OnCreate(ref SystemState state) { }
    public void OnUpdate(ref SystemState state) { }
}
```

**迁移方案：** 参考 Unity ECS 迁移指南，需进行重大架构调整。

---

### Input System — 旧版 Input 已废弃
**影响版本：** Unity 6.0+

```csharp
// ❌ 旧写法：Input 类（已废弃）
if (Input.GetKeyDown(KeyCode.Space)) { }

// ✅ 新写法：Input System 包
using UnityEngine.InputSystem;
if (Keyboard.current.spaceKey.wasPressedThisFrame) { }
```

**迁移方案：** 安装 Input System 包，将所有 `Input.*` 调用替换为新 API。

---

### URP/HDRP Renderer Feature API 变更
**影响版本：** Unity 6.0+

```csharp
// ❌ 旧写法：ScriptableRenderPass.Execute 签名
public override void Execute(ScriptableRenderContext context, ref RenderingData data)

// ✅ 新写法：使用 RenderGraph API
public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameData)
```

**迁移方案：** 将自定义渲染通道更新为 RenderGraph API。

---

## 中风险 — 行为变更

### Addressables — 资产加载返回值变更
**影响版本：** Unity 6.2+

资产加载失败现在默认抛出异常，而不是返回 null。
添加正确的异常处理，或使用 `TryLoad` 变体。

```csharp
// ❌ 旧写法：失败时静默返回 null
var handle = Addressables.LoadAssetAsync<Sprite>("key");
var sprite = handle.Result; // 失败时为 null

// ✅ 新写法：失败时抛出异常，使用 try/catch 或 TryLoad
try {
    var handle = Addressables.LoadAssetAsync<Sprite>("key");
    var sprite = await handle.Task;
} catch (Exception e) {
    Debug.LogError($"加载失败: {e}");
}
```

---

### Physics — 默认求解器迭代次数变更
**影响版本：** Unity 6.0+

默认求解器迭代次数已增加以提升稳定性。
如果依赖旧行为，请检查 `Physics.defaultSolverIterations`。

---

## 低风险 — 废弃项（仍可使用）

### UGUI（旧版 UI）
**状态：** 已废弃但仍受支持
**替代方案：** UI Toolkit

UGUI 仍然可用，但新项目推荐使用 UI Toolkit。

---

### 旧版粒子系统
**状态：** 已废弃
**替代方案：** Visual Effect Graph（VFX Graph）

---

### 旧版动画系统
**状态：** 已废弃
**替代方案：** Animator Controller（Mecanim）

---

## 平台专项破坏性变更

### WebGL
- **Unity 6.0+**：WebGPU 成为默认（WebGL 2.0 作为回退选项）
- 需更新着色器以兼容 WebGPU

### Android
- **Unity 6.0+**：最低 API 等级提升至 24（Android 7.0）

### iOS
- **Unity 6.0+**：最低部署目标提升至 iOS 13

---

## 迁移检查清单

从 2022 LTS 升级到 Unity 6.3 LTS 时：

- [ ] 审查所有 DOTS/ECS 代码（可能需要完整重写）
- [ ] 将 `Input` 类替换为 Input System 包
- [ ] 将自定义渲染通道更新为 RenderGraph API
- [ ] 为 Addressables 调用添加异常处理
- [ ] 测试物理行为（求解器迭代次数已变更）
- [ ] 考虑将新 UI 从 UGUI 迁移至 UI Toolkit
- [ ] 更新 WebGL 着色器以兼容 WebGPU
- [ ] 验证最低平台版本要求（Android/iOS）

---

**参考来源：**
- https://docs.unity3d.com/6000.0/Documentation/Manual/upgrade-guides.html
- https://docs.unity3d.com/Packages/com.unity.entities@1.3/manual/upgrade-guide.html
