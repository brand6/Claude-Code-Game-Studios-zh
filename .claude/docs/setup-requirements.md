# 安装要求

此模板需要安装少量工具才能发挥完整功能。
所有 hooks 在缺少工具时均会优雅降级——不会报错，但会丢失对应的验证功能。

## 必需工具

| 工具 | 用途 | 安装方式 |
| ---- | ---- | ---- |
| **Git** | 版本控制、分支管理 | [git-scm.com](https://git-scm.com/) |
| **Claude Code** | AI Agent CLI | `npm install -g @anthropic-ai/claude-code` |

## 推荐工具

| 工具 | 使用方 | 用途 | 安装方式 |
| ---- | ---- | ---- | ---- |
| **jq** | Hooks（8 个中的 4 个）| 在提交/推送/资源/Agent hooks 中解析 JSON | 见下方 |
| **Python 3** | Hooks（8 个中的 2 个）| 数据文件的 JSON 校验 | [python.org](https://www.python.org/) |
| **Bash** | 所有 hooks | Shell 脚本执行 | Windows 版 Git 自带 |

### 安装 jq

**Windows**（任选其一）：
```
winget install jqlang.jq
choco install jq
scoop install jq
```

**macOS**：
```
brew install jq
```

**Linux**：
```
sudo apt install jq     # Debian/Ubuntu
sudo dnf install jq     # Fedora
sudo pacman -S jq       # Arch
```

## 平台说明

### Windows
- Windows 版 Git 自带 **Git Bash**，提供所有 hooks 所需的 `bash` 命令
- 确保 Git Bash 已加入 PATH（通过 Git 安装程序安装时默认添加）
- Hooks 使用 `bash .claude/hooks/[name].sh` ——在 Windows 上可正常运行，因为 Claude Code 通过可找到 `bash.exe` 的 shell 调用命令

### macOS / Linux
- Bash 原生可用
- 通过包管理器安装 `jq` 以获得完整 hook 支持

## 验证安装

运行以下命令检查前置条件：

```bash
git --version          # 应显示 git 版本
bash --version         # 应显示 bash 版本
jq --version           # 应显示 jq 版本（可选）
python3 --version      # 应显示 python 版本（可选）
```

## 缺少可选工具时的影响

| 缺少工具 | 影响 |
| ---- | ---- |
| **jq** | 提交校验、推送保护、资源校验和 Agent 审计 hooks 会静默跳过检查。提交和推送仍可正常进行。|
| **Python 3** | 提交和资源 hooks 中的 JSON 数据文件校验被跳过。无效 JSON 可能被提交而不发出警告。|
| **两者均缺** | 所有 hooks 仍会执行且不报错（exit 0），但不提供任何校验。相当于在没有安全网的情况下工作。|

## 推荐 IDE

Claude Code 可与任何编辑器配合使用，但本模板针对以下环境进行了优化：
- 安装了 Claude Code 插件的 **VS Code**
- **Cursor**（兼容 Claude Code）
- 终端版 Claude Code CLI
