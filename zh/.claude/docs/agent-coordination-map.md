# Agent 协调与委托图

## 组织层级结构

```
                           [人类开发者]
                                 |
                 +---------------+---------------+
                 |               |               |
         creative-director  technical-director  producer
                 |               |               |
        +--------+--------+     |        （协调所有人）
        |        |        |     |
  game-designer art-dir  narr-dir  lead-programmer  qa-lead  audio-dir
        |        |        |         |                |        |
     +--+--+     |     +--+--+  +--+--+--+--+--+   |        |
     |  |  |     |     |     |  |  |  |  |  |  |   |        |
    sys lvl eco  ta   wrt  wrld gp ep  ai net tl ui qa-t    snd
                                 |
                             +---+---+
                             |       |
                          perf-a   devops   analytics

  附加负责人（向 producer/directors 汇报）：
    release-manager         -- 发布流水线、版本控制、部署
    localization-lead       -- 国际化、字符串表、翻译流水线
    prototyper              -- 快速可丢弃原型、概念验证
    security-engineer       -- 反作弊、漏洞、数据隐私、网络安全
    accessibility-specialist -- WCAG、色盲、按键重映射、文字缩放
    live-ops-designer       -- 赛季、活动、通行证、留存、直播经济
    community-manager       -- 更新日志、玩家反馈、危机沟通

  引擎专员（使用与你引擎匹配的那套）：
    unreal-specialist  -- UE5 负责人：Blueprint/C++、GAS 概览、UE 子系统
      ue-gas-specialist         -- GAS：ability、effect、属性、标签、预测
      ue-blueprint-specialist   -- Blueprint：BP/C++ 边界、图表规范、优化
      ue-replication-specialist -- 网络：同步、RPC、预测、带宽
      ue-umg-specialist         -- UI：UMG、CommonUI、widget 层级、数据绑定

    unity-specialist   -- Unity 负责人：MonoBehaviour/DOTS、Addressables、URP/HDRP
      unity-dots-specialist         -- DOTS/ECS：Jobs、Burst、混合渲染器
      unity-shader-specialist       -- Shader：Shader Graph、VFX Graph、SRP 定制
      unity-addressables-specialist -- 资产：异步加载、bundle、内存、CDN
      unity-ui-specialist           -- UI：UI Toolkit、UGUI、UXML/USS、数据绑定

    godot-specialist   -- Godot 4 负责人：GDScript、节点/场景、信号、资源
      godot-gdscript-specialist    -- GDScript：静态类型、模式、信号、性能
      godot-shader-specialist      -- Shader：Godot 着色器语言、可视化 shader、VFX
      godot-gdextension-specialist -- 原生：C++/Rust 绑定、GDExtension、构建系统
```

### 图例
```
sys  = systems-designer       gp  = gameplay-programmer
lvl  = level-designer         ep  = engine-programmer
eco  = economy-designer       ai  = ai-programmer
ta   = technical-artist       net = network-programmer
wrt  = writer                 tl  = tools-programmer
wrld = world-builder          ui  = ui-programmer
snd  = sound-designer         qa-t = qa-tester
narr-dir = narrative-director perf-a = performance-analyst
art-dir = art-director
```

## 委托规则

### 谁可以向谁委托

| 发起方 | 可委托对象 |
|------|----------------|
| creative-director | game-designer、art-director、audio-director、narrative-director |
| technical-director | lead-programmer、devops-engineer、performance-analyst、technical-artist（技术决策） |
| producer | 任意 Agent（仅限其职责范围内的任务分配） |
| game-designer | systems-designer、level-designer、economy-designer |
| lead-programmer | gameplay-programmer、engine-programmer、ai-programmer、network-programmer、tools-programmer、ui-programmer |
| art-director | technical-artist、ux-designer |
| audio-director | sound-designer |
| narrative-director | writer、world-builder |
| qa-lead | qa-tester |
| release-manager | devops-engineer（发布构建）、qa-lead（发布测试） |
| localization-lead | writer（字符串评审）、ui-programmer（文字排版适配） |
| prototyper | （独立工作，将发现汇报给 producer 及相关负责人） |
| security-engineer | network-programmer（安全评审）、lead-programmer（安全模式） |
| accessibility-specialist | ux-designer（无障碍模式）、ui-programmer（实现）、qa-tester（无障碍测试） |
| [engine]-specialist | 引擎子专员（委托子系统专项工作） |
| [engine] 子专员 | （向所有程序员提供引擎子系统模式和优化建议） |
| live-ops-designer | economy-designer（直播经济）、community-manager（活动沟通）、analytics-engineer（参与度指标） |
| community-manager | （与 producer 协作审批，与 release-manager 协调更新日志时机） |

### 升级路径

| 情形 | 升级至 |
|-----------|------------|
| 两位设计师对某机制意见不一 | game-designer |
| 游戏设计与叙事冲突 | creative-director |
| 游戏设计与技术可行性冲突 | producer（协调），再到 creative-director + technical-director |
| 美术与音频基调冲突 | creative-director |
| 代码架构分歧 | technical-director |
| 跨系统代码冲突 | lead-programmer，再到 technical-director |
| 部门间排期冲突 | producer |
| 范围超出容量 | producer，再到 creative-director 决定裁减 |
| 质量门禁意见不一 | qa-lead，再到 technical-director |
| 性能预算超标 | performance-analyst 标记，technical-director 决策 |

## 常见工作流模式

### 模式 1：新功能（完整流水线）

