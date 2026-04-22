---
name: smoke-check
description: "在移交 QA 前运行关键路径冒烟测试门禁。执行自动化测试套件，验证核心功能，并生成 PASS/FAIL 报告。在迭代用户故事实现完成后、手动 QA 开始前运行。冒烟测试失败意味着构建未准备好进入 QA。"
argument-hint: "[sprint | quick | --platform pc|console|mobile|all]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Write, AskUserQuestion
---

# 冒烟测试

本 skill 是"实现完成"到"准备移交 QA"之间的门禁。它运行自动化测试套件、检查测试覆盖缺口、与开发者批量验证关键路径，并生成 PASS/FAIL 报告。

简单规则：**冒烟测试失败的构建不得移交 QA。** 将损坏的构建交给 QA 会浪费他们的时间并打击团队士气。

**输出：** `production/qa/smoke-[日期].md`

---

## 解析参数

参数可组合使用：`/smoke-check sprint --platform console`

**基础模式**（第一个参数，默认：`sprint`）：
- `sprint` — 针对当前冲刺所有 Story 运行完整冒烟检查
- `quick` — 跳过覆盖率扫描（阶段 3）和批次 3；用于快速复查

**平台标志**（`--platform`，默认：无）：
- `--platform pc` — 添加 PC 专属检查（键盘、鼠标、窗口模式）
- `--platform console` — 添加主机专属检查（手柄、电视安全区、平台认证要求）
- `--platform mobile` — 添加移动端专属检查（触控、竖横屏、电量/热管理行为）
- `--platform all` — 添加所有平台变体；输出各平台裁定表

若提供 `--platform`，阶段 4 会添加平台专属批次，阶段 5 在总体裁定之外还会输出各平台裁定表。

---

## 阶段 1：检测测试配置

在运行任何内容之前，先了解环境：

1. **测试框架检查**：验证 `tests/` 目录是否存在。
   如果不存在："在 `tests/` 处未找到测试目录。运行 `/test-setup`
   搭建测试基础设施，或手动创建目录（如测试存放在其他位置）。"然后停止。

2. **CI 检查**：检查 `.github/workflows/` 中是否有引用测试的工作流文件。
   在报告中注明 CI 是否已配置。

3. **引擎检测**：读取 `.claude/docs/technical-preferences.md`，提取 `Engine:` 值。
   存储备用于阶段 2 的命令选择。

4. **冒烟测试列表**：检查 `production/qa/smoke-tests.md` 或 `tests/smoke/` 是否存在。
   如果找到冒烟测试列表，加载供阶段 4 使用。如果两者都不存在，冒烟测试将从当前
   QA 计划中提取（阶段 4 备用）。

5. **QA 计划检查**：glob `production/qa/qa-plan-*.md`，取最新修改的文件。
   如果找到，记录路径——将在阶段 3 和阶段 4 中使用。如果未找到，记录："未找到
   QA 计划。运行 `/qa-plan sprint` 以获得最佳冒烟检查效果。"

继续前报告发现结果："环境：[引擎]。测试目录：[已找到 / 未找到]。CI 已配置：[是 / 否]。QA 计划：[路径 / 未找到]。"

---

## 阶段 2：运行自动化测试

根据阶段 1 检测到的引擎，通过 Bash 运行测试套件。选取基于阶段 1 引擎检测的命令。

**Godot 4：**
```bash
godot --headless --script tests/gdunit4_runner.gd 2>&1
```
如果该路径的 GDUnit4 运行器脚本不存在，尝试：
```bash
godot --headless -s addons/gdunit4/GdUnitRunner.gd 2>&1
```
如果两个路径均不存在，记录："未找到 GDUnit4 运行器——请确认您测试框架的运行器路径。"

**Unity：**
Unity 测试需要编辑器，在大多数环境中无法通过 shell 无头运行。
检查最近的测试结果产物：
```bash
ls -t test-results/ 2>/dev/null | head -5
```
如果测试结果文件（XML 或 JSON）存在，读取最新文件并解析 PASS/FAIL 数量。
如果不存在产物："Unity 测试必须从编辑器或 CI 流水线运行。在继续前请手动确认测试状态。"

