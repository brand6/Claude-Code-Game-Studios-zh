# GLOSSARY — 中英文术语对照表

> 本词汇表是所有中文翻译工作的基准规范。
> 翻译时必须保持术语一致性。

---

## 使用规则

1. **标识符（ID）绝对不翻**：name: 字段值、斜杠命令、YAML键名、文件路径
2. **正文描述可翻**：description、user-visible text、说明性段落
3. **裁定词保留英文**：PASS / FAIL / CONCERNS / BLOCKED / COMPLETE / APPROVED
4. **角色称谓**：frontmatter 中的 agent name 不翻，正文可用中文称谓

---

## A — Agent 与架构

| 英文（原文） | 中文译法 | 用法说明 |
| ------------ | -------- | -------- |
| Agent | Agent（智能体） | 标识符用英文，说明文字可加"智能体" |
| Skill | 技能/指令 | 统一用"技能"（作名词），"指令"（作命令时） |
| Hook | 钩子/Hook | 技术文档用 Hook，说明文字用"钩子" |
| Rules | 规则 | 可直接翻为"规则"，paths 字段不翻 |
| Tier | 层级 | Tier 1/2/3 → 第一/二/三层 |
| subagent | 子智能体 | 说明文字用"子智能体" |
| workflow | 工作流 | |
| pipeline | 流水线 | |
| frontmatter | frontmatter | 技术术语不翻 |

---

## B — 开发流程

| 英文（原文） | 中文译法 | 用法说明 |
| ------------ | -------- | -------- |
| Sprint | 迭代 | 统一用"迭代"（不用"冲刺"） |
| Epic | 功能模块 | 有时可保留 Epic |
| Story | 用户故事 | |
| Milestone | 里程碑 | |
| Backlog | 待办列表 | |
| velocity | 迭代速度 | |
| burndown | 燃尽图 | |
| scope creep | 范围蔓延 | |
| estimate | 估算 | （名词/动词均用"估算"） |
| kick-off | 启动会 | |

---

## C — 设计文档

| 英文（原文） | 中文译法 | 用法说明 |
| ------------ | -------- | -------- |
| GDD | GDD（游戏设计文档） | 缩写保留，首次出现括注中文 |
| ADR | ADR（架构决策记录） | 缩写保留 |
| Art Bible | 美术圣经 | |
| Concept Document | 概念文档 | |
| Technical Preferences | 技术偏好配置 | |
| Control Manifest | 控制清单 | |
| traceability matrix | 可追溯矩阵 | |
| systems index | 系统索引 | |
| entity registry | 实体注册表 | |

---

## D — 游戏开发专业词汇

| 英文（原文） | 中文译法 | 用法说明 |
| ------------ | -------- | -------- |
| core loop | 核心循环 | |
| progression | 进度成长 | |
| balance | 平衡性 | |
| meta | 元游戏/meta | 视语境 |
| loot | 战利品/掉落 | |
| spawn | 生成/刷怪 | 视语境 |
| collision | 碰撞 | |
| physics | 物理 | |
| rendering | 渲染 | |
| shader | 着色器/Shader | 技术语境保留 Shader |
| VFX | 视觉特效/VFX | 缩写保留 |
| SFX | 音效/SFX | 缩写保留 |
| HUD | HUD（平视显示器） | 缩写保留 |
| UI | UI（用户界面） | 缩写保留 |
| UX | UX（用户体验） | 缩写保留 |
| cutscene | 过场动画 | |
| dialogue | 对话 | |
| localization | 本地化 | |
| i18n | 国际化/i18n | 缩写保留 |

---

## E — QA 与测试

| 英文（原文） | 中文译法 | 用法说明 |
| ------------ | -------- | -------- |
| Gate Check | 门禁检查 | |
| Verdict | 裁定结果 | PASS/FAIL 本身保留英文 |
| PASS | PASS | **不翻** |
| FAIL | FAIL | **不翻** |
| CONCERNS | CONCERNS | **不翻** |
| BLOCKED | BLOCKED | **不翻** |
| COMPLETE | COMPLETE | **不翻** |
| APPROVED | APPROVED | **不翻** |
| smoke test | 冒烟测试 | |
| soak test | 浸泡测试/长时测试 | |
| regression test | 回归测试 | |
| QA | QA（质量保证） | 缩写保留 |
| bug triage | bug 分级 | |
| severity | 严重级别 | |
| priority | 优先级 | |
| acceptance criteria | 验收标准 | |
| test evidence | 测试证据 | |
| flaky test | 不稳定测试 | |

