# Agent 测试规格：ue-replication-specialist

## Agent 概述
- **职责领域**：UPROPERTY 复制、RPC（Server/Client/NetMulticast）、客户端预测、网络相关性（Net Relevancy）、FArchive/NetSerialize，以及带宽优化
- **不负责**：Gameplay 逻辑（gameplay-programmer）、服务器基础设施与部署（devops-engineer）、GAS 预测（ue-gas-specialist）
- **模型层级**：Sonnet
- **关卡 ID**：无；跨领域裁决委托给 lead-programmer 或 unreal-specialist

---

## 静态断言（结构检查）

- [ ] `description:` 字段存在且领域明确（引用 UE 复制、RPC、客户端预测）
- [ ] `allowed-tools:` 列表与 Agent 角色匹配（Read、Write、Edit、Grep；无部署工具）
- [ ] 模型层级为 Sonnet（专员的默认层级）
- [ ] Agent 定义未主张对服务器基础设施或 GAS 拥有权

---

## 测试用例

### 用例 1：领域内请求——已复制玩家生命值与 OnRep
**输入**："实现一个玩家生命值属性，使其在服务器与所有客户端之间同步，并在生命值变更时触发客户端 UI 回调。"
**预期行为**：
- 使用带 `UPROPERTY(Replicated)` 或 `UPROPERTY(ReplicatedUsing=OnRep_Health)` 的浮点型 `Health` 属性
- 实现 `GetLifetimeReplicatedProps()` 并调用 `DOREPLIFETIME(AMyCharacter, Health)`
- 产出调用 UI 更新委托或函数的 `OnRep_Health()` 实现
- 注明复制方向（仅服务器写 → 客户端接收）
- 提醒不要在非所有者客户端上修改 Health——所有写操作必须通过服务器 RPC

### 用例 2：领域外——服务器基础设施
**输入**："配置我们的专用服务器以实现低延迟的自动伸缩。"
**预期行为**：
- 不产出服务器基础设施配置内容
- 明确声明："服务器配置与部署属于 devops-engineer 的职责范围"
- 将请求重定向给 devops-engineer
- 可选：注明与 UE 相关的服务器配置（如 `DefaultEngine.ini` 中的 `NetServerMaxTickRate`）是在职责范围内的，同时将底层基础设施工作交由 devops-engineer 处理

### 用例 3：安全问题——未验证的 RPC 参数（安全关键）
**输入**："实现 `ServerSpendCurrency`——一个让客户端能够扣减其货币余额的 Server RPC。"
**预期行为**：
- **将此标记为安全问题**：客户端不应自行验证或授权货币消费
- 指出正确的模式：Server RPC 必须在服务器端验证该玩家是否有足够余额，然后再扣减
- 产出包含服务器端验证逻辑的代码（检查余额 >= 花费，拒绝无效请求，记录/踢出作弊行为可选）
- 不在未添加安全注意事项的情况下直接产出不安全的实现
- 不使用 `Reliable` 传输未经验证的货币数量——任何 Reliable RPC 必须具备服务器端授权

### 用例 4：带宽优化——高频 Vector 复制
**输入**："我们每次 Tick 都在复制玩家的 `FVector Position`，占用了大量带宽。"
**预期行为**：
- 识别每次 Tick 复制完整 FVector 为高带宽负担（3 × float32 = 12 字节/Tick）
- 建议量化方案：使用 `FVector_NetQuantize` 或 `FVector_NetQuantize10`
- 建议降低复制频率：非激烈动作时降低 `NetUpdateFrequency`，或改用基于事件的复制
- 注明权衡取舍：量化精度降低，但对移动类数据通常可以接受
- 产出配置示例，而非仅作文字描述

### 用例 5：上下文传递——多人游戏带宽预算
**输入上下文**：项目规范规定每玩家带宽预算为 64KB/s。
**输入**："审查我们的背包物品列表的复制方案，该列表包含 100 个字段并在每次变更时全量发送。"
**预期行为**：
- 将每次变更全量同步 100 个字段与 64KB/s 的预算进行比对
- 标记全量序列化为预算超标风险
- 建议增量复制（仅同步变更的槽位）——可以是自定义 FastArray 序列化，或带脏位追踪的 FFastArraySerializer
- 产出使用 `FFastArraySerializer` 的代码框架
- 注明若背包更新不频繁，可使用 `COND_OwnerOnly` 条件限制复制范围

---

## 协议合规性

- [ ] 保持在声明的职责范围内（UE 复制、RPC、带宽优化）
- [ ] 将 Gameplay 逻辑问题重定向给 gameplay-programmer
- [ ] 将服务器基础设施问题重定向给 devops-engineer
- [ ] 将 GAS 预测问题重定向给 ue-gas-specialist
- [ ] 返回带 UE 复制宏的结构化 C++ 代码（DOREPLIFETIME、OnRep 等）
- [ ] 对含有服务器端授权缺失的 RPC 发出安全警告

---

## 覆盖说明
- 用例 3（未验证的 RPC）是安全关键测试——货币漏洞是多人游戏中最常见的利用载体之一
- 用例 5 验证 Agent 能够在项目规范约束下工作，而非泛泛给出优化建议
- 无自动化运行器；手动审查或通过 `/skill-test` 进行
