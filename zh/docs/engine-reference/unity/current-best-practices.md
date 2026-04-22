# Unity 6.3 LTS — 当前最佳实践

**最后验证：** 2026-02-13

Unity 6 现代化模式，可能不在 LLM 的训练数据中。
以下是截至 Unity 6.3 LTS 的生产就绪推荐方案。

---

## 项目设置

### 生产项目使用 Unity 6.3 LTS
- **Tech Stream**（6.4+）：最新特性，稳定性较低
- **LTS**（6.3）：生产就绪，2 年支持期（至 2027 年 12 月）✅ 推荐

### 选择正确的渲染管线
- **URP（通用渲染管线）**：移动端、跨平台、性能优秀 ✅ 大多数游戏推荐
- **HDRP（高清渲染管线）**：高端 PC/主机，照片级真实感
- **内置管线**：已废弃，新项目不要使用

---

## 脚本

### 使用 C# 9+ 特性（Unity 6 支持 C# 9）

```csharp
// ✅ 数据使用 Record 类型
public record PlayerData(string Name, int Level, float Health);

// ✅ 只读初始化属性
public class Config {
    public string GameMode { get; init; }
}

// ✅ 模式匹配
var result = enemy switch {
    Boss boss => boss.Enrage(),
    Minion minion => minion.Flee(),
    _ => null
};
```

### 资产加载使用 Async/Await

```csharp
// ✅ 现代异步模式
public async Task<GameObject> LoadEnemyAsync(string key) {
    var handle = Addressables.LoadAssetAsync<GameObject>(key);
    return await handle.Task;
}
```

### 序列化使用 Source Generators（Unity 6+）

```csharp
// ✅ Source 生成的序列化（更快，减少反射）
[GenerateSerializer]
public partial struct PlayerStats : IComponentData {
    public int Health;
    public int Mana;
}
```

---

## DOTS/ECS（Unity 6.3 LTS 生产就绪）

### 使用 ISystem（不要用 ComponentSystem）

```csharp
// ✅ 现代非托管 ISystem（兼容 Burst）
public partial struct MovementSystem : ISystem {
    public void OnCreate(ref SystemState state) { }

    public void OnUpdate(ref SystemState state) {
        foreach (var (transform, speed) in
            SystemAPI.Query<RefRW<LocalTransform>, RefRO<MoveSpeed>>()) {
            transform.ValueRW.Position += speed.ValueRO.Value * SystemAPI.Time.DeltaTime;
        }
    }
}
```

### 并行任务使用 IJobEntity

```csharp
// ✅ IJobEntity（替代 IJobForEach）
[BurstCompile]
public partial struct DamageJob : IJobEntity {
    public float DeltaTime;

    void Execute(ref Health health, in DamageOverTime dot) {
        health.Value -= dot.DamagePerSecond * DeltaTime;
    }
}

// 调度执行
var job = new DamageJob { DeltaTime = SystemAPI.Time.DeltaTime };
job.ScheduleParallel();
```

---

## 输入

### 使用 Input System 包（不要用旧版 Input）

```csharp
// ✅ Input Actions（可重绑定，跨平台）
using UnityEngine.InputSystem;

public class PlayerInput : MonoBehaviour {
    private PlayerControls controls;

    void Awake() {
        controls = new PlayerControls();
        controls.Gameplay.Jump.performed += ctx => Jump();
    }

    void OnEnable() => controls.Enable();
    void OnDisable() => controls.Disable();
}
```

在编辑器中创建 Input Actions 资产，通过 Inspector 生成 C# 类。

---

## UI

### 运行时 UI 使用 UI Toolkit（Unity 6 已生产就绪）

```csharp
// ✅ UI Toolkit（新项目替代 UGUI）
using UnityEngine.UIElements;

public class MainMenu : MonoBehaviour {
    void OnEnable() {
        var root = GetComponent<UIDocument>().rootVisualElement;

        var playButton = root.Q<Button>("play-button");
        playButton.clicked += StartGame;

        var scoreLabel = root.Q<Label>("score");
        scoreLabel.text = $"最高分: {PlayerPrefs.GetInt("HighScore")}";
    }
}
```

**UXML**（UI 结构）+ **USS**（样式）= 类 HTML/CSS 工作流。

---

## 资产管理

### 使用 Addressables（不要用 Resources）