---

## F — 团队角色

| 英文（Agent 名） | 正文中文称谓 | 说明 |
| ---------------- | ------------ | ---- |
| creative-director | 创意总监 | **标识符不翻** |
| technical-director | 技术总监 | |
| producer | 制作人/Producer | |
| game-designer | 游戏设计师 | |
| lead-programmer | 主程序员 | |
| art-director | 美术总监 | |
| audio-director | 音频总监 | |
| narrative-director | 叙事总监 | |
| qa-lead | QA 负责人 | |
| release-manager | 发布经理 | |
| localization-lead | 本地化负责人 | |
| gameplay-programmer | 游戏玩法程序员 | |
| engine-programmer | 引擎程序员 | |
| ai-programmer | AI 程序员 | |
| network-programmer | 网络程序员 | |
| technical-artist | 技术美术 | |
| performance-analyst | 性能分析师 | |
| sound-designer | 音效设计师 | |
| systems-designer | 系统设计师 | |
| ui-programmer | UI 程序员 | |
| ux-designer | UX 设计师 | |
| level-designer | 关卡设计师 | |
| writer | 文案/编剧 | 视语境 |
| world-builder | 世界观构建师 | |
| prototyper | 原型开发者 | |
| qa-tester | QA 测试员 | |
| security-engineer | 安全工程师 | |
| devops-engineer | DevOps 工程师 | |
| analytics-engineer | 数据分析工程师 | |
| economy-designer | 经济系统设计师 | |
| live-ops-designer | 运营活动设计师 | |
| community-manager | 社区运营 | |
| accessibility-specialist | 无障碍专家 | |
| tools-programmer | 工具开发程序员 | |

---

## G — 发布与运营

| 英文（原文） | 中文译法 | 用法说明 |
| ------------ | -------- | -------- |
| launch | 发布/上线 | |
| hotfix | 热修复 | |
| patch | 补丁 | |
| day-one patch | 首发补丁 | |
| release candidate | 发布候选版本 | |
| gold master | 金片（最终版本） | |
| certification | 认证 | 平台认证 |
| store metadata | 商店元数据 | |
| live ops | 运营活动/live ops | |
| season | 赛季 | |
| battle pass | 战令 | |
| A/B test | A/B 测试 | |
| telemetry | 遥测/数据采集 | |
| analytics | 数据分析 | |
| KPI | KPI | 缩写保留 |
| DAU / MAU | DAU / MAU | 缩写保留 |
| retention | 留存率 | |
| churn | 流失率 | |

---

## H — 专业技术词汇（引擎相关）

| 英文（原文） | 中文译法 | 用法说明 |
| ------------ | -------- | -------- |
| GDScript | GDScript | 不翻 |
| GDExtension | GDExtension | 不翻 |
| Blueprint | 蓝图/Blueprint | UE 语境 |
| MonoBehaviour | MonoBehaviour | Unity 语境，不翻 |
| ECS / DOTS | ECS / DOTS | Unity 语境，缩写保留 |
| GAS | GAS（Gameplay Ability System） | UE 语境 |
| node | 节点 | Godot 语境 |
| scene | 场景 | |
| prefab | 预制体 | Unity 语境 |
| asset bundle | 资产包 | |
| Addressables | Addressables | Unity 语境，不翻 |
| Niagara | Niagara | UE 语境，不翻 |

---

## 说明：不翻译清单

以下内容**绝对不翻译**：

1. `name:` 字段的值（所有 agent/skill 标识符）
2. 斜杠命令：`/start`、`/brainstorm`、`/gate-check` 等
3. YAML 的键名：`description:`、`tools:`、`model:` 等
4. `paths:` 字段的值（规则文件路径绑定）
5. Hooks 脚本文件（.sh 文件）内容
6. `settings.json`、`.gitignore` 等配置文件
7. 裁定词：PASS / FAIL / CONCERNS / BLOCKED / COMPLETE / APPROVED
8. 引擎专属 API 名称（GDExtension、MonoBehaviour 等）
9. 外部工具名称（Claude Code、Perforce、GitHub 等）
