# Unreal Engine 5.7 — 当前最佳实践

**最后验证：** 2026-02-13

UE5 现代模式，这些内容可能不在 LLM 的训练数据中。
以下是截至 UE 5.7 的生产就绪推荐方案。

---

## 项目设置

### 新项目使用 UE 5.7
- 最新特性：Megalights、生产就绪的 Substrate 和 PCG
- 更好的性能和稳定性

### 选择合适的渲染特性
- **Lumen**：实时全局光照（大多数项目**推荐**）
- **Nanite**：高精度网格虚拟化几何体（详细环境**推荐**）
- **Megalights**：数百万动态灯光（复杂光照**推荐**）
- **Substrate**：模块化材质系统（新项目**推荐**）

---

## C++ 编码

### 使用现代 C++ 特性（UE5.7 支持 C++20）

```cpp
// ✅ 使用 TObjectPtr<T>（UE5 类型安全指针）
UPROPERTY()
TObjectPtr<UStaticMeshComponent> MeshComp;

// ✅ 结构化绑定
if (auto [bSuccess, Value] = TryGetValue(); bSuccess) {
    // 使用 Value
}

// ✅ 概念与约束（C++20）
template<typename T>
concept Damageable = requires(T t, float damage) {
    { t.TakeDamage(damage) } -> std::same_as<void>;
};
```

### 使用 UPROPERTY() 进行垃圾回收

```cpp
// ✅ UPROPERTY 确保 GC 不会回收此对象
UPROPERTY()
TObjectPtr<AActor> MyActor;

// ❌ 裸指针可能变成悬空指针
AActor* MyActor; // 危险！可能被垃圾回收
```

### 使用 UFUNCTION() 暴露给蓝图

```cpp
// ✅ 可从蓝图调用
UFUNCTION(BlueprintCallable, Category="Combat")
void TakeDamage(float Damage);

// ✅ 可在蓝图中实现
UFUNCTION(BlueprintImplementableEvent, Category="Combat")
void OnDeath();
```

---

## 蓝图最佳实践

### Blueprint vs C++ 的选择

- **C++**：核心玩法系统、性能敏感代码、底层引擎交互
- **Blueprint**：快速原型、内容创作、数据驱动逻辑、设计师工作流

### 蓝图性能技巧

```cpp
// ✅ 谨慎使用 Event Tick（开销大）
// 优先使用计时器或事件

// ✅ 使用蓝图原生化（Blueprint → C++）
// 项目设置 > 打包 > Blueprint 原生化

// ✅ 缓存频繁访问的组件
// 不要每帧调用 GetComponent
```

---

## 渲染（UE 5.7）

### 使用 Lumen 进行全局光照

```cpp
// 启用：项目设置 > 引擎 > 渲染 > 动态全局光照方法 = Lumen
// 实时 GI，无需烘焙光照贴图（推荐）
```

### 使用 Nanite 处理高精度网格

```cpp
// 在静态网格体上启用：细节 > Nanite 设置 > 启用 Nanite 支持
// 自动 LOD 数百万三角形（详细网格推荐）
```

### 使用 Megalights 处理复杂光照（UE 5.5+）

```cpp
// 启用：项目设置 > 引擎 > 渲染 > Megalights = 已启用
// 支持数百万动态灯光，成本极低
```

### 使用 Substrate 材质（5.7 生产就绪）

```cpp
// 启用：项目设置 > 引擎 > Substrate > 启用 Substrate
// 模块化、物理精确材质（新项目推荐）
```

---

## Enhanced Input 系统

### 设置 Enhanced Input

```cpp
// 1. 创建 Input Action（IA_Jump）
// 2. 创建 Input Mapping Context（IMC_Default）
// 3. 添加映射：IA_Jump → 空格键

// C++ 设置：
#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"

void AMyCharacter::BeginPlay() {
    Super::BeginPlay();

    if (APlayerController* PC = Cast<APlayerController>(GetController())) {
        if (UEnhancedInputLocalPlayerSubsystem* Subsystem =
            ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(PC->GetLocalPlayer())) {
            Subsystem->AddMappingContext(DefaultMappingContext, 0);
        }
    }
}

void AMyCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) {
    UEnhancedInputComponent* EIC = Cast<UEnhancedInputComponent>(PlayerInputComponent);
    EIC->BindAction(JumpAction, ETriggerEvent::Started, this, &ACharacter::Jump);
    EIC->BindAction(MoveAction, ETriggerEvent::Triggered, this, &AMyCharacter::Move);
}

void AMyCharacter::Move(const FInputActionValue& Value) {
    FVector2D MoveVector = Value.Get<FVector2D>();
    AddMovementInput(GetActorForwardVector(), MoveVector.Y);
    AddMovementInput(GetActorRightVector(), MoveVector.X);
}
```

---

## Gameplay Ability System（GAS）

