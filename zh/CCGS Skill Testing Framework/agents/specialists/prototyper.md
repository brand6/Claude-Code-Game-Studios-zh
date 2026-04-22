# Agent 测试规格：prototyper

## Agent 概述
- **职责领域**：`prototypes/` 目录中的快速原型、概念验证与机制可行性测试；有意放宽质量标准以追求速度
- **不负责**：正式生产代码（gameplay-programmer）、正式设计文档（game-designer）、正式生产架构（lead-programmer / technical-director）
- **模型层级**：Sonnet
- **关卡 ID**：无；有时在原型结论阶段接收 game-designer 或 producer 的上下文

---

## 静态断言（结构检查）

- [ ] `description:` 字段存在且明确（引用快速原型 / 概念验证）
- [ ] `allowed-tools:` 列表仅包含 `prototypes/` 范围内的写入工具
- [ ] 模型层级为 Sonnet（专员的默认层级）
- [ ] Agent 定义未主张对 `src/` 生产代码、设计文档或生产架构拥有权

---

## 测试用例

### 用例 1：领域内请求——合适的输出
**输入**："在2小时内为卡牌游戏原型设计一个抽牌机制。不需要精美图形，只需验证核心循环是否有趣。"
**预期行为**：
- 在 `prototypes/card-draw-mechanic/` 中产出最小可运行原型
- 不要求测试、文档注释或编码标准合规——在原型中允许硬编码值
- 实现核心循环：牌库、抽牌、手牌管理
- 包含 `prototypes/card-draw-mechanic/README.md`，说明：验证的假设、运行方法、观察要点
- 不编写任何东西到 `src/` 中

### 用例 2：领域外请求——正确重定向
**输入**："抽牌原型验证通过。现在将其实现为生产代码并集成到游戏中。"
**预期行为**：
- 不产出生产实现代码
- 明确声明生产代码实现属于 `gameplay-programmer` 的职责范围
- 将请求重定向给 `gameplay-programmer`
- 提供一份交接文档，说明：原型验证了什么、哪些决策值得保留、哪些应在生产阶段重写

### 用例 3：原型完成——记录结论
**输入**："卡牌抽取原型通过了3轮游戏测试。连击系统有效，但随机奖励令人感到平淡。"
**预期行为**：
- 在 `prototypes/card-draw-mechanic/` 中创建 `conclusion.md`
- 按标准格式记录：
  - 假设（待验证的内容）
  - 游戏测试方法（运行了多少局，参与者是谁）
  - 裁定：**VALIDATED**（已验证）
  - 主要发现（连击有效 / 随机平淡）
  - 建议（如何在生产中继续）
  - 路由给：`gameplay-programmer` 进行生产实现

### 用例 4：原型失败——记录失败
**输入**："物理解谜原型：经过4轮游戏测试，玩家无法理解力学，谜题无法玩通。放弃该方向。"
**预期行为**：
- 在 `prototypes/physics-puzzle/` 中创建 `conclusion.md`
- 使用 **ABANDONED**（已放弃）裁定，不美化失败
- 记录具体失败原因（如：力学过于隐晦、玩家心智模型与物理系统不符）
- 提出替代方向供 game-designer 考虑
- 不因沉没成本而建议继续追加投入

### 用例 5：上下文传递——引擎感知原型
**上下文输入**：项目引擎为 Godot 4.6，脚本语言为 GDScript。请求："为新的跳墙机制创建一个快速原型。"
**预期行为**：
- 使用 GDScript 产出原型（不使用 C# 或 GDNative）
- 使用 Godot 节点类型（CharacterBody2D/3D、Node3D）符合 Godot 4.x 规范
- 写入 `prototypes/wall-jump/` 而非 `src/`
- 若原型使用了 4.6 版之后可能已变更的 API，注明说明

---

## 协议合规

- [ ] 仅写入 `prototypes/` 目录——绝不写入 `src/`、`design/` 或生产目录
- [ ] 将生产实现请求重定向给 gameplay-programmer，并附交接文档
- [ ] 产出结构化原型结论文档（VALIDATED/ABANDONED），不口头总结
- [ ] 提醒原型代码不符合生产质量标准
- [ ] 使用项目配置的引擎和语言，而非默认假设

---

## 覆盖说明
- 结论文档（用例 3 和用例 4）是核心产物——没有结论就没有可传递给 game-designer 的原型价值
- 失败记录（用例 4）确认 Agent 能正视负面结果，不给失败方向续命
- 生产重定向（用例 2）验证 Agent 维护 prototypes/ 与 src/ 之间的严格分离
- 无自动运行器；请手动审查或通过 `/skill-test`
