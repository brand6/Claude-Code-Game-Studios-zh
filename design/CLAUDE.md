# 设计目录

在此目录中创建或编辑文件时，请遵循以下标准。

## GDD 文件（`design/gdd/`）

每份 GDD 必须按以下顺序包含全部 **8 个必填章节**：
1. 概述 — 一段式摘要
2. 玩家幻想 — 预期的感受与体验
3. 详细规则 — 无歧义的机制说明
4. 公式 — 所有数学公式，含变量定义
5. 边界情况 — 处理异常情况的方式
6. 依赖关系 — 列出依赖的其他系统
7. 调节旋钮 — 标明可配置的数值
8. 验收标准 — 可测试的成功条件

**文件命名：** `[system-slug].md`（例如 `movement-system.md`、`combat-system.md`）

**系统索引：** `design/gdd/systems-index.md` — 添加新 GDD 时同步更新。

**设计顺序：** 基础层 → 核心层 → 功能层 → 表现层 → 打磨层

**验证：** 撰写任何 GDD 后运行 `/design-review [path]`。
完成一组相关 GDD 后运行 `/review-all-gdds`。

## 快速规格（`design/quick-specs/`）

用于调整数值、小型机制或平衡调整的轻量级规格文档。
使用 `/quick-design` 撰写。

## UX 规格（`design/ux/`）

- 逐界面规格：`design/ux/[screen-name].md`
- HUD 设计：`design/ux/hud.md`
- 交互模式库：`design/ux/interaction-patterns.md`
- 无障碍要求：`design/ux/accessibility-requirements.md`

使用 `/ux-design` 撰写。交付给 `/team-ui` 前先用 `/ux-review` 验证。
