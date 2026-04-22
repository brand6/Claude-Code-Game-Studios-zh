# CCGS Skill Testing Framework（技能测试框架）

**Claude Code Game Studios** 框架的质量保障基础设施。
测试框架本身的技能和 agents —— 而非用该框架开发的游戏。

> **本文件夹完全自包含，可选安装。**
> 使用 CCGS 的游戏开发者无需安装本框架。如需完整删除：
> `rm -rf "CCGS Skill Testing Framework"` —— `.claude/` 中没有任何内容依赖它。

---

## 目录结构

```
CCGS Skill Testing Framework/
├── README.md              ← 当前位置
├── CLAUDE.md              ← 告诉 Claude 如何使用本框架
├── catalog.yaml           ← 主注册表：所有 72 个技能 + 49 个 agents，含覆盖度跟踪
├── quality-rubric.md      ← /skill-test category 的分类通过/失败指标
│
├── skills/                ← 技能的行为规格文件（每个技能一份）
│   ├── gate/              ← gate 类规格
│   ├── review/            ← review 类规格
│   ├── authoring/         ← authoring 类规格
│   ├── readiness/         ← readiness 类规格
│   ├── pipeline/          ← pipeline 类规格
│   ├── analysis/          ← analysis 类规格
│   ├── team/              ← team 类规格
│   ├── sprint/            ← sprint 类规格
│   └── utility/           ← utility 类规格
│
├── agents/                ← agent 的行为规格文件（每个 agent 一份）
│   ├── directors/         ← creative-director、technical-director、producer、art-director
│   ├── leads/             ← lead-programmer、narrative-director、audio-director 等
│   ├── specialists/       ← 引擎/代码/着色器/UI 专家
│   ├── godot/             ← Godot 专项专家
│   ├── unity/             ← Unity 专项专家
│   ├── unreal/            ← Unreal 专项专家
│   ├── operations/        ← QA、live-ops、发布、本地化等
│   └── creative/          ← writer、world-builder、game-designer 等
│
├── templates/             ← 编写新规格文件的模板
│   ├── skill-test-spec.md ← 技能行为规格模板
│   └── agent-test-spec.md ← agent 行为规格模板
│
└── results/               ← 测试运行输出（由 /skill-test spec 写入，已 gitignore）
```

---

## 使用方法

所有测试均由框架中的两个技能驱动：

### 结构合规性检查

```
/skill-test static [skill-name]     # 检查单个技能（7 项检查）
/skill-test static all              # 检查全部 72 个技能
```

### 运行行为规格测试

```
/skill-test spec gate-check         # 对照编写的规格评估技能
/skill-test spec design-review
```

### 对照分类评分标准检查

```
/skill-test category gate-check     # 对照分类指标评估单个技能
/skill-test category all            # 跨所有分类技能运行评分标准检查
```

### 查看完整覆盖度概况

```
/skill-test audit                   # 技能 + agents：是否有规格、上次测试时间、结果
```

### 改进失败的技能

```
/skill-improve gate-check           # 测试 → 诊断 → 提议修复 → 重测循环
```

---

## 技能分类

| 分类 | 技能 | 关键指标 |
|------|------|---------|
| `gate` | gate-check | 读取评审模式、完整/精简/单机 director 面板、禁止自动推进 |
| `review` | design-review、architecture-review、review-all-gdds | 只读、8 节检查、正确裁决词 |
| `authoring` | design-system、quick-design、art-bible、create-architecture 等 | 逐节 May-I-write、骨架优先 |
| `readiness` | story-readiness、story-done | 浮现阻塞项、完整模式下 director 关卡 |
| `pipeline` | create-epics、create-stories、dev-story、map-systems 等 | 上游依赖检查、交接路径畅通 |
| `analysis` | consistency-check、balance-check、code-review、tech-debt 等 | 只读报告、裁决关键词、不写入文件 |
| `team` | team-combat、team-narrative、team-audio 等 | 所有必要 agents 已启动、阻塞项已浮现 |
| `sprint` | sprint-plan、sprint-status、milestone-review 等 | 读取 Sprint 数据、状态关键词存在 |
| `utility` | start、adopt、hotfix、localize、setup-engine 等 | 通过静态检查 |

---

## Agent 层级

| 层级 | Agents |
|------|--------|
| `directors` | creative-director、technical-director、producer、art-director |
| `leads` | lead-programmer、narrative-director、audio-director、ux-designer、qa-lead、release-manager、localization-lead |
| `specialists` | gameplay-programmer、engine-programmer、ui-programmer、tools-programmer、network-programmer、ai-programmer、level-designer、sound-designer、technical-artist |
| `godot` | godot-specialist、godot-gdscript-specialist、godot-csharp-specialist、godot-shader-specialist、godot-gdextension-specialist |
| `unity` | unity-specialist、unity-ui-specialist、unity-shader-specialist、unity-dots-specialist、unity-addressables-specialist |
| `unreal` | unreal-specialist、ue-gas-specialist、ue-replication-specialist、ue-umg-specialist、ue-blueprint-specialist |
| `operations` | devops-engineer、security-engineer、performance-analyst、analytics-engineer、community-manager |
| `creative` | writer、world-builder、game-designer、economy-designer、systems-designer、prototyper |

---

## 更新 catalog

`catalog.yaml` 跟踪每个技能和 agent 的测试覆盖度。运行测试后：

- `/skill-test spec [name]` 会提议更新 `last_spec` 和 `last_spec_result`
- `/skill-test category [name]` 会提议更新 `last_category` 和 `last_category_result`
- `last_static` 和 `last_static_result` 通过手动方式或 `/skill-improve` 更新

---

## 编写新规格

1. 在 `templates/skill-test-spec.md` 找到规格模板
2. 将其复制到 `skills/[category]/[skill-name].md`
3. 在 `catalog.yaml` 中将 `spec:` 字段更新为指向新文件
4. 运行 `/skill-test spec [skill-name]` 进行验证

---

## 删除本框架

本文件夹与主项目没有任何钩子关联。如需删除：

```bash
rm -rf "CCGS Skill Testing Framework"
```

技能 `/skill-test` 和 `/skill-improve` 仍可正常运行——它们只会报告 `catalog.yaml` 缺失，
并建议运行 `/skill-test audit` 进行初始化。
