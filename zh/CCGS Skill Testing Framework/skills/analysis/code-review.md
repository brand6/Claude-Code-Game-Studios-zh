# 技能测试规范：/code-review

## 技能概要

`/code-review` 对 `src/` 中的指定文件或文件集进行架构和质量代码审查。
技能检查编码标准合规性（文档注释、依赖注入而非单例、数据驱动、
可测试性），以及架构模式遵循情况（ADR 中定义的模式是否正确应用）。

技能不进行任何编辑——仅生成带有判定的代码审查报告。
审查报告显示每个文件的问题列表，并附有严重性级别和建议。
无 director 门控（但技能在发现关键问题时可能建议咨询首席程序员 agent）。
判定结果：APPROVED（全部符合标准）、CONCERNS（存在小问题）
或 NEEDS CHANGES（存在明确问题需在合并前解决）。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判定关键词：APPROVED、CONCERNS、NEEDS CHANGES
- [ ] 不包含"May I write"语言（代码审查技能不修改代码）
- [ ] 包含下一步交接（例如 `/dev-story` 修复问题，或 `/story-done` 确认通过）

---

## Director 门控检查

无。`/code-review` 是只读分析技能，不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——所有标准符合，APPROVED

**夹具：**
- `src/gameplay/combat/CombatSystem.gd` 存在
- 包含类级文档注释
- 使用构造函数注入（无全局单例引用）
- 伤害公式从数据文件加载（数据驱动）
- 所有方法均可通过公共接口进行单元测试

**输入：** `/code-review src/gameplay/combat/CombatSystem.gd`

**预期行为：**
1. 技能读取 `CombatSystem.gd`
2. 技能根据编码标准检查每个标准
3. 所有 4 个标准均通过（文档注释、依赖注入、数据驱动、可测试性）
4. 不发现架构问题
5. 判定结果为 APPROVED

**断言：**
- [ ] 检查文档注释（类级注释存在）
- [ ] 检查依赖注入（无单例引用）
- [ ] 检查数据驱动模式（数据从文件加载而非硬编码）
- [ ] 检查可测试性（方法可通过公共接口访问）
- [ ] 0 个问题 → 判定结果为 APPROVED
- [ ] 不修改代码文件

---

### 用例 2：缺失文档注释 + 使用单例——NEEDS CHANGES

**夹具：**
- `src/gameplay/ui/InventoryUI.gd` 存在：
  - 无类级文档注释
  - 直接引用 `GameManager` 单例：`GameManager.instance.add_item(item)`

**输入：** `/code-review src/gameplay/ui/InventoryUI.gd`

**预期行为：**
1. 技能读取 `InventoryUI.gd`
2. 技能检测到问题：
   - 标准 1 失败：缺少类级文档注释（MEDIUM 严重性）
   - 标准 2 失败：单例引用 `GameManager.instance`（HIGH 严重性）
3. 报告列出两个问题，附严重性级别和修复建议
4. 判定结果为 NEEDS CHANGES（存在 HIGH 严重性问题）

**断言：**
- [ ] 检测到缺失文档注释（MEDIUM 严重性）
- [ ] 检测到单例使用（HIGH 严重性）
- [ ] 报告提供每个问题的修复建议
- [ ] 判定结果为 NEEDS CHANGES（存在 HIGH 严重性问题）
- [ ] 代码文件不被修改

---

### 用例 3：ADR 状态为 Proposed（非 Accepted）——CONCERNS（架构风险）

**夹具：**
- `src/networking/StateSync.gd` 实现了 ADR-007（状态同步模式）
- `docs/architecture/adr-007-state-sync.md` 存在且状态为"Proposed"（非"Accepted"）

**输入：** `/code-review src/networking/StateSync.gd`

**预期行为：**
1. 技能读取 `StateSync.gd` 并识别引用的 ADR（ADR-007）
2. 技能读取 ADR-007 状态——Proposed，非 Accepted
3. 技能报告架构风险："Code implements ADR-007, but ADR is still Proposed.
   Architecture decision may change."
4. 标记为 MEDIUM 严重性（架构问题，非代码问题）
5. 判定结果为 CONCERNS

**断言：**
- [ ] 检测到 ADR 引用并读取 ADR 状态
- [ ] 将 Proposed 状态标记为架构风险
- [ ] 问题标记为 MEDIUM 严重性
- [ ] 判定结果为 CONCERNS（存在风险但代码本身无误）
- [ ] 代码不被修改

---

### 用例 4：路径未找到——报告错误信息

**夹具：**
- 提供的路径不存在：`src/gameplay/magic/SpellSystem.gd`

**输入：** `/code-review src/gameplay/magic/SpellSystem.gd`

**预期行为：**
1. 技能尝试读取指定路径——未找到文件
2. 技能输出错误信息：
   "File not found: `src/gameplay/magic/SpellSystem.gd`. Check the path and try again."
3. 不生成部分审查报告
4. 技能礼貌退出

**断言：**
- [ ] 文件不存在时技能不崩溃
- [ ] 错误信息中包含提供的路径
- [ ] 不生成部分/无效报告

---

### 用例 5：门控合规性——无 director 门控；LP 咨询为建议

**夹具：**
- 包含 HIGH 严重性问题的代码文件

**输入：** `/code-review src/some-system.gd`

**预期行为：**
1. 技能完成代码审查
2. 未调用 director 门控
3. 若发现关键问题，报告建议咨询首席程序员 agent（但不强制执行）

**断言：**
- [ ] 未调用任何 director 门控
- [ ] 发现 HIGH 严重性问题时，报告中可选择性建议咨询首席程序员
- [ ] 不修改任何文件

---

## 协议合规性

- [ ] 读取指定文件（不批量扫描整个 src/ 目录，除非被明确要求）
- [ ] 检查编码标准中定义的每个标准
- [ ] 检测并报告 ADR 引用及其状态
- [ ] 从不修改任何代码文件
- [ ] 报告每个问题时附严重性级别和修复建议
- [ ] 返回 APPROVED、CONCERNS 或 NEEDS CHANGES 判定

---

## 覆盖说明

- 批量审查（整个目录或多个文件）此处未测试，但遵循相同的逐文件检查模式。
- 编码标准中的具体规则在 `.claude/docs/coding-standards.md` 中定义；
  此处对标准进行断言测试，但不对具体规则文本进行断言。
- 跨文件的架构一致性（例如系统 A 的 API 与系统 B 期望不匹配）
  超出单文件代码审查范围，由 `/architecture-review` 处理。
- 测试覆盖率检查（验证相应测试文件是否存在）是扩展目标，此处未进行测试；
  这主要属于 `/test-evidence-review` 的职责范围。