### 使用 GAS 处理复杂玩法

```cpp
// ✅ GAS 适用于：技能、Buff、伤害计算、冷却
// 模块化、可扩展、支持多人

// 安装：启用"Gameplay Abilities"插件

// 示例技能：
UCLASS()
class UGA_Fireball : public UGameplayAbility {
    GENERATED_BODY()

public:
    virtual void ActivateAbility(...) override {
        // 技能逻辑
        SpawnFireball();
        CommitAbility(); // 提交消耗/冷却
    }
};
```

---

## World Partition（大型世界）

### 使用 World Partition 构建开放世界

```cpp
// 启用：世界设置 > 启用 World Partition
// 根据玩家位置自动流式加载世界格子

// 数据层：组织内容（如"Gameplay"、"Audio"、"Lighting"）
// 运行时数据层：运行时加载/卸载
```

---

## Niagara（视觉特效）

### 使用 Niagara（不用 Cascade）

```cpp
// 创建：内容浏览器 > 右键 > FX > Niagara 系统
// GPU 加速、节点式粒子系统（推荐）

// 生成粒子：
UNiagaraComponent* NiagaraComp = UNiagaraFunctionLibrary::SpawnSystemAtLocation(
    GetWorld(),
    ExplosionSystem,
    GetActorLocation()
);
```

---

## MetaSounds（音频）

### 使用 MetaSounds 实现程序化音频

```cpp
// 创建：内容浏览器 > 右键 > 声音 > MetaSound Source
// 节点式音频，复杂逻辑替代 Sound Cue（推荐）

// 播放 MetaSound：
UAudioComponent* AudioComp = UGameplayStatics::SpawnSound2D(
    GetWorld(),
    MetaSoundSource
);
```

---

## 复制（多人游戏）

### 服务器权威模式

```cpp
// ✅ 客户端发送输入，服务器验证并复制
UFUNCTION(Server, Reliable)
void Server_Move(FVector Direction);

void AMyCharacter::Server_Move_Implementation(FVector Direction) {
    // 服务器验证并应用移动
    AddMovementInput(Direction);
}
```

### 复制重要状态

```cpp
// ✅ 复制重要状态
UPROPERTY(Replicated)
int32 Health;

void AMyCharacter::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const {
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);
    DOREPLIFETIME(AMyCharacter, Health);
}
```

---

## 性能优化

### 使用对象池

```cpp
// ✅ 复用对象，而不是频繁 Spawn/Destroy
TArray<AActor*> ProjectilePool;

AActor* GetPooledProjectile() {
    for (AActor* Proj : ProjectilePool) {
        if (!Proj->IsActive()) {
            Proj->SetActive(true);
            return Proj;
        }
    }
    // 池已耗尽，生成新对象
    return SpawnNewProjectile();
}
```

### 使用实例化静态网格体

```cpp
// ✅ 层级实例化静态网格体组件（HISM）
// 单次 Draw Call 渲染数千个相同网格体
UHierarchicalInstancedStaticMeshComponent* HISM = CreateDefaultSubobject<UHierarchicalInstancedStaticMeshComponent>(TEXT("Trees"));
for (int i = 0; i < 1000; i++) {
    HISM->AddInstance(FTransform(RandomLocation));
}
```

---

## 调试

### 使用日志

```cpp
// ✅ 结构化日志
UE_LOG(LogTemp, Warning, TEXT("玩家血量：%d"), Health);

// 自定义日志类别
DECLARE_LOG_CATEGORY_EXTERN(LogMyGame, Log, All);
DEFINE_LOG_CATEGORY(LogMyGame);
UE_LOG(LogMyGame, Error, TEXT("严重错误！"));
```

### 使用 Visual Logger

```cpp
// ✅ 可视化调试
#include "VisualLogger/VisualLogger.h"

UE_VLOG_SEGMENT(this, LogTemp, Log, StartPos, EndPos, FColor::Red, TEXT("射线检测"));
UE_VLOG_LOCATION(this, LogTemp, Log, TargetLocation, 50.f, FColor::Green, TEXT("目标"));
```
---

## 总结：UE 5.7 推荐技术栈

| 特性 | 2026 推荐方案 | 说明 |
|------|-------------|------|
| **光照** | Lumen + Megalights | 实时全局光照，支持数百万灯光 |
| **几何体** | Nanite | 高精度网格，自动 LOD |
| **材质** | Substrate | 模块化、物理精确 |
| **输入** | Enhanced Input | 可重绑定、模块化 |
| **视觉特效** | Niagara | GPU 加速 |
| **音频** | MetaSounds | 程序化音频 |
| **世界流式加载** | World Partition | 大型开放世界 |
| **游戏玩法** | Gameplay Ability System | 复杂技能、Buff |

---

**参考来源：**
- https://docs.unrealengine.com/5.7/en-US/
- https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-7-release-notes