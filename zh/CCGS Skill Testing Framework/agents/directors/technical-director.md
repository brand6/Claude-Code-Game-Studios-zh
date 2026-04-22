# Agent 测试规格：technical-director

## Agent 摘要
**拥有领域：** 系统架构决策、技术可行性评估、ADR 监督与批准、引擎风险评估、技术阶段关卡。
**不拥有：** 游戏设计决策（creative-director / game-designer）、创意方向、视觉美术风格、生产排期（producer）。
**模型层级：** Opus（多文档综合、高风险架构及阶段关卡裁决）。
**处理的关卡 ID：** TD-SYSTEM-BOUNDARY、TD-FEASIBILITY、TD-ARCHITECTURE、TD-ADR、TD-ENGINE-RISK、TD-PHASE-GATE。

---

## 静态断言（结构性）

通过读取 agent 的 `.claude/agents/technical-director.md` frontmatter 验证：

- [ ] `description:` 字段存在且针对特定领域（引用架构、可行性、ADR — 而非通用描述）
- [ ] `allowed-tools:` 列表可包含用于架构文档的 Read；仅在技术检查有合理需求时包含 Bash
- [ ] 模型层级为 `claude-opus-4-6`，符合 coordination-rules.md（具有关卡综合职能的 directors = Opus）
- [ ] Agent 定义不声明对游戏设计决策或创意方向的权限

---

## 测试用例

### 用例 1：领域内请求 — 适当的输出格式
**场景：** "战斗系统"的架构文档提交审查。文档描述了分层设计：输入层 → 游戏逻辑层 → 表现层，各层之间有明确定义的接口。请求标记为 TD-ARCHITECTURE。
**预期：** 返回 `TD-ARCHITECTURE: APPROVE`，附理由确认系统边界正确分离且接口定义良好。
**断言：**
- [ ] 裁决恰好为 APPROVE / CONCERNS / REJECT 之一
- [ ] 裁决令牌格式为 `TD-ARCHITECTURE: APPROVE`
- [ ] 理由具体引用分层结构和接口定义 — 而非通用架构建议
- [ ] 输出保持在技术范围内 — 不评论该机制是否有趣或符合创意愿景

### 用例 2：领域外请求 — 重定向或升级
**场景：** 编剧请求 technical-director 评审并批准游戏开场过场动画的对白脚本。
**预期：** Agent 拒绝评估对白质量，并重定向至 narrative-director。
**断言：**
- [ ] 不对对白内容或结构做出任何约束性决策
- [ ] 明确指明 `narrative-director` 为正确的处理方
- [ ] 可以指出影响对白的技术约束（例如本地化字符串限制、数据格式），但将所有内容决策交由对方

### 用例 3：关卡裁决 — 正确的裁决词汇
**场景：** 一个多人游戏机制提案要求每帧对所有活跃实体进行视线检测的射线投射。在预期玩家数量下（大型区域 1000 个实体），这是每帧 O(n²) 的操作。请求标记为 TD-FEASIBILITY。
**预期：** 返回 `TD-FEASIBILITY: CONCERNS`，并具体引用 O(n²) 复杂度及使其在目标帧率下不可行的实体数量。
**断言：**
- [ ] 裁决恰好为 APPROVE / CONCERNS / REJECT 之一 — 而非自由文本
- [ ] 裁决令牌格式为 `TD-FEASIBILITY: CONCERNS`
- [ ] 理由包含具体的算法复杂度问题和实体数量阈值
- [ ] 建议至少一种替代方案（例如空间分区、兴趣管理），但不强制要求选择哪种

### 用例 4：冲突升级 — 正确的上级
**场景：** game-designer 希望为每个库存物品添加实时物理模拟（同时在屏幕上显示数百个物品）。technical-director 评估此方案技术成本过高，建议简化模拟。game-designer 表示不同意，认为这对游戏手感至关重要。
**预期：** technical-director 明确陈述技术成本和约束，提出可以达到类似手感的替代实现方案，但明确将最终设计优先级决策交由 creative-director 作为玩家体验权衡的仲裁者。
**断言：**
- [ ] 以具体数据（例如性能预算、预估成本）表达技术顾虑
- [ ] 提出至少一种可降低成本同时保留意图的替代方案
- [ ] 明确将"这是否值得"的决策交由 creative-director — 不单方面削减功能
- [ ] 不声称拥有凌驾于 game-designer 设计意图的权限

### 用例 5：上下文传递 — 使用所提供的上下文
**场景：** Agent 收到一个关卡上下文块，包含目标平台约束：移动端、60fps 目标、2GB 内存上限、不支持计算着色器。一个提议的架构包含 GPU 驱动的渲染管线。
**预期：** 评估引用上下文中的具体硬件约束，识别计算着色器依赖项与所述平台约束不兼容，并返回带有具体引用的 CONCERNS 或 REJECT 裁决。
**断言：**
- [ ] 引用所提供的具体平台约束（移动端、2GB 内存、不支持计算着色器）
- [ ] 不给出与所提供约束脱节的通用性能建议
- [ ] 正确识别与平台约束冲突的架构组件
- [ ] 裁决理由来源于所提供的上下文，而非样板式警告

---

## 协议合规性

- [ ] 仅使用 APPROVE / CONCERNS / REJECT 词汇返回裁决
- [ ] 严守声明的技术领域
- [ ] 将设计优先级冲突交由 creative-director 判断
- [ ] 在输出中使用关卡 ID（例如 `TD-FEASIBILITY: CONCERNS`），而非内联散文裁决
- [ ] 不做约束性游戏设计或创意方向决策

---

## 覆盖说明
- TD-ADR（架构决策记录审批）未覆盖 — 待 /architecture-decision 技能产出 ADR 文档后应补充专项用例。
- 特定引擎版本（例如 Godot 4.6 训练截止后的 API）的 TD-ENGINE-RISK 评估未覆盖 — 推迟至引擎专家集成测试。
- TD-PHASE-GATE（完整技术阶段推进）涉及综合多个子关卡结果，推迟处理。
- 同时触及 TD-ARCHITECTURE 和 TD-ENGINE-RISK 的多领域架构评审未在此覆盖。