**Unreal Engine：**
```bash
ls -t Saved/Logs/ 2>/dev/null | grep -i "test\|automation" | head -5
```
如果未找到匹配日志："UE 自动化测试必须通过 Session Frontend 或 CI 流水线运行。请手动确认测试状态。"

**未知引擎 / 未配置：**
"引擎未在 `.claude/docs/technical-preferences.md` 中配置。运行
`/setup-engine` 指定引擎，然后重新运行 `/smoke-check`。"

**如果测试运行器在此环境中不可用**（引擎可执行文件不在 PATH 中、运行器脚本未找到等），清楚地报告：

"无法执行自动化测试——在 PATH 中未找到引擎可执行文件。
状态将记录为 NOT RUN。请从本地 IDE 或 CI 流水线确认测试结果。
未确认的 NOT RUN 视为 PASS WITH WARNINGS，而非 FAIL——开发者必须手动确认结果。"

不要将 NOT RUN 视为自动 FAIL。将其记录为警告。阶段 4 中开发者的手动确认可以解决此问题。

解析运行器输出并提取：
- 总测试运行数
- 通过数量
- 失败数量
- 任何失败测试的名称（最多 10 个；如果更多，记录数量）
- 运行器本身的任何崩溃或错误输出

---

## 阶段 3：检查测试覆盖率

按优先级从以下来源提取 Story 列表：
1. 阶段 1 中找到的 QA 计划（其测试摘要表列出了每个 Story 的预期测试文件路径）
2. `production/sprints/` 中的当前冲刺计划（最新修改的文件）
3. 如果传入了 `quick` 参数，完全跳过此阶段并记录：
   "覆盖率扫描已跳过——运行 `/smoke-check sprint` 进行完整覆盖率分析。"

对范围内的每个 Story：

1. 从 Story 文件路径中提取系统缩写
   （例如 `production/epics/combat/story-001.md` → `combat`）
2. Glob `tests/unit/[系统]/` 和 `tests/integration/[系统]/` 中名称包含 Story 缩写或密切相关词的文件
3. 检查 Story 文件本身是否有 `Test file:` 标题字段或"Test Evidence"部分

为每个 Story 分配覆盖状态：

| 状态 | 含义 |
|------|------|
| **COVERED** | 找到与该 Story 系统和范围匹配的测试文件 |
| **MANUAL** | Story 类型为 Visual/Feel 或 UI；找到测试证据文档 |
| **MISSING** | Logic 或 Integration Story 没有匹配的测试文件 |
| **EXPECTED** | Config/Data Story——不需要测试文件；抽查即可 |
| **UNKNOWN** | Story 文件缺失或不可读 |

MISSING 条目为建议性缺口。它们不会导致 FAIL 裁定，但必须在报告中醒目显示，
且必须在 `/story-done` 完全关闭这些 Story 之前解决。

---

## 阶段 4：运行手动冒烟检查

按优先级从以下来源提取冒烟测试清单：
1. QA 计划的"冒烟测试范围"部分（如阶段 1 中找到 QA 计划）
2. `production/qa/smoke-tests.md`（如果存在）
3. `tests/smoke/` 目录内容（如果存在）
4. 以下标准备用列表（仅在以上来源均不存在时使用）

根据冲刺或 QA 计划中识别的实际系统，定制批次 2 和批次 3。将括号中的占位符
替换为当前冲刺 Story 中真实的功能名称。

使用 `AskUserQuestion` 批量验证。最多调用 3 次。

**批次 1 — 核心稳定性（始终运行）：**
```
question: "冒烟检查 — 批次 1：核心稳定性。请逐项验证："
options:
  - "游戏正常启动进入主菜单且无崩溃 — PASS"
  - "游戏正常启动进入主菜单且无崩溃 — FAIL"
  - "新游戏 / 会话成功启动 — PASS"
  - "新游戏 / 会话成功启动 — FAIL"
  - "主菜单响应所有输入 — PASS"
  - "主菜单响应所有输入 — FAIL"
```

**批次 2 — 本冲刺功能与回归检查（始终运行）：**
```
question: "冒烟检查 — 批次 2：本冲刺变更与回归检查："
options:
  - "[本冲刺主要功能] — PASS"
  - "[本冲刺主要功能] — FAIL：[描述具体问题]"
  - "[本冲刺第二项重要变更（如有）] — PASS"
  - "[本冲刺第二项重要变更] — FAIL"
  - "上一冲刺功能仍正常（无回归）— PASS"
  - "上一冲刺功能 — 发现回归：[简要描述]"
```

