# Unreal Engine 5.7 — 输入模块参考

**最后验证：** 2026-02-13
**知识空白：** UE 5.7 默认使用 Enhanced Input（旧版输入已废弃）

---

## 概述

UE 5.7 输入系统：
- **Enhanced Input**（**推荐**，UE5 默认）：模块化、可重绑定、基于上下文
- **旧版输入**：已废弃，新项目请勿使用

---

## Enhanced Input 系统

### 设置 Enhanced Input

1. **启用插件**：`编辑 > 插件 > Enhanced Input`（UE5 默认启用）
2. **项目设置**：`引擎 > 输入 > 默认类 > 默认 Player Input 类 = EnhancedPlayerInput`

---

### 创建 Input Actions

1. 内容浏览器 > 输入 > Input Action
2. 命名（如 `IA_Jump`、`IA_Move`）
3. 配置：
   - **值类型**：数字（bool）、Axis1D（float）、Axis2D（Vector2D）、Axis3D（Vector）

示例 Input Actions：
- `IA_Jump`：数字（bool）
- `IA_Move`：Axis2D（Vector2D）
- `IA_Look`：Axis2D（Vector2D）
- `IA_Fire`：数字（bool）

---

### 创建 Input Mapping Context

1. 内容浏览器 > 输入 > Input Mapping Context
2. 命名（如 `IMC_Default`）
3. 添加映射：
   - `IA_Jump` → 空格键
   - `IA_Move` → W/A/S/D 键（组合 X/Y）
   - `IA_Look` → 鼠标 XY
   - `IA_Fire` → 鼠标左键

---

### 在 C++ 中绑定输入

```cpp
#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"
#include "InputActionValue.h"

class AMyCharacter : public ACharacter {
public:
    // Input Actions（在蓝图中赋值）
    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Input")
    TObjectPtr<UInputAction> MoveAction;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Input")
    TObjectPtr<UInputAction> LookAction;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Input")
    TObjectPtr<UInputAction> JumpAction;

    UPROPERTY(EditAnywhere, BlueprintReadOnly, Category = "Input")
    TObjectPtr<UInputMappingContext> DefaultMappingContext;

protected:
    virtual void BeginPlay() override {
        Super::BeginPlay();

        // 添加 Input Mapping Context
        if (APlayerController* PC = Cast<APlayerController>(Controller)) {
            if (UEnhancedInputLocalPlayerSubsystem* Subsystem =
                ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(PC->GetLocalPlayer())) {
                Subsystem->AddMappingContext(DefaultMappingContext, 0);
            }
        }
    }

    virtual void SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) override {
        Super::SetupPlayerInputComponent(PlayerInputComponent);

        UEnhancedInputComponent* EIC = Cast<UEnhancedInputComponent>(PlayerInputComponent);
        if (EIC) {
            // 绑定动作
            EIC->BindAction(JumpAction, ETriggerEvent::Started, this, &ACharacter::Jump);
            EIC->BindAction(JumpAction, ETriggerEvent::Completed, this, &ACharacter::StopJumping);

            EIC->BindAction(MoveAction, ETriggerEvent::Triggered, this, &AMyCharacter::Move);
            EIC->BindAction(LookAction, ETriggerEvent::Triggered, this, &AMyCharacter::Look);
        }
    }

    void Move(const FInputActionValue& Value) {
        FVector2D MoveVector = Value.Get<FVector2D>();

        if (Controller) {
            AddMovementInput(GetActorForwardVector(), MoveVector.Y);
            AddMovementInput(GetActorRightVector(), MoveVector.X);
        }
    }

    void Look(const FInputActionValue& Value) {
        FVector2D LookVector = Value.Get<FVector2D>();

        if (Controller) {
            AddControllerYawInput(LookVector.X);
            AddControllerPitchInput(LookVector.Y);
        }
    }
};
```

---

## 输入触发器

### 触发器类型

Input Actions 可配置触发器以控制触发时机：
- **Pressed**：输入开始时
- **Released**：输入结束时
- **Hold**：持续按住一段时间
- **Tap**：快速点按
- **Pulse**：按住时重复触发

