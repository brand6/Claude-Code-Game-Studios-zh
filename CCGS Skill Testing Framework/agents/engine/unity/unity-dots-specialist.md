# Agent 测试规格：unity-dots-specialist

## Agent 概述
职责领域：ECS 架构（IComponentData、ISystem、SystemAPI）、Jobs 系统（IJob、IJobEntity、Burst）、Burst 编译器约束、DOTS 游戏玩法系统，以及混合渲染器。
不负责：MonoBehaviour 游戏玩法代码（gameplay-programmer）、UI 实现（unity-ui-specialist）。
模型层级：Sonnet（默认）。
未分配关卡 ID。

---

## 静态断言（结构检查）

- [ ] `description:` 字段存在且领域明确（引用 ECS / Jobs / Burst / IComponentData）
- [ ] `allowed-tools:` 列表包含 Read、Write、Edit、Bash、Glob、Grep
- [ ] 模型层级为 Sonnet（专员的默认层级）
- [ ] Agent 定义未主张对 MonoBehaviour 游戏玩法或 UI 系统拥有权

---

## 测试用例

### 用例 1：领域内请求——合适的输出
**输入**："将玩家移动系统转换为 ECS。"
**预期行为**：
- 产出：
  - 包含速度、移速和输入向量字段的 `PlayerMovementData : IComponentData` 结构体
  - 使用 `SystemAPI.Query<>` 或 `IJobEntity` 在 `OnUpdate()` 中实现的 `PlayerMovementSystem : ISystem`
  - 通过 `IBaker` 从创作 MonoBehaviour 烘焙玩家初始状态
- 使用 `RefRW<LocalTransform>` 进行位置更新（不使用已废弃的 `Translation`）
- 将 Job 标记为 `[BurstCompile]` 并注明 Burst 兼容性所需的非托管条件
- 不修改输入轮询系统——从现有 `PlayerInputData` 组件读取

### 用例 2：反对使用 MonoBehaviour
**输入**："直接用 MonoBehaviour 做玩家移动就行——更简单。"
**预期行为**：
- 承认简单性论点
- 解释 DOTS 权衡：前期设置更多，但 ECS/Burst 方案可提供项目 ADR 或需求中记录的性能特性
- 若项目已承诺使用 DOTS，则不实现 MonoBehaviour 版本
- 若尚无承诺，则将架构决策上报给 `lead-programmer` / `technical-director` 解决
- 不单方面做出 MonoBehaviour vs DOTS 的决定

### 用例 3：Burst 不兼容的托管内存
**输入**："这个 Burst Job 访问一个 `List<EnemyData>` 来查找最近的敌人。"
**预期行为**：
- 将 `List<T>` 标记为 Burst 编译不兼容的托管类型
- 不批准带有托管内存访问的 Burst Job
- 提供正确替代方案：根据使用场景选用 `NativeArray<EnemyData>`、`NativeList<EnemyData>` 或 `NativeHashMap<>`
- 注明 `NativeArray` 必须显式销毁，或使用 `[DeallocateOnJobCompletion]`
- 产出使用非托管原生容器的修正 Job

### 用例 4：混合访问——DOTS 系统需要 MonoBehaviour 数据
**输入**："DOTS 移动系统需要读取由 MonoBehaviour CameraController 管理的摄像机变换。"
**预期行为**：
- 识别为混合访问场景
- 提供正确的混合模式：将摄像机变换存储在单例 `IComponentData` 中（每帧由 MonoBehaviour 侧通过 `EntityManager.SetComponentData` 更新）
- 作为替代方案，建议使用 `CompanionComponent` / 托管组件方案
- 不从 Burst Job 内部访问 MonoBehaviour——将此标记为不安全
- 在 MonoBehaviour 侧（写入 ECS）和 DOTS 系统侧（从 ECS 读取）分别提供桥接代码

### 用例 5：上下文传递——性能目标
**输入**：技术偏好上下文：目标帧率 60fps，每帧 CPU 脚本预算最大 2ms。请求："为 10000 个敌人实体设计 ECS Chunk 布局。"
**预期行为**：
- 在设计依据中明确引用 2ms CPU 预算
- 为缓存效率设计 `IComponentData` Chunk 布局：
  - 将频繁查询的组件归入同一原型以保持紧密排列
  - 将不常用数据分离到独立组件，保持热数据紧凑
  - 根据 2ms 预算估算实体遍历时间
- 提供内存布局分析（每个实体字节数、以 16KB Chunk 大小计算每 Chunk 可容纳实体数）
- 不设计明显会超出所述 2ms 预算的布局（若超出须明确标记）

---

## 协议合规性

- [ ] 保持在声明的职责范围内（ECS、Jobs、Burst、DOTS 游戏玩法系统）
- [ ] 将仅使用 MonoBehaviour 的游戏玩法重定向给 gameplay-programmer
- [ ] 返回结构化输出（IComponentData 结构体、ISystem 实现、IBaker 创作类）
- [ ] 将 Burst Job 中的托管内存访问标记为编译错误，并提供非托管替代方案
- [ ] 在 DOTS 系统需要与 MonoBehaviour 系统交互时提供混合访问模式
- [ ] 根据提供的性能预算设计 Chunk 布局

---

## 覆盖说明
- ECS 转换（用例 1）必须包含使用 ECS 测试框架（`World`、`EntityManager`）的单元测试
- Burst 不兼容性（用例 3）属于安全关键项——Agent 必须在代码写出前捕获此问题
- Chunk 布局（用例 5）验证 Agent 将量化的性能推理应用于架构决策
