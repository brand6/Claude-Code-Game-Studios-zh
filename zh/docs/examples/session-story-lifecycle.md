# 示例会话：完整故事生命周期 — /story-readiness → 实现 → /story-done

**背景：** 独立游戏开发者，处于生产冲刺中期。移动系统 GDD 和架构已完成。一个移动核心实现的故事已由 `/create-stories` 生成。

**初始状态：**
- `design/gdd/movement-system.md` — 完整，包含所有 8 个章节
- `docs/architecture/movement-adr-001.md` — 状态：已接受
- `production/sprints/sprint-03.md` — 在待办列表中列出 STORY-MOV-001
- `production/stories/STORY-MOV-001.md` — 已存在但尚未验证
- 尚无实现代码

**会话时长：** 约 50 分钟
**轮数：** 13
**结果：** 故事验证就绪、实现完成、通过 `/story-done` 验证完成

---

## 阶段 1：故事就绪检查

### 第 1 轮：用户运行就绪检查

**用户：**
> /story-readiness production/stories/STORY-MOV-001.md

### 第 2 轮：智能体验证故事

**智能体（通过 /story-readiness）：**
> 读取 `production/stories/STORY-MOV-001.md`……
>
> **STORY-MOV-001：实现带地形修正器的 CharacterBody2D 移动**
>
> 运行 4 项验证检查：
>
> **1. 设计完整性**
> - GDD 已引用：`design/gdd/movement-system.md` ✅
> - GDD 章节覆盖：详细规则 ✅、公式 ✅、边缘情况 ✅
> - TR-ID 已嵌入：TR-MOV-001 至 TR-MOV-008 ✅
>
> **2. 架构完整性**
> - ADR 已引用：`docs/architecture/movement-adr-001.md` ✅
> - ADR 状态：**已接受** ✅ *（若为"已提议"则 BLOCKED）*
> - 故事中的控制清单版本：`2026-03-10` — 当前清单为 `2026-03-10` ✅
>
> **3. 范围清晰度**
> - 验收标准：9 项，均可测量 ✅
> - 已列出超出范围项：游泳、攀爬 ✅
> - 发现歧义：**1 项**
>   - ⚠️ 故事说"翻滚方向跟随最后的输入方向"，但 GDD 说"朝移动方向翻滚"——当玩家停止后立即翻滚时这两者相冲突。请在开始前澄清。
>
> **4. 完成定义**
> - 需要的测试：公式函数的单元测试 ✅
> - 集成信号：`on_stamina_event` 必须正确触发 ✅
>
> ---
> **结论：需要修改**
>
> 必须在开始实现前解决一个歧义。你想现在解决，以便我将故事标记为就绪吗？

### 第 3 轮：用户解决歧义

**用户：**
> 翻滚使用最后的移动方向。如果玩家站立不动，则翻滚使用当前朝向。

### 第 4 轮：智能体更新故事

**智能体：**
> 更新故事的详细规则章节：
>
> > 翻滚方向：最后的移动方向。如果输入翻滚时速度为零，翻滚使用当前朝向。
>
> 我可以将此写入 `production/stories/STORY-MOV-001.md` 并将状态设置为 `ready-for-dev` 吗？

**用户：**
> 可以

**智能体写入更新。故事状态：`ready-for-dev`。**

> **结论：就绪**
> 故事已准备好实现。准备好构建时即可开始。

---

## 阶段 2：实现

### 第 5 轮：用户开始实现

**用户：**
> 让我们实现 STORY-MOV-001。我准备好开始编码了。

### 第 6 轮：智能体读取故事和 ADR

**智能体（gameplay-programmer）：**
> 读取 `production/stories/STORY-MOV-001.md`、`design/gdd/movement-system.md` 和 `docs/architecture/movement-adr-001.md`……
>
> **架构（来自 ADR-001）：**
> - `MovementComponent.gd` — 附加到玩家场景，不是单例
> - 通过 `TerrainLayer.get_modifier(tile_position)` 辅助方法进行地形修正器查找
> - 耐力事件通过信号（不直接调用 StaminaSystem）
>
> **我提议的文件结构：**
> ```
> src/gameplay/movement/
>   movement_component.gd       # CharacterBody2D 逻辑、状态机
>   terrain_modifier_table.gd   # 常量表：terrain_type -> {speed_mod, drain_mod}
> tests/unit/
>   test_movement_formulas.gd   # 速度/消耗计算的单元测试
> ```
>
> 可以继续这个结构吗？

**用户：**
> 可以

### 第 7 轮：智能体实现并展示关键代码

**智能体：**
> 实现 `movement_component.gd`。在我写入文件之前供你审查的关键代码节选：
>
> ```gdscript
> class_name MovementComponent
> extends Node
>
> signal stamina_event(type: String, amount: float)
>
> @export var base_walk_speed: float = 120.0
> @export var run_multiplier: float = 1.7
> @export var stamina_drain_walk: float = 2.0
> @export var stamina_drain_run: float = 6.0
> @export var stamina_cost_roll: float = 15.0
>
> var _is_carrying_heavy: bool = false
>
> func _physics_process(delta: float) -> void:
>     var terrain_mod := _get_terrain_modifier()
>     var effective_speed := _calculate_speed(terrain_mod)
>     # ...
> ```
>
> 所有值均为 `@export` — 无硬编码值。这是你想要的方向吗？

