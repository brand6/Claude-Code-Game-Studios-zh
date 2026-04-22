---
name: setup-engine
description: "配置项目的游戏引擎与版本。在 CLAUDE.md 中固定引擎，检测知识盲区，并在版本超出 LLM 训练数据时通过 WebSearch 填充引擎参考文档。"
argument-hint: "[engine] | [engine version] | refresh | upgrade [old-version] [new-version] | 无参数则进入引导选择"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, WebSearch, WebFetch, Task, AskUserQuestion
---

调用本技能时：

## 1. 解析参数

四种运行模式：

- **完整规格**：`/setup-engine godot 4.6` — 已提供引擎和版本
- **仅指定引擎**：`/setup-engine unity` — 已提供引擎，版本将自动查询
- **无参数**：`/setup-engine` — 完全引导模式（引擎推荐 + 版本选择）
- **刷新**：`/setup-engine refresh` — 更新参考文档（详见第 10 节）
- **升级**：`/setup-engine upgrade [old-version] [new-version]` — 迁移至新引擎版本（详见第 11 节）

---

## 2. 引导模式（无参数）

若未指定引擎，运行交互式引擎选择流程：

### 检查现有游戏概念
- 若 `design/gdd/game-concept.md` 存在，读取该文件，提取：类型、规模、目标平台、美术风格、团队规模，以及 `/brainstorm` 中的引擎建议
- 若不存在概念文档，告知用户：
  > "未找到游戏概念文档。建议先运行 `/brainstorm` 探索想要开发的游戏——它也会推荐引擎。或者告诉我你的游戏想法，我来帮你选择。"

### 若用户想在没有概念文档的情况下选择引擎，按以下顺序提问：

**问题 1 — 既有经验**（第一个问题，始终通过 `AskUserQuestion` 提问）：
- 提示："您曾使用过以下哪款引擎？"
- 选项：`Godot` / `Unity` / `Unreal Engine 5` / `多个引擎，我来说明` / `都没用过`
- 若选择了具体引擎 → 推荐该引擎。既有经验优先于所有其他因素。确认后跳过决策矩阵。
- 若选择"都没用过"或"多个引擎" → 继续以下问题。

**问题 2-6 — 决策矩阵输入**（仅当无既有引擎经验时）：

**问题 2 — 目标平台**（第二个问题，始终通过 `AskUserQuestion` 提问——平台因素在其他因素之前就能淘汰或强力倾向某引擎）：
- 提示："您的游戏计划覆盖哪些平台？"
- 选项：`PC（Steam / Epic）` / `移动端（iOS / Android）` / `主机` / `网页 / 浏览器` / `多平台`
- 平台规则（直接影响推荐结果）：
  - 移动端 → 强烈推荐 Unity；Unreal 不适合；Godot 适用于简单移动游戏
  - 主机 → Unity 或 Unreal；Godot 主机支持需要第三方发行商或大量额外工作
  - 网页 → Godot 导出网页最顺畅；Unity WebGL 可用；Unreal 网页支持差
  - 仅 PC → 三款引擎均可；由其他因素决定
  - 多平台 → Unity 跨 PC/移动/主机 的可移植性最强

1. **游戏类型？**（2D、3D 还是两者兼有？）
2. **主要输入方式？**（键鼠、手柄、触控还是混合？）
3. **团队规模与经验？**（独立新手、独立老手还是小团队？）
4. **语言偏好？**（GDScript、C#、C++ 还是可视化脚本？）
5. **引擎授权预算？**（仅免费，还是商业授权也可接受？）

### 给出推荐

**不要**使用淘汰引擎的简单评分矩阵。而是根据用户画像，结合以下真实利弊进行推理，再提出 1-2 个建议并给出完整背景说明。最终始终由用户做决定——绝不强行给出结论。

**各引擎真实利弊：**

**Godot 4**
- 真正的优势：2D（同类最佳）、风格化/独立 3D、快速迭代、永久免费（MIT 开源）、学习曲线最平缓、最适合想要完全掌控的独立开发者
- 真实局限：与 Unity/Unreal 相比，3D 生态系统较薄弱（教程、资源和社区对于 3D 专题问题的解答较少）；大型开放世界 3D 非常困难，在 Godot 中基本未经生产验证；主机导出需要第三方发行商或大量额外工作；职业市场较小
- 授权实情：真正免费，永远没有收入门槛。MIT 许可证意味着你拥有一切。
- 最适合：任何规模的 2D 游戏；风格化/氛围感 3D；有限的 3D 世界（非开放世界）；学习曲线很重要的第一个游戏项目；预算在任何规模都是硬约束的项目