**批次 3 — 数据完整性与性能（若非 `quick` 参数则运行）：**
```
question: "冒烟检查 — 批次 3：数据完整性与性能："
options:
  - "存档 / 读档完成且无数据丢失 — PASS"
  - "存档 / 读档 — FAIL：[描述具体问题]"
  - "存档 / 读档 — N/A（存档系统尚未实现）"
  - "未观察到新的帧率下降或卡顿 — PASS"
  - "发现帧率下降或卡顿 — FAIL：[位置]"
  - "性能 — 本次未检查"
```

逐项记录每个回答供阶段 5 报告使用。

**平台批次** *（仅在提供 `--platform` 参数时运行）*：

**PC 平台**（`--platform pc` 或 `--platform all`）：
```
question: "冒烟检查 — PC 平台：验证平台专属行为："
options:
  - "键盘控制在所有菜单和游戏玩法中正常工作 — PASS"
  - "键盘控制 — FAIL：[描述问题]"
  - "鼠标输入和光标在所有状态下显示正确 — PASS"
  - "鼠标输入 — FAIL：[描述问题]"
  - "窗口模式和全屏模式正常切换且无图形问题 — PASS"
  - "窗口/全屏模式 — FAIL：[描述问题]"
  - "分辨率变更正确应用 — PASS"
  - "分辨率变更 — FAIL：[描述问题]"
```

**主机平台**（`--platform console` 或 `--platform all`）：
```
question: "冒烟检查 — 主机平台：验证平台专属行为："
options:
  - "手柄输入对所有操作均正常工作 — PASS"
  - "手柄输入 — FAIL：[描述问题]"
  - "UI 在电视安全区内显示完整（无文字被裁剪）— PASS"
  - "电视安全区 — FAIL：[描述被裁剪内容]"
  - "手柄用户未看到键鼠专属的回退提示 — PASS"
  - "输入提示不一致 — FAIL：[描述]"
  - "游戏从冷启动正确启动（无先前存档）— PASS"
  - "冷启动 — FAIL：[描述问题]"
```

**移动端平台**（`--platform mobile` 或 `--platform all`）：
```
question: "冒烟检查 — 移动端平台：验证平台专属行为："
options:
  - "触控操作对所有主要行为正常工作 — PASS"
  - "触控操作 — FAIL：[描述问题]"
  - "游戏正确处理方向切换（竖屏 ↔ 横屏）— PASS"
  - "方向切换 — FAIL：[描述具体问题]"
  - "前台/后台切换（Home 键）处理正常 — PASS"
  - "前台/后台 — FAIL：[描述问题]"
  - "目标设备上无明显性能问题（无热限速迹象）— PASS"
  - "移动端性能 — FAIL：[描述问题]"
```

---

## 阶段 5：生成报告

汇总完整冒烟检查报告：

````markdown
## 冒烟检查报告
**日期**：[日期]
**冲刺**：[冲刺名称 / 编号，或"未识别"]
**引擎**：[引擎]
**QA 计划**：[路径，或"未找到——请先运行 /qa-plan"]
**参数**：[sprint | quick | 空白]

---

### 自动化测试

**状态**：[PASS（[N] 个测试，[N] 个通过）| FAIL（[N] 个失败）|
NOT RUN（[原因]）]

[如果 FAIL，列出失败测试：]
- `[测试名称]` — [来自运行器输出的简要失败描述]

[如果 NOT RUN：]
"需要手动确认：测试是否在本地 IDE 或 CI 中通过？这将决定自动化测试行是否
贡献 FAIL 裁定。"

---

### 测试覆盖率

| Story | 类型 | 测试文件 | 覆盖状态 |
|-------|------|----------|----------|
| [标题] | Logic | `tests/unit/[系统]/[缩写]_test.[扩展名]` | COVERED |
| [标题] | Visual/Feel | `tests/evidence/[缩写]-screenshots.md` | MANUAL |
| [标题] | Logic | — | MISSING ⚠ |
| [标题] | Config/Data | — | EXPECTED |