```
1. creative-director  -- 确认功能概念与愿景一致
2. game-designer      -- 创建包含完整规格的设计文档
3. producer           -- 排期工作，识别依赖关系
4. lead-programmer    -- 设计代码架构，创建接口草图
5. [专员程序员]        -- 实现功能
6. technical-artist   -- 实现视觉效果（如需）
7. writer             -- 创建文字内容（如需）
8. sound-designer     -- 创建音频事件列表（如需）
9. qa-tester          -- 编写测试用例
10. qa-lead           -- 评审并确认测试覆盖范围
11. lead-programmer   -- 代码评审
12. qa-tester         -- 执行测试
13. producer          -- 标记任务完成
```

### 模式 2：Bug 修复

```
1. qa-tester          -- 用 /bug-report 提交 Bug 报告
2. qa-lead            -- 分级确定严重程度和优先级
3. producer           -- 排入 sprint（若非 S1 级别）
4. lead-programmer    -- 定位根因，分配给程序员
5. [专员程序员]        -- 修复 Bug
6. lead-programmer    -- 代码评审
7. qa-tester          -- 验证修复并执行回归测试
8. qa-lead            -- 关闭 Bug
```

### 模式 3：平衡调整

```
1. analytics-engineer -- 通过数据（或玩家反馈）识别失衡问题
2. game-designer      -- 对照设计意图评估问题
3. economy-designer   -- 对调整方案建模
4. game-designer      -- 确认新数值
5. [更新数据文件]      -- 修改配置值
6. qa-tester          -- 回归测试受影响的系统
7. analytics-engineer -- 监控变更后的指标
```

### 模式 4：新区域/关卡

```
1. narrative-director -- 定义该区域的叙事目的与关键节拍
2. world-builder      -- 创建传说与环境背景
3. level-designer     -- 设计布局、遭遇、节奏
4. game-designer      -- 评审遭遇的机制设计
5. art-director       -- 为该区域定义视觉方向
6. audio-director     -- 为该区域定义音频方向
7. [相关程序员与美术师实现]
8. writer             -- 创建区域专属文字内容
9. qa-tester          -- 测试完整区域
```

### 模式 5：Sprint 周期

```
1. producer           -- 用 /sprint-plan new 规划 sprint
2. [全体 Agent]       -- 执行分配的任务
3. producer           -- 用 /sprint-plan status 进行日常状态更新
4. qa-lead            -- sprint 期间持续测试
5. lead-programmer    -- sprint 期间持续代码评审
6. producer           -- 用 post-sprint hook 进行 sprint 回顾
7. producer           -- 结合经验教训规划下一个 sprint
```

### 模式 6：里程碑检查点

```
1. producer           -- 运行 /milestone-review
2. creative-director  -- 评审创意进展
3. technical-director -- 评审技术健康度
4. qa-lead            -- 评审质量指标
5. producer           -- 主持通过/不通过讨论
6. [所有总监]         -- 如需调整范围则达成一致
7. producer           -- 记录决策并更新计划
```

### 模式 7：发布流水线

```text
1. producer             -- 宣布发布候选版本，确认里程碑标准已达成
2. release-manager      -- 切发布分支，生成 /release-checklist
3. qa-lead              -- 执行完整回归，确认质量
4. localization-lead    -- 核实所有字符串已翻译，文字排版通过
5. performance-analyst  -- 确认性能基准在目标范围内
6. devops-engineer      -- 构建发布产物，运行部署流水线
7. release-manager      -- 生成 /changelog，打标签，创建发布说明
8. technical-director   -- 重大发布的最终确认
9. release-manager      -- 部署并监控 48 小时
10. producer            -- 标记发布完成
```

### 模式 8：快速原型

```text
1. game-designer        -- 定义假设和成功标准
2. prototyper           -- 用 /prototype 搭建原型
3. prototyper           -- 构建最小实现（以小时计，而非天）
4. game-designer        -- 对照标准评估原型
5. prototyper           -- 记录发现报告
6. creative-director    -- 决定是否继续推进至生产
7. producer             -- 若批准则安排生产工作
```

### 模式 9：直播活动/赛季发布

```text
1. live-ops-designer     -- 设计活动/赛季内容、奖励、排期
2. game-designer         -- 验证活动的游戏机制
3. economy-designer      -- 平衡活动经济和奖励价值
4. narrative-director    -- 提供赛季叙事主题
5. writer                -- 创建活动描述和传说
6. producer              -- 安排实现工作排期
7. [相关程序员实现]
8. qa-lead               -- 端到端测试活动流程
9. community-manager     -- 起草活动公告和更新日志
10. release-manager      -- 部署活动内容
11. analytics-engineer   -- 监控活动参与度和指标
12. live-ops-designer    -- 活动后分析与总结
```

## 跨领域沟通协议

### 设计变更通知

当设计文档变更时，game-designer 必须通知：
- lead-programmer（实现影响）
- qa-lead（需要更新测试计划）
- producer（排期影响评估）
- 视变更内容通知相关专员智能体

### 架构变更通知

当 ADR 创建或修改时，technical-director 必须通知：
- lead-programmer（需要代码变更）
- 所有受影响的专员程序员
- qa-lead（测试策略可能变更）
- producer（排期影响）

### 美术规范变更通知

当美术圣经或资源规范变更时，art-director 必须通知：
- technical-artist（流水线变更）
- 所有处理受影响资源的内容创作者
- devops-engineer（若构建流水线受影响）

## 应避免的反模式

1. **绕过层级**：专员智能体不应在未与其负责人协商的情况下做出本属于负责人的决策。
2. **跨领域实现**：智能体不应在未获得相关所有者明确委托的情况下修改其指定范围之外的文件。
3. **隐形决策**：所有决策必须有文档记录。没有书面记录的口头协议会导致矛盾。
4. **单体任务**：分配给智能体的每项任务应在 1-3 天内可完成。如果更大，必须先拆解。
5. **基于假设的实现**：若规格存在歧义，实现者必须向规格制定者提问，而不是猜测。错误的猜测比一个问题代价更高。