**Unity**
- 真正的优势：中等规模 3D 和移动游戏的行业标准；资源商店和教程生态系统庞大；C# 是专业语言；对独立开发者来说主机认证支持最好；几乎所有类型都有强大的社区支持
- 真实局限：2023 年的授权风波损害了信任（曾提出运行时收费后撤回——政策变更的风险依然存在）；C# 比 GDScript 初期学习曲线更陡；对简单项目而言编辑器比 Godot 更重
- 授权实情：收入低于 20 万美元**且**安装量低于 20 万次时免费（Unity Personal/Plus）。只有游戏真正成功时才会产生费用——大多数独立游戏永远达不到这个门槛。2023 年的风波值得了解，但当前实际条款对大多数独立开发者来说是合理的。
- 最适合：移动游戏；中等规模 3D；面向主机的游戏；有 C# 背景的开发者；需要大型资源商店的项目；2-5 人小团队

**Unreal Engine 5**
- 真正的优势：业界最佳 3D 视觉效果（Lumen、Nanite、Chaos 物理）；AAA 和照片级真实感 3D 的行业标准；大型开放世界支持成熟且经生产验证；蓝图可视化脚本降低了 C++ 门槛；面向高端 PC 或主机的游戏最佳
- 真实局限：学习曲线最陡；编辑器最重（编译时间慢、项目体积大）；对风格化/2D/小规模游戏来说过度设计；C++ 真的很难；不适合移动或网页；超过 100 万美元毛收入后需缴纳 5% 版税
- 授权实情：5% 版税仅适用于每款游戏毛收入超过 100 万美元之后。对于第一款游戏或任何达不到 100 万美元的游戏，完全免费。这个门槛足够高，大多数独立开发者永远不会触达。
- 最适合：AAA 级 3D 品质；大型开放世界游戏；照片级真实感画面；有 C++ 经验或愿意使用蓝图的开发者；以画面品质为核心卖点、面向高端 PC/主机的游戏

**类型专项指导**（将此纳入推荐）：
- 2D 任何风格 → 强烈推荐 Godot
- 3D 风格化 / 氛围感 / 有限世界 → Godot 可行，Unity 是可靠的替代
- 3D 开放世界（大型、无缝衔接）→ Unity 或 Unreal；Godot 尚未在这方面经过生产验证
- 3D 照片级真实感 / AAA 品质 → Unreal
- 移动优先 → 强烈推荐 Unity
- 主机优先 → Unity 或 Unreal；Godot 主机支持需要额外工作
- 恐怖 / 叙事 / 步行模拟 → 任何引擎；根据美术风格和团队经验匹配
- 动作 RPG / 魂系游戏 → Unity 或 Unreal 用于 3D；社区支持和资源很重要
- 2D 平台跳跃 → Godot
- 策略 / 俯视角 / RTS → 根据 2D vs 3D 选择 Godot 或 Unity

**推荐格式：**
1. 展示以用户具体因素为行的对比表格
2. 给出主要推荐及诚实的推理
3. 说明最佳替代方案及何时应选择它
4. 明确说明："这只是起点，不是最终结论——你随时可以更换引擎，许多开发者在不同项目间切换引擎。"
5. 使用 `AskUserQuestion` 确认："这个推荐感觉合适吗？还是您想探索其他引擎？"
   - 选项：`[主推引擎]（推荐）` / `[替代引擎]` / `[第三引擎]` / `进一步探索` / `输入其他想法`

**若用户选择"进一步探索"：**
使用 `AskUserQuestion` 提供针对概念的深度问题选项。始终根据用户的实际概念生成这些选项——不要使用通用选项。至少包含：
- 主推引擎针对该概念的具体局限性（例如"Godot 3D 对于 [类型] 到底能做到什么程度？"）
- 替代引擎针对该概念的具体利弊
- 语言选择对该概念技术挑战的影响
- 任何概念专属的技术问题（如自适应音频、开放世界流式加载、多人游戏网络同步）

用户可以选择多个主题。在返回引擎确认问题之前，逐一深入解答每个主题。

---

## 3. 查询当前版本

确定引擎后：

- 若已提供版本，直接使用
- 若未提供版本，使用 WebSearch 查找最新稳定版本：
  - 搜索：`"[engine] latest stable version [current year]"`
  - 向用户确认："[engine] 最新稳定版是 [version]。使用此版本吗？"

