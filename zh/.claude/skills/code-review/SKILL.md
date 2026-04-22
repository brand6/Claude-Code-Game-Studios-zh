---
name: code-review
description: "对指定文件或文件集执行架构和质量代码评审。检查编码标准合规性、架构模式遵循情况、SOLID 原则、可测试性及性能问题。"
argument-hint: "[文件或目录路径]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Task
agent: lead-programmer
---

## 阶段 1：加载目标文件

完整读取目标文件。读取 CLAUDE.md 获取项目编码标准。

---

## 阶段 2：识别引擎专家

读取 `.claude/docs/technical-preferences.md` 中的 `## Engine Specialists` 章节，记录：

- **主要**专家（用于架构和宏观引擎问题）
- **语言/代码专家**（用于评审项目主要语言文件）
- **Shader 专家**（用于评审 shader 文件）
- **UI 专家**（用于评审 UI 代码）

若该章节内容为 `[TO BE CONFIGURED]`，则引擎未锁定——跳过引擎专家步骤。

---

## 阶段 3：ADR 合规检查

在 Story 文件、提交信息和头部注释中搜索 ADR 引用，查找 `ADR-NNN` 或 `docs/architecture/ADR-` 等模式。

若未找到 ADR 引用，记录："未找到 ADR 引用——跳过 ADR 合规检查。"

对每个引用的 ADR：读取文件，提取 **Decision** 和 **Consequences** 章节，然后对偏差进行分类：

- **ARCHITECTURAL VIOLATION**（阻塞性）：使用了 ADR 中明确拒绝的模式
- **ADR DRIFT**（警告）：与所选方法产生有意义的偏差，但未使用被禁止的模式
- **MINOR DEVIATION**（信息）：与 ADR 指导略有不同，但不影响整体架构

---

## 阶段 4：标准合规

识别系统类别（引擎层、游戏逻辑层、AI、网络、UI、工具），并评估：

- [ ] 公共方法和类有文档注释
- [ ] 每个方法的圈复杂度低于 10
- [ ] 无方法超过 40 行（排除数据声明）
- [ ] 依赖通过注入提供（游戏状态不使用静态单例）
- [ ] 配置值从数据文件加载
- [ ] 系统暴露接口（而非具体类依赖）

---

## 阶段 5：架构与 SOLID

**架构：**
- [ ] 依赖方向正确（引擎层 ← 游戏逻辑层，不反向）
- [ ] 模块间无循环依赖
- [ ] 层级分离正确（UI 不持有游戏状态）
- [ ] 跨系统通信使用事件/信号
- [ ] 与代码库中已有模式一致

**SOLID：**
- [ ] 单一职责：每个类只有一个变更原因
- [ ] 开闭原则：可扩展而无需修改
- [ ] 里氏替换：子类型可替换基类型
- [ ] 接口隔离：无臃肿接口
- [ ] 依赖倒置：依赖抽象而非具体实现

---

## 阶段 6：游戏特定关注点

- [ ] 帧率无关性（使用 delta time）
- [ ] 热路径中无内存分配（Update 循环）
- [ ] 正确处理空/空值状态
- [ ] 需要时保证线程安全
- [ ] 资源清理（无内存泄漏）

---

## 阶段 7：专家评审（并行）

通过 Task 同时生成所有适用的专家——不要等一个完成再启动下一个。

### 引擎专家

若已配置引擎，判断每个文件适用的专家并并行生成：

- 主要语言文件（`.gd`、`.cs`、`.cpp`）→ 语言/代码专家
- Shader 文件（`.gdshader`、`.hlsl`、shader graph）→ Shader 专家
- UI 界面/Widget 代码 → UI 专家
- 跨领域或不确定 → 主要专家

同时为所有涉及引擎架构的文件（Scene 结构、节点层级、生命周期钩子）生成**主要专家**。

### QA 可测试性评审

对于逻辑型和集成型 Story，通过 Task 与引擎专家并行生成 `qa-tester`。提供：
- 被评审的实现文件
- Story 的 `## QA Test Cases` 章节（QA Lead 预先编写的测试规格）
- Story 的 `## Acceptance Criteria`

要求 qa-tester 评估：
- [ ] 所有测试钩子和接口是否已暴露（未隐藏在 private/internal 访问权限后）？
- [ ] Story 的 `## QA Test Cases` 中的测试用例是否可映射到可测试的代码路径？
- [ ] 是否有验收标准因实现方式（如硬编码值、无注入接缝）而无法测试？
- [ ] 实现是否引入了现有 QA 测试用例未覆盖的新边缘情况？
- [ ] 是否存在应有测试但未覆盖的可观测副作用？

对于视觉/感受型和 UI 型 Story：qa-tester 评审 `## QA Test Cases` 中的手动验证步骤是否能基于当前实现执行——例如"手动检查者所需的状态是否实际可达？"

收集所有专家发现后再输出结果。

---

## 阶段 8：输出评审结果

```
## 代码评审：[文件/系统名称]

### 引擎专家发现：[N/A——未配置引擎 / CLEAN / ISSUES FOUND]
[来自引擎专家的发现，若跳过则写"未配置引擎。"]

### 可测试性：[N/A——视觉/感受或配置型 Story / TESTABLE / GAPS / BLOCKING]
[qa-tester 发现：测试钩子、覆盖缺口、无法测试的路径、新边缘情况]
[若 BLOCKING：实现必须暴露 [X] 后，## QA Test Cases 中的测试才能运行]

### ADR 合规：[NO ADRS FOUND / COMPLIANT / DRIFT / VIOLATION]
[列出每个已检查的 ADR、结果及任何偏差（含严重性）]

### 标准合规：[X/6 通过]
[列出不通过项，附行号引用]

### 架构：[CLEAN / MINOR ISSUES / VIOLATIONS FOUND]
[列出具体的架构问题]

### SOLID：[COMPLIANT / ISSUES FOUND]
[列出具体的违规项]

### 游戏特定关注点
[列出游戏开发特定的问题]

### 亮点
[做得好的地方——此章节必须包含]

### 必须修改项
[批准前必须修复的内容——ARCHITECTURAL VIOLATION 始终出现在此处]

### 建议
[可选的改进建议]

### 判定：[APPROVED / APPROVED WITH SUGGESTIONS / CHANGES REQUIRED]
```

本技能为只读——不写入任何文件。

---

## 阶段 9：下一步

- 若判定为 APPROVED：运行 `/story-done [story路径]` 关闭 Story。
- 若判定为 CHANGES REQUIRED：修复问题后重新运行 `/code-review`。
- 若发现 ARCHITECTURAL VIOLATION：运行 `/architecture-decision` 记录正确的处理方式。
