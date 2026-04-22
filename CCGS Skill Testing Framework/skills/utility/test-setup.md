# 技能测试规范：/test-setup

## 技能概要

`/test-setup` 根据项目的游戏引擎搭建测试框架和目录结构。
它创建 `tests/` 目录及 4 个标准子目录：`unit/`、`integration/`、
`performance/` 和 `playtest/`，并安装引擎特定的测试运行器配置
（Godot→GdUnit4、Unity→.asmdef 文件、Unreal→无头运行器脚本）。

每个文件/目录写入均需"May I write"批准。若 `tests/` 已存在且有内容，
技能会验证其符合预期结构——而不是重新初始化（以防止覆盖现有测试）。
若未配置引擎，技能会重定向至 `/setup-engine`。
无 director 门控；始终以 COMPLETE 判定结束。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判定关键词：COMPLETE
- [ ] 在写入测试框架文件前包含"May I write"协作协议语言
- [ ] 包含下一步交接（例如 `/test-helpers` 生成辅助工具，或 `/qa-plan` 开始规划）

---

## Director 门控检查

无。`/test-setup` 是项目搭建技能，不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——Godot 4 + GdUnit4 测试运行器，创建所有 4 个目录

**夹具：**
- `technical-preferences.md` 显示引擎为 Godot 4，语言为 GDScript
- `tests/` 目录不存在

**输入：** `/test-setup`

**预期行为：**
1. 技能读取 `technical-preferences.md` 获取引擎（Godot 4 + GDScript）
2. 技能展示将要创建内容的完整清单：
   - `tests/` 目录
   - `tests/unit/`、`tests/integration/`、`tests/performance/`、`tests/playtest/`
   - `tests/GdUnit4/` 运行器配置（或等效配置）
   - `tests/.gdignore`（如适用）
3. 技能询问"May I write the test framework structure?"
4. 批准后创建所有目录和配置文件
5. 技能报告每个已创建的内容
6. 判定结果为 COMPLETE

**断言：**
- [ ] 读取引擎配置前不生成任何内容
- [ ] 创建恰好 4 个测试子目录（unit/、integration/、performance/、playtest/）
- [ ] 包含 GdUnit4 测试运行器配置（Godot 特有）
- [ ] 写入框架前询问"May I write"
- [ ] 判定结果为 COMPLETE

---

### 用例 2：Unity 引擎——创建 Tests/ 目录和 .asmdef 文件

**夹具：**
- `technical-preferences.md` 显示引擎为 Unity，语言为 C#
- `tests/` 目录不存在

**输入：** `/test-setup`

**预期行为：**
1. 技能读取引擎（Unity + C#）
2. 技能规划 Unity 特定结构：
   - `tests/` 带有 `tests/EditMode/` 和 `tests/PlayMode/`
   - 每个子目录配有 `.asmdef` 文件（Unity 测试集成所需）
3. 技能询问"May I write the test framework structure?"
4. 创建目录和 .asmdef 文件
5. 判定结果为 COMPLETE

**断言：**
- [ ] 生成 .asmdef 文件（Unity 特有，非 GdUnit4 配置）
- [ ] 包含 EditMode 和 PlayMode 目录（Unity 测试规范）
- [ ] 不生成 GdUnit4 引用
- [ ] 判定结果为 COMPLETE

---

### 用例 3：框架已存在——验证而非重新初始化

**夹具：**
- `tests/unit/`、`tests/integration/` 存在且包含测试文件
- `tests/performance/` 缺失，`tests/playtest/` 缺失

**输入：** `/test-setup`

**预期行为：**
1. 技能检测到 `tests/` 已存在
2. 技能检查预期的子目录结构
3. 技能报告：
   - `tests/unit/` ✓（已存在）
   - `tests/integration/` ✓（已存在）
   - `tests/performance/` ✗（缺失）
   - `tests/playtest/` ✗（缺失）
4. 技能提出仅添加缺失目录（而非重新创建全部）
5. 询问"May I write `tests/performance/` and `tests/playtest/`?"
6. 仅创建缺失目录；现有测试文件保持不变
7. 判定结果为 COMPLETE

**断言：**
- [ ] 检测到现有 `tests/` 目录结构
- [ ] 不覆盖或重新初始化现有目录
- [ ] 识别并仅提出添加缺失目录
- [ ] 现有测试文件不被修改
- [ ] 判定结果为 COMPLETE

---

### 用例 4：引擎未配置——重定向至 /setup-engine

**夹具：**
- `technical-preferences.md` 引擎字段为占位符（"[CHOOSE: Godot 4 / Unity / Unreal Engine 5]"）
- `tests/` 目录不存在

**输入：** `/test-setup`

**预期行为：**
1. 技能读取 `technical-preferences.md`，检测到引擎字段仍为占位符
2. 技能停止并输出：
   "Engine not configured. Run `/setup-engine` first to configure your project engine."
3. 不创建任何目录或文件
4. 技能不继续执行

**断言：**
- [ ] 检测到引擎占位符（未配置）
- [ ] 输出重定向消息（提及 `/setup-engine`）
- [ ] 不写入任何文件或目录
- [ ] 技能停止而不继续执行

---

### 用例 5：Director 门控检查——无门控；test-setup 是项目搭建技能

**夹具：**
- 引擎已配置，`tests/` 目录不存在

**输入：** `/test-setup`

**预期行为：**
1. 技能完成完整的测试框架搭建
2. 任何时候都不会生成 director agent
3. 输出中不出现门控 ID

**断言：**
- [ ] 未调用任何 director 门控
- [ ] 不出现门控跳过消息
- [ ] 判定结果为 COMPLETE——无门控判定

---

## 协议合规性

- [ ] 生成任何内容前读取引擎配置
- [ ] 根据引擎生成不同配置（GdUnit4 vs .asmdef vs 无头运行器）
- [ ] 框架已存在时验证而非重新初始化
- [ ] 引擎未配置时重定向至 `/setup-engine`
- [ ] 写入前询问"May I write"
- [ ] 始终以 COMPLETE 判定结束

---

## 覆盖说明

- Unreal Engine 5 测试设置遵循与用例 1（Godot）相同的模式，
  但使用 Unreal 的无头测试运行器配置。该变体未单独测试。
- 在此基础上的 CI/CD 管道搭建（GitHub Actions、Jenkins）由 `/devops-engineer` 处理，
  超出 `/test-setup` 的技能范围。
- 多根工作区或子项目（一个 monorepo 中多个游戏）的测试框架搭建
  此处未测试。
