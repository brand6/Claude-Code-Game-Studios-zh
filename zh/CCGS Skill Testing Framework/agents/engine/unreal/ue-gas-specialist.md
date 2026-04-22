# Agent 测试规格：ue-gas-specialist

## Agent 概述
- **职责领域**：Gameplay Ability System（GAS）——UGameplayAbility、UGameplayEffect、UAttributeSet、GameplayTags、AbilityTasks，以及 GAS 客户端预测
- **不负责**：能力状态的 UI 显示（ue-umg-specialist）、底层网络序列化（ue-replication-specialist）、美术资源（art-director）
- **模型层级**：Sonnet
- **关卡 ID**：无；跨领域裁决委托给 unreal-specialist 或 lead-programmer

---

## 静态断言（结构检查）

- [ ] `description:` 字段存在且领域明确（引用 GAS——UGameplayAbility、UGameplayEffect、UAttributeSet、GameplayTags）
- [ ] `allowed-tools:` 列表包含 Read、Write、Edit，无服务器或部署工具
- [ ] 模型层级为 Sonnet（专员的默认层级）
- [ ] Agent 定义未主张对 UI 显示或底层复制序列化拥有权

---

## 测试用例

### 用例 1：领域内请求——含冷却的 Dash 技能
**输入**："使用 GAS 实现一个具有 1.5 秒冷却时间的 Dash 技能。"
**预期行为**：
- 定义继承 `UGameplayAbility` 的 `UGA_Dash` 类
- 使用 `UGameplayEffect` 并将 `DurationPolicy` 设为 `HasDuration`（持续时间 1.5 秒）实现冷却效果
- 在 `UGA_Dash::CanActivateAbility()` 中通过 `GameplayTag` 阻断来阻止重复激活（如 `Ability.Cooldown.Dash`）
- 产出用于移动偏移的 `UAbilityTask_ApplyRootMotionConstantForce` 或等价的 AbilityTask
- 代码结构符合 GAS 约定（构造函数初始化标志、ActivateAbility 生命周期）

### 用例 2：领域内——GAS 复制模式
**输入**："我们的多人 GAS 游戏在同步 Gameplay Effects 时出现延迟——应该选择哪种复制模式？"
**预期行为**：
- 解释三种 GAS 复制模式：Full（全量，适用于单人/小型多人）、Mixed（混合，适用于玩家主控角色）、Minimal（最小，适用于 AI/NPC）
- 根据游戏类型推荐特定模式（如多人动作游戏使用 Mixed）
- 说明客户端预测的影响：使用 Mixed/Full 模式时，预测的 Gameplay Effects 会立即在客户端本地应用
- 不将 GAS 复制配置错误地指向 ue-replication-specialist——这属于 GAS 配置，而非底层复制

### 用例 3：领域边界——Tag 层级结构不匹配导致技能无法激活
**输入**："Dash 技能未触发，但我已在技能资源中添加了 `Ability.Dash` tag，并在 AbilitySystemComponent 上授予了 `Character.Movement.Dash` tag。"
**预期行为**：
- 识别 GameplayTag 层级结构不匹配
- 解释激活时的 tag 匹配规则：GrantedTags 和 ActivationRequiredTags 必须对应正确
- 明确区分所使用的具体 GAS tag 槽位：ActivationRequiredTags、ActivationBlockedTags、OwnedTagsContainer
- 提供诊断步骤：使用 `UAbilitySystemComponent::GetActivatableGameplayAbilitySpecsByAllMatchingTags` 确认 tag 解析
- 不在未提供 tag 匹配规则解释的情况下直接给出修正后的 tag 字符串

### 用例 4：领域冲突——属性叠加
**输入**："当护盾 GameplayEffect 和护甲 GameplayEffect 同时应用时，我们不确定它们是否应当叠加。最近因这个问题出现了平衡性 Bug。"
**预期行为**：
- 识别为 GAS 叠加策略问题（`GameplayEffectStackingType`：`AggregateBySource`、`AggregateByTarget`、`NoStacking` 等）
- 解释可用的叠加策略，并说明各自对护甲/护盾叠加逻辑的影响
- 注明平衡性影响：叠加方式会直接影响有效 HP 的伤害计算
- 标记此决策需要与 game-designer 或 systems-designer 协调以确定预期的游戏感受
- 产出多种叠加配置方案（非单一的主观答案），并说明各自的平衡性含义

### 用例 5：上下文传递——使用已有 AttributeSet
**输入上下文**：项目已有一个包含以下属性的 `UBaseAttributeSet`：Health、MaxHealth、Stamina、Defense、AttackPower。
**输入**："为连击攻击系统添加一个 `ComboMultiplier` 属性。"
**预期行为**：
- 将 `ComboMultiplier` 添加到已有的 `UBaseAttributeSet`，而非创建新的 AttributeSet
- 提供正确的 UPROPERTY 宏声明和 `GAMEPLAYATTRIBUTE_VALUE_GETTER`/`SETTER` 访问器模板
- 注明属性复制注意事项（若多人项目需设为 `Replicated`）
- 不忽略已有的 AttributeSet 上下文，也不建议创建单独的 AttributeSet 仅用于存储 ComboMultiplier

---

## 协议合规性

- [ ] 保持在声明的职责范围内（GAS——Ability、Effect、AttributeSet、Tag、AbilityTask）
- [ ] 将 UI 状态显示请求重定向给 ue-umg-specialist
- [ ] 将底层序列化问题重定向给 ue-replication-specialist
- [ ] 在叠加策略决策中调用 game-designer / systems-designer 参与
- [ ] 返回结构化 GAS 代码，符合 UE C++ / GAS 约定

---

## 覆盖说明
- 用例 3（Tag 层级结构）是高频问题；建议针对 tag 配置错误定期测试
- 用例 4（叠加策略）验证 Agent 不自行做出平衡性决策——这是设计领域，而非纯技术问题
- 无自动化运行器；手动审查或通过 `/skill-test` 进行
