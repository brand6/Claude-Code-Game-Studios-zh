# 技能测试规范：/setup-engine

## 技能概要

`/setup-engine` 通过填充 `technical-preferences.md` 来配置项目的引擎、语言、
渲染后端、物理引擎、专项 agent 分配及命名约定。可接受可选的引擎参数
（例如 `/setup-engine godot`）以跳过引擎选择步骤。对于 `technical-preferences.md`
的每个章节，技能均会展示草稿并询问"May I write to `technical-preferences.md`?"，
然后再进行更新。

该技能还会根据所选引擎填充专项路由表（文件扩展名 → agent 映射）。
无 director 门控——配置是技术实用工具任务。文件完整写入后判定结果始终为 COMPLETE。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判定关键词：COMPLETE
- [ ] 在更新 technical-preferences.md 前包含"May I write"协作协议语言
- [ ] 包含下一步交接（例如 `/brainstorm` 或 `/start`，取决于流程）

---

## Director 门控检查

无。`/setup-engine` 是技术配置技能，不适用 director 门控。

---

## 测试用例

### 用例 1：Godot 4 + GDScript——完整引擎配置

**夹具：**
- `technical-preferences.md` 仅包含占位符
- 已提供引擎参数：`godot`

**输入：** `/setup-engine godot`

**预期行为：**
1. 技能跳过引擎选择步骤（已提供参数）
2. 技能展示 Godot 的语言选项：GDScript 或 C#
3. 用户选择 GDScript
4. 技能起草所有引擎章节：引擎/语言/渲染/物理字段、命名约定（GDScript 用 snake_case）、
   专项分配（godot-specialist、gdscript-specialist、godot-shader-specialist 等）
5. 技能填充路由表：`.gd` → gdscript-specialist，`.gdshader` → godot-shader-specialist，
   `.tscn` → godot-specialist
6. 技能询问"May I write to `technical-preferences.md`?"
7. 批准后写入文件；判定结果为 COMPLETE

**断言：**
- [ ] 引擎字段设置为 Godot 4（非占位符）
- [ ] 语言字段设置为 GDScript
- [ ] 命名约定符合 GDScript 规范（snake_case）
- [ ] 路由表包含 `.gd`、`.gdshader` 和 `.tscn` 条目
- [ ] 已分配专项 agent（非占位符）
- [ ] 写入前询问"May I write"
- [ ] 判定结果为 COMPLETE

---

### 用例 2：Unity + C#——Unity 专项配置

**夹具：**
- `technical-preferences.md` 仅包含占位符
- 已提供引擎参数：`unity`

**输入：** `/setup-engine unity`

**预期行为：**
1. 技能将引擎设置为 Unity，语言设置为 C#
2. 命名约定符合 C# 规范（类名用 PascalCase，字段用 camelCase）
3. 专项分配引用 unity-specialist、csharp-specialist
4. 路由表：`.cs` → csharp-specialist，`.asmdef` → unity-specialist，
   `.unity`（场景）→ unity-specialist
5. 技能询问"May I write to `technical-preferences.md`?"并在批准后写入

**断言：**
- [ ] 引擎字段设置为 Unity（非 Godot 或 Unreal）
- [ ] 语言字段设置为 C#
- [ ] 命名约定反映 C# 规范
- [ ] 路由表包含 `.cs` 和 `.unity` 条目
- [ ] 判定结果为 COMPLETE

---

### 用例 3：Unreal + Blueprint——Unreal 专项配置

**夹具：**
- `technical-preferences.md` 仅包含占位符
- 已提供引擎参数：`unreal`

**输入：** `/setup-engine unreal`

**预期行为：**
1. 技能将引擎设置为 Unreal Engine 5，主要语言设置为 Blueprint（可视化脚本）
2. 专项分配引用 unreal-specialist、blueprint-specialist
3. 路由表：`.uasset` → blueprint-specialist 或 unreal-specialist，`.umap` → unreal-specialist
4. 性能预算预设为 Unreal 默认值（例如更高的 draw call 预算）
5. 技能询问"May I write"并在批准后写入；判定结果为 COMPLETE

**断言：**
- [ ] 引擎字段设置为 Unreal Engine 5
- [ ] 路由表包含 `.uasset` 和 `.umap` 条目
- [ ] 已分配 Blueprint 专项
- [ ] 判定结果为 COMPLETE

---

### 用例 4：引擎已配置——提供特定章节重新配置选项

**夹具：**
- `technical-preferences.md` 已将引擎设置为 Godot 4，所有字段均已填充
- 未提供引擎参数

**输入：** `/setup-engine`

**预期行为：**
1. 技能读取 `technical-preferences.md` 并检测到已完整配置的引擎（Godot 4）
2. 技能报告："Engine already configured as Godot 4 + GDScript"
3. 技能展示选项：重新配置全部、仅重新配置特定章节
   （引擎/语言、命名约定、专项、性能预算）
4. 用户选择"仅重新配置性能预算"
5. 仅更新性能预算章节；所有其他字段保持不变
6. 技能询问"May I write to `technical-preferences.md`?"并在批准后写入

**断言：**
- [ ] 仅请求更新章节时，技能不会覆盖所有字段
- [ ] 向用户提供特定章节重新配置选项
- [ ] 写入文件时仅修改所选章节
- [ ] 判定结果为 COMPLETE

---

### 用例 5：Director 门控检查——无门控；setup-engine 是实用技能

**夹具：**
- 未配置引擎的全新项目

**输入：** `/setup-engine godot`

**预期行为：**
1. 技能完成完整的引擎配置
2. 任何时候都不会生成 director agent
3. 输出中不出现门控 ID

**断言：**
- [ ] 未调用任何 director 门控
- [ ] 不出现门控跳过消息
- [ ] 不经过任何门控检查即得出 COMPLETE 判定

---

## 协议合规性

- [ ] 在询问是否写入前展示配置草稿
- [ ] 在写入前询问"May I write to `technical-preferences.md`?"
- [ ] 提供引擎参数时予以遵循（跳过选择步骤）
- [ ] 检测现有配置并提供部分重新配置
- [ ] 为所选引擎的所有关键文件类型填充路由表
- [ ] 文件写入后判定结果为 COMPLETE

---

## 覆盖说明

- Godot 4 + C#（而非 GDScript）遵循与用例 1 相同的流程，但使用不同的命名约定
  并分配 godot-csharp-specialist。该变体未单独测试。
- 引擎版本专项指导（例如来自 VERSION.md 的 Godot 4.6 知识空白警告）由技能提示，
  但此处未进行断言测试。
- 各引擎的性能预算默认值作为引擎专项内容说明，但未对精确默认值进行断言测试。
