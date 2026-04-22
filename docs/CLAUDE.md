# 文档目录

在此目录中创作或编辑文件时，请遵循以下规范。

## 架构决策记录（`docs/architecture/`）

使用 ADR 模板：`.claude/docs/templates/architecture-decision-record.md`

**必需章节：** 标题、状态、背景、决策、影响、
ADR 依赖项、引擎兼容性、关联的 GDD 需求

**状态生命周期：** `Proposed`（提议）→ `Accepted`（已接受）→ `Superseded`（已废止）
- 不得跳过 `Accepted` 状态——引用 `Proposed` ADR 的用户故事会被自动阻塞
- 使用 `/architecture-decision` 通过引导式流程创建 ADR

**TR 注册表：** `docs/architecture/tr-registry.yaml`
- 稳定的需求 ID（如 `TR-MOV-001`），将 GDD 需求与用户故事关联
- 禁止重新编号现有 ID——只能追加新 ID
- 由 `/architecture-review` 第 8 阶段更新

**控制清单：** `docs/architecture/control-manifest.md`
- 扁平化程序员规则表：按层级列出必须遵守、禁止操作和防护机制
- 头部标注日期的 `Manifest Version:`
- 用户故事中嵌入此版本；`/story-done` 会检查是否已过期

**验证：** 完成一组 ADR 后运行 `/architecture-review`。

## 引擎参考（`docs/engine-reference/`）

版本固定的引擎 API 快照。**在使用任何引擎 API 前，必须先查阅此处**
——LLM 的训练数据早于当前固定的引擎版本。

当前引擎：参见 `docs/engine-reference/godot/VERSION.md`