---

## 4. 更新 CLAUDE.md 技术栈

### 语言选择（仅限 Godot）

若选择了 Godot，在展示建议的技术栈之前，先询问用户使用哪种语言：

> "Godot 支持两种主要语言：
>
>   **A) GDScript** — 类 Python 语法，Godot 原生，迭代速度最快。最适合初学者、独立开发者以及有 Python 或 Lua 经验的团队。
>   **B) C#** — .NET 8+，Unity 开发者熟悉，更强大的 IDE 工具支持（Rider / Visual Studio），重逻辑场景下有轻微性能优势。
>   **C) 两者兼用** — GDScript 用于游戏逻辑/UI 脚本，C# 用于性能关键系统。高级配置——需要在 Godot 旁安装 .NET SDK。
>
> 本项目主要使用哪种？"

记录选择结果。这将决定 CLAUDE.md 模板、命名规范、专家智能体路由，以及整个项目中代码文件调用的智能体。

---

读取 `CLAUDE.md`，向用户展示建议的技术栈变更。
询问："May I write these engine settings to `CLAUDE.md`？"

等待确认后再进行任何编辑。

更新技术栈章节，将 `[CHOOSE]` 占位符替换为实际值：

**Godot** — 使用与上方语言选择匹配的模板。所有三个变体（GDScript、C#、两者兼用）详见本技能末尾的**附录 A**。

**Unity：**
```markdown
- **Engine**: Unity [version]
- **Language**: C#
- **Build System**: Unity Build Pipeline
- **Asset Pipeline**: Unity Asset Import Pipeline + Addressables
```

**Unreal：**
```markdown
- **Engine**: Unreal Engine [version]
- **Language**: C++（主要），Blueprint（游戏逻辑原型）
- **Build System**: Unreal Build Tool (UBT)
- **Asset Pipeline**: Unreal Content Pipeline
```

---

## 5. 填充技术偏好配置

更新 CLAUDE.md 后，创建或更新 `.claude/docs/technical-preferences.md`，填入适合所选引擎的默认值。先读取现有模板，然后填写：

### 引擎与语言章节
- 根据第 4 步的引擎选择填写

### 命名规范（引擎默认值）

**Godot** — GDScript、C# 和两者兼用的变体详见**附录 A**。

**Unity（C#）：**
- 类：PascalCase（如 `PlayerController`）
- 公共字段/属性：PascalCase（如 `MoveSpeed`）
- 私有字段：_camelCase（如 `_moveSpeed`）
- 方法：PascalCase（如 `TakeDamage()`）
- 文件：PascalCase 与类名匹配（如 `PlayerController.cs`）
- 常量：PascalCase 或 UPPER_SNAKE_CASE

**Unreal（C++）：**
- 类：带前缀的 PascalCase（`A` 表示 Actor，`U` 表示 UObject，`F` 表示结构体）
- 变量：PascalCase（如 `MoveSpeed`）
- 函数：PascalCase（如 `TakeDamage()`）
- 布尔值：`b` 前缀（如 `bIsAlive`）
- 文件：与类名匹配但去掉前缀（如 `PlayerController.h`）

### 输入与平台章节

使用第 2 节收集的答案（或从游戏概念中提取），填充 `## Input & Platform`，通过以下映射关系推导值：

| 目标平台 | 手柄支持 | 触控支持 |
|---------|---------|---------|
| 仅 PC | 部分（推荐） | 无 |
| 主机 | 完整 | 无 |
| 移动端 | 无 | 完整 |
| PC + 主机 | 完整 | 无 |
| PC + 移动端 | 部分 | 完整 |
| 网页 | 部分 | 部分 |

**主要输入**，根据游戏类型的主导输入判断：
- 面向主机的动作/RPG/平台跳跃 → 手柄
- 策略/点击/RTS → 键鼠
- 移动游戏 → 触控
- 跨平台 → 询问用户

展示推导的值并请用户确认或调整，再写入文件。

填写示例：
```markdown
## Input & Platform
- **Target Platforms**: PC, Console
- **Input Methods**: Keyboard/Mouse, Gamepad
- **Primary Input**: Gamepad
- **Gamepad Support**: Full
- **Touch Support**: None
- **Platform Notes**: 所有 UI 必须支持十字键导航。不允许仅悬停交互。
```

