---
name: test-setup
description: "为项目引擎搭建测试框架和 CI/CD 流水线。创建 tests/ 目录结构、引擎特定测试运行器配置以及 GitHub Actions 工作流。在首次冲刺开始前的技术设置阶段运行一次。"
argument-hint: "[force]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Write
---

# 测试设置

本技能为项目搭建自动化测试基础设施。
检测已配置的引擎，生成相应的测试运行器配置，创建标准目录布局，
并接入 CI/CD，以便在每次推送时运行测试。

在技术设置阶段运行一次，在任何实现开始之前。
在冲刺开始时安装测试框架需要 30 分钟。在第四个冲刺时安装需要 3 个冲刺的代价。

**输出：** `tests/` 目录结构 + `.github/workflows/tests.yml`

---

## 阶段 1：检测引擎和现有状态

1. **读取引擎配置**：
   - 读取 `.claude/docs/technical-preferences.md` 并提取 `Engine:` 值。
   - 若引擎未配置（`[TO BE CONFIGURED]`），停止：
     "引擎未配置。先运行 `/setup-engine`，然后重新运行 `/test-setup`。"

2. **检查现有测试基础设施**：
   - Glob `tests/` — 目录是否存在？
   - Glob `tests/unit/` 和 `tests/integration/` — 子目录是否存在？
   - Glob `.github/workflows/` — CI 工作流文件是否存在？
   - Glob `tests/gdunit4_runner.gd`（Godot）、`tests/EditMode/`（Unity）或
     `Source/Tests/`（Unreal）用于引擎特定制品。

3. **报告发现结果**：
   - "引擎：[engine]。测试目录：[找到 / 未找到]。CI 工作流：[找到 / 未找到]。"
   - 若所有内容已存在且未传入 `force` 参数：
     "测试基础设施似乎已就位。使用 `/test-setup force` 重新运行以重新生成。
     继续操作不会覆盖现有测试文件。"

若传入 `force` 参数，跳过"已存在"的提前退出并继续——
但仍不要覆盖给定路径上已存在的文件。仅创建缺失的文件。

---

## 阶段 2：呈现计划

根据检测到的引擎和现有状态，呈现计划：

```
## 测试设置计划 — [Engine]

我将创建以下内容（跳过已存在的）：

tests/
  unit/           — 用于公式、状态和逻辑的隔离单元测试
  integration/    — 跨系统测试和存档/读档往返测试
  smoke/          — 关键路径测试列表（15 分钟手动门控）
  evidence/       — 截图和手动测试签收记录
  README.md       — 测试框架文档

[引擎特定文件——见各引擎详情]

.github/workflows/tests.yml  — CI：每次推送到 main 时运行测试

预估时间：创建所有文件约需 5 分钟。
```

询问："我可以创建这些文件吗？我不会覆盖这些路径上已存在的任何测试文件。"

未经批准不得继续。

---

## 阶段 3：创建目录结构

批准后，创建以下文件：

### `tests/README.md`

````markdown
# Test Infrastructure

**Engine**: [engine name + version]
**Test Framework**: [GdUnit4 | Unity Test Framework | UE Automation]
**CI**: `.github/workflows/tests.yml`
**Setup date**: [date]

## Directory Layout

```
tests/
  unit/           # Isolated unit tests (formulas, state machines, logic)
  integration/    # Cross-system and save/load tests
  smoke/          # Critical path test list for /smoke-check gate
  evidence/       # Screenshot logs and manual test sign-off records
```

## Running Tests

[Engine-specific command — see below]

## Test Naming

- **Files**: `[system]_[feature]_test.[ext]`
- **Functions**: `test_[scenario]_[expected]`
- **Example**: `combat_damage_test.gd` → `test_base_attack_returns_expected_damage()`

## Story Type → Test Evidence

