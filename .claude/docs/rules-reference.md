# 路径专属规则

`.claude/rules/` 中的规则会在编辑匹配路径中的文件时自动执行：

| 规则文件 | 路径模式 | 强制要求 |
| ---- | ---- | ---- |
| `gameplay-code.md` | `src/gameplay/**` | 数据驱动的值、delta time、禁止引用 UI |
| `engine-code.md` | `src/core/**` | 热路径零分配、线程安全、API 稳定性 |
| `ai-code.md` | `src/ai/**` | 性能预算、可调试性、数据驱动参数 |
| `network-code.md` | `src/networking/**` | 服务端权威、消息版本控制、安全性 |
| `ui-code.md` | `src/ui/**` | 不持有游戏状态、本地化就绪、无障碍支持 |
| `design-docs.md` | `design/gdd/**` | 必须包含 8 个规定章节、公式格式、边界情况 |
| `narrative.md` | `design/narrative/**` | 世界观一致性、角色声线、规范化程度 |
| `data-files.md` | `assets/data/**` | JSON 有效性、命名规范、schema 规则 |
| `test-standards.md` | `tests/**` | 测试命名、覆盖要求、fixture 模式 |
| `prototype-code.md` | `prototypes/**` | 放宽标准，必须提供 README，并记录假设条件 |
| `shader-code.md` | `assets/shaders/**` | 命名规范、性能目标、跨平台规则 |
