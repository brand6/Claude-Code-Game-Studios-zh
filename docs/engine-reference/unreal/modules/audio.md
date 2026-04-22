# Unreal Engine 5.7 — 音频模块参考

**最后验证：** 2026-02-13
**知识空白：** UE 5.7 MetaSounds 生产就绪

---

## 概述

UE 5.7 音频系统：
- **MetaSounds**：节点式程序化音频（**推荐**，生产就绪）
- **Sound Cues**：旧版节点式音频（简单场景仍可使用）
- **Audio Component**：在 Actor 上播放声音

---

## 基础音频播放

### 在位置播放声音

```cpp
#include "Kismet/GameplayStatics.h"

// ✅ 播放 2D 声音（无空间化）
UGameplayStatics::PlaySound2D(GetWorld(), ExplosionSound);

// ✅ 在位置播放声音（3D 空间音频）
UGameplayStatics::PlaySoundAtLocation(GetWorld(), ExplosionSound, GetActorLocation());

// ✅ 带音量和音调
UGameplayStatics::PlaySoundAtLocation(GetWorld(), ExplosionSound, GetActorLocation(), 0.7f, 1.2f);
```

---

## Audio Component

### Audio Component（持续音效）

```cpp
// 创建音频组件
UAudioComponent* AudioComp = CreateDefaultSubobject<UAudioComponent>(TEXT("Audio"));
AudioComp->SetupAttachment(RootComponent);
AudioComp->SetSound(LoopingAmbience);

// 播放/停止
AudioComp->Play();
AudioComp->Stop();

// 淡入/淡出
AudioComp->FadeIn(2.0f);  // 2 秒淡入
AudioComp->FadeOut(1.5f, 0.0f); // 1.5 秒淡出到音量 0

// 调整音量/音调
AudioComp->SetVolumeMultiplier(0.5f);
AudioComp->SetPitchMultiplier(1.2f);
```

---

## 3D 空间音频

### 衰减设置

```cpp
// 创建 Sound Attenuation 资产：
// 内容浏览器 > 声音 > Sound Attenuation

// 配置：
// - 衰减形状：球体、胶囊体、盒体、锥体
// - 衰减距离：声音变得不可听的距离
// - 衰减函数：线性、对数、反比等

// 在 C++ 中指定：
AudioComp->AttenuationSettings = AttenuationAsset;
```

### 代码覆盖衰减设置

```cpp
FSoundAttenuationSettings AttenuationOverride;
AttenuationOverride.AttenuationShape = EAttenuationShape::Sphere;
AttenuationOverride.FalloffDistance = 1000.0f;
AttenuationOverride.AttenuationShapeExtents = FVector(1000.0f);

AudioComp->AttenuationOverrides = AttenuationOverride;
AudioComp->bOverrideAttenuation = true;
```

---

## MetaSounds（程序化音频）

### 创建 MetaSound Source

1. 内容浏览器 > 声音 > MetaSound Source
2. 打开 MetaSound 编辑器
3. 构建节点图：
   - **输入**：触发器、参数
   - **生成器**：振荡器、噪声、采样
   - **调制器**：包络、LFO
   - **效果**：滤波器、混响、延迟
   - **输出**：音频输出

### 播放 MetaSound

```cpp
// 像普通声音一样播放 MetaSound
UGameplayStatics::PlaySound2D(GetWorld(), MetaSoundSource);

// 或通过 Audio Component
AudioComp->SetSound(MetaSoundSource);
AudioComp->Play();
```

### 设置 MetaSound 参数

```cpp
// 在 MetaSound 中定义参数（带暴露参数的 Input 节点）
// 在 C++ 中设置参数：
AudioComp->SetFloatParameter(FName("Volume"), 0.8f);
AudioComp->SetIntParameter(FName("OctaveShift"), 2);
AudioComp->SetBoolParameter(FName("EnableReverb"), true);
```

---

## Sound Cues（旧版）

