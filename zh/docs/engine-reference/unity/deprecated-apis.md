# Unity 6.3 LTS — 已废弃 API

**最后验证：** 2026-02-13

已废弃 API 及其替代方案速查表。
格式：**不要使用 X** → **改用 Y**

---

## 输入

| 已废弃 | 替代方案 | 说明 |
|--------|---------|------|
| `Input.GetKey()` | `Keyboard.current[Key.X].isPressed` | 新 Input System |
| `Input.GetKeyDown()` | `Keyboard.current[Key.X].wasPressedThisFrame` | 新 Input System |
| `Input.GetMouseButton()` | `Mouse.current.leftButton.isPressed` | 新 Input System |
| `Input.GetAxis()` | `InputAction` 回调 | 新 Input System |
| `Input.mousePosition` | `Mouse.current.position.ReadValue()` | 新 Input System |

**迁移方案：** 安装 `com.unity.inputsystem` 包。

---

## UI

| 已废弃 | 替代方案 | 说明 |
|--------|---------|------|
| `Canvas`（UGUI）| `UIDocument`（UI Toolkit）| UI Toolkit 现已生产就绪 |
| `Text` 组件 | `TextMeshPro` 或 UI Toolkit `Label` | 渲染更优、绘制调用更少 |
| `Image` 组件 | 带背景的 UI Toolkit `VisualElement` | 样式更灵活 |

**迁移方案：** UGUI 仍可使用，但新项目推荐 UI Toolkit。

---

## DOTS/Entities

| 已废弃 | 替代方案 | 说明 |
|--------|---------|------|
| `ComponentSystem` | `ISystem`（非托管）| Entities 1.0+ 完整重写 |
| `JobComponentSystem` | 带 `IJobEntity` 的 `ISystem` | 兼容 Burst |
| `GameObjectEntity` | 纯 ECS 工作流 | 不再通过 GameObject 转换 |
| `EntityManager.CreateEntity()`（旧签名）| `EntityManager.CreateEntity(EntityArchetype)` | 显式指定 Archetype |
| `ComponentDataFromEntity<T>` | `ComponentLookup<T>` | Entities 1.0+ 重命名 |

**迁移方案：** 参考 Entities 包迁移指南，需要重大重构。

---

## 渲染

| 已废弃 | 替代方案 | 说明 |
|--------|---------|------|
| `CommandBuffer.DrawMesh()` | RenderGraph API | URP/HDRP 渲染通道 |
| `OnPreRender()` / `OnPostRender()` | `RenderPipelineManager` 回调 | SRP 兼容性 |
| `Camera.SetReplacementShader()` | 自定义渲染通道 | SRP 中不支持 |

---

## 物理

| 已废弃 | 替代方案 | 说明 |
|--------|---------|------|
| `Physics.RaycastAll()` | `Physics.RaycastNonAlloc()` | 避免 GC 分配 |
| 直接写入 `Rigidbody.velocity` | `Rigidbody.AddForce()` | 更好的物理稳定性 |

---

## 资产加载

| 已废弃 | 替代方案 | 说明 |
|--------|---------|------|
| `Resources.Load()` | Addressables | 更好的内存控制，异步加载 |
| 同步资产加载 | `Addressables.LoadAssetAsync()` | 非阻塞 |

---

## 动画

| 已废弃 | 替代方案 | 说明 |
|--------|---------|------|
| 旧版 Animation 组件 | Animator Controller（Mecanim）| 现代状态机动画 |
| `Animation.Play()` | `Animator.Play()` | 状态机控制 |

---

## 粒子

| 已废弃 | 替代方案 | 说明 |
|--------|---------|------|
| 旧版粒子系统（Legacy Particle System）| Visual Effect Graph | GPU 加速，性能更佳 |

---

## 脚本

| 已废弃 | 替代方案 | 说明 |
|--------|---------|------|
| `WWW` 类 | `UnityWebRequest` | 现代异步网络请求 |
| `Application.LoadLevel()` | `SceneManager.LoadScene()` | 场景管理 |

---

## 平台专项

### WebGL
| 已废弃 | 替代方案 | 说明 |
|--------|---------|------|
| WebGL 1.0 | WebGL 2.0 或 WebGPU | Unity 6+ 默认使用 WebGPU |

---

## 快速迁移示例

### 输入
```csharp
// ❌ 已废弃
if (Input.GetKeyDown(KeyCode.Space)) {
    Jump();
}

// ✅ 新 Input System
using UnityEngine.InputSystem;
if (Keyboard.current.spaceKey.wasPressedThisFrame) {
    Jump();
}
```

### 资产加载
```csharp
// ❌ 已废弃
var prefab = Resources.Load<GameObject>("Enemies/Goblin");

// ✅ Addressables
var handle = Addressables.LoadAssetAsync<GameObject>("Enemies/Goblin");
await handle.Task;
var prefab = handle.Result;
```

### UI
```csharp
// ❌ 已废弃（UGUI）
GetComponent<Text>().text = "分数: 100";

// ✅ TextMeshPro
GetComponent<TextMeshProUGUI>().text = "分数: 100";

// ✅ UI Toolkit
rootVisualElement.Q<Label>("score-label").text = "分数: 100";
```

---

**参考来源：**
- https://docs.unity3d.com/6000.0/Documentation/Manual/deprecated-features.html
- https://docs.unity3d.com/Packages/com.unity.inputsystem@1.11/manual/Migration.html
