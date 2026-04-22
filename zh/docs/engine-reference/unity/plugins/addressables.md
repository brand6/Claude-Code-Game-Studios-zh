# Unity 6.3 — Addressables

**最后验证：** 2026-02-13
**状态：** 生产就绪
**包：** `com.unity.addressables`（Package Manager）

---

## 概述

**Addressables** 是 Unity 的高级资产管理系统，用异步加载、远程内容分发和更精细的内存控制替代了 `Resources.Load()`。

**以下场景使用 Addressables：**
- 异步资产加载（非阻塞）
- DLC 与远程内容
- 内存优化（按需加载/卸载）
- 资产依赖管理
- 资产数量庞大的大型项目

**以下场景不要使用 Addressables：**
- 小型项目（开销不值得）
- 启动时需立即使用的资产（改用直接引用）

---

## 安装

### 通过 Package Manager 安装

1. `Window > Package Manager`
2. Unity Registry > 搜索 "Addressables"
3. 安装 `Addressables`

---

## 核心概念

### 1. **可寻址资产（Addressable Assets）**
- 标记为"Addressable"的资产（分配唯一键值）
- 可在运行时通过键值加载

### 2. **资产组（Asset Groups）**
- 组织资产（如 "UI"、"武器"、"Level1"）
- 组决定构建设置（本地 vs 远程）

### 3. **异步加载**
- 所有加载操作均为异步（非阻塞）
- 返回 `AsyncOperationHandle`

### 4. **引用计数**
- Addressables 跟踪资产使用情况
- 使用完毕后必须手动释放资产

---

## 配置

### 1. 将资产标记为 Addressable

1. 在 Project 窗口中选择资产
2. Inspector > 勾选 "Addressable"
3. 指定键值（如 "Enemies/Goblin"）

**或通过脚本：**
```csharp
#if UNITY_EDITOR
using UnityEditor.AddressableAssets;
using UnityEditor.AddressableAssets.Settings;

AddressableAssetSettings.AddAssetEntry(guid, "MyAssetKey", "Default Local Group");
#endif
```

---

### 2. 创建资产组

`Window > Asset Management > Addressables > Groups`

- **默认本地组（Default Local Group）**：随构建包打包
- **远程组（Remote Group）**：托管在服务器（CDN）上

---

## 基础加载

### 异步加载资产

```csharp
using UnityEngine.AddressableAssets;
using UnityEngine.ResourceManagement.AsyncOperations;

public class AssetLoader : MonoBehaviour {
    async void Start() {
        // ✅ 异步加载资产
        AsyncOperationHandle<GameObject> handle = Addressables.LoadAssetAsync<GameObject>("Enemies/Goblin");
        await handle.Task;

        if (handle.Status == AsyncOperationStatus.Succeeded) {
            GameObject prefab = handle.Result;
            Instantiate(prefab);
        } else {
            Debug.LogError("资产加载失败");
        }

        // ⚠️ 重要：用完后释放
        Addressables.Release(handle);
    }
}
```

---

### 加载并实例化

```csharp
async void SpawnEnemy() {
    // ✅ 一步完成加载与实例化
    AsyncOperationHandle<GameObject> handle = Addressables.InstantiateAsync("Enemies/Goblin");
    await handle.Task;

    GameObject enemy = handle.Result;
    // 使用 enemy...

    // ✅ 销毁时释放
    Addressables.ReleaseInstance(enemy);
}
```

---

### 批量加载多个资产

```csharp
async void LoadAllWeapons() {
    // 加载所有带 "Weapons" 标签的资产
    AsyncOperationHandle<IList<GameObject>> handle = Addressables.LoadAssetsAsync<GameObject>("Weapons", null);
    await handle.Task;

    foreach (var weapon in handle.Result) {
        Debug.Log($"已加载：{weapon.name}");
    }

    Addressables.Release(handle);
}
```

---

## 资产标签（Labels）

### 指定标签

1. `Window > Asset Management > Addressables > Groups`
2. 选择资产 > Inspector > Labels > 添加标签（如 "Level1"、"UI"）

### 按标签加载

```csharp
// 加载所有带 "Level1" 标签的资产
Addressables.LoadAssetsAsync<GameObject>("Level1", null);
```

---

## 远程内容（DLC）

### 配置远程组

1. 新建组：`Window > Addressables > Groups > Create New Group > Packed Assets`
2. 组设置：
   - **构建路径（Build Path）**：`ServerData/[BuildTarget]`
   - **加载路径（Load Path）**：`http://yourcdn.com/content/[BuildTarget]`

