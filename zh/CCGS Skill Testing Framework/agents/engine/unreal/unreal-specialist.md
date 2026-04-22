# Agent 测试规格：unreal-specialist

## Agent 概述
- **职责领域**：虚幻引擎模式与架构——Blueprint vs C++ 决策、UE 子系统（GAS、Enhanced Input、Niagara）、UE 项目结构、插件集成，以及引擎级配置
- **不负责**：美术风格与视觉方向（art-director）、服务器基础设施与部署（devops-engineer）、UI/UX 流程设计（ux-designer）
- **模型层级**：Sonnet
- **关卡 ID**：无；将关卡裁决委托给 technical-director

---

## 静态断言（结构检查）

- [ ] `description:` 字段存在且领域明确（引用虚幻引擎）
- [ ] `allowed-tools:` 列表与 Agent 角色匹配（Read、Write 用于 UE 项目文件；无部署工具）
- [ ] 模型层级为 Sonnet（专员的默认层级）
- [ ] Agent 定义未主张超出声明职责范围的权限（不涉及美术、不涉及服务器基础设施）

---

## 测试用例

### 用例 1：领域内请求——Blueprint vs C++ 决策依据
**输入**："连击攻击系统应该用 Blueprint 还是 C++ 实现？"
**预期行为**：
- 提供结构化决策依据：复杂度、复用频率、团队技能，以及性能需求
- 推荐 C++：适用于每帧调用或跨 5 个以上技能类型共享的系统
- 推荐 Blueprint：适用于设计师可调参数和一次性逻辑
- 在缺乏项目上下文时不单方面给出最终结论——会提出澄清问题
- 输出为结构化形式（条件表格或项目符号列表），而非随意表达的意见

### 用例 2：领域外请求——Unity C# 代码
**输入**："写一个处理玩家生命值并在死亡时触发 Unity 事件的 C# MonoBehaviour。"
**预期行为**：
- 不产出 Unity C# 代码
- 明确声明："本项目使用虚幻引擎；Unity 的等价物在 UE C++ 中是 ActorComponent，或 Blueprint Actor Component"
- 如有需要，可主动提供 UE 等价方案
- 不重定向到 Unity 专员（框架中无此角色）

### 用例 3：领域边界——UE5.4 API 需求
**输入**："我需要使用 UE5.4 中引入的新 Motion Matching API。"
**预期行为**：
- 标记 UE5.4 是特定版本，LLM 训练覆盖可能有限
- 建议在采信任何 API 建议之前，先与官方虚幻文档或项目 engine-reference 目录进行交叉验证
- 提供尽力而为的 API 指导，并附上明确的不确定性标记（如"请对照 UE5.4 发行说明验证此内容"）
- 不在未添加注意事项的情况下静默产出过时或不正确的 API 签名

### 用例 4：冲突——核心系统中的 Blueprint 意大利面
**输入**："我们的复制逻辑完全写在一个深度嵌套的 Blueprint 事件图中，包含 300 多个节点且无函数封装，越来越难以维护。"
**预期行为**：
- 识别为 Blueprint 架构问题，而非小的风格问题
- 建议将核心复制逻辑迁移到 C++ ActorComponent 或 Gameplay Ability 系统
- 注明所需协调：对复制架构的更改必须由 lead-programmer 参与
- 不在未向用户说明重构规模的情况下单方面宣布"迁移到 C++"
- 产出具体的迁移建议，而非模糊的意见

### 用例 5：上下文传递——版本对应的 API 建议
**输入上下文**：项目 engine-reference 文件注明虚幻引擎 5.3。
**输入**："如何为新角色设置 Enhanced Input 输入动作？"
**预期行为**：
- 使用 UE5.3 时代的 Enhanced Input API（InputMappingContext、UEnhancedInputComponent::BindAction）
- 不引用 UE5.3 之后引入的 API（若引用须标记为可能不可用）
- 在回复中引用项目所述引擎版本
- 提供具体的、版本锚定的代码或 Blueprint 节点名称

---

## 协议合规性

- [ ] 保持在声明的职责范围内（虚幻引擎模式、Blueprint/C++、UE 子系统）
- [ ] 将 Unity 或其他引擎的请求重定向，不产出错误引擎的代码
- [ ] 返回结构化结果（条件表格、决策树、迁移计划），而非随意表达的意见
- [ ] 在产出 API 建议前明确标记版本不确定性
- [ ] 在架构规模的重构中与 lead-programmer 协调，而非单方面决策

---

## 覆盖说明
- 无 Agent 行为测试的自动化运行器——需手动审查或通过 `/skill-test` 进行
- 版本意识（用例 3、用例 5）是此 Agent 最高风险的失效模式；引擎版本变更时须定期测试
- 用例 4 与 lead-programmer 的集成属于协调性测试，而非技术正确性测试
