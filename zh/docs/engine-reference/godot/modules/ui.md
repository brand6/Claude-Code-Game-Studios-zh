# Godot UI — 快速参考

Last verified: 2026-02-12 | Engine: Godot 4.6

## 自 ~4.3（LLM 截止版本）以来的变更

### 4.6 变更
- **双焦点系统**：鼠标/触摸焦点现与键盘/手柄焦点**分开**
  - 不同输入方式的视觉反馈有所不同
  - 自定义焦点实现可能需要更新
- **TabContainer**：标签属性可直接在检查器中编辑
- **TileMapLayer 场景瓦片旋转**：场景瓦片可像图集瓦片一样旋转

### 4.5 变更
- **FoldableContainer**：新增折叠式 UI 节点，用于可收起区块
- **递归 Control 行为**：通过单一属性禁用整个节点层级的鼠标/焦点
- **屏幕阅读器支持**：Control 节点与 AccessKit 协同工作
- **实时翻译预览**：可在编辑器内测试不同语言
- **`RichTextLabel.push_meta`**：新增可选 `tooltip` 参数（来自 4.4）

### 4.4 变更
- **`GraphEdit.connect_node`**：新增可选 `keep_alive` 参数

## 当前 API 模式

### 主题与样式（4.6）
```gdscript
# 编辑器默认使用新的"Modern"主题
# 对于游戏 UI，照常使用自定义主题：
var theme := Theme.new()
theme.set_color(&"font_color", &"Label", Color.WHITE)
theme.set_font_size(&"font_size", &"Label", 24)
```

### 焦点管理（4.6 — 已变更）
```gdscript
# 键盘/手柄焦点（grab_focus 仍然有效）
func _ready() -> void:
    %StartButton.grab_focus()

# 重要：在 4.6 中，鼠标悬停焦点与键盘焦点是分开的
# 两者可以同时激活在不同控件上
# 务必分别用鼠标和键盘/手柄测试 UI

# 焦点邻居（不变）
%Button1.focus_neighbor_bottom = %Button2.get_path()
%Button1.focus_neighbor_right = %Button3.get_path()
```

### FoldableContainer（4.5 — 新增）
```gdscript
# 手风琴式可收起容器
# 作为要折叠内容的父节点添加
# 点击标题时子节点显示/隐藏
# 通过编辑器属性或代码配置
```

### 递归禁用（4.5 — 新增）
```gdscript
# 禁用整个节点层级的鼠标/焦点交互
# 适用于禁用整个菜单区块
%SettingsPanel.mouse_filter = Control.MOUSE_FILTER_IGNORE
# 在 4.5+ 中，此设置可递归传播到子节点
```

### 本地化就绪 UI（最佳实践）
```gdscript
# 对所有可见字符串使用 tr()
label.text = tr("MENU_START_GAME")

# 对标签使用自动换行（不同语言文本长度不同）
label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART

# 在编辑器中使用实时翻译预览测试（4.5+）
```

## 常见错误
- 假设 `grab_focus()` 影响鼠标焦点（4.6 中仅影响键盘/手柄）
- 升级到 4.6 后未分别用鼠标和手柄测试 UI
- 未使用 `tr()` 而是硬编码字符串（本地化问题）
- 未使用 `FoldableContainer` 实现可收起 UI（4.5 新增，比自定义实现更简洁）
