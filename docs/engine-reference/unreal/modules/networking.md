# Unreal Engine 5.7 — 网络模块参考

**最后验证：** 2026-02-13
**知识空白：** UE 5.7 网络改进

---

## 概述

UE 5.7 网络系统：
- **客户端-服务器架构**：服务器权威（**推荐**）
- **复制**：自动状态同步
- **RPC（远程过程调用）**：跨网络调用函数
- **相关性**：仅复制相关 Actor 以优化带宽

---

## 基础多人设置

### 在 Actor 上启用复制

```cpp
UCLASS()
class AMyActor : public AActor {
    GENERATED_BODY()

public:
    AMyActor() {
        // ✅ 启用复制
        bReplicates = true;
        bAlwaysRelevant = true; // 始终向所有客户端复制
    }
};
```

### 网络角色检查

```cpp
// 检查角色
if (HasAuthority()) {
    // 在服务器上运行
}

if (GetLocalRole() == ROLE_AutonomousProxy) {
    // 这是拥有者客户端（本地玩家）
}

if (GetRemoteRole() == ROLE_SimulatedProxy) {
    // 这是远程客户端（其他玩家）
}
```

---

## 复制变量

### 基础复制

```cpp
UPROPERTY(Replicated)
int32 Health;

UPROPERTY(Replicated)
FVector Position;

// ✅ 实现 GetLifetimeReplicatedProps
void AMyActor::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const {
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);

    DOREPLIFETIME(AMyActor, Health);
    DOREPLIFETIME(AMyActor, Position);
}
```

### 条件复制

```cpp
// 仅复制给拥有者
DOREPLIFETIME_CONDITION(AMyCharacter, Ammo, COND_OwnerOnly);

// 跳过拥有者（复制给其他所有人）
DOREPLIFETIME_CONDITION(AMyCharacter, TeamID, COND_SkipOwner);

// 仅首次复制
DOREPLIFETIME_CONDITION(AMyCharacter, Score, COND_InitialOnly);
```

### RepNotify（复制时的回调）

```cpp
UPROPERTY(ReplicatedUsing=OnRep_Health)
int32 Health;

UFUNCTION()
void OnRep_Health() {
    // Health 变化时在客户端调用
    UpdateHealthUI();
}

// 实现 GetLifetimeReplicatedProps（同上）
```

---

## RPC（远程过程调用）

### Server RPC（客户端 → 服务器）

```cpp
// 客户端调用，服务器执行
UFUNCTION(Server, Reliable)
void Server_TakeDamage(int32 Damage);

void AMyCharacter::Server_TakeDamage_Implementation(int32 Damage) {
    // 仅在服务器上运行
    Health -= Damage;

    if (Health <= 0) {
        Server_Die();
    }
}

bool AMyCharacter::Server_TakeDamage_Validate(int32 Damage) {
    // 验证输入（防作弊）
    return Damage >= 0 && Damage <= 100;
}
```

### Client RPC（服务器 → 客户端）

```cpp
// 服务器调用，客户端执行
UFUNCTION(Client, Reliable)
void Client_ShowDeathScreen();

void AMyCharacter::Client_ShowDeathScreen_Implementation() {
    // 仅在客户端运行
    ShowDeathUI();
}
```

### Multicast RPC（服务器 → 所有客户端）

```cpp
// 服务器调用，所有客户端执行
UFUNCTION(NetMulticast, Reliable)
void Multicast_PlayExplosion(FVector Location);

void AMyActor::Multicast_PlayExplosion_Implementation(FVector Location) {
    // 在服务器和所有客户端上运行
    UGameplayStatics::SpawnEmitterAtLocation(GetWorld(), ExplosionEffect, Location);
}
```

### RPC 可靠性

```cpp
// Reliable：保证送达（重要事件）
UFUNCTION(Server, Reliable)
void Server_FireWeapon();

// Unreliable：尽力送达（高频更新、位置同步）
UFUNCTION(Server, Unreliable)
void Server_UpdateAim(FRotator AimRotation);
```

---

## 服务器权威模式（推荐）

### 移动示例

```cpp
class AMyCharacter : public ACharacter {
    UPROPERTY(Replicated)
    FVector ServerPosition;

    void Tick(float DeltaTime) override {
        Super::Tick(DeltaTime);

        if (GetLocalRole() == ROLE_AutonomousProxy) {
            // 客户端：将输入发送给服务器
            FVector Input = GetMovementInput();
            Server_Move(Input);

            // 客户端预测（本地移动）
            AddMovementInput(Input);
        }

        if (HasAuthority()) {
            // 服务器：权威位置
            ServerPosition = GetActorLocation();
        } else {
            // 客户端：向服务器位置插值
            FVector NewPos = FMath::VInterpTo(GetActorLocation(), ServerPosition, DeltaTime, 5.0f);
            SetActorLocation(NewPos);
        }
    }

    UFUNCTION(Server, Unreliable)
    void Server_Move(FVector Input);

    void Server_Move_Implementation(FVector Input) {
        // 服务器验证并应用移动
        AddMovementInput(Input);
    }
};
```