| Story Type | Required Evidence | Location |
|---|---|---|
| Logic | Automated unit test — must pass | `tests/unit/[system]/` |
| Integration | Integration test OR playtest doc | `tests/integration/[system]/` |
| Visual/Feel | Screenshot + lead sign-off | `tests/evidence/` |
| UI | Manual walkthrough OR interaction test | `tests/evidence/` |
| Config/Data | Smoke check pass | `production/qa/smoke-*.md` |

## CI

Tests run automatically on every push to `main` and on every pull request.
A failed test suite blocks merging.
````

### 引擎特定文件

#### Godot 4（`Engine: Godot`）

创建 `tests/gdunit4_runner.gd`：

```gdscript
# GdUnit4 test runner — invoked by CI and /smoke-check
# Usage: godot --headless --script tests/gdunit4_runner.gd
extends SceneTree

func _init() -> void:
    var runner := load("res://addons/gdunit4/GdUnitRunner.gd")
    if runner == null:
        push_error("GdUnit4 not found. Install via AssetLib or addons/.")
        quit(1)
        return
    var instance = runner.new()
    instance.run_tests()
    quit(0)
```

创建 `tests/unit/.gdignore_placeholder`，内容为：
`# Unit tests go here — one subdirectory per system (e.g., tests/unit/combat/)`

创建 `tests/integration/.gdignore_placeholder`，内容为：
`# Integration tests go here — one subdirectory per system`

在 README 中说明：**安装 GdUnit4**
```
1. 打开 Godot → AssetLib → 搜索 "GdUnit4" → 下载并安装
2. 启用插件：项目 → 项目设置 → 插件 → GdUnit4 ✓
3. 重启编辑器
4. 验证：res://addons/gdunit4/ 存在
```

#### Unity（`Engine: Unity`）

创建 `tests/EditMode/README.md` 占位文件：
```markdown
# Edit Mode Tests
Unit tests that run without entering Play Mode.
Use for pure logic: formulas, state machines, data validation.
Assembly definition required: `tests/EditMode/EditModeTests.asmdef`
```

创建 `tests/PlayMode/README.md`：
```markdown
# Play Mode Tests
Integration tests that run in a real game scene.
Use for cross-system interactions, physics, and coroutines.
Assembly definition required: `tests/PlayMode/PlayModeTests.asmdef`
```

在 README 中说明：**启用 Unity 测试框架**
```
Window → General → Test Runner
（Unity 测试框架默认包含在 Unity 2019+ 中）
```

#### Unreal Engine（`Engine: Unreal` 或 `Engine: UE5`）

创建 `Source/Tests/README.md`：
```markdown
# Unreal Automation Tests
Tests use the UE Automation Testing Framework.
Run via: Session Frontend → Automation → select "MyGame." tests
Or headlessly: UnrealEditor -nullrhi -ExecCmds="Automation RunTests MyGame.; Quit"

Test class naming: F[SystemName]Test
Test category naming: "MyGame.[System].[Feature]"
```

---

## 阶段 4：创建 CI/CD 工作流

### Godot 4

创建 `.github/workflows/tests.yml`：

```yaml
name: Automated Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    name: Run GdUnit4 Tests
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          lfs: true

      - name: Run GdUnit4 Tests
        uses: MikeSchulze/gdUnit4-action@v1
        with:
          godot-version: '[VERSION FROM docs/engine-reference/godot/VERSION.md]'
          paths: |
            tests/unit
            tests/integration
          report-name: test-results

      - name: Upload Test Results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results
          path: reports/
```

### Unity

创建 `.github/workflows/tests.yml`：

```yaml
name: Automated Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    name: Run Unity Tests
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          lfs: true

      - name: Run Edit Mode Tests
        uses: game-ci/unity-test-runner@v4
        env:
          UNITY_LICENSE: ${{ secrets.UNITY_LICENSE }}
        with:
          testMode: editmode
          artifactsPath: test-results/editmode

      - name: Run Play Mode Tests
        uses: game-ci/unity-test-runner@v4
        env:
          UNITY_LICENSE: ${{ secrets.UNITY_LICENSE }}
        with:
          testMode: playmode
          artifactsPath: test-results/playmode

      - name: Upload Test Results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results
          path: test-results/
```

