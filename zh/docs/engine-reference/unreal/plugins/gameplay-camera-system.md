# Unreal Engine 5.7 — 游戏摄像机系统

**最后验证：** 2026-02-13
**状态：** ⚠️ 实验性（UE 5.5 引入）
**插件：** `GameplayCameras`（内置，在 Plugins 中启用）

---

## 概述

**游戏摄像机系统** 是 UE 5.5 引入的模块化摄像机管理框架，用灵活的节点式系统替代了传统摄像机设置，可处理摄像机模式、混合和情境感知的摄像机行为。

**以下场景使用游戏摄像机系统：**
- 动态摄像机行为（第三人称、瞄准、载具、电影级镜头）
- 情境感知的摄像机切换（战斗、探索、对话）
- 摄像机模式间的平滑混合
- 程序化摄像机运动（摄像机抖动、延迟、偏移）

**⚠️ 警告：** 此插件在 UE 5.5-5.7 中为实验性状态，预期后续版本 API 可能变更。

---

## 核心概念

### 1. **摄像机绑架（Camera Rig）**
- 定义摄像机配置（位置、旋转、视野等）
- 模块化节点图（类似材质编辑器）

### 2. **摄像机导演（Camera Director）**
- 管理当前激活的摄像机绑架
- 处理摄像机绑架之间的混合

### 3. **摄像机节点（Camera Nodes）**
- 摄像机行为的基础构件：
  - **位置节点**：轨道（Orbit）、跟随（Follow）、固定位置
  - **旋转节点**：注视目标（Look At）、匹配 Actor 旋转
  - **修改器**：摄像机抖动、延迟、偏移

---

## 配置

### 1. 启用插件

`Edit > Plugins > Gameplay Cameras > Enabled > Restart`

### 2. 添加摄像机组件

```cpp
#include "GameplayCameras/Public/GameplayCameraComponent.h"

UCLASS()
class AMyCharacter : public ACharacter {
    GENERATED_BODY()

public:
    AMyCharacter() {
        // 创建摄像机组件
        CameraComponent = CreateDefaultSubobject<UGameplayCameraComponent>(TEXT("GameplayCamera"));
        CameraComponent->SetupAttachment(RootComponent);
    }

protected:
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera")
    TObjectPtr<UGameplayCameraComponent> CameraComponent;
};
```

---

## 创建摄像机绑架

### 1. 创建摄像机绑架资产

1. Content Browser > Gameplay > Gameplay Camera Rig
2. 打开摄像机绑架编辑器（节点式图）

### 2. 构建摄像机绑架（示例：第三人称）

**节点设置：**
```
Actor 位置（角色）
  ↓
轨道节点（围绕角色旋转）
  ↓
偏移节点（肩膀偏移）
  ↓
注视节点（注视角色）
  ↓
摄像机输出
```

---

## 摄像机节点

### 位置节点

#### 轨道节点（第三人称）
- 围绕目标 Actor 旋转
- 配置：
  - **轨道距离（Orbit Distance）**：距目标的距离（如 300 单位）
  - **俯仰范围（Pitch Range）**：最小/最大俯仰角
  - **偏航范围（Yaw Range）**：最小/最大偏航角

#### 跟随节点（平滑跟随）
- 带延迟地跟随目标
- 配置：
  - **延迟速度（Lag Speed）**：摄像机追上目标的速度
  - **偏移（Offset）**：距目标的固定偏移

#### 固定位置节点
- 世界空间中的静态摄像机位置

---

### 旋转节点

#### 注视节点
- 将摄像机朝向目标
- 配置：
  - **目标（Target）**：要注视的 Actor 或组件
  - **偏移（Offset）**：注视点偏移（如瞄准头部而非脚部）

#### 匹配 Actor 旋转
- 匹配目标 Actor 的旋转
- 适用于第一人称或载具摄像机

---

### 修改器节点

#### 摄像机抖动
- 添加程序化抖动（如脚步声、爆炸）
- 配置：
  - **抖动模式（Shake Pattern）**：柏林噪声、正弦波、自定义
  - **振幅（Amplitude）**：抖动强度

#### 摄像机延迟
- 对摄像机运动进行平滑阻尼
- 配置：
  - **延迟速度（Lag Speed）**：阻尼系数（0 = 即时，数值越大延迟越明显）