### 构建远程内容

1. `Window > Asset Management > Addressables > Build > New Build > Default Build Script`
2. 将 `ServerData/` 文件夹上传到 CDN
3. 游戏从远程服务器加载资产

---

## 预加载与缓存

### 下载依赖项

```csharp
async void PreloadLevel() {
    // 下载组内所有资产但不加载到内存
    AsyncOperationHandle handle = Addressables.DownloadDependenciesAsync("Level1");
    await handle.Task;

    // 现在 "Level1" 资产已缓存，加载将立即完成
    Addressables.Release(handle);
}
```

### 查看下载大小

```csharp
async void CheckDownloadSize() {
    AsyncOperationHandle<long> handle = Addressables.GetDownloadSizeAsync("Level1");
    await handle.Task;

    long sizeInBytes = handle.Result;
    Debug.Log($"下载大小：{sizeInBytes / (1024 * 1024)} MB");

    Addressables.Release(handle);
}
```

---

## 内存管理

### 释放资产

```csharp
// ✅ 使用完毕后始终释放
Addressables.Release(handle);

// ✅ 对于实例化的对象
Addressables.ReleaseInstance(gameObject);
```

### 查看引用计数

```csharp
// Addressables 使用引用计数
// 当 refCount == 0 时，资产被卸载
```

---

## 资产引用（Inspector 赋值）

### 使用 AssetReference

```csharp
using UnityEngine.AddressableAssets;

public class EnemySpawner : MonoBehaviour {
    // ✅ 在 Inspector 中赋值（拖放即可）
    public AssetReference enemyPrefab;

    async void SpawnEnemy() {
        AsyncOperationHandle<GameObject> handle = enemyPrefab.InstantiateAsync();
        await handle.Task;

        GameObject enemy = handle.Result;
        // 使用 enemy...

        enemyPrefab.ReleaseInstance(enemy);
    }
}
```

---

## 场景

### 加载可寻址场景

```csharp
using UnityEngine.SceneManagement;

async void LoadScene() {
    AsyncOperationHandle<SceneInstance> handle = Addressables.LoadSceneAsync("MainMenu", LoadSceneMode.Additive);
    await handle.Task;

    SceneInstance sceneInstance = handle.Result;
    // 场景已加载

    // 卸载场景
    await Addressables.UnloadSceneAsync(handle).Task;
}
```

---

## 常用模式

### 懒加载（按需加载）

```csharp
Dictionary<string, AsyncOperationHandle<GameObject>> loadedAssets = new();

async Task<GameObject> GetAsset(string key) {
    if (!loadedAssets.ContainsKey(key)) {
        var handle = Addressables.LoadAssetAsync<GameObject>(key);
        await handle.Task;
        loadedAssets[key] = handle;
    }
    return loadedAssets[key].Result;
}
```

---

### 场景卸载时清理

```csharp
void OnDestroy() {
    // 释放所有句柄
    foreach (var handle in loadedAssets.Values) {
        Addressables.Release(handle);
    }
    loadedAssets.Clear();
}
```

---

## 内容目录更新（热更新）

### 检查目录更新

```csharp
async void CheckForUpdates() {
    AsyncOperationHandle<List<string>> handle = Addressables.CheckForCatalogUpdates();
    await handle.Task;

    if (handle.Result.Count > 0) {
        Debug.Log("有可用更新");
        await Addressables.UpdateCatalogs(handle.Result).Task;
    }

    Addressables.Release(handle);
}
```

---

## 性能建议

- 在启动时**预加载**常用资产
- 不再需要时立即**释放**资产
- 使用**标签**批量加载相关资产
- **缓存**远程内容以支持离线使用

---

## 调试

### Addressables 事件查看器

`Window > Asset Management > Addressables > Event Viewer`

- 显示所有加载/释放操作
- 每个资产的内存占用
- 引用计数

### Addressables Profiler

`Window > Asset Management > Addressables > Profiler`

- 实时资产使用情况
- Bundle 加载统计

---

## 从 Resources 迁移

```csharp
// ❌ 旧方式：Resources.Load（同步，会阻塞帧）
GameObject prefab = Resources.Load<GameObject>("Enemies/Goblin");

// ✅ 新方式：Addressables（异步，不阻塞）
var handle = await Addressables.LoadAssetAsync<GameObject>("Enemies/Goblin").Task;
GameObject prefab = handle.Result;
```

---

## 参考资料
- https://docs.unity3d.com/Packages/com.unity.addressables@2.0/manual/index.html
- https://learn.unity.com/tutorial/addressables
