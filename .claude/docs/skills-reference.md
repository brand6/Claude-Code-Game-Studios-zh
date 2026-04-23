# 可用技能（斜杠命令）

68 个按阶段组织的斜杠命令。在 Claude Code 中输入 `/` 即可访问任意命令。

## 入门与导航

| 命令 | 用途                                      |
| ----------------------- | --------------------------------------- |
| `/start` | 首次入门引导——询问当前所处阶段，然后引导至对应工作流             |
| `/help` | 情境感知的「下一步做什么？」——读取当前阶段并呈现所需的下一个步骤       |
| `/project-stage-detect` | 全项目审计——检测阶段、识别文件缺口、推荐后续步骤               |
| `/setup-engine` | 配置引擎及版本，检测知识缺口，填充版本感知参考文档               |
| `/adopt` | 存量项目格式审计——检查现有 GDD/ADR/故事文件的内部结构，生成迁移计划 |

## 游戏设计

| 命令 | 用途 |
|------|------|
| `/brainstorm` | 使用专业工作室方法（MDA、SDT、Bartle、动词优先）进行引导式创意构思 |
| `/map-systems` | 将游戏概念拆解为系统，绘制依赖关系图，确定设计优先级 |
| `/design-system` | 逐章节引导式创作单一游戏系统的 GDD（游戏设计文档） |
| `/quick-design` | 小幅变更的轻量设计规格——调参、微调、小功能添加 |
| `/review-all-gdds` | 跨 GDD 一致性与游戏设计整体性评审 |
| `/propagate-design-change` | 当 GDD 修订时，查找受影响的 ADR 并生成影响报告 |

## UX 与界面设计

| 命令 | 用途 |
|------|------|
| `/ux-design` | 逐章节引导式 UX 规格创作（界面/流程、HUD 或交互模式库） |
| `/ux-review` | 验证 UX 规格的 GDD 对齐性、无障碍合规性和模式合规性 |

## 架构

| 命令 | 用途 |
|------|------|
| `/create-architecture` | 引导式创作主架构文档 |
| `/architecture-decision` | 创建架构决策记录（ADR） |
| `/architecture-review` | 验证所有 ADR 的完整性、依赖顺序和 GDD 覆盖情况 |
| `/create-control-manifest` | 从已接受的 ADR 生成扁平化程序员规则表 |

## 用户故事与迭代

| 命令 | 用途 |
|------|------|
| `/create-epics` | 将 GDD 与 ADR 转化为功能模块——每个架构模块对应一个 |
| `/create-stories` | 将单个功能模块拆解为可实现的用户故事文件 |
| `/dev-story` | 读取故事并实现——路由至正确的程序员 Agent |
| `/sprint-plan` | 生成或更新迭代计划；初始化 sprint-status.yaml |
| `/sprint-status` | 快速 30 行迭代快照（读取 sprint-status.yaml） |
| `/story-readiness` | 在拾取前验证故事是否具备实现条件（READY / NEEDS WORK / BLOCKED） |
| `/story-done` | 实现完成后的 8 阶段完成评审；更新故事文件，呈现下一个待做故事 |
| `/estimate` | 含复杂度、依赖关系和风险分解的结构化工作量估算 |

## 评审与分析

| 命令 | 用途 |
|------|------|
| `/design-review` | 评审游戏设计文档的完整性与一致性 |
| `/code-review` | 对文件或变更集进行架构层面的代码评审 |
| `/balance-check` | 分析游戏平衡性数据、公式和配置——标记异常值 |
| `/asset-audit` | 审计资产的命名规范、文件大小预算和流水线合规性 |
| `/content-audit` | 对比 GDD 规划的内容数量与已实现内容 |
| `/scope-check` | 对照原始计划分析功能或迭代范围，标记范围蔓延 |
| `/perf-profile` | 含瓶颈识别的结构化性能分析 |
| `/tech-debt` | 扫描、跟踪、优先级排序并报告技术债务 |
| `/gate-check` | 验证能否推进至下一开发阶段（PASS / CONCERNS / FAIL） |
| `/consistency-check` | 扫描所有 GDD 与实体注册表，检测跨文档不一致性（互相矛盾的属性、数值、规则） |

## QA 与测试

| 命令 | 用途 |
|------|------|
| `/qa-plan` | 为迭代或功能生成 QA 测试计划 |
| `/smoke-check` | 在移交 QA 前运行关键路径冒烟测试门禁 |
| `/soak-test` | 为长时游戏会话生成浸泡测试方案 |
| `/regression-suite` | 将测试覆盖映射至 GDD 关键路径，识别缺少回归测试的已修复 bug |
| `/test-setup` | 为项目引擎搭建测试框架和 CI/CD 流水线 |
| `/test-helpers` | 为测试套件生成引擎专属的测试辅助库 |
| `/test-evidence-review` | 对测试文件和手工测试证据文档进行质量评审 |
| `/test-flakiness` | 从 CI 运行日志中检测不确定性（不稳定）测试 |
| `/skill-test` | 验证技能文件的结构合规性与行为正确性 |

## 生产管理

| 命令 | 用途 |
|------|------|
| `/milestone-review` | 评审里程碑进度并生成状态报告 |
| `/retrospective` | 执行结构化的迭代或里程碑回顾 |
| `/bug-report` | 创建结构化 bug 报告 |
| `/bug-triage` | 读取所有开放 bug，重新评估优先级与严重级别，分配负责人和标签 |
| `/reverse-document` | 从现有实现反向生成设计或架构文档 |
| `/playtest-report` | 生成结构化游戏测试报告或分析现有游戏测试笔记 |

## 发布

| 命令 | 用途 |
|------|------|
| `/release-checklist` | 生成并验证当前构建版本的发布前检查清单 |
| `/launch-checklist` | 跨所有部门的完整上线就绪性验证 |
| `/changelog` | 从 git 提交和迭代数据自动生成变更日志 |
| `/patch-notes` | 从 git 历史和内部数据生成面向玩家的补丁说明 |
| `/hotfix` | 含审计追踪的紧急修复工作流，绕过正常迭代流程 |

## 创意与内容

| 命令 | 用途 |
|------|------|
| `/prototype` | 快速一次性原型，用于验证游戏机制（宽松规范，隔离工作树） |
| `/onboard` | 为新贡献者或 Agent 生成情境化入门文档 |
| `/localize` | 本地化工作流：字符串提取、验证、翻译就绪性 |

## 团队编排

将多个 Agent 协同调度到单一功能领域：

| 命令 | 编排成员 |
|------|---------|
| `/team-combat` | game-designer + gameplay-programmer + ai-programmer + technical-artist + sound-designer + qa-tester |
| `/team-narrative` | narrative-director + writer + world-builder + level-designer |
| `/team-ui` | ux-designer + ui-programmer + art-director + accessibility-specialist |
| `/team-release` | release-manager + qa-lead + devops-engineer + producer |
| `/team-polish` | performance-analyst + technical-artist + sound-designer + qa-tester |
| `/team-audio` | audio-director + sound-designer + technical-artist + gameplay-programmer |
| `/team-level` | level-designer + narrative-director + world-builder + art-director + systems-designer + qa-tester |
| `/team-live-ops` | live-ops-designer + economy-designer + community-manager + analytics-engineer |
| `/team-qa` | qa-lead + qa-tester + gameplay-programmer + producer |