### 创建 Sound Cue

1. 内容浏览器 > 声音 > Sound Cue
2. 打开 Sound Cue 编辑器
3. 添加节点：Random、Modulator、Mixer 等

### 使用 Sound Cue

```cpp
// 像普通声音一样播放
UGameplayStatics::PlaySound2D(GetWorld(), SoundCue);
```

---

## Sound Classes 与 Sound Mixes

### Sound Class（音量分组）

```cpp
// 创建 Sound Class：内容浏览器 > 声音 > Sound Class
// 层级：主 > 音乐、音效、对话

// 为声音资产指定：
// Sound Wave > Sound Class = SFX

// 在 C++ 中设置音量：
UAudioSettings* AudioSettings = GetMutableDefault<UAudioSettings>();
// 通过 Sound Class 层级配置
```

### Sound Mix（动态混音）

```cpp
// 创建 Sound Mix 资产
// 定义调整：对话期间降低音乐音量等

// 推送音效混合
UGameplayStatics::PushSoundMixModifier(GetWorld(), DuckedMusicMix);

// 弹出音效混合
UGameplayStatics::PopSoundMixModifier(GetWorld(), DuckedMusicMix);
```

---

## 音频遮蔽与混响

### 音频遮蔽（墙壁阻挡声音）

```cpp
// 在 Audio Component 上启用：
AudioComp->bEnableOcclusion = true;

// 需要带碰撞的几何体
```

### 混响体积

```cpp
// 在关卡中添加 Audio Volume（体积 > Audio Volume）
// 在细节面板配置混响设置
// 在体积内时，Audio Component 自动获取混响效果
```

---

## 常用模式

### 脚步声（随机变奏）

```cpp
// 使用带 Random 节点的 Sound Cue，或：
UPROPERTY(EditAnywhere, Category = "Audio")
TArray<TObjectPtr<USoundBase>> FootstepSounds;

void PlayFootstep() {
    int32 Index = FMath::RandRange(0, FootstepSounds.Num() - 1);
    UGameplayStatics::PlaySoundAtLocation(GetWorld(), FootstepSounds[Index], GetActorLocation());
}
```

### 音乐交叉淡入淡出

```cpp
UAudioComponent* MusicA;
UAudioComponent* MusicB;

void CrossfadeMusic(float Duration) {
    MusicA->FadeOut(Duration, 0.0f);
    MusicB->FadeIn(Duration);
}
```

### 检查声音是否正在播放

```cpp
if (AudioComp->IsPlaying()) {
    // 声音正在播放
}
```

---

## 音频并发

### 限制并发声音数量

```cpp
// 创建 Sound Concurrency 资产：
// 内容浏览器 > 声音 > Sound Concurrency

// 配置：
// - 最大数量：此声音的最大同时实例数
// - 解决规则：停止最旧、停止最安静等

// 指定给声音：
// Sound Wave > Concurrency Settings
```

---

## 性能优化

### 音频优化

```cpp
// 压缩设置（Sound Wave 资产）：
// - Compression Quality: 40（在质量与大小之间取得平衡）
// - Streaming：对大文件（音乐）启用流式传输

// 降低音频混合成本：
// - 通过 Sound Concurrency 限制并发声音数量
// - 使用简单的衰减形状

// 禁用远处 Actor 的音频：
if (Distance > MaxAudibleDistance) {
    AudioComp->Stop();
}
```

---

## 调试

### 音频调试命令

```cpp
// 控制台命令：
// au.Debug.Sounds 1 - 显示活跃声音
// au.3dVisualize.Enabled 1 - 可视化 3D 音频
// stat soundwaves - 显示声波统计
// stat soundmixes - 显示活跃音效混合
```

---

## 来源
- https://docs.unrealengine.com/5.7/en-US/audio-system-in-unreal-engine/
- https://docs.unrealengine.com/5.7/en-US/metasounds-in-unreal-engine/
