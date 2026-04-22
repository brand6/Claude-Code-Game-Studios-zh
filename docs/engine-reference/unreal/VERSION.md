# Unreal Engine — 版本参考

| 字段 | 值 |
|------|-----|
| **引擎版本** | Unreal Engine 5.7 |
| **发布日期** | 2025年11月 |
| **项目固定版本** | 2026-02-13 |
| **文档最后验证** | 2026-02-13 |
| **LLM 知识截止日期** | 2025年5月 |

## 知识空白警告

LLM 的训练数据可能覆盖到 Unreal Engine ~5.3。5.4、5.5、5.6 和 5.7 版本引入了模型**不了解**的重大变化。
在建议任何 Unreal API 调用前，请务必先交叉参考本目录。

## 截止日期后的版本时间线

| 版本 | 发布时间 | 风险等级 | 核心主题 |
|------|---------|----------|---------|
| 5.4 | ~2025年中 | 高 | Motion Design 工具、动画改进、PCG 增强 |
| 5.5 | ~2025年9月 | 高 | Megalights（数百万灯光）、动画制作、MegaCity 演示 |
| 5.6 | ~2025年10月 | 中 | 性能优化、Bug 修复 |
| 5.7 | 2025年11月 | 高 | PCG 生产就绪、Substrate 生产就绪、AI 助手 |

## UE 5.3 到 UE 5.7 的主要变化

### 破坏性变更
- **Substrate 材质系统**：新材质框架（替代旧版材质）
- **PCG（程序化内容生成）**：生产就绪，API 重大变更
- **Megalights**：新光照系统（支持数百万动态灯光）
- **动画制作工具**：全新绑定和动画工具
- **AI 助手**：编辑器内 AI 引导（实验性）

### 新功能（截止日期后）
- **Megalights**：超大规模动态光照（数百万灯光）
- **Substrate 材质**：生产就绪的模块化材质系统
- **PCG 框架**：程序化世界生成（5.7 生产就绪）
- **增强虚拟制作**：MetaHuman 集成，更深层的 VP 工作流
- **动画改进**：更好的绑定、混合、程序化动画
- **AI 助手**：编辑器内 AI 辅助（实验性）

### 废弃系统
- **旧版材质系统**：新项目迁移到 Substrate
- **旧版 PCG API**：使用新的生产就绪 PCG API（5.7+）

## 已验证来源

- 官方文档：https://docs.unrealengine.com/5.7/
- UE 5.7 发布说明：https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-7-release-notes
- 5.7 新特性：https://dev.epicgames.com/documentation/en-us/unreal-engine/whats-new
- UE 5.7 公告：https://www.unrealengine.com/en-US/news/unreal-engine-5-7-is-now-available
- UE 5.5 博客：https://www.unrealengine.com/en-US/blog/unreal-engine-5-5-is-now-available
- 迁移指南：https://docs.unrealengine.com/5.7/en-US/upgrading-projects/