### 其余章节
- **性能预算**：使用 `AskUserQuestion`：
  - 提示："现在设置默认性能预算，还是留到之后？"
  - 选项：`[A] 现在设置默认值（60fps、16.6ms 帧预算、引擎适当的 Draw Call 上限）` / `[B] 留作 [待配置]——等确定目标硬件后再设置`
  - 若选 [A]：填入建议的默认值。若选 [B]：留作占位符。
- **测试**：建议引擎适合的测试框架（Godot 用 GUT，Unity 用 NUnit 等）——询问后再添加。
- **禁止模式**：留作占位符——**不要**预先填写。
- **允许的库**：留作占位符——**不要**预先填写项目目前不需要的依赖。只有在某个库被主动集成时才添加到此处，而不是投机性地预填。

> **防护规则**：永远不要在"允许的库"中添加投机性依赖。例如，除非本会话中正在开始集成 Steam，否则**不要**添加 GodotSteam。上线后的集成应在该工作开始时才添加到"允许的库"，而不是在引擎配置阶段。

### 引擎专家路由

同时填充 `technical-preferences.md` 中的 `## Engine Specialists` 章节，填入所选引擎的正确路由：

**Godot** — 与所选语言匹配的路由表详见**附录 A**。

**Unity：**
```markdown
## Engine Specialists
- **Primary**: unity-specialist
- **Language/Code Specialist**: unity-specialist（C# 审查——主专家已覆盖）
- **Shader Specialist**: unity-shader-specialist（Shader Graph、HLSL、URP/HDRP 材质）
- **UI Specialist**: unity-ui-specialist（UI Toolkit UXML/USS、UGUI Canvas、运行时 UI）
- **Additional Specialists**: unity-dots-specialist（ECS、Jobs 系统、Burst 编译器），unity-addressables-specialist（资源加载、内存管理、内容目录）
- **Routing Notes**: 架构决策和通用 C# 代码审查调用主专家。ECS/Jobs/Burst 代码调用 DOTS 专家。渲染和视觉效果调用 Shader 专家。所有界面实现调用 UI 专家。资源管理系统调用 Addressables 专家。

### 文件扩展名路由

| 文件扩展名 / 类型 | 调用的专家智能体 |
|-----------------|---------------|
| 游戏代码（.cs 文件）| unity-specialist |
| Shader / 材质文件（.shader, .shadergraph, .mat）| unity-shader-specialist |
| UI / 界面文件（.uxml, .uss, Canvas 预制体）| unity-ui-specialist |
| 场景 / 预制体 / 关卡文件（.unity, .prefab）| unity-specialist |
| 原生扩展 / 插件文件（.dll, native plugins）| unity-specialist |
| 通用架构审查 | unity-specialist |
```

**Unreal：**
```markdown
## Engine Specialists
- **Primary**: unreal-specialist
- **Language/Code Specialist**: ue-blueprint-specialist（蓝图图表）或 unreal-specialist（C++）
- **Shader Specialist**: unreal-specialist（无专用 Shader 专家——主专家覆盖材质）
- **UI Specialist**: ue-umg-specialist（UMG 控件、CommonUI、输入路由、控件样式）
- **Additional Specialists**: ue-gas-specialist（游戏能力系统、属性、游戏效果），ue-replication-specialist（属性复制、RPC、客户端预测、网络代码）
- **Routing Notes**: C++ 架构和宏观引擎决策调用主专家。蓝图图表架构和 BP/C++ 边界设计调用蓝图专家。所有技能和属性代码调用 GAS 专家。任何多人游戏或网络系统调用复制专家。所有 UI 实现调用 UMG 专家。

### 文件扩展名路由

| 文件扩展名 / 类型 | 调用的专家智能体 |
|-----------------|---------------|
| 游戏代码（.cpp, .h 文件）| unreal-specialist |
| Shader / 材质文件（.usf, .ush, Material 资源）| unreal-specialist |
| UI / 界面文件（.umg, UMG Widget 蓝图）| ue-umg-specialist |
| 场景 / 预制体 / 关卡文件（.umap, .uasset）| unreal-specialist |
| 原生扩展 / 插件文件（Plugin .uplugin, 模块）| unreal-specialist |
| 蓝图图表（.uasset BP 类）| ue-blueprint-specialist |
| 通用架构审查 | unreal-specialist |
```

### 协作步骤
向用户展示填写好的偏好配置。Godot 项目需注明所选语言，并说明完整命名规范和路由表的位置：
> "以下是 [engine]（[若为 Godot 则注明语言]）的默认技术偏好配置。命名规范和专家路由在本技能的附录 A 中——我将应用 [GDScript/C#/两者兼用] 变体。需要自定义这些配置，还是直接保存默认值？"

