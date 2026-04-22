# Unity 6.3 — Cinemachine

**最后验证：** 2026-02-13
**状态：** 生产就绪
**包：** `com.unity.cinemachine` v3.0+（Package Manager）

---

## 概述

**Cinemachine** 是 Unity 的虚拟摄像机系统，无需手动编写脚本即可实现专业、动态的摄像机行为，是 Unity 摄像机开发的行业标准。

**以下场景使用 Cinemachine：**
- 第三人称跟随摄像机
- 过场动画与电影级镜头
- 摄像机混合与过渡
- 动态构图取景
- 画面抖动与摄像机特效

**⚠️ 知识缺口：** Cinemachine 3.0（Unity 6）是对 2.x 的重大重写，许多 API 名称和组件均已变更。

---

## 安装

### 通过 Package Manager 安装

1. `Window > Package Manager`
2. Unity Registry > 搜索 "Cinemachine"
3. 安装 `Cinemachine`（版本 3.0+）

---

## 核心概念

### 1. **虚拟摄像机（Virtual Cameras）**
- 定义摄像机行为（位置、旋转、镜头参数）
- 可同时存在多个虚拟摄像机，但同一时刻只有一个处于"激活"状态

### 2. **Cinemachine Brain**
- 挂载在主摄像机上的组件
- 在虚拟摄像机之间进行混合
- 将虚拟摄像机设置应用到 Unity Camera 上

### 3. **优先级（Priorities）**
- 虚拟摄像机各有优先级数值
- 优先级最高的摄像机处于激活状态
- 优先级变更时平滑过渡

---

## 基础配置

### 1. 为主摄像机添加 Cinemachine Brain

```csharp
// 创建首个虚拟摄像机时会自动添加
// 也可手动添加：Add Component > Cinemachine Brain
```

### 2. 创建虚拟摄像机

`GameObject > Cinemachine > Cinemachine Camera`

这将创建一个带有默认设置的 **CinemachineCamera** GameObject。

---

## 虚拟摄像机组件

### CinemachineCamera（Unity 6 / Cinemachine 3.0+）

```csharp
using Unity.Cinemachine;

public class CameraController : MonoBehaviour {
    public CinemachineCamera virtualCamera;

    void Start() {
        // 设置优先级（越高越优先激活）
        virtualCamera.Priority = 10;

        // 设置跟随目标
        virtualCamera.Follow = playerTransform;

        // 设置观察目标
        virtualCamera.LookAt = playerTransform;
    }
}
```

---

## 跟随模式（Body 组件）

### 第三人称跟随（轨道跟随）

```csharp
// 在 Inspector 中：
// CinemachineCamera > Body > 3rd Person Follow

// 配置：
// - Shoulder Offset: (0.5, 0, 0) 用于肩膀视角
// - Camera Distance: 5.0
// - Vertical Damping: 0.5（平滑上下移动）
```

### 取景构图（平滑跟随）

```csharp
// CinemachineCamera > Body > Position Composer

// 配置：
// - Screen Position: 居中 (0.5, 0.5)
// - Dead Zone: 目标在此区域内时不移动摄像机
// - Damping: 平滑跟随
```

### 硬锁定（精确跟随）

```csharp
// CinemachineCamera > Body > Hard Lock to Target
// 摄像机完全匹配目标位置（无偏移或阻尼）
```

---

## 瞄准模式（Aim 组件）

### 构图器（取景目标）

```csharp
// CinemachineCamera > Aim > Composer

// 配置：
// - Tracked Object Offset: 瞄准目标头部而非脚部
// - Screen Position: 目标在画面中的位置
// - Dead Zone: 目标在此区域内时不旋转摄像机
```

### 跟随目标朝向

```csharp
// CinemachineCamera > Aim > Rotate With Follow Target
// 摄像机旋转与目标旋转保持一致（如第一人称）
```

---

## 摄像机间混合

### 基于优先级的混合

```csharp
public CinemachineCamera normalCamera; // 优先级：10
public CinemachineCamera aimCamera;    // 优先级：5

void StartAiming() {
    // 将瞄准摄像机设为更高优先级
    aimCamera.Priority = 15; // 现在处于激活状态
    // Brain 自动从 normalCamera 混合到 aimCamera
}

void StopAiming() {
    aimCamera.Priority = 5; // 恢复正常
}
```

### 自定义混合时长

```csharp
// 创建自定义混合资产：
// Assets > Create > Cinemachine > Cinemachine Blender Settings

// 在 Cinemachine Brain 中：
// - Custom Blends = 你的资产
// - 为每对摄像机配置混合时长
```

---

## 摄像机抖动

### 冲量源（触发抖动）

```csharp
using Unity.Cinemachine;

public class ExplosionShake : MonoBehaviour {
    public CinemachineImpulseSource impulseSource;

    void Explode() {
        // 触发摄像机抖动
        impulseSource.GenerateImpulse();
    }
}
```

### 冲量监听器（接收抖动）

```csharp
// 为 CinemachineCamera 添加：
// Add Component > CinemachineImpulseListener

// 冲量监听器自动接收附近冲量源发出的抖动信号
```

---

## 自由视角摄像机（鼠标环绕第三人称）

### Cinemachine Free Look

```csharp
// GameObject > Cinemachine > Cinemachine Free Look

// 创建 3 个轨道（顶部、中部、底部），根据垂直输入混合
// 配置：
// - Orbit Radius: 距目标的距离
// - Height Offset: 每个轨道的摄像机高度
// - X/Y Axis: 鼠标或摇杆输入
```

---

## 状态驱动摄像机（基于 Animator）

### Cinemachine State-Driven Camera

```csharp
// GameObject > Cinemachine > Cinemachine State-Driven Camera

// 配置：
// - Animated Target: 带 Animator 的角色
// - Layer: 要跟踪的 Animator 层
// - State: 为每个动画状态（Idle、Run、Jump 等）指定摄像机

// 摄像机根据动画状态自动切换
```

---

## 轨道摄像机（过场动画）

### Cinemachine Dolly Track

```csharp
// 1. 创建样条曲线：GameObject > Cinemachine > Cinemachine Spline

// 2. 创建轨道摄像机：
//    GameObject > Cinemachine > Cinemachine Camera
//    Body > Spline Dolly
//    指定样条曲线

// 3. 在样条曲线上为轨道位置添加动画（Timeline 或脚本）
```

---

## 常用模式

### 第三人称跟随摄像机

```csharp
// CinemachineCamera
// - Follow: 玩家 Transform
// - Body: 3rd Person Follow（肩膀偏移，距离：5）
// - Aim: Composer（将玩家取景居中）
```

---

### 瞄准摄像机（拉近）

```csharp
// 普通摄像机（优先级 10）：
//   - Distance: 5.0

// 瞄准摄像机（优先级 5）：
//   - Distance: 2.0
//   - FOV: 更窄

// 脚本：
void StartAiming() {
    aimCamera.Priority = 15; // 混合到瞄准摄像机
}
```

---

### 过场动画摄像机序列

```csharp
// 使用 Timeline：
// 1. 创建 Timeline（Assets > Create > Timeline）
// 2. 添加 Cinemachine Track
// 3. 将虚拟摄像机作为片段添加
// 4. Timeline 自动在摄像机之间混合
```

---

## 从 Cinemachine 2.x（Unity 2021）迁移

### API 变更（Unity 6 / Cinemachine 3.0）

```csharp
// ❌ 旧版（Cinemachine 2.x）：
CinemachineVirtualCamera vcam;
vcam.m_Follow = target;

// ✅ 新版（Cinemachine 3.0+）：
CinemachineCamera vcam;
vcam.Follow = target; // 更简洁的 API
```

**主要变更：**
- `CinemachineVirtualCamera` → `CinemachineCamera`
- `m_Follow`、`m_LookAt` → `Follow`、`LookAt`（去除 "m_" 前缀）
- 组件名称更加清晰
- 性能提升

---

## 性能建议

- 限制激活的虚拟摄像机数量（仅在需要时激活）
- 改用低优先级摄像机，而非频繁销毁/创建
- 距玩家较远时禁用虚拟摄像机

---

## 调试

### Cinemachine 调试

```csharp
// Window > Analysis > Cinemachine Debugger
// 显示当前激活摄像机、混合信息、镜头质量
```

---

## 参考资料
- https://docs.unity3d.com/Packages/com.unity.cinemachine@3.0/manual/index.html
- https://learn.unity.com/tutorial/cinemachine
