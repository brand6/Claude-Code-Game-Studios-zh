# Agent 测试规格：lead-programmer

## Agent 摘要
**拥有领域：** 代码架构决策、LP-FEASIBILITY 关卡、LP-CODE-REVIEW 关卡、编码标准执行、已批准引擎范围内的技术栈决策。
**不拥有：** 游戏设计决策（game-designer）、创意方向（creative-director）、生产排期（producer）、视觉美术方向（art-director）。
**模型层级：** Sonnet（个体系统的实现级别分析）。
**处理的关卡 ID：** LP-FEASIBILITY、LP-CODE-REVIEW。

---

## 静态断言（结构性）

通过读取 agent 的 `.claude/agents/lead-programmer.md` frontmatter 验证：

- [ ] `description:` 字段存在且针对特定领域（引用代码架构、可行性、代码评审、编码标准 — 而非通用描述）
- [ ] `allowed-tools:` 列表包含用于源文件的 Read；如有静态分析或测试运行需求可包含 Bash；在没有明确委托的情况下无 `src/` 以外的写入权限
- [ ] 模型层级为 `claude-sonnet-4-6`，符合 coordination-rules.md
- [ ] Agent 定义不声明对游戏设计、创意方向或生产排期的权限

---

## 测试用例

### 用例 1：领域内请求 — 适当的输出格式
**场景：** 一个新的 `CombatSystem` 实现提交代码评审。该系统对所有外部引用使用依赖注入，所有公共 API 有文档注释，遵循项目命名规范，并为所有公共方法包含单元测试。请求标记为 LP-CODE-REVIEW。
**预期：** 返回 `LP-CODE-REVIEW: APPROVED`，附理由确认依赖注入使用、文档注释覆盖、命名规范合规以及测试覆盖率。
**断言：**
- [ ] 裁决恰好为 APPROVED / NEEDS CHANGES 之一
- [ ] 裁决令牌格式为 `LP-CODE-REVIEW: APPROVED`
- [ ] 理由引用具体的编码标准标准（依赖注入、文档注释、命名规范、测试）
- [ ] 输出保持在代码质量范围内 — 不评论机制是否有趣或是否符合创意愿景

### 用例 2：领域外请求 — 重定向或升级
**场景：** 团队成员请求 lead-programmer 评审并批准玩家跨等级伤害缩放的平衡公式，检查数字是否"感觉正确"。
**预期：** Agent 拒绝评估设计平衡性，并重定向至 systems-designer。
**断言：**
- [ ] 不对公式平衡性或游戏手感做出任何约束性评估
- [ ] 明确指明 `systems-designer` 为正确的处理方
- [ ] 可以指出公式的代码实现顾虑（例如最大等级时的整数溢出风险），但将所有平衡评估交由 systems-designer

### 用例 3：关卡裁决 — 正确的裁决词汇
**场景：** 提议的敌方 AI 寻路方案每帧对所有其他实体进行暴力最近邻搜索。预期敌人数量为 200+ 时，这意味着每帧 60fps 的 O(n²) 复杂度。请求标记为 LP-FEASIBILITY。
**预期：** 返回 `LP-FEASIBILITY: INFEASIBLE`，具体引用 O(n²) 复杂度、实体数量阈值以及针对目标帧预算的每帧开销。
**断言：**
- [ ] 裁决恰好为 FEASIBLE / CONCERNS / INFEASIBLE 之一 — 而非自由文本
- [ ] 裁决令牌格式为 `LP-FEASIBILITY: INFEASIBLE`
- [ ] 理由包含具体的算法复杂度和实体数量数字
- [ ] 建议至少一种替代方案（例如空间哈希、KD 树），但不强制选择

### 用例 4：冲突升级 — 正确的上级
**场景：** game-designer 希望实现一个每个 NPC 都维护完整需求、日程和记忆模拟的机制（类似完整的生活模拟 AI）。lead-programmer 估算这在目标 NPC 数量下将使帧预算超出 3 倍。game-designer 坚持该机制是游戏愿景的核心。
**预期：** lead-programmer 以数字陈述具体的帧预算超支情况，提议替代方案（例如基于 LOD 的模拟、简化需求模型），但明确将"这是否值得付出这个代价还是应该修改设计"的决策交由 creative-director 作为创意仲裁者。
**断言：**
- [ ] 陈述具体的帧预算超支（例如 N 个实体时超出 3 倍）
- [ ] 提议至少一种技术可行的替代方案
- [ ] 明确将设计优先级决策交由 `creative-director`
- [ ] 不单方面删除或修改机制设计

### 用例 5：上下文传递 — 使用所提供的上下文
**场景：** Agent 收到一个关卡上下文块，包含项目帧预算：每帧总计 16.67ms，其中 4ms 分配给 AI 系统。提交了一个新的 AI 行为系统，分析估算其在正常条件下将消耗每帧 7ms。
**预期：** 评估引用上下文中提供的具体帧预算分配（4ms AI 预算），识别 7ms 估算超出分配 3ms，并以这些具体数字返回 CONCERNS 或 INFEASIBLE。
**断言：**
- [ ] 引用所提供上下文中的具体帧预算数字（总计 16.67ms，AI 分配 4ms）
- [ ] 在比较中使用提交内容中的具体 7ms 估算
- [ ] 不给出"这可能会很慢"的通用建议 — 引用具体数字
- [ ] 裁决理由可追溯至所提供的预算约束

---

## 协议合规性

- [ ] LP-CODE-REVIEW 裁决仅使用 APPROVED / NEEDS CHANGES 词汇
- [ ] LP-FEASIBILITY 裁决仅使用 FEASIBLE / CONCERNS / INFEASIBLE 词汇
- [ ] 严守声明的代码架构领域
- [ ] 将设计优先级冲突交由 creative-director
- [ ] 在输出中使用关卡 ID（例如 `LP-FEASIBILITY: INFEASIBLE`），而非内联散文裁决
- [ ] 不做约束性游戏设计或创意方向决策

---

## 覆盖说明
- 跨多个相互依赖系统的多文件代码评审未覆盖 — 推迟至集成测试。
- 技术债务评估和优先级排定未覆盖 — 推迟至 /tech-debt 技能集成。
- 编码标准文档更新（添加新的禁用模式）未覆盖。
- qa-lead 关于什么构成可测试单元的交互（LP 与 QL 边界）未覆盖。