其他引擎直接展示默认值，无需引用附录。

等待批准后再写入文件。

---

## 6. 确定知识盲区

检查所选引擎版本是否可能超出 LLM 的训练数据。

**已知大致覆盖范围**（随模型更新）：
- LLM 知识截止日期：**2025 年 5 月**
- Godot：训练数据大约覆盖至 ~4.3
- Unity：训练数据大约覆盖至 ~2023.x / 2024 年初 6000.x
- Unreal：训练数据大约覆盖至 ~5.3 / 5.4 早期版本

将用户选择的版本与上述基线对比：

- **在训练数据范围内** → `LOW RISK`（低风险）— 参考文档可选但推荐创建
- **接近边界** → `MEDIUM RISK`（中风险）— 推荐创建参考文档
- **超出训练数据** → `HIGH RISK`（高风险）— 必须创建参考文档

告知用户所处类别及原因。

---

## 7. 填充引擎参考文档

### 如果在训练数据范围内（LOW RISK）：

创建简洁的 `docs/engine-reference/<engine>/VERSION.md`：

```markdown
# [Engine] — 版本参考

| 字段 | 值 |
|------|-----|
| **引擎版本** | [version] |
| **项目固定日期** | [今日日期] |
| **LLM 知识截止日期** | 2025 年 5 月 |
| **风险等级** | LOW — 版本在 LLM 训练数据范围内 |

## 说明

此引擎版本在 LLM 训练数据范围内。引擎参考文档可选，
但如果智能体建议了不正确的 API，可以随时添加。

随时运行 `/setup-engine refresh` 填充完整参考文档。
```

**不要**创建 breaking-changes.md、deprecated-apis.md 等文件——它们会增加上下文成本但价值极低。

### 如果超出训练数据（MEDIUM 或 HIGH RISK）：

通过网络搜索创建完整参考文档集：

1. **搜索官方迁移/升级指南**：
   - `"[engine] [old version] to [new version] migration guide"`
   - `"[engine] [version] breaking changes"`
   - `"[engine] [version] changelog"`
   - `"[engine] [version] deprecated API"`

2. **从官方文档中获取并提取**：
   - 从知识截止日期到当前版本的每个版本间的破坏性变更
   - 已弃用的 API 及替代方案
   - 新功能和最佳实践

询问："May I create the engine reference docs under `docs/engine-reference/<engine>/`？"

等待确认后再写入任何文件。

3. **创建完整参考目录**：
   ```
   docs/engine-reference/<engine>/
   ├── VERSION.md                    # 版本固定 + 知识盲区分析
   ├── breaking-changes.md           # 逐版本破坏性变更
   ├── deprecated-apis.md            # "禁止使用 X → 改用 Y"表格
   ├── current-best-practices.md     # 知识截止日期后的新最佳实践
   └── modules/                      # 按子系统分类的参考（按需创建）
   ```

4. **填充每个文件**，使用从网络搜索中获取的真实数据，遵循现有参考文档的格式。每个文件必须有"Last verified: [日期]"头部。

5. **对于模块文件**：只为发生了重大变更的子系统创建模块文件。不要创建空的或内容极少的模块文件。

---

## 8. 更新 CLAUDE.md 导入

询问："May I update the `@` import in `CLAUDE.md` to point to the new engine reference？"

等待确认后，将 CLAUDE.md 中"Engine Version Reference"下的 `@` 导入更新为指向正确引擎：

```markdown
## Engine Version Reference

@docs/engine-reference/<engine>/VERSION.md
```

若之前的导入指向不同引擎（如从 Godot 切换到 Unity），进行更新。

---

## 9. 更新智能体指令

询问："May I add a Version Awareness section to the engine specialist agent files？"，再进行任何编辑。

对所选引擎的专家智能体文件，验证是否存在"Version Awareness"章节。若不存在，按照现有 Godot 专家智能体中的模式添加一个。

该章节应指示智能体：
1. 读取 `docs/engine-reference/<engine>/VERSION.md`
2. 在建议代码前检查已弃用的 API
3. 检查相关版本迁移的破坏性变更
4. 使用 WebSearch 验证不确定的 API

---

## 10. 刷新子命令

若以 `/setup-engine refresh` 调用：

