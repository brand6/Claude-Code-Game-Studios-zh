# Unity 引擎 — 版本参考

| 字段 | 值 |
|------|-----|
| **引擎版本** | Unity 6.3 LTS |
| **发布日期** | 2025 年 12 月 |
| **项目锁定** | 2026-02-13 |
| **文档最后验证** | 2026-02-13 |
| **LLM 知识截止日期** | 2025 年 5 月 |

## 知识空白警告

LLM 的训练数据可能只覆盖到 Unity 2022 LTS（2022.3）。完整的
Unity 6 发行系列（前身为 Unity 2023 Tech Stream）引入了大量
该模型**不了解**的重大变更。建议使用任何 Unity API 前，先查阅本目录。

## 截止日期后的版本时间线

| 版本 | 发布时间 | 风险等级 | 核心主题 |
|------|---------|---------|---------|
| 6.0 | 2024 年 10 月 | 高 | Unity 6 品牌重塑、新渲染特性、Entities 1.3、DOTS 改进 |
| 6.1 | 2024 年 11 月 | 中 | Bug 修复、稳定性改进 |
| 6.2 | 2024 年 12 月 | 中 | 性能优化、新输入系统改进 |
| 6.3 LTS | 2025 年 12 月 | 高 | 6.0 以来首个 LTS、生产就绪的 DOTS、增强图形特性 |

## 2022 LTS 至 Unity 6.3 LTS 的主要变更

### 破坏性变更
- **Entities/DOTS**：Entities 1.0+ 完整 API 重构，ECS 模式全面重新设计
- **Input System**：旧版 Input Manager 已废弃，新 Input System 成为默认
- **渲染**：URP/HDRP 重大升级，SRP Batcher 改进
- **Addressables**：资产管理工作流变更
- **脚本**：支持 C# 9，新 API 模式

### 新特性（截止日期后）
- **DOTS**：生产就绪的 Entity Component System（Entities 1.3+）
- **图形**：增强的 URP/HDRP 管线、GPU Resident Drawer
- **多人游戏**：Netcode for GameObjects 改进
- **UI Toolkit**：运行时 UI 生产就绪（新项目建议替代 UGUI）
- **异步资产加载**：改进的 Addressables 性能
- **Web**：WebGPU 支持

### 已废弃的系统
- **旧版 Input Manager**：使用新 Input System 包
- **旧版粒子系统**：使用 Visual Effect Graph
- **UGUI**：仍受支持，但新项目推荐 UI Toolkit
- **旧版 ECS（GameObjectEntity）**：已被现代 DOTS/Entities 取代

## 已验证来源

- 官方文档：https://docs.unity3d.com/6000.0/Documentation/Manual/index.html
- Unity 6 发布：https://unity.com/releases/unity-6
- Unity 6.3 LTS 公告：https://unity.com/blog/unity-6-3-lts-is-now-available
- 迁移指南：https://docs.unity3d.com/6000.0/Documentation/Manual/upgrade-guides.html
- Unity 6 支持：https://unity.com/releases/unity-6/support
- C# API 参考：https://docs.unity3d.com/6000.0/Documentation/ScriptReference/index.html