### 在编辑器中添加触发器

1. 打开 Input Action 资产
2. 触发器 > 添加 > 选择触发器类型（如 `Hold`）
3. 配置（如 Hold Time = 0.5s）

---

## 输入修改器

### 修改器类型

修改器对输入值进行变换：
- **Negate**：翻转符号（-1 ↔ 1）
- **Dead Zone**：忽略小输入
- **Scalar**：乘以指定值
- **Smooth**：随时间平滑

### 在编辑器中添加修改器

1. 打开 Input Action 资产
2. 修改器 > 添加 > 选择修改器（如 `Negate`）
3. 配置

---

## Input Mapping Context（上下文切换）

### 多上下文切换

```cpp
// 定义上下文
UPROPERTY(EditAnywhere, Category = "Input")
TObjectPtr<UInputMappingContext> DefaultContext;

UPROPERTY(EditAnywhere, Category = "Input")
TObjectPtr<UInputMappingContext> VehicleContext;

// 切换上下文
void EnterVehicle() {
    if (APlayerController* PC = Cast<APlayerController>(Controller)) {
        if (UEnhancedInputLocalPlayerSubsystem* Subsystem =
            ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(PC->GetLocalPlayer())) {
            Subsystem->RemoveMappingContext(DefaultContext);
            Subsystem->AddMappingContext(VehicleContext, 0);
        }
    }
}
```

---

## 旧版输入（已废弃）

### 旧版输入绑定

```cpp
// ❌ 已废弃：新项目请勿使用

void AMyCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent) {
    // 旧版动作绑定
    PlayerInputComponent->BindAction("Jump", IE_Pressed, this, &ACharacter::Jump);

    // 旧版轴绑定
    PlayerInputComponent->BindAxis("MoveForward", this, &AMyCharacter::MoveForward);
}

void MoveForward(float Value) {
    AddMovementInput(GetActorForwardVector(), Value);
}
```

**迁移：** 改用 Enhanced Input。

---

## 手柄输入

### Enhanced Input 下的手柄

```cpp
// Input Mapping Context：
// - IA_Move → 手柄左摇杆
// - IA_Look → 手柄右摇杆
// - IA_Jump → 手柄底部面按钮（A/Cross）

// 只需在 Input Mapping Context 中添加手柄映射，无需修改代码
```

---

## 触摸输入（移动端）

### Enhanced Input 下的触摸

```cpp
// Input Mapping Context：
// - IA_Move → 触摸（虚拟摇杆）
// - IA_Look → 触摸（滑动）

// 使用 Touch Interface 资产配置虚拟控件
```

---

## 运行时重新绑定输入

### 更改按键映射

```cpp
#include "PlayerMappableInputConfig.h"

// 获取子系统
UEnhancedInputLocalPlayerSubsystem* Subsystem = /* 获取子系统 */;

// 获取玩家可映射按键
FPlayerMappableKeySlot KeySlot = FPlayerMappableKeySlot(/*..*/);
FKey NewKey = EKeys::F; // 重绑定到 F 键

// 应用新映射
Subsystem->AddPlayerMappedKey(/*..*/);
```

---

## 输入调试

### 调试输入

```cpp
// 控制台命令：
// showdebug input — 显示输入调试信息

// 记录输入值：
UE_LOG(LogTemp, Warning, TEXT("移动输入：%s"), *MoveVector.ToString());
```

---

## 常用模式

### 检查按键是否按下（快速调试用）

```cpp
// 仅用于调试（不推荐用于游戏逻辑）
if (GetWorld()->GetFirstPlayerController()->IsInputKeyDown(EKeys::SpaceBar)) {
    // 空格键按下中
}
```

---

## 来源
- https://docs.unrealengine.com/5.7/en-US/enhanced-input-in-unreal-engine/
- https://docs.unrealengine.com/5.7/en-US/enhanced-input-action-and-input-mapping-context-in-unreal-engine/