1. 读取现有 `docs/engine-reference/<engine>/VERSION.md`，获取当前引擎和版本
2. 使用 WebSearch 检查：
   - 上次验证以来的新引擎版本
   - 更新的迁移指南
   - 新弃用的 API
3. 用新发现更新所有参考文档
4. 在所有修改的文件上更新"Last verified"日期
5. 报告变更内容

---

## 11. 升级子命令

若以 `/setup-engine upgrade [old-version] [new-version]` 调用：

### 步骤 1 — 读取当前版本状态

读取 `docs/engine-reference/<engine>/VERSION.md`，确认当前固定版本、风险等级以及已记录的迁移指南 URL。若未通过参数提供 `old-version`，使用此文件中固定的版本。

### 步骤 2 — 获取迁移指南

使用 WebSearch 和 WebFetch 查找 `old-version` 到 `new-version` 之间的官方迁移指南：

- 搜索：`"[engine] [old-version] to [new-version] migration guide"`
- 搜索：`"[engine] [new-version] breaking changes changelog"`
- 若 VERSION.md 中已记录迁移指南 URL，直接获取；否则使用搜索到的 URL。

提取：重命名的 API、移除的 API、默认值变更、行为变更以及任何"必须迁移"的项目。

### 步骤 3 — 升级前审计

扫描 `src/` 目录中使用了目标版本中已弃用或已变更 API 的代码：

- 使用 Grep 搜索从迁移指南中提取的弃用 API 名称（如旧函数名、已移除的节点类型、已变更的属性名）
- 列出每个匹配的文件及找到的具体 API 引用

以表格形式展示审计结果：

```
升级前审计：[engine] [old-version] → [new-version]
==========================================================

需要修改的文件：
  文件                              | 发现的弃用 API            | 工作量
  --------------------------------- | -------------------------- | ------
  src/gameplay/player_movement.gd   | old_api_name               | 低
  src/ui/hud.gd                     | removed_node_type          | 中

需要注意的破坏性变更：
  - [来自迁移指南的变更描述]
  - [来自迁移指南的变更描述]

建议的迁移顺序（按依赖关系排序）：
  1. [依赖最少的系统/层级优先]
  2. [下一个系统]
  ...
```

若 `src/` 中未发现弃用 API，报告："在 src/ 中未发现弃用 API 使用——升级风险可能较低。"

### 步骤 4 — 更新前确认

在进行任何更改前询问用户：

> "升级前审计完成。发现 [N] 个文件使用了弃用 API。
> 是否继续将 VERSION.md 升级至 [new-version]？
> （此操作将更新固定版本并添加迁移说明——**不会**修改任何源代码文件。源码迁移通过手动操作或用户故事完成。）"

等待明确确认后再继续。

### 步骤 5 — 更新 VERSION.md

确认后：

1. 更新 `docs/engine-reference/<engine>/VERSION.md`：
   - `Engine Version` → `[new-version]`
   - `Project Pinned` → 今日日期
   - `Last Docs Verified` → 今日日期
   - 若新版本超出 LLM 知识截止日期，重新评估并更新 `Risk Level` 和 `Post-Cutoff Version Timeline` 表格
   - 添加 `## Migration Notes — [old-version] → [new-version]` 章节，包含：迁移指南 URL、关键破坏性变更、在本项目中发现的弃用 API，以及审计中得出的建议迁移顺序

2. 若引擎参考目录中存在 `breaking-changes.md` 或 `deprecated-apis.md`，将新版本的变更追加到这些文件中。

### 步骤 6 — 升级后提示

更新 VERSION.md 后，输出：

```
VERSION.md 已更新：[engine] [old-version] → [new-version]

后续步骤：
1. 迁移上方列出的 [N] 个文件中的弃用 API 使用
2. 升级实际引擎二进制文件后运行 /setup-engine refresh，
   验证是否遗漏了新的弃用项
3. 运行 /architecture-review——引擎升级可能使引用了特定
   API 或引擎能力的 ADR 失效
4. 若有 ADR 失效，运行 /propagate-design-change 更新
   下游用户故事
```

---

## 12. 输出摘要

配置完成后，输出：

```
引擎配置完成
=====================
引擎：          [name] [version]
语言：          [GDScript | C# | GDScript + C# | C# | C++ + Blueprint]
知识风险：      [LOW/MEDIUM/HIGH]
参考文档：      [已创建/已跳过]
CLAUDE.md：     [已更新]
技术偏好：      [已创建/已更新]
智能体配置：    [已验证]

后续步骤：
1. 查看 docs/engine-reference/<engine>/VERSION.md
2. [若来自 /brainstorm] 运行 /map-systems 将概念分解为独立系统
3. [若来自 /brainstorm] 运行 /design-system 逐章节编写系统 GDD（引导式）
4. [若来自 /brainstorm] 运行 /prototype [core-mechanic] 测试核心循环
5. [若全新开始] 运行 /brainstorm 探索游戏概念
6. 创建第一个里程碑：/sprint-plan new
```

