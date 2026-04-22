# 技能测试规范：/test-helpers

## 技能概要

`/test-helpers` 为项目的测试套件生成引擎特定的测试辅助工具库。
辅助工具包括：工厂函数（从 GDD 默认值生成实体）、夹具加载器、
断言辅助工具（测试特定断言）和模拟对象存根（用于隔离外部依赖）。
辅助工具写入 `tests/helpers/` 目录。

每个辅助工具文件均需"May I write to `tests/helpers/[文件名]`?"批准。
若辅助工具文件已存在，技能会提供扩展现有文件与创建新文件的选项。
若不存在 `tests/` 目录，技能会将用户重定向至 `/test-setup`。
无 director 门控；始终以 COMPLETE 判定结束。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判定关键词：COMPLETE
- [ ] 在写入辅助工具文件前包含"May I write"协作协议语言
- [ ] 包含下一步交接（例如 `/smoke-check` 或 `/qa-plan` 以使用生成的辅助工具）

---

## Director 门控检查

无。`/test-helpers` 是测试基础设施技能，不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——Godot/GDScript 玩家工厂辅助工具

**夹具：**
- `technical-preferences.md` 显示引擎为 Godot 4，语言为 GDScript
- `design/gdd/player-character.md` 包含玩家属性默认值（生命值：100，移动速度：300）
- `tests/helpers/` 目录存在但为空

**输入：** `/test-helpers player`

**预期行为：**
1. 技能读取 `technical-preferences.md` 获取引擎/语言（Godot 4 + GDScript）
2. 技能读取玩家 GDD 获取默认值（生命值 100，移动速度 300）
3. 技能生成 GDScript 工厂辅助工具：
   - 函数名使用 snake_case（GDScript 规范）
   - 工厂函数支持参数覆盖（依赖注入模式）
   - GDD 中的默认值（生命值 100）成为工厂默认参数
4. 技能询问"May I write to `tests/helpers/player_factory.gd`?"
5. 写入文件；判定结果为 COMPLETE

**断言：**
- [ ] 生成的代码使用 snake_case 命名（符合 GDScript 规范）
- [ ] 工厂函数参数从 GDD 中的默认值获取（生命值 100，移动速度 300）
- [ ] 工厂函数支持参数覆盖（依赖注入）
- [ ] 写入前询问"May I write to `tests/helpers/player_factory.gd`?"
- [ ] 判定结果为 COMPLETE

---

### 用例 2：无 tests/ 目录——重定向至 /test-setup

**夹具：**
- 项目没有 `tests/` 目录（尚未搭建测试框架）

**输入：** `/test-helpers enemy`

**预期行为：**
1. 技能检查 `tests/` 目录——不存在
2. 技能停止并输出：
   "No `tests/` directory found. Run `/test-setup` first to scaffold the test framework."
3. 不生成辅助工具文件
4. 技能不继续执行

**断言：**
- [ ] 检测到 `tests/` 目录缺失
- [ ] 输出重定向消息（提及 `/test-setup`）
- [ ] 不写入任何文件
- [ ] 技能不继续执行

---

### 用例 3：辅助工具文件已存在——扩展与新建文件选项

**夹具：**
- `tests/helpers/player_factory.gd` 已存在（包含基本工厂函数）
- 请求用新的辅助方法增强玩家辅助工具

**输入：** `/test-helpers player`

**预期行为：**
1. 技能检测到 `tests/helpers/player_factory.gd` 已存在
2. 技能提供选项：
   - 扩展现有文件（追加新辅助函数）
   - 创建新文件（例如 `player_factory_v2.gd`）
3. 用户选择"扩展现有文件"
4. 技能生成要追加的新辅助函数
5. 技能询问"May I extend `tests/helpers/player_factory.gd`?"
6. 追加新函数；判定结果为 COMPLETE

**断言：**
- [ ] 检测到现有辅助工具文件
- [ ] 提供扩展与新建选项（不默认覆盖）
- [ ] 扩展时不替换现有内容（仅追加）
- [ ] 询问"May I extend"（而非 "May I write"，反映追加操作）
- [ ] 判定结果为 COMPLETE

---

### 用例 4：无 GDD——使用 TODO 注释的占位符默认值

**夹具：**
- `technical-preferences.md` 显示 Godot 4 + GDScript
- 系统（`inventory`）不存在 GDD 文件

**输入：** `/test-helpers inventory`

**预期行为：**
1. 技能检查是否有 inventory GDD——未找到
2. 技能生成带有占位符默认值的辅助工具，并附有 TODO 注释：
   ```gdscript
   # TODO: Replace placeholder defaults with values from GDD once designed
   const DEFAULT_INVENTORY_SIZE = 20  # placeholder
   const DEFAULT_ITEM_COUNT = 0        # placeholder
   ```
3. 技能告知用户："No GDD found for inventory. Generated helpers with placeholder defaults.
   Update after `/design-system inventory` is complete."
4. 询问"May I write to `tests/helpers/inventory_factory.gd`?"
5. 写入；判定结果为 COMPLETE

**断言：**
- [ ] 检测到 GDD 缺失并通知用户
- [ ] 生成的辅助工具包含 TODO 注释标记占位符
- [ ] 提及 `/design-system inventory` 作为下一步
- [ ] 尽管无 GDD 仍写入有效的辅助工具文件
- [ ] 判定结果为 COMPLETE

---

### 用例 5：Director 门控检查——无门控；test-helpers 是测试基础设施

**夹具：**
- `tests/` 目录存在，`technical-preferences.md` 已配置

**输入：** `/test-helpers combat`

**预期行为：**
1. 技能完成辅助工具生成
2. 任何时候都不会生成 director agent
3. 输出中不出现门控 ID

**断言：**
- [ ] 未调用任何 director 门控
- [ ] 不出现门控跳过消息
- [ ] 判定结果为 COMPLETE——无门控判定

---

## 协议合规性

- [ ] 在生成代码前读取引擎/语言配置
- [ ] 从 GDD 读取默认值（若可用）
- [ ] 无 GDD 时使用带 TODO 注释的占位符
- [ ] `tests/` 目录不存在时重定向至 `/test-setup`
- [ ] 检测现有辅助工具文件并提供扩展与新建选项
- [ ] 每个文件写入均获"May I write"或"May I extend"批准
- [ ] 始终以 COMPLETE 判定结束

---

## 覆盖说明

- Unity (C#) 和 Unreal (C++/Blueprint) 引擎的辅助工具使用不同的命名规范
  （PascalCase 而非 snake_case）并生成不同的测试框架代码。
  Unity 变体未单独测试——遵循与用例 1 相同的模式，但使用 C# 规范。
- 跨多个系统的批量辅助工具生成（例如 `/test-helpers player enemy inventory`）
  此处未测试；技能应支持通过多次调用分别处理每个系统。
