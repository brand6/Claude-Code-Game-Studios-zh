# 技能测试规范：/reverse-document

## 技能概要

`/reverse-document` 从现有源代码生成设计或架构文档，
推断设计意图，并生成 GDD 骨架（游戏系统）或架构概述（技术系统）。

当源代码结构清晰（清晰的类名、有意义的变量名、内联注释）时，
技能生成完整的文档草稿，判决为 COMPLETE。
当存在魔法数字或逻辑不明确时，技能在文档中标记模糊区域，
判决为 PARTIAL。

多个相互依赖的文件可以一起处理，以生成跨系统概述文档。
不适用 director 门控。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判决关键词：COMPLETE、PARTIAL
- [ ] 在写入文档前包含"May I write"协作协议语言
- [ ] 包含下一步交接（例如 `/design-review` 以验证生成的文档）

---

## Director 门控检查

无。`/reverse-document` 是文档生成工具。不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——结构清晰的源代码生成完整 GDD，COMPLETE

**夹具：**
- `src/gameplay/combat/damage-system.gd` 存在：
  - 清晰的函数名：`calculate_damage()`、`apply_status_effect()`
  - 内联注释解释了游戏设计意图
  - 有意义的常量名：`BASE_DAMAGE_MULTIPLIER = 1.5`

**输入：** `/reverse-document src/gameplay/combat/damage-system.gd`

**预期行为：**
1. 技能读取 `damage-system.gd`
2. 技能推断游戏系统目的：伤害计算和状态效果
3. 技能生成 GDD 骨架草稿，包含：
   - 系统概述
   - 核心机制（根据函数名推断）
   - 参数（根据常量推断）
   - 缺失的已知内容（如：是否有设计意图说明）
4. 技能询问"May I write to `design/gdd/damage-system.md`?"
5. 文件写入；判决为 COMPLETE

**断言：**
- [ ] 推断的游戏系统目的与源代码相符
- [ ] GDD 骨架中包含从函数名推断的核心机制
- [ ] 写入前询问"May I write"
- [ ] 判决为 COMPLETE

---

### 用例 2：含魔法数字的模糊源代码——PARTIAL

**夹具：**
- `src/gameplay/economy/shop-system.gd` 包含硬编码的魔法数字：
  - `if player_gold >= 42` → 未命名的价格阈值
  - `discount = item_price * 0.73` → 未命名的折扣常量
  - 几乎没有内联注释

**输入：** `/reverse-document src/gameplay/economy/shop-system.gd`

**预期行为：**
1. 技能读取 `shop-system.gd`
2. 技能检测到多个魔法数字（42、0.73）及模糊的设计意图
3. 技能生成包含模糊区域标注的 GDD 草稿：
   - "UNCLEAR: `42` — appears to be a gold threshold; design intent unknown"
   - "UNCLEAR: `0.73` — appears to be a 27% discount; source unknown"
4. 判决为 PARTIAL（存在模糊区域需要人工审查）

**断言：**
- [ ] 模糊区域以 UNCLEAR 或类似标记标注
- [ ] 魔法数字（42、0.73）在文档中被识别并标记
- [ ] 判决为 PARTIAL（不是 COMPLETE）
- [ ] 写入前询问"May I write"（PARTIAL 文档仍然写入，附标注）

---

### 用例 3：多个互相依赖的文件——生成跨系统概述

**夹具：**
- `src/core/save-manager.gd`：处理存档/读档
- `src/gameplay/progression/level-up-system.gd`：处理角色升级
- 两个文件有互相调用的函数引用

**输入：** `/reverse-document src/core/save-manager.gd src/gameplay/progression/level-up-system.gd`

**预期行为：**
1. 技能读取两个文件
2. 技能检测到文件间的依赖关系（level-up-system 调用 save-manager 函数）
3. 技能生成跨系统概述，说明两个系统如何协同工作
4. 文档标注系统间的依赖关系
5. 询问"May I write to `design/gdd/save-progression-systems.md`?"
6. 写入文件；判决为 COMPLETE（或若存在模糊区域则为 PARTIAL）

**断言：**
- [ ] 两个系统均出现在生成的文档中
- [ ] 系统间的依赖关系在文档中有所记录
- [ ] 生成一个文档（而非每个文件各一个）

---

### 用例 4：源文件未找到——报错

**夹具：**
- `src/gameplay/ai/pathfinding.gd` 不存在

**输入：** `/reverse-document src/gameplay/ai/pathfinding.gd`

**预期行为：**
1. 技能尝试读取文件——未找到
2. 技能输出："Error: `src/gameplay/ai/pathfinding.gd` not found"
3. 技能建议检查文件路径或运行 `/map-systems` 以确认正确的源文件
4. 不生成文档

**断言：**
- [ ] 源文件未找到时输出错误消息
- [ ] 提供备选建议（检查路径或运行 `/map-systems`）
- [ ] 不写入任何文件
- [ ] 不发出 COMPLETE 或 PARTIAL 判决——技能终止于报错状态

---

### 用例 5：Director 门控检查——无门控；reverse-document 为文档生成工具

**夹具：**
- 有效的源文件

**输入：** `/reverse-document`

**预期行为：**
1. 技能生成并写入文档
2. 未调用任何 director agent
3. 输出中无门控 ID

**断言：**
- [ ] 未调用 director 门控
- [ ] 输出中无门控跳过消息
- [ ] 技能在不经过任何门控检查的情况下达到 COMPLETE 或 PARTIAL

---

## 协议合规

- [ ] 读取源文件以推断设计意图
- [ ] 在文档草稿中标记模糊区域（魔法数字、不明确的逻辑）
- [ ] 源代码清晰时判决为 COMPLETE
- [ ] 存在模糊区域时判决为 PARTIAL
- [ ] 写入前询问"May I write"
- [ ] 对多文件输入生成跨系统概述

---

## 覆盖说明

- 生成架构概述与 GDD 骨架的判断逻辑在技能主体中定义（由文件路径暗示）；
  `src/core/` 和 `src/networking/` 中的文件生成架构文档，
  `src/gameplay/` 中的文件生成 GDD 文档。
- 语言适配（GDScript vs. C# vs. Blueprints）在技能主体中定义；
  此规范不对跨引擎语言分析进行硬编码断言。
- 逆向文档的质量取决于源代码的质量——此规范接受 PARTIAL 判决作为低质量代码的有效结果。
