# Unity 6.3 — 动画模块参考

**最后验证：** 2026-02-13
**知识空白：** Unity 6 动画改进、Timeline 增强

---

## 概述

Unity 6.3 动画系统：
- **Animator Controller（Mecanim）**：基于状态机（推荐）
- **Timeline**：过场动画序列、剧情演出
- **Animation Rigging**：程序化运行时动画
- **旧版 Animation**：已废弃，不要使用

---

## 与 2022 LTS 的主要变更

### Animation Rigging 包（Unity 6 生产就绪）

```csharp
// 安装：Package Manager > Animation Rigging
// 运行时 IK、瞄准约束、程序化动画
```

### Timeline 改进
- 性能更优
- 更多轨道类型
- 改进的信号系统

---

## Animator Controller（Mecanim）

### 基本设置

```csharp
// 创建：Assets > Create > Animator Controller
// 添加到 GameObject：Add Component > Animator
// 指定控制器：Animator > Controller = YourAnimatorController
```

### 状态转换

```csharp
Animator animator = GetComponent<Animator>();

// ✅ 触发转换
animator.SetTrigger("Jump");

// ✅ Bool 参数
animator.SetBool("IsRunning", true);

// ✅ Float 参数（混合树）
animator.SetFloat("Speed", currentSpeed);

// ✅ Integer 参数
animator.SetInteger("WeaponType", 2);
```

### 动画层
- **基础层**：默认动画（移动）
- **Override 层**：替换基础层（如换武器）
- **Additive 层**：叠加在基础层上（如呼吸、瞄准偏移）

```csharp
// 设置层权重（0-1）
animator.SetLayerWeight(1, 0.5f); // 50% 混合
```

---

## 混合树

### 1D 混合树（速度混合）

```csharp
// 站立（Speed = 0）→ 走路（Speed = 0.5）→ 奔跑（Speed = 1.0）
animator.SetFloat("Speed", moveSpeed);
```

### 2D 混合树（方向移动）

```csharp
// X 轴：横向移动（-1 到 1）
// Y 轴：前进/后退（-1 到 1）
animator.SetFloat("MoveX", input.x);
animator.SetFloat("MoveY", input.y);
```

---

## 动画事件

### 从动画片段触发事件

```csharp
// 在 Animation 窗口中添加：右键点击时间轴 > Add Animation Event
// 必须在 GameObject 上有对应方法：

public void OnFootstep() {
    // 播放脚步声
    AudioSource.PlayClipAtPoint(footstepClip, transform.position);
}

public void OnAttackHit() {
    // 造成伤害
    DealDamageInFrontOfPlayer();
}
```

---

## 根骨骼运动

### 通过动画驱动角色移动

```csharp
Animator animator = GetComponent<Animator>();
animator.applyRootMotion = true; // 根据动画移动角色

void OnAnimatorMove() {
    // 自定义根骨骼运动处理
    transform.position += animator.deltaPosition;
    transform.rotation *= animator.deltaRotation;
}
```

---

## Animation Rigging（Unity 6+）

### IK（逆向动力学）

```csharp
// 安装：Package Manager > Animation Rigging
// 添加：Rig Builder 组件 + Rig GameObject

// Two Bone IK（手臂/腿部）
// - 添加 Two Bone IK Constraint
// - 指定 Tip（手/脚）、Mid（肘/膝）、Root（肩/髋）
// - 设置 Target（手/脚应到达的目标位置）

// 运行时控制：
TwoBoneIKConstraint ikConstraint = rig.GetComponentInChildren<TwoBoneIKConstraint>();
ikConstraint.data.target = targetTransform;
ikConstraint.weight = 1f; // 0-1 混合权重
```

### 瞄准约束（注视目标）

```csharp
// 角色注视目标
MultiAimConstraint aimConstraint = rig.GetComponentInChildren<MultiAimConstraint>();
aimConstraint.data.sourceObjects[0] = new WeightedTransform(targetTransform, 1f);
```

---

## Timeline（过场动画）

### 基本 Timeline 设置

```csharp
// 创建：Assets > Create > Timeline
// 添加到 GameObject：Add Component > Playable Director
// 指定 Timeline：Playable Director > Playable = YourTimeline

// 通过脚本播放：
PlayableDirector director = GetComponent<PlayableDirector>();
director.Play();
```

### Timeline 轨道
- **Activation Track**：启用/禁用 GameObject
- **Animation Track**：在 Animator 上播放动画
- **Audio Track**：同步音频播放
- **Cinemachine Track**：摄像机运动
- **Signal Track**：在指定时间触发事件

### 信号系统（事件）

```csharp
// 创建 Signal 资产：Assets > Create > Signals > Signal
// 在 Timeline 轨道中添加 Signal Emitter
// 在 GameObject 上添加 Signal Receiver 组件

public class CutsceneEvents : MonoBehaviour {
    public void OnDialogueStart() {
        // 由 Signal 触发
    }
}
```

---

## 动画播放控制

### 直接播放动画（无状态机）

```csharp
// ✅ CrossFade（平滑过渡）
animator.CrossFade("Attack", 0.2f); // 0.2秒过渡

// ✅ Play（立即切换）
animator.Play("Idle");

// ❌ 避免使用：旧版 Animation 组件
Animation anim = GetComponent<Animation>(); // 已废弃
```

---

## 动画曲线

### 自定义属性动画

```csharp
// 在 Animation 窗口：Add Property > Custom Component > 你的脚本 > 你的 Float

public class WeaponTrail : MonoBehaviour {
    public float trailIntensity; // 由动画片段驱动

    void Update() {
        // 强度由动画曲线控制
        trailRenderer.startWidth = trailIntensity;
    }
}
```

---

## 性能优化

### 剔除设置
- `Animator > Culling Mode`：
  - **Always Animate**：始终更新（开销大）
  - **Cull Update Transforms**：屏幕外停止更新骨骼（推荐）
  - **Cull Completely**：屏幕外完全停止动画

### LOD（细节层级）
- 为远处角色使用更简单的动画
- 减少 LOD 网格的骨架骨骼数量

---

## 常用模式

### 检测动画是否播放完毕

```csharp
AnimatorStateInfo stateInfo = animator.GetCurrentAnimatorStateInfo(0);
if (stateInfo.IsName("Attack") && stateInfo.normalizedTime >= 1.0f) {
    // 攻击动画已结束
}
```

### 覆盖动画速度

```csharp
animator.speed = 1.5f; // 150% 速度
```

### 获取当前动画名称

```csharp
AnimatorClipInfo[] clipInfo = animator.GetCurrentAnimatorClipInfo(0);
string currentClip = clipInfo[0].clip.name;
```

---

## 调试

### Animator 窗口
- `Window > Animation > Animator`
- 可视化状态机、查看当前激活状态

### Animation 窗口
- `Window > Animation > Animation`
- 编辑动画片段、添加动画事件

---

## 参考资料
- https://docs.unity3d.com/6000.0/Documentation/Manual/AnimationOverview.html
- https://docs.unity3d.com/Packages/com.unity.animation.rigging@1.3/manual/index.html
- https://docs.unity3d.com/Packages/com.unity.timeline@1.8/manual/index.html