---

裁定：**COMPLETE** — 引擎已配置，参考文档已填充。

## 防护规则

- 永远不要猜测引擎版本——始终通过 WebSearch 或用户确认来核实
- 永远不要在未询问的情况下覆盖现有参考文档——追加或更新
- 若已存在其他引擎的参考文档，在替换前先询问
- 始终在编辑 CLAUDE.md 之前向用户展示将要进行的变更
- 若 WebSearch 返回结果不明确，展示给用户让其决定
- 当用户选择了 **GDScript** 时：严格复制附录 A1 中的 GDScript CLAUDE.md 模板。**永远不要**在 Language 字段添加"C++ via GDExtension"。GDScript 项目可以使用 GDExtension，但它不是项目主要语言。路由表中的 `godot-gdextension-specialist` 供需要原生扩展时使用——这不代表 C++ 是项目语言。

---

## 附录 A — Godot 语言配置

所有依赖语言选择的 Godot 专属配置变体。从第 4 节和第 5 节引用——仅当 Godot 为所选引擎时相关。使用与第 4 步所选语言匹配的子节。

---

### A1. CLAUDE.md 技术栈模板

**GDScript：**
```markdown
- **Engine**: Godot [version]
- **Language**: GDScript
- **Build System**: SCons（引擎），Godot Export Templates
- **Asset Pipeline**: Godot Import System + 自定义资源管线
```

> **防护规则**：使用此 GDScript 模板时，Language 字段必须严格写为"`GDScript`"——不得添加任何内容。**不要**追加"C++ via GDExtension"或其他语言。下方的 C# 模板包含 GDExtension 是因为 C# 项目通常会包装原生代码；GDScript 项目则不然。

**C#：**
```markdown
- **Engine**: Godot [version]
- **Language**: C#（.NET 8+，主要），C++ via GDExtension（仅限原生插件）
- **Build System**: .NET SDK + Godot Export Templates
- **Asset Pipeline**: Godot Import System + 自定义资源管线
```

**两者兼用 — GDScript + C#：**
```markdown
- **Engine**: Godot [version]
- **Language**: GDScript（游戏逻辑/UI 脚本），C#（性能关键系统），C++ via GDExtension（仅限原生）
- **Build System**: .NET SDK + Godot Export Templates
- **Asset Pipeline**: Godot Import System + 自定义资源管线
```

---

### A2. 命名规范

**GDScript：**
- 类：PascalCase（如 `PlayerController`）
- 变量/函数：snake_case（如 `move_speed`）
- 信号：过去式 snake_case（如 `health_changed`）
- 文件：与类名匹配的 snake_case（如 `player_controller.gd`）
- 场景：与根节点匹配的 PascalCase（如 `PlayerController.tscn`）
- 常量：UPPER_SNAKE_CASE（如 `MAX_HEALTH`）

**C#：**
- 类：PascalCase（`PlayerController`）——同时必须是 `partial`
- 公共属性/字段：PascalCase（`MoveSpeed`、`JumpVelocity`）
- 私有字段：`_camelCase`（`_currentHealth`、`_isGrounded`）
- 方法：PascalCase（`TakeDamage()`、`GetCurrentHealth()`）
- 信号委托：PascalCase + `EventHandler` 后缀（`HealthChangedEventHandler`）
- 文件：与类名匹配的 PascalCase（`PlayerController.cs`）
- 场景：与根节点匹配的 PascalCase（`PlayerController.tscn`）
- 常量：PascalCase（`MaxHealth`、`DefaultMoveSpeed`）

**两者兼用 — GDScript + C#：**
`.gd` 文件使用 GDScript 规范，`.cs` 文件使用 C# 规范。不存在混合语言文件——边界以文件为单位。若对新系统应使用哪种语言有疑问，询问用户并将决策记录在 `technical-preferences.md` 中。

---

### A3. 引擎专家路由

