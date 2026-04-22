# 目录结构

```text
/
├── CLAUDE.md                    # 主配置文件
├── .claude/                     # Agent 定义、skills、hooks、rules、docs
├── src/                         # 游戏源代码（core、gameplay、ai、networking、ui、tools）
├── assets/                      # 游戏资产（art、audio、vfx、shaders、data）
├── design/                      # 游戏设计文档（gdd、narrative、levels、balance）
├── docs/                        # 技术文档（architecture、api、postmortems）
│   └── engine-reference/        # 引擎 API 精选快照（版本锁定）
├── tests/                       # 测试套件（unit、integration、performance、playtest）
├── tools/                       # 构建与流水线工具（ci、build、asset-pipeline）
├── prototypes/                  # 临时原型（与 src/ 隔离）
└── production/                  # 生产管理（sprints、milestones、releases）
    ├── session-state/           # 临时会话状态（active.md — 已加入 .gitignore）
    └── session-logs/            # 会话审计日志（已加入 .gitignore）
```
