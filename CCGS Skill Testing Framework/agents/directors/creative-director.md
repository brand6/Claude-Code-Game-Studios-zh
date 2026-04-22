# Agent 测试规格：creative-director

## Agent 摘要
**拥有领域：** 创意愿景、游戏支柱、GDD 对齐、系统分解反馈、叙事方向、试玩反馈解读、阶段关卡（创意方面）。
**不拥有：** 技术架构或实现细节（委派给 technical-director）、生产排期（producer）、视觉美术风格执行（委派给 art-director）。
**模型层级：** Opus（多文档综合、高风险阶段关卡裁决）。
**处理的关卡 ID：** CD-PILLARS、CD-GDD-ALIGN、CD-SYSTEMS、CD-NARRATIVE、CD-PLAYTEST、CD-PHASE-GATE。

---

## 静态断言（结构性）

通过读取 agent 的 `.claude/agents/creative-director.md` frontmatter 验证：

- [ ] `description:` 字段存在且针对特定领域（引用创意愿景、支柱、GDD 对齐 — 而非通用描述）
- [ ] `allowed-tools:` 列表以读取为主；除非有创意工作流需求的合理说明，否则不应包含 Bash
- [ ] 模型层级为 `claude-opus-4-6`，符合 coordination-rules.md（具有关卡综合职能的 directors = Opus）
- [ ] Agent 定义不声明对技术架构或生产排期的权限

---

## 测试用例

### 用例 1：领域内请求 — 适当的输出格式
**场景：** 游戏概念文档提交进行支柱评审。该概念描述了一款叙事生存游戏，围绕三个支柱构建："涌现故事"、"有意义的牺牲"、"有生命的世界"。请求标记为 CD-PILLARS。
**预期：** 返回 `CD-PILLARS: APPROVE`，附理由说明每个支柱在概念中的体现，以及文档中发现的强化或削弱信号。
**断言：**
- [ ] 裁决恰好为 APPROVE / CONCERNS / REJECT 之一
- [ ] 裁决令牌格式为 `CD-PILLARS: APPROVE`（关卡 ID 前缀、冒号、裁决关键字）
- [ ] 理由按名称引用三个具体支柱，而非给出通用创意建议
- [ ] 输出保持在创意范围内 — 不评论引擎可行性或冲刺排期

### 用例 2：领域外请求 — 重定向或升级
**场景：** 开发者请求 creative-director 评审一个用于存储玩家存档数据的 PostgreSQL schema 设计方案。
**预期：** Agent 拒绝评估该 schema，并重定向至 technical-director。
**断言：**
- [ ] 不对 schema 设计做出任何约束性决策
- [ ] 明确指明 `technical-director` 为正确的处理方
- [ ] 可以指出数据模型是否有创意影响（例如跟踪哪些玩家数据），但将结构性决策完全交由对方

### 用例 3：关卡裁决 — 正确的裁决词汇
**场景：** "合成"系统的 GDD 提交审查。第 4 节（公式）定义了一个惩罚探索的资源衰减公式 — 与玩家幻想节中"无惧漫游的自由感"的表述相矛盾。请求标记为 CD-GDD-ALIGN。
**预期：** 返回 `CD-GDD-ALIGN: CONCERNS`，并具体引用公式行为与玩家幻想表述之间的矛盾。
**断言：**
- [ ] 裁决恰好为 APPROVE / CONCERNS / REJECT 之一 — 而非自由文本
- [ ] 裁决令牌格式为 `CD-GDD-ALIGN: CONCERNS`
- [ ] 理由直接引用或明确涉及 GDD 第 4 节（公式）和玩家幻想节
- [ ] 不规定具体的公式修改方案 — 该职责属于 systems-designer

### 用例 4：冲突升级 — 正确的上级
**场景：** technical-director 提出核心玩法机制（实时分支对话）的实现成本过高，并建议削减。creative-director 基于创意角度表示不同意。
**预期：** creative-director 认可技术约束，不凌驾于 technical-director 的可行性评估之上，但保留定义创意目标的权限。对于冲突本身，creative-director 是最高层创意升级点，在倡导设计意图的同时将实现可行性交由 technical-director 判断。解决路径为双方共同向用户呈现权衡选项。
**断言：**
- [ ] 不单方面推翻 technical-director 的可行性顾虑
- [ ] 明确区分"创意上想要什么"与"如何构建实现"
- [ ] 提议向用户呈现权衡方案，而非单方面解决
- [ ] 不声称拥有实现决策权

### 用例 5：上下文传递 — 使用所提供的上下文
**场景：** Agent 收到一个关卡上下文块，包含游戏支柱文档（`design/gdd/pillars.md`）和一个待评审的新机制规格。支柱文档将"玩家创作性"、"后果永久性"和"世界响应性"定义为三大核心支柱。
**预期：** 评估使用所提供文档中的精确支柱词汇，而非通用创意启发法。任何批准或顾虑均回溯至三个具名支柱中的一个或多个。
**断言：**
- [ ] 使用所提供上下文文档中的精确支柱名称
- [ ] 不生成与所提供支柱脱节的通用创意反馈
- [ ] 引用与被评审机制最相关的具体支柱
- [ ] 不引用所提供文档中未出现的支柱

---

## 协议合规性

- [ ] 仅使用 APPROVE / CONCERNS / REJECT 词汇返回裁决
- [ ] 严守声明的创意领域
- [ ] 通过向用户呈现权衡方案（而非单方面推翻）来升级冲突
- [ ] 在输出中使用关卡 ID（例如 `CD-PILLARS: APPROVE`），而非内联散文裁决
- [ ] 不做跨领域的约束性决策（技术、生产、美术执行）

---

## 覆盖说明
- 多关卡场景（例如单次提交同时触发 CD-PILLARS 和 CD-GDD-ALIGN）未在此覆盖 — 推迟至集成测试。
- CD-PHASE-GATE（完整阶段推进）涉及综合多个子关卡结果；该复杂用例推迟处理。
- 试玩报告解读（CD-PLAYTEST）未覆盖 — 待 playtest-report 技能产出结构化输出后应补充专项用例。
- art-director 在视觉支柱对齐方面的交互未覆盖。