**GDScript：**
```markdown
## Engine Specialists
- **Primary**: godot-specialist
- **Language/Code Specialist**: godot-gdscript-specialist（所有 .gd 文件）
- **Shader Specialist**: godot-shader-specialist（.gdshader 文件，VisualShader 资源）
- **UI Specialist**: godot-specialist（无专用 UI 专家——主专家覆盖所有 UI）
- **Additional Specialists**: godot-gdextension-specialist（仅限 GDExtension / 原生 C++ 绑定）
- **Routing Notes**: 架构决策、ADR 验证和跨模块代码审查调用主专家。代码质量、信号架构、静态类型强制和 GDScript 惯用法调用 GDScript 专家。材质设计和 Shader 代码调用 Shader 专家。仅当涉及原生扩展时调用 GDExtension 专家。

### 文件扩展名路由

| 文件扩展名 / 类型 | 调用的专家智能体 |
|-----------------|---------------|
| 游戏代码（.gd 文件）| godot-gdscript-specialist |
| Shader / 材质文件（.gdshader, VisualShader）| godot-shader-specialist |
| UI / 界面文件（Control 节点, CanvasLayer）| godot-specialist |
| 场景 / 预制体 / 关卡文件（.tscn, .tres）| godot-specialist |
| 原生扩展 / 插件文件（.gdextension, C++）| godot-gdextension-specialist |
| 通用架构审查 | godot-specialist |
```

**C#：**
```markdown
## Engine Specialists
- **Primary**: godot-specialist
- **Language/Code Specialist**: godot-csharp-specialist（所有 .cs 文件）
- **Shader Specialist**: godot-shader-specialist（.gdshader 文件，VisualShader 资源）
- **UI Specialist**: godot-specialist（无专用 UI 专家——主专家覆盖所有 UI）
- **Additional Specialists**: godot-gdextension-specialist（仅限 GDExtension / 原生 C++ 绑定）
- **Routing Notes**: 架构决策、ADR 验证和跨模块代码审查调用主专家。代码质量、[Signal] 委托模式、[Export] 特性、.csproj 管理和 C# 专属 Godot 惯用法调用 C# 专家。材质设计和 Shader 代码调用 Shader 专家。仅当涉及原生 C++ 插件时调用 GDExtension 专家。

### 文件扩展名路由

| 文件扩展名 / 类型 | 调用的专家智能体 |
|-----------------|---------------|
| 游戏代码（.cs 文件）| godot-csharp-specialist |
| Shader / 材质文件（.gdshader, VisualShader）| godot-shader-specialist |
| UI / 界面文件（Control 节点, CanvasLayer）| godot-specialist |
| 场景 / 预制体 / 关卡文件（.tscn, .tres）| godot-specialist |
| 项目配置（.csproj, NuGet）| godot-csharp-specialist |
| 原生扩展 / 插件文件（.gdextension, C++）| godot-gdextension-specialist |
| 通用架构审查 | godot-specialist |
```

**两者兼用 — GDScript + C#：**
```markdown
## Engine Specialists
- **Primary**: godot-specialist
- **GDScript Specialist**: godot-gdscript-specialist（.gd 文件——游戏逻辑/UI 脚本）
- **C# Specialist**: godot-csharp-specialist（.cs 文件——性能关键系统）
- **Shader Specialist**: godot-shader-specialist（.gdshader 文件，VisualShader 资源）
- **UI Specialist**: godot-specialist（无专用 UI 专家——主专家覆盖所有 UI）
- **Additional Specialists**: godot-gdextension-specialist（仅限 GDExtension / 原生 C++ 绑定）
- **Routing Notes**: 跨语言架构决策以及哪些系统属于哪种语言调用主专家。.gd 文件调用 GDScript 专家。.cs 文件和 .csproj 管理调用 C# 专家。在边界处优先使用信号而非跨语言直接方法调用。

### 文件扩展名路由

| 文件扩展名 / 类型 | 调用的专家智能体 |
|-----------------|---------------|
| 游戏代码（.gd 文件）| godot-gdscript-specialist |
| 游戏代码（.cs 文件）| godot-csharp-specialist |
| 跨语言边界决策 | godot-specialist |
| Shader / 材质文件（.gdshader, VisualShader）| godot-shader-specialist |
| UI / 界面文件（Control 节点, CanvasLayer）| godot-specialist |
| 场景 / 预制体 / 关卡文件（.tscn, .tres）| godot-specialist |
| 项目配置（.csproj, NuGet）| godot-csharp-specialist |
| 原生扩展 / 插件文件（.gdextension, C++）| godot-gdextension-specialist |
| 通用架构审查 | godot-specialist |
```
