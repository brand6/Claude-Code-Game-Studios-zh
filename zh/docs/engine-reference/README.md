# 引擎参考文档

本目录包含本项目所用游戏引擎的精选版本固定文档快照。这些文件的存在是因为 **LLM 的训练数据存在截止日期**，而游戏引擎更新频繁。

## 为什么需要这些文件

Claude 的训练数据存在知识截止日期（目前为 2025 年 5 月）。Godot、Unity、Unreal 等游戏引擎不断推出更新，引入破坏性 API 变更、新功能和已废弃的模式。如果没有这些参考文件，Agent 将会建议使用过时的代码。

## 目录结构

每个引擎拥有独立子目录：

```
<engine>/
├── VERSION.md              # 固定版本、验证日期、知识空白窗口
├── breaking-changes.md     # 各版本之间的 API 变更，按风险级别整理
├── deprecated-apis.md      # "不要用 X → 改用 Y" 对照表
├── current-best-practices.md  # 模型训练数据之外的新实践
└── modules/                # 按子系统划分的快速参考（每文件最多约150行）
    ├── rendering.md
    ├── physics.md
    └── ...
```

## Agent 如何使用这些文件

引擎专家 Agent 被要求：

1. 读取 `VERSION.md` 确认当前引擎版本
2. 在建议任何引擎 API 之前检查 `deprecated-apis.md`
3. 查阅 `breaking-changes.md` 了解特定版本问题
4. 阅读相关 `modules/*.md` 了解子系统细节

## 维护

### 何时更新

- 升级引擎版本之后
- LLM 模型更新时（新的知识截止日期）
- 运行 `/refresh-docs` 之后（如有）
- 当你发现模型对某个 API 的理解有误时

### 如何更新

1. 更新 `VERSION.md`，填入新引擎版本和日期
2. 在 `breaking-changes.md` 中添加版本过渡的新条目
3. 将新废弃的 API 移入 `deprecated-apis.md`
4. 用新的模式更新 `current-best-practices.md`
5. 更新相关 `modules/*.md` 中的 API 变更
6. 在所有修改过的文件上设置"最后验证"日期

### 质量规范

- 每个文件必须包含"Last verified: YYYY-MM-DD"日期
- 模块文件保持在 150 行以内（上下文预算限制）
- 包含展示正确/错误模式的代码示例
- 链接到官方文档 URL 以供核实
- 只记录与模型训练数据不同的内容
