# Agent 测试规格：ue-blueprint-specialist

## Agent 概述
- **职责领域**：Blueprint 架构、Blueprint/C++ 边界、Blueprint 图表质量、Blueprint 性能优化、Blueprint Function Library 设计
- **不负责**：C++ 实现（engine-programmer 或 gameplay-programmer）、美术资源或着色器、UI/UX 流程设计（ux-designer）
- **模型层级**：Sonnet
- **关卡 ID**：无；跨领域裁决委托给 unreal-specialist 或 lead-programmer

---

## 静态断言（结构检查）

- [ ] `description:` 字段存在且领域明确（引用 Blueprint 架构与优化）
- [ ] `allowed-tools:` 列表与 Agent 角色匹配（Read 用于 Blueprint 项目文件；无服务器或部署工具）
- [ ] 模型层级为 Sonnet（专员的默认层级）
- [ ] Agent 定义未主张对 C++ 实现决策拥有权

---

## 测试用例

### 用例 1：领域内请求——Blueprint 图表性能审查
**输入**："审查我们的 AI 行为 Blueprint。其中有基于 Tick 的逻辑每帧运行，同时为 30 个 NPC 检查视线。"
**预期行为**：
- 将 Tick 密集型逻辑识别为性能问题
- 建议从 EventTick 切换到事件驱动模式（感知系统事件、计时器，或降低轮询频率）
- 标记同时进行视线检查的每个 NPC 成本
- 提出替代方案：AIPerception 组件事件、错开 Tick 分组，或如果 Blueprint 开销经测量较大则移至 C++
- 输出为结构化形式：已识别的问题、估算的影响、列出的替代方案

### 用例 2：领域外请求——C++ 实现
**输入**："为这个技能冷却系统编写 C++ 实现。"
**预期行为**：
- 不产出 C++ 实现代码
- 提供冷却逻辑的 Blueprint 等价方案（如使用 Timeline 或 GAS 启用时的 GameplayEffect）
- 明确声明："C++ 实现由 engine-programmer 或 gameplay-programmer 负责；我可以展示 Blueprint 方案，或描述 Blueprint 调用 C++ 的边界"
- 可选：注明冷却逻辑复杂度何时需要 C++ 后端

### 用例 3：领域边界——Blueprint 中不安全的原始指针访问
**输入**："我们的 Blueprint 在调用 GetOwner() 之后立即访问返回对象上的组件，不做有效性检查。"
**预期行为**：
- 将此标记为运行时崩溃风险：GetOwner() 在某些生命周期状态下可能返回 null
- 提供正确的 Blueprint 模式：任何属性/组件访问前先使用 IsValid() 节点
- 注明 Blueprint 中对 Actor 派生引用的空值检查不是可选项
- 不在未解释原因的情况下静默修复代码

### 用例 4：Blueprint 图表复杂度——Function Library 重构准备
**输入**："我们的主 GameMode Blueprint 在单个图表中有 600 多个节点，伤害计算逻辑在 8 个地方重复。"
**预期行为**：
- 将其诊断为可维护性和可测试性问题
- 建议将重复逻辑提取到 Blueprint Function Library（BFL）
- 描述 BFL 的结构方式：计算逻辑用纯函数、任何 Blueprint 均可静态调用
- 注明：若伤害逻辑对性能敏感或与 C++ 共享，可能需要升级为 unreal-specialist 审查
- 输出为具体的重构计划，而非模糊的建议

### 用例 5：上下文传递——Blueprint 复杂度预算
**输入上下文**：项目规范规定每个 Blueprint 事件图表最多 100 个节点，超出后必须强制提取到 Function Library。
**输入**："这是我们的背包 Blueprint 图表 [展示 150 个节点]，可以发布吗？"
**预期行为**：
- 将所述的 150 个节点与项目规范中的 100 个节点预算进行比对
- 标记图表超出复杂度阈值
- 不批准其现状
- 产出候选子图表列表，用于提取到 Function Library 以使主图表回归预算范围内

---

## 协议合规性

- [ ] 保持在声明的职责范围内（Blueprint 架构、性能、图表质量）
- [ ] 将 C++ 实现请求重定向给 engine-programmer 或 gameplay-programmer
- [ ] 返回结构化结果（问题/影响/替代方案格式），而非随意表达的意见
- [ ] 主动执行 Blueprint 安全模式（空值检查、IsValid）
- [ ] 在评估图表复杂度时引用项目规范

---

## 覆盖说明
- 用例 3（空指针安全）是安全关键测试——这是发布崩溃的常见来源
- 用例 5 要求项目规范中包含明确的节点预算；若未配置，Agent 应注明缺失并建议设置
- 无自动化运行器；手动审查或通过 `/skill-test` 进行