---

## 网络相关性（带宽优化）

### 自定义相关性

```cpp
bool AMyActor::IsNetRelevantFor(const AActor* RealViewer, const AActor* ViewTarget, const FVector& SrcLocation) const {
    // 仅在范围内时复制
    float Distance = FVector::Dist(SrcLocation, GetActorLocation());
    return Distance < 5000.0f;
}
```

### 始终相关的 Actor

```cpp
AMyActor() {
    bAlwaysRelevant = true;       // 向所有客户端复制（如 GameState、PlayerController）
    bOnlyRelevantToOwner = true;  // 仅向拥有者复制（如 PlayerController）
}
```

---

## 所有权

### 设置所有者

```cpp
// 指定所有者（对 RPC 和相关性很重要）
MyActor->SetOwner(OwningPlayerController);
```

### 检查所有者

```cpp
if (GetOwner() == PlayerController) {
    // 此 Actor 属于该玩家
}
```

---

## Game Mode 与 Game State

### Game Mode（仅服务器）

```cpp
UCLASS()
class AMyGameMode : public AGameMode {
    GENERATED_BODY()

public:
    // Game Mode 仅在服务器存在
    // 用于服务器端逻辑（生成、计分、规则）
};
```

### Game State（向所有客户端复制）

```cpp
UCLASS()
class AMyGameState : public AGameState {
    GENERATED_BODY()

public:
    // ✅ 向所有客户端复制游戏状态
    UPROPERTY(Replicated)
    int32 RedTeamScore;

    UPROPERTY(Replicated)
    int32 BlueTeamScore;

    virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const override {
        Super::GetLifetimeReplicatedProps(OutLifetimeProps);
        DOREPLIFETIME(AMyGameState, RedTeamScore);
        DOREPLIFETIME(AMyGameState, BlueTeamScore);
    }
};
```

---

## Player Controller 与 Player State

### Player Controller（每个玩家一个）

```cpp
UCLASS()
class AMyPlayerController : public APlayerController {
    GENERATED_BODY()

public:
    // 在服务器和拥有者客户端上存在
    // 用于玩家特定逻辑、输入处理
};
```

### Player State（复制的玩家信息）

```cpp
UCLASS()
class AMyPlayerState : public APlayerState {
    GENERATED_BODY()

public:
    UPROPERTY(Replicated)
    int32 Kills;

    UPROPERTY(Replicated)
    int32 Deaths;

    virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const override {
        Super::GetLifetimeReplicatedProps(OutLifetimeProps);
        DOREPLIFETIME(AMyPlayerState, Kills);
        DOREPLIFETIME(AMyPlayerState, Deaths);
    }
};
```

---

## Sessions 与 Matchmaking

### 创建会话

```cpp
#include "OnlineSubsystem.h"
#include "OnlineSessionSettings.h"

void CreateSession() {
    IOnlineSubsystem* OnlineSub = IOnlineSubsystem::Get();
    IOnlineSessionPtr Sessions = OnlineSub->GetSessionInterface();

    TSharedPtr<FOnlineSessionSettings> SessionSettings = MakeShareable(new FOnlineSessionSettings());
    SessionSettings->bIsLANMatch = false;
    SessionSettings->NumPublicConnections = 4;
    SessionSettings->bShouldAdvertise = true;

    Sessions->CreateSession(0, FName("MySession"), *SessionSettings);
}
```

### 查找会话

```cpp
void FindSessions() {
    IOnlineSubsystem* OnlineSub = IOnlineSubsystem::Get();
    IOnlineSessionPtr Sessions = OnlineSub->GetSessionInterface();

    TSharedRef<FOnlineSessionSearch> SearchSettings = MakeShareable(new FOnlineSessionSearch());
    SearchSettings->bIsLanQuery = false;
    SearchSettings->MaxSearchResults = 20;

    Sessions->FindSessions(0, SearchSettings);
}
```

---

## 性能技巧

### 减少带宽

```cpp
// 对高频更新使用 Unreliable RPC
UFUNCTION(Server, Unreliable)
void Server_UpdatePosition(FVector Pos);

// 条件复制（仅向相关客户端复制）
DOREPLIFETIME_CONDITION(AMyActor, Health, COND_OwnerOnly);

// 限制复制频率
SetReplicationFrequency(10.0f); // 每秒更新 10 次（默认 100 次）
```

---

## 调试

### 网络调试

```cpp
// 控制台命令：
// stat net — 显示网络统计
// stat netplayerupdate — 显示玩家更新统计
// NetEmulation PktLoss=10 — 模拟 10% 丢包
// NetEmulation PktLag=100 — 模拟 100ms 延迟

// 复制调试日志：
UE_LOG(LogNet, Warning, TEXT("正在复制 Health：%d"), Health);
```

---

## 来源
- https://docs.unrealengine.com/5.7/en-US/networking-and-multiplayer-in-unreal-engine/
- https://docs.unrealengine.com/5.7/en-US/actor-replication-in-unreal-engine/
- https://docs.unrealengine.com/5.7/en-US/rpcs-in-unreal-engine/