#### 偏移节点
- 在计算位置基础上添加静态偏移
- 适用于肩膀摄像机偏移

---

## 摄像机导演（在绑架间切换）

### 指定摄像机绑架

```cpp
#include "GameplayCameras/Public/GameplayCameraComponent.h"

void AMyCharacter::SetCameraMode(UGameplayCameraRig* NewRig) {
    if (CameraComponent) {
        CameraComponent->SetCameraRig(NewRig);
    }
}
```

### 混合切换摄像机绑架

```cpp
// 在 0.5 秒内混合切换到瞄准摄像机
CameraComponent->BlendToCameraRig(AimingCameraRig, 0.5f);
```

---

## 示例：第三人称 + 瞄准

### 1. 创建两个摄像机绑架

**第三人称绑架：**
```
Actor 位置 → 轨道（距离：300）→ 注视 → 输出
```

**瞄准绑架：**
```
Actor 位置 → 轨道（距离：150）→ 偏移（肩膀）→ 注视 → 输出
```

### 2. 按瞄准状态切换

```cpp
UPROPERTY(EditAnywhere, Category = "Camera")
TObjectPtr<UGameplayCameraRig> ThirdPersonRig;

UPROPERTY(EditAnywhere, Category = "Camera")
TObjectPtr<UGameplayCameraRig> AimingRig;

void StartAiming() {
    CameraComponent->BlendToCameraRig(AimingRig, 0.3f); // 0.3 秒内混合
}

void StopAiming() {
    CameraComponent->BlendToCameraRig(ThirdPersonRig, 0.3f);
}
```

---

## 常用模式

### 越肩摄像机

```
Actor 位置
  ↓
轨道节点（距离：250，偏航偏移：30°）
  ↓
偏移节点（X: 0, Y: 50, Z: 50）// 肩膀偏移
  ↓
注视节点（目标：角色头部）
  ↓
输出
```

---

### 载具摄像机

```
载具位置
  ↓
跟随节点（延迟：0.2）
  ↓
偏移节点（载具后方：X: -400, Z: 150）
  ↓
注视节点（目标：载具）
  ↓
输出
```

---

### 第一人称摄像机

```
角色头部插槽
  ↓
匹配 Actor 旋转
  ↓
输出
```

---

## 摄像机抖动

### 触发摄像机抖动

```cpp
#include "GameplayCameras/Public/GameplayCameraShake.h"

void TriggerExplosionShake() {
    if (APlayerController* PC = GetWorld()->GetFirstPlayerController()) {
        if (UGameplayCameraComponent* CameraComp = PC->FindComponentByClass<UGameplayCameraComponent>()) {
            CameraComp->PlayCameraShake(ExplosionShakeClass, 1.0f);
        }
    }
}
```

---

## 性能建议

- 限制摄像机抖动频率（不要每帧触发）
- 谨慎使用摄像机延迟（高延迟值性能开销较大）
- 缓存摄像机绑架引用（不要每帧搜索）

---

## 调试

### 摄像机调试可视化

```cpp
// 控制台命令：
// GameplayCameras.Debug 1 - 显示活动摄像机绑架信息
// showdebug camera - 显示摄像机调试信息
```

---

## 从传统摄像机迁移

### 旧版弹簧臂 + 摄像机组件

```cpp
// ❌ 旧方式：弹簧臂组件
USpringArmComponent* SpringArm;
UCameraComponent* Camera;

// ✅ 新方式：游戏摄像机组件
UGameplayCameraComponent* CameraComponent;
// 在 Camera Rig 资产中构建轨道 + 注视节点图
```

---

## 局限性（实验性状态）

- **API 不稳定**：预期 UE 5.8+ 中可能有破坏性变更
- **文档有限**：官方文档仍在完善中
- **Blueprint 支持**：主要面向 C++（Blueprint 支持正在改进）
- **生产风险**：发布前请充分测试

---

## 参考资料
- https://docs.unrealengine.com/5.7/en-US/gameplay-cameras-in-unreal-engine/
- UE 5.5+ Release Notes
- **注意：** 此系统为实验性质，请始终查阅最新官方文档以获取 API 变更信息。
