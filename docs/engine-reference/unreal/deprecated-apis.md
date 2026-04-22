# Unreal Engine 5.7 — 废弃 API

**最后验证：** 2026-02-13

废弃 API 及其替代方案快速查表。
格式：**不要用 X** → **改用 Y**

---

## 输入

| 废弃项 | 替代方案 | 说明 |
|--------|---------|------|
| `InputComponent->BindAction()` | Enhanced Input `BindAction()` | 新输入系统 |
| `InputComponent->BindAxis()` | Enhanced Input `BindAxis()` | 新输入系统 |
| `PlayerController->GetInputAxisValue()` | Enhanced Input 动作值 | 新输入系统 |

**迁移：** 安装 Enhanced Input 插件，创建 Input Actions 和 Input Mapping Contexts。

---

## 渲染

| 废弃项 | 替代方案 | 说明 |
|--------|---------|------|
| 旧版材质节点 | Substrate 材质节点 | 5.7 Substrate 生产就绪 |
| 前向着色（默认） | 延迟着色 + Lumen | Lumen 是 UE5 默认选项 |
| 旧版光照工作流 | Lumen 全局光照 | 实时 GI |

---

## 世界构建

| 废弃项 | 替代方案 | 说明 |
|--------|---------|------|
| UE4 World Composition | World Partition（UE5） | 大型世界流式加载 |
| Level Streaming Volumes | World Partition 数据层 | 更好的关卡流式加载 |

---

## 动画

| 废弃项 | 替代方案 | 说明 |
|--------|---------|------|
| 旧版动画重定向 | IK Rig + IK Retargeter | UE5 重定向系统 |
| 旧版 Control Rig | Control Rig 2.0 | 生产就绪的绑定系统 |

---

## 玩法

| 废弃项 | 替代方案 | 说明 |
|--------|---------|------|
| `UGameplayStatics::LoadStreamLevel()` | World Partition 流式加载 | 使用数据层 |
| 硬编码输入绑定 | Enhanced Input 系统 | 可重绑定、模块化输入 |

---

## Niagara（视觉特效）

| 废弃项 | 替代方案 | 说明 |
|--------|---------|------|
| Cascade 粒子系统 | Niagara | Cascade 已完全废弃 |

---

## 音频

| 废弃项 | 替代方案 | 说明 |
|--------|---------|------|
| 旧版音频混合器 | MetaSounds | 程序化音频系统 |
| Sound Cue（复杂逻辑） | MetaSounds | 更强大的节点式音频 |

---

## 网络

| 废弃项 | 替代方案 | 说明 |
|--------|---------|------|
| `DOREPLIFETIME()`（基础版） | `DOREPLIFETIME_CONDITION()` | 条件复制以优化带宽 |

---

## C++ 脚本

| 废弃项 | 替代方案 | 说明 |
|--------|---------|------|
| `TSharedPtr<T>`（用于 UObject） | `TObjectPtr<T>` | UE5 类型安全指针 |
| 手动 RTTI 检查 | `Cast<T>()` / `IsA<T>()` | 类型安全转换 |

---

## 快速迁移示例

### 输入示例
```cpp
// ❌ 废弃写法
void AMyCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) {
    PlayerInputComponent->BindAction("Jump", IE_Pressed, this, &ACharacter::Jump);
}

// ✅ Enhanced Input
#include "EnhancedInputComponent.h"

void AMyCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) {
    UEnhancedInputComponent* EIC = Cast<UEnhancedInputComponent>(PlayerInputComponent);
    if (EIC) {
        EIC->BindAction(JumpAction, ETriggerEvent::Started, this, &ACharacter::Jump);
    }
}
```

### 材质示例
```cpp
// ❌ 废弃：旧版材质
// 使用标准材质图（仍可用，但不推荐）

// ✅ Substrate 材质
// 启用：项目设置 > 引擎 > Substrate > 启用 Substrate
// 在材质编辑器中使用 Substrate 节点
```

### World Partition 示例
```cpp
// ❌ 废弃：Level Streaming Volumes
// 手动加载/卸载关卡

// ✅ World Partition
// 启用：世界设置 > 启用 World Partition
// 使用数据层进行流式加载
```

### 粒子系统示例
```cpp
// ❌ 废弃：Cascade
UParticleSystemComponent* PSC = CreateDefaultSubobject<UParticleSystemComponent>(TEXT("Particles"));

// ✅ Niagara
UNiagaraComponent* NiagaraComp = CreateDefaultSubobject<UNiagaraComponent>(TEXT("Niagara"));
```

### 音频示例
```cpp
// ❌ 废弃：Sound Cue 用于复杂逻辑
// 使用 Sound Cue 编辑器节点

// ✅ MetaSounds
// 创建 MetaSound Source 资产，使用节点式音频
```

---

## 总结：UE 5.7 技术栈

| 功能 | 2026 年推荐 | 旧版（避免使用） |
|------|------------|-----------------|
| **输入** | Enhanced Input | 旧版输入绑定 |
| **材质** | Substrate | 旧版材质系统 |
| **光照** | Lumen + Megalights | 光照贴图 + 有限灯光 |
| **粒子** | Niagara | Cascade |
| **音频** | MetaSounds | Sound Cue（逻辑用） |
| **世界流式** | World Partition | World Composition |
| **动画重定向** | IK Rig + Retargeter | 旧版重定向 |
| **几何体** | Nanite（高精度） | 标准静态网格 LOD |

---

**来源：**
- https://docs.unrealengine.com/5.7/en-US/deprecated-and-removed-features/
- https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-7-release-notes
