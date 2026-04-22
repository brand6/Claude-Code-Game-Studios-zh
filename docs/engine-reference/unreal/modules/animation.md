# Unreal Engine 5.7 — 动画模块参考

**最后验证：** 2026-02-13
**知识空白：** UE 5.7 动画制作改进、Control Rig 2.0

---

## 概述

UE 5.7 动画系统：
- **Animation Blueprint**：基于状态机的动画逻辑
- **Control Rig**：运行时程序化动画（UE5 生产就绪）
- **IK Rig + Retargeter**：现代重定向系统
- **Sequencer**：过场动画

---

## Animation Blueprint

### 创建 Animation Blueprint

1. 内容浏览器 > 右键 > 动画 > Animation Blueprint
2. 选择父类：`AnimInstance`
3. 选择骨骼

### 动画状态机

```cpp
// 在 Animation Blueprint 事件图中：
// - 状态机驱动动画状态（Idle、Walk、Run、Jump）
// - Blend Space 用于方向移动

// 在 C++ 中访问：
UAnimInstance* AnimInstance = Mesh->GetAnimInstance();
AnimInstance->Montage_Play(AttackMontage);
```

---

## 播放动画 Montage

### Animation Montage

```cpp
// 播放 Montage
UAnimInstance* AnimInstance = GetMesh()->GetAnimInstance();
AnimInstance->Montage_Play(AttackMontage, 1.0f);

// 停止 Montage
AnimInstance->Montage_Stop(0.2f, AttackMontage);

// 检查 Montage 是否正在播放
bool bIsPlaying = AnimInstance->Montage_IsPlaying(AttackMontage);
```

### Montage 通知事件

```cpp
// 在 Animation Montage 中添加通知（右键时间轴 > Add Notify > New Notify）
// 在 C++ 中实现：

UCLASS()
class UMyAnimInstance : public UAnimInstance {
    GENERATED_BODY()

public:
    UFUNCTION()
    void AnimNotify_AttackHit() {
        // 到达通知时调用
        DealDamage();
    }
};
```

---

## Blend Space

### 1D Blend Space（速度混合）

```cpp
// 创建：内容浏览器 > 动画 > Blend Space 1D
// 横轴：速度（0 = 待机，1 = 行走，2 = 跑步）
// 在关键点添加动画

// 在 Anim Blueprint 中使用：
// - 从角色获取速度
// - 输入 Blend Space
```

### 2D Blend Space（方向移动）

```cpp
// 创建：内容浏览器 > 动画 > Blend Space
// 横轴：方向 X（-1 到 1）
// 纵轴：方向 Y（-1 到 1）
// 放置动画（前、后、左、右、斜向）
```

---

## Control Rig（程序化动画）

### 创建 Control Rig

1. 内容浏览器 > 动画 > Control Rig
2. 选择骨骼
3. 构建绑定层级（骨骼、控制器、IK）

### 在 Animation Blueprint 中使用 Control Rig

```cpp
// 将"Control Rig"节点添加到 Anim Blueprint
// 指定 Control Rig 资产
// 在运行时程序化修改骨骼
```

### 在 C++ 中使用 Control Rig

```cpp
// 获取 Control Rig 组件
UControlRig* ControlRig = /* 从动画实例获取 */;

// 设置控制器值
ControlRig->SetControlValue<FVector>(TEXT("IK_Hand_R"), TargetLocation);
```

---

## IK Rig 与重定向（UE5）

### 创建 IK Rig

1. 内容浏览器 > 动画 > IK Rig
2. 选择骨骼
3. 添加 IK 目标（手、脚）
4. 设置求解链

### 重定向动画

1. 为源骨骼创建 IK Rig
2. 为目标骨骼创建 IK Rig
3. 创建 IK Retargeter 资产
4. 指定源和目标 IK Rig
5. 批量重定向动画

### 在 C++ 中重定向