**摘要**：[N] 个已覆盖，[N] 个手动，[N] 个缺失，[N] 个预期。

---

### 手动冒烟检查

- [x] 游戏正常启动且无崩溃 — PASS
- [x] 新游戏启动 — PASS
- [x] [核心功能] — PASS
- [ ] [其他检查] — FAIL：[用户描述]
- [x] 存档 / 读档 — PASS
- [-] 性能 — 本次未检查

---

### 缺失测试证据

通过 `/story-done` 标记为 COMPLETE 之前必须提供测试证据的 Story：

- **[Story 标题]** (`[路径]`) — Logic Story 没有测试文件。
  预期位置：`tests/unit/[系统]/[story-slug]_test.[扩展名]`

[如果没有：] "所有 Logic 和 Integration Story 均有测试覆盖。"

---

### 平台专属结果 *（仅在提供 `--platform` 时显示）*

| 平台 | 已运行检查 | 通过 | 失败 | 平台裁定 |
|------|-----------|------|------|----------|
| PC | [N] | [N] | [N] | PASS / FAIL |
| 主机 | [N] | [N] | [N] | PASS / FAIL |
| 移动端 | [N] | [N] | [N] | PASS / FAIL |

**平台备注**：[未在通过/失败中捕获的平台专属观察]

任何有一个或多个 FAIL 检查的平台都会导致总体 FAIL 裁定。

---

### 裁定：[PASS | PASS WITH WARNINGS | FAIL]

[裁定规则——首条匹配规则优先：]

**FAIL** 如果满足以下任一条件：
- 自动化测试套件运行并报告一个或多个测试失败
- 任何批次 1（核心稳定性）检查返回 FAIL
- 任何批次 2（本冲刺主要功能或回归检查）返回 FAIL

**PASS WITH WARNINGS** 如果满足以下所有条件：
- 自动化测试 PASS 或 NOT RUN（开发者尚未确认）
- 所有批次 1 和批次 2 冒烟检查 PASS
- 一个或多个 Logic/Integration Story 有 MISSING 测试证据

**PASS** 如果满足以下所有条件：
- 自动化测试 PASS
- 所有批次中的所有冒烟检查均 PASS 或 N/A
- 无 MISSING 测试证据条目
````

---

## 阶段 6：写入并门禁

在对话中展示完整报告，然后询问：

"May I write this smoke check report to `production/qa/smoke-[date].md`?"

仅在获得批准后写入。

写入后，根据裁定给出门禁结论：

**如果裁定为 FAIL：**

"冒烟检查失败。在解决以下失败项之前，不得移交 QA：

[列出每个失败的自动化测试或冒烟检查及一行描述]

修复失败项后重新运行 `/smoke-check`，在 QA 移交前重新通过门禁。"

**如果裁定为 PASS WITH WARNINGS：**

"冒烟检查带警告通过。构建已准备好进行手动 QA。

在对受影响 Story 运行 `/story-done` 之前需解决的建议项：
[列出 MISSING 测试证据条目]

QA 移交：将 `production/qa/qa-plan-[冲刺].md` 分享给 qa-tester agent 开始手动验证。"

**如果裁定为 PASS：**

"冒烟检查顺利通过。构建已准备好进行手动 QA。

QA 移交：将 `production/qa/qa-plan-[冲刺].md` 分享给 qa-tester agent 开始手动验证。"

---

## 协作协议

- **永远不要将 NOT RUN 视为自动 FAIL** — 将其记录为 NOT RUN 并让开发者手动确认状态。未确认的 NOT RUN 贡献 PASS WITH WARNINGS，而非 FAIL。
- **永远不要自动修复失败** — 报告失败并说明必须解决什么。不要尝试编辑源代码或测试文件。
- **PASS WITH WARNINGS 不阻止 QA 移交** — 它记录建议性缺口，供 `/story-done` 后续跟进。
- **`quick` 参数**跳过阶段 3（覆盖率扫描）和阶段 4 批次 3。用于修复特定失败后的快速复查。
- 所有手动冒烟检查验证均使用 `AskUserQuestion`。
- **在询问之前绝不写入报告** — 阶段 6 在创建任何文件之前需要明确批准。