注意：Unity CI 需要 `UNITY_LICENSE` Secret。首次 CI 运行前将其添加到 GitHub 仓库 Secrets 中。

### Unreal Engine

创建 `.github/workflows/tests.yml`：

```yaml
name: Automated Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    name: Run UE Automation Tests
    runs-on: self-hosted  # UE requires a local runner with the editor installed

    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          lfs: true

      - name: Run Automation Tests
        run: |
          "$UE_EDITOR_PATH" "${{ github.workspace }}/[ProjectName].uproject" \
            -nullrhi -nosound \
            -ExecCmds="Automation RunTests MyGame.; Quit" \
            -log -unattended
        shell: bash

      - name: Upload Logs
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-logs
          path: Saved/Logs/
```

注意：UE CI 需要安装了 Unreal Editor 的自托管运行器。
在运行器上设置 `UE_EDITOR_PATH` 环境变量。

---

## 阶段 5：创建冒烟测试种子

创建 `tests/smoke/critical-paths.md`：

```markdown
# Smoke Test: Critical Paths

**Purpose**: Run these 10-15 checks in under 15 minutes before any QA hand-off.
**Run via**: `/smoke-check` (which reads this file)
**Update**: Add new entries when new core systems are implemented.

## Core Stability (always run)

1. Game launches to main menu without crash
2. New game / session can be started from the main menu
3. Main menu responds to all inputs without freezing

## Core Mechanic (update per sprint)

<!-- Add the primary mechanic for each sprint here as it is implemented -->
<!-- Example: "Player can move, jump, and the camera follows correctly" -->
4. [Primary mechanic — update when first core system is implemented]

## Data Integrity

5. Save game completes without error (once save system is implemented)
6. Load game restores correct state (once load system is implemented)

## Performance

7. No visible frame rate drops on target hardware (60fps target)
8. No memory growth over 5 minutes of play (once core loop is implemented)
```

---

## 阶段 6：设置后摘要

写入所有文件后，报告：

```
已为 [engine] 创建测试基础设施。

已创建文件：
- tests/README.md
- tests/unit/（目录）
- tests/integration/（目录）
- tests/smoke/critical-paths.md
- tests/evidence/（目录）
[引擎特定文件]
- .github/workflows/tests.yml

下一步：
1. [引擎特定安装步骤，例如"通过 AssetLib 安装 GdUnit4"]
2. 编写第一个测试：创建 tests/unit/[first-system]/[system]_test.[ext]
3. 在第一个冲刺前运行 `/qa-plan sprint` 对故事进行分类并设置测试证据要求
4. 每次 QA 移交前运行 `/smoke-check`

门控说明：`/gate-check` 技术设置 → 前期制作现在需要：
- tests/ 目录包含 unit/ 和 integration/ 子目录
- .github/workflows/tests.yml
- 至少一个示例测试文件
运行 /test-setup 并编写一个示例测试后再推进。

结论：**COMPLETE** — 测试框架已搭建，CI/CD 已接入。
```

---

## Collaborative Protocol

- **绝不覆盖已有测试文件** — 仅创建缺失的文件。若测试运行器文件已存在，保持原样。
- **创建文件前始终询问** — 阶段 2 需要明确批准。
- **引擎检测不可协商** — 若引擎未配置，停止并重定向到 `/setup-engine`。不猜测。
- **`force` 标志跳过"已存在"的提前退出，但绝不覆盖。** 它的含义是"即使目录已存在也创建所有缺失文件。"
- 对于 Unity CI，注意 `UNITY_LICENSE` Secret 必须手动配置。不要尝试自动化许可证管理。