```csharp
// ✅ Addressables（异步，内存高效）
using UnityEngine.AddressableAssets;

public async Task SpawnEnemyAsync(string enemyKey) {
    var handle = Addressables.InstantiateAsync(enemyKey);
    var enemy = await handle.Task;

    // 清理：销毁时释放
    Addressables.ReleaseInstance(enemy);
}
```

**优势：** 异步加载、远程内容分发、更好的内存控制。

---

## 渲染

### 自定义渲染通道使用 RenderGraph API（URP/HDRP）

```csharp
// ✅ RenderGraph API（Unity 6+）
public override void RecordRenderGraph(RenderGraph renderGraph, ContextContainer frameData) {
    using (var builder = renderGraph.AddRasterRenderPass<PassData>("My Pass", out var passData)) {
        // 配置通道
        builder.SetRenderFunc((PassData data, RasterGraphContext context) => {
            // 执行命令
        });
    }
}
```

**替代：** 旧版 `CommandBuffer.Execute()` 模式。

---

## 性能

### 使用 Burst 编译器 + Jobs 系统

```csharp
// ✅ Burst 编译的 Job（性能大幅提升）
[BurstCompile]
struct ParticleUpdateJob : IJobParallelFor {
    public NativeArray<float3> Positions;
    public NativeArray<float3> Velocities;
    public float DeltaTime;

    public void Execute(int index) {
        Positions[index] += Velocities[index] * DeltaTime;
    }
}

// 调度执行
var job = new ParticleUpdateJob {
    Positions = positions,
    Velocities = velocities,
    DeltaTime = Time.deltaTime
};
job.Schedule(positions.Length, 64).Complete();
```

**比等效 C# 代码快 20-100 倍。**

---

### 重复对象使用 GPU Instancing

```csharp
// ✅ GPU Instancing（数千个对象，极少绘制调用）
Graphics.RenderMeshInstanced(
    new RenderParams(material),
    mesh,
    0,
    matrices // NativeArray<Matrix4x4>
);
```

---

## 内存管理

### Job 中使用 NativeContainers（不要用托管数组）

```csharp
// ✅ NativeArray（无 GC，兼容 Burst）
NativeArray<int> data = new NativeArray<int>(1000, Allocator.TempJob);
// ... 在 Job 中使用
data.Dispose(); // 需要手动清理

// ✅ 或使用 using 语句
using var data = new NativeArray<int>(1000, Allocator.TempJob);
// 自动释放
```

---

## 多人游戏

### 使用 Netcode for GameObjects（官方方案）

```csharp
// ✅ Unity 官方网络代码
using Unity.Netcode;

public class Player : NetworkBehaviour {
    private NetworkVariable<int> health = new NetworkVariable<int>(100);

    [ServerRpc]
    public void TakeDamageServerRpc(int damage) {
        health.Value -= damage;
    }
}
```

**替代：** UNet（已废弃）、MLAPI（已更名为 Netcode for GameObjects）。

---

## 测试

### 使用 Unity Test Framework（基于 NUnit）

```csharp
// ✅ Play Mode 测试
[UnityTest]
public IEnumerator Player_TakesDamage_HealthDecreases() {
    var player = new GameObject().AddComponent<Player>();
    player.Health = 100;

    player.TakeDamage(25);
    yield return null; // 等待一帧

    Assert.AreEqual(75, player.Health);
}
```

---

## 调试

### 使用日志最佳实践

```csharp
// ✅ 结构化日志（Unity 6+）
using UnityEngine;

Debug.Log($"玩家 {playerName} 得了 {score} 分");

// ✅ 调试代码使用条件编译
#if UNITY_EDITOR || DEVELOPMENT_BUILD
    Debug.DrawRay(transform.position, direction, Color.red);
#endif
```

---

## 汇总：Unity 6 技术栈

| 功能 | 使用（2026）| 避免（旧版）|
|------|------------|------------|
| **输入** | Input System 包 | `Input` 类 |
| **UI** | UI Toolkit | UGUI（Canvas） |
| **ECS** | ISystem + IJobEntity | ComponentSystem |
| **渲染** | URP + RenderGraph | 内置管线 |
| **资产** | Addressables | Resources |
| **任务** | Burst + IJobParallelFor | 协程用于重计算 |
| **多人游戏** | Netcode for GameObjects | UNet |

---

**参考来源：**
- https://docs.unity3d.com/6000.0/Documentation/Manual/BestPracticeGuides.html
- https://docs.unity3d.com/Packages/com.unity.entities@1.3/manual/index.html
- https://docs.unity3d.com/Packages/com.unity.inputsystem@1.11/manual/index.html
