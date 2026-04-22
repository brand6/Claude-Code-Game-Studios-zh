# Agent 测试规格：devops-engineer

## Agent 概述
- **职责领域**：CI/CD 流水线配置、构建脚本、版本控制工作流执行、部署基础设施、分支策略、环境管理、CI 中自动化测试集成
- **不负责**：游戏逻辑或游戏玩法系统、安全审计（security-engineer）、QA 测试策略（qa-lead）、游戏网络逻辑（network-programmer）
- **模型层级**：Sonnet
- **关卡 ID**：无；部署阻塞项上报 producer

---

## 静态断言（结构检查）

- [ ] `description:` 字段存在且领域明确（引用 CI/CD、构建、部署、版本控制）
- [ ] `allowed-tools:` 列表与角色职责匹配（可读写流水线配置文件、shell 脚本、YAML；不含游戏源码编辑工具）
- [ ] 模型层级为 Sonnet（运营专员的默认层级）
- [ ] Agent 定义未主张对游戏逻辑、安全审计或 QA 测试设计拥有权

---

## 测试用例

### 用例 1：领域内请求——为 Godot 项目设置 CI
**输入**："为我们的 Godot 4 项目设置 CI 流水线。每次推送到 main 分支和每个 PR 时运行测试，测试失败则构建失败。"
**预期行为**：
- 产出 GitHub Actions 工作流 YAML（`.github/workflows/ci.yml` 或等效文件）
- 使用 `coding-standards.md` 中的 Godot 无头测试运行命令：`godot --headless --script tests/gdunit4_runner.gd`
- 配置 `push` 到 main 分支和 `pull_request` 时触发
- 测试失败时设置任务失败（`exit 1` 或非零退出）——不配置测试失败后继续构建
- 在输出或注释中引用项目的 coding standards CI 规则

### 用例 2：领域外请求——游戏网络实现
**输入**："为我们的多人游戏实现服务器权威的移动系统。"
**预期行为**：
- 不产出游戏网络或移动代码
- 明确声明："游戏网络实现由 network-programmer 负责；我负责构建、测试和部署游戏的基础设施"
- 不将 CI 流水线配置与游戏内网络架构混淆

### 用例 3：构建失败诊断
**输入**："我们的 CI 流水线在合并步骤失败。错误信息：'Asset import failed: texture compression format unsupported in headless mode.'"
**预期行为**：
- 诊断根本原因：无头 CI 环境不支持依赖 GPU 的纹理压缩
- 提出具体修复方案：(a) 在 CI 运行前在本地预先导入资产（将 .import 文件提交到版本控制），(b) 将 Godot 导入设置配置为在 CI 中使用 CPU 兼容的压缩格式，(c) 若有条件，使用带 GPU 模拟的 Docker 镜像
- 不宣布流水线无法修复——至少提供一个可行路径
- 注明各方案的权衡（提交 .import 文件会增加仓库体积；CPU 压缩可能与 GPU 输出不同）

### 用例 4：分支策略冲突
**输入**："团队一半人想用 GitFlow 配合长期 feature 分支，另一半想用主干开发。如何设置？"
**预期行为**：
- 根据项目惯例（CLAUDE.md / coordination-rules.md 规定采用 Git 主干开发）推荐主干开发
- 在该项目背景下提供具体推荐理由：团队规模较小、集成冲突更少、CI 反馈更快
- 若项目已有既定惯例，不将此呈现为50/50的自由选择
- 解释如何通过短期 feature 分支和功能开关实现主干开发
- 不在未标注"需更新 CLAUDE.md"的情况下覆盖项目惯例

### 用例 5：上下文传递——多平台构建矩阵
**上下文输入**：项目目标平台：PC（Windows、Linux）、Nintendo Switch、PlayStation 5。
**输入**："设置 CI 构建矩阵，使每次向 release 分支推送时，都能为各目标平台生成构建产物。"
**预期行为**：
- 产出包含三个平台条目的构建矩阵：Windows、Linux、Switch、PS5
- 为各平台应用对应的构建步骤：PC 使用标准 Godot 导出模板；Switch 和 PS5 需要平台专属导出模板（注明主机模板需要授权 SDK，不公开分发）
- 不假设所有平台可使用相同构建运行器——标记主机构建可能需要安装了授权 SDK 的自托管运行器
- 在流水线输出中按平台名称组织产物

---

## 协议合规

- [ ] 保持在声明领域内（CI/CD、构建脚本、版本控制、部署）
- [ ] 将游戏逻辑和网络请求重定向给对应程序员
- [ ] 在分支策略存在争议时，根据项目惯例推荐主干开发
- [ ] 返回结构化的流水线配置（YAML、脚本），而非自由形式建议
- [ ] 标记主机构建的 SDK 许可限制，而非静默产出错误配置

---

## 覆盖说明
- 用例 1（Godot CI）引用 `coding-standards.md` 的 CI 规则——运行此测试前，请验证该文件存在且是最新版
- 用例 4（分支策略）是惯例执行测试——Agent 必须了解项目惯例，而非只给出中立建议
- 用例 5 需要项目目标平台已记录在案（在 `technical-preferences.md` 或等效文件中）
- 无自动化运行程序；通过人工审阅或 `/skill-test` 进行测试