**用户：**
> 看起来不错。写入。

### 第 8-9 轮：智能体写入文件和测试

**智能体写入：**
- `src/gameplay/movement/movement_component.gd`
- `src/gameplay/movement/terrain_modifier_table.gd`
- `tests/unit/test_movement_formulas.gd`

**智能体：**
> 文件已写入。运行可用的代码检查……
>
> 无错误。测试文件已创建，包含 6 个单元测试，涵盖：
> - 行走速度公式（3 种地形类型）
> - 奔跑速度公式
> - 耐力消耗计算
> - 翻滚耐力消耗（含和不含速度为零的边缘情况）
>
> 以下需要手动测试：无敌帧、坡度阻挡、地形集成（需要运行场景）。

---

## 阶段 3：故事完成

### 第 10 轮：用户手动测试并运行 /story-done

**用户：**
> 我在场景中测试过了——一切正常。/story-done production/stories/STORY-MOV-001.md

### 第 11 轮：智能体运行完成审查

**智能体（通过 /story-done）：**
> 读取故事、GDD、ADR……
>
> **阶段 1：故事已定位** ✅ `production/stories/STORY-MOV-001.md`
>
> **阶段 2：验收标准验证**
>
> | # | 标准 | 验证 | 状态 |
> |---|------|------|------|
> | 1 | 普通地面行走速度正确 | 自动：公式单元测试通过 | ✅ 自动 |
> | 2 | 奔跑速度正确 | 自动：公式单元测试通过 | ✅ 自动 |
> | 3 | 耐力为 0 时奔跑取消 | 手动：用户已确认 | ✅ 手动 |
> | 4 | 翻滚无敌帧正常 | 手动：用户已确认 | ✅ 手动 |
> | 5 | 地形修正器正确应用 | 手动：用户已确认 | ✅ 手动 |
> | 6 | 携带重物禁用奔跑 | 自动：尚不可测（背包未集成） | ⏳ 已推迟 |
> | 7 | 耐力信号正确触发 | 自动：集成测试待完成 | ⏳ 已推迟 |
> | 8 | 无硬编码值 | 自动：grep 魔法数字 → 0 个 | ✅ 自动 |
> | 9 | >45° 坡度阻挡移动 | 手动：用户已确认 | ✅ 手动 |
>
> **阶段 3：GDD/ADR 偏差**
>
> 扫描实现与 TR-ID 的对比……
>
> - TR-MOV-001 至 TR-MOV-007：✅ 按规格实现
> - TR-MOV-008（重物携带信号）：⚠️ 建议 — 推迟到背包集成故事。不是偏差，只是现在无法验证。
>
> **阶段 4：清单陈旧性检查**
>
> 故事控制清单版本 `2026-03-10` 与当前清单 `2026-03-10` 匹配。✅
>
> **阶段 5：代码审查提示**
>
> 建议在标记为完成之前运行 `/code-review src/gameplay/movement/`。不构成阻塞。
>
> ---
> **完成报告：带注释完成**
>
> 故事已完成。两个标准推迟至背包集成——记录为已推迟，而非被阻塞。
>
> 我可以将故事状态更新为 `Status: Complete` 并添加完成注释，同时更新 `production/sprint-status.yaml` 吗？

**用户：**
> 可以

### 第 12 轮：智能体关闭故事

**智能体写入：**
- 故事 `Status: Complete` + 完成注释（已推迟标准已记录）
- `production/sprint-status.yaml` — STORY-MOV-001 设置为 `done`

**智能体：**
> STORY-MOV-001 已关闭。
>
> **已推迟标准已记录**（将在背包集成故事中自动浮现）：
> - 携带重物禁用奔跑（需要背包信号）
> - 耐力信号集成测试（需要耐力系统）
>
> **冲刺中下一个就绪故事：**
> - STORY-MOV-002：耐力系统 — 这是逻辑上的下一个故事（下游依赖现已解除阻塞）
> - STORY-HUD-001：移动 HUD 指示器 — 也已解除阻塞
>
> 运行 `/story-readiness` 检查你接下来选择的故事。

---

## 本示例展示了什么

- **就绪关卡捕获真实问题**：翻滚方向歧义在没有 `/story-readiness` 的情况下会导致后期实现决策
- **ADR 状态是硬性关卡**：如果 `movement-adr-001.md` 是"已提议"而非"已接受"，故事将是 `BLOCKED`，实现不会开始
- **已推迟标准**：不是每个验收标准都能在故事关闭时验证——`/story-done` 跟踪已推迟项而非阻塞完成
- **TR-ID 引用**：故事存储 `TR-MOV-001` ID，不是引用 GDD 文本——当 GDD 措辞后续被清理时，避免误判偏差标志
- **sprint-status.yaml**：冲刺状态的单一权威来源，由 `/story-done` 更新，由 `/sprint-status` 读取
- **清单版本检查**：确保故事的实现指导没有偏离当前架构决策