```cpp
// 重定向主要在编辑器中完成
// 动画重定向一次，之后正常使用
```

---

## 动画通知状态（持续时间事件）

### 自定义通知状态

```cpp
UCLASS()
class UAnimNotifyState_Invulnerable : public UAnimNotifyState {
    GENERATED_BODY()

public:
    virtual void NotifyBegin(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation, float TotalDuration, const FAnimNotifyEventReference& EventReference) override {
        // 开始无敌
        AMyCharacter* Character = Cast<AMyCharacter>(MeshComp->GetOwner());
        Character->bIsInvulnerable = true;
    }

    virtual void NotifyEnd(USkeletalMeshComponent* MeshComp, UAnimSequenceBase* Animation, const FAnimNotifyEventReference& EventReference) override {
        // 结束无敌
        AMyCharacter* Character = Cast<AMyCharacter>(MeshComp->GetOwner());
        Character->bIsInvulnerable = false;
    }
};
```

---

## 骨骼网格体与插槽

### 将物体附加到插槽

```cpp
// 在骨骼网格体编辑器中创建插槽（骨骼树 > 添加插槽）

// 将组件附加到插槽
UStaticMeshComponent* Weapon = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("Weapon"));
Weapon->SetupAttachment(GetMesh(), TEXT("hand_r_socket"));
```

---

## 动画曲线

### 使用动画曲线

```cpp
// 为动画添加曲线：
// 动画编辑器 > 曲线 > 添加曲线

// 在 Anim Blueprint 或 C++ 中读取曲线值：
UAnimInstance* AnimInstance = GetMesh()->GetAnimInstance();
float CurveValue = AnimInstance->GetCurveValue(TEXT("MyCurve"));
```

---

## 根运动

### 启用根运动

```cpp
// 在动画序列中：资产细节 > 根运动 > 启用根运动

// 在角色类中：
GetCharacterMovement()->bAllowPhysicsRotationDuringAnimRootMotion = true;
```

---

## 动画层（Linked Anim Graphs）

### 使用 Linked Anim Layers

```cpp
// 为各层创建独立的 Anim Blueprint（如上身、下身）
// 在主 Anim Blueprint 中链接：添加"Linked Anim Graph"节点

// 动态切换层：
UAnimInstance* AnimInstance = GetMesh()->GetAnimInstance();
AnimInstance->LinkAnimClassLayers(NewLayerClass);
```

---

## Sequencer（过场动画）

### 创建序列

1. 内容浏览器 > 过场动画 > 关卡序列
2. 添加轨道：摄像机、角色、动画等

### 从 C++ 播放序列

```cpp
#include "LevelSequenceActor.h"
#include "LevelSequencePlayer.h"

ALevelSequenceActor* SequenceActor = /* 在关卡中生成或查找 */;
SequenceActor->GetSequencePlayer()->Play();
```

---

## 性能技巧

### 动画优化

```cpp
// 骨骼网格体 LOD（细节层次）
// 减少远处角色的骨骼数量

// Anim Blueprint 优化：
// - 使用"动画节点相关性"（不可见时跳过更新）
// - 屏幕外时禁用更新：
GetMesh()->VisibilityBasedAnimTickOption = EVisibilityBasedAnimTickOption::OnlyTickPoseWhenRendered;
```

---

## 调试

### 动画调试可视化

```cpp
// 控制台命令：
// showdebug animation — 显示动画状态信息
// a.VisualizeSkeletalMeshBones 1 — 显示骨骼

// 绘制调试骨骼：
DrawDebugCoordinateSystem(GetWorld(), BoneLocation, BoneRotation, 50.0f, false, -1.0f, 0, 2.0f);
```

---

## 来源
- https://docs.unrealengine.com/5.7/en-US/animation-in-unreal-engine/
- https://docs.unrealengine.com/5.7/en-US/control-rig-in-unreal-engine/
- https://docs.unrealengine.com/5.7/en-US/ik-rig-in-unreal-engine/
