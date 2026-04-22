# 技能测试规范：/prototype

## 技能概要

`/prototype` 是快速原型验证工作流。它跳过正常标准（无需 ADR、允许硬编码），
在 `prototypes/[机制名]/` 目录下快速验证游戏概念或机制。

原型完成后生成 findings 文档，记录：机制是否可行、
发现了哪些问题，以及是否建议推进至 `/design-system`。
若同名原型已存在，技能提供三个选项：扩展现有原型、替换原型或归档。

不适用 director 门控——原型阶段意图快速实验。
判决为 PROTOTYPE COMPLETE（机制可行）或 PROTOTYPE ABANDONED（机制不可行）。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判决关键词：PROTOTYPE COMPLETE、PROTOTYPE ABANDONED
- [ ] 记录放宽的标准（允许硬编码，无需 ADR）
- [ ] 记录三个冲突处理选项：扩展/替换/归档

---

## Director 门控检查

无。`/prototype` 是快速实验技能。不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——机制原型化，findings 文档，PROTOTYPE COMPLETE

**夹具：**
- 不存在 `prototypes/` 目录
- 需要原型化：力矩拉杆跳跃机制

**输入：** `/prototype momentum-jump`

**预期行为：**
1. 技能在 `prototypes/momentum-jump/` 创建原型目录
2. 技能生成原型代码（允许硬编码的魔法数字）
3. 技能询问"May I write to `prototypes/momentum-jump/`?"
4. 用户批准；代码写入
5. 技能生成 `prototypes/momentum-jump/findings.md`，包含：
   - 验证的机制
   - 发现的问题
   - 建议：推进至 `/design-system`
6. 判决为 PROTOTYPE COMPLETE

**断言：**
- [ ] 在 `prototypes/momentum-jump/` 下创建原型文件
- [ ] 写入前询问"May I write"
- [ ] `findings.md` 生成于原型目录内
- [ ] `findings.md` 包含建议章节
- [ ] 判决为 PROTOTYPE COMPLETE

---

### 用例 2：原型已存在——提供三个选项（扩展/替换/归档）

**夹具：**
- `prototypes/momentum-jump/` 已存在，包含之前的原型代码和 findings.md

**输入：** `/prototype momentum-jump`

**预期行为：**
1. 技能检测到 `prototypes/momentum-jump/` 已存在
2. 技能呈现三个选项：
   - **Extend**（扩展）：在现有原型基础上新增功能
   - **Replace**（替换）：从头创建新原型（覆盖现有内容）
   - **Archive**（归档）：将现有原型移至 `prototypes/archived/`，再创建新原型
3. 用户选择一个选项
4. 技能继续执行所选的原型工作流

**断言：**
- [ ] 检测到现有原型，呈现三个选项
- [ ] 三个选项标签准确：Extend、Replace、Archive
- [ ] 技能在用户选择后才继续（不假设任何默认选项）
- [ ] 三条路径均到达 PROTOTYPE COMPLETE 或 PROTOTYPE ABANDONED

---

### 用例 3：原型验证机制——建议推进至 /design-system

**夹具：**
- 原型创建完成，机制在测试过程中表现良好

**输入：** `/prototype`（用户在测试后报告结果）

**预期行为：**
1. 原型完成，用户报告正向测试结果
2. `findings.md` 记录："Mechanism validated. Ready for full design."
3. 技能建议运行 `/design-system [机制名]` 进行正式设计
4. 判决为 PROTOTYPE COMPLETE

**断言：**
- [ ] `findings.md` 中的建议包含 `/design-system` 的下一步指引
- [ ] 判决为 PROTOTYPE COMPLETE
- [ ] 建议中包含机制名称（不是通用的"运行 /design-system"）

---

### 用例 4：机制不可行——PROTOTYPE ABANDONED，findings 记录原因

**夹具：**
- 原型创建完成
- 测试结果：机制导致帧率下降至 15fps，无法达到目标性能

**输入：** `/prototype`（用户报告性能问题）

**预期行为：**
1. 用户报告机制在性能方面不可行
2. `findings.md` 记录："Mechanism abandoned: performance cost too high (15fps)"
3. 技能不建议推进至 `/design-system`
4. 技能建议探索替代方案或取消该机制
5. 判决为 PROTOTYPE ABANDONED

**断言：**
- [ ] `findings.md` 包含放弃原因
- [ ] 判决为 PROTOTYPE ABANDONED（不是 PROTOTYPE COMPLETE）
- [ ] 技能不强行建议推进至 `/design-system`

---

### 用例 5：Director 门控检查——无门控；prototype 为实验工具

**夹具：**
- 标准原型设置

**输入：** `/prototype`

**预期行为：**
1. 技能执行原型工作流
2. 未调用任何 director agent
3. 输出中无门控 ID

**断言：**
- [ ] 未调用 director 门控
- [ ] 输出中无门控跳过消息
- [ ] 技能在不经过任何门控检查的情况下达到 PROTOTYPE COMPLETE 或 PROTOTYPE ABANDONED

---

## 协议合规

- [ ] 在 `prototypes/[机制名]/` 目录下创建原型文件
- [ ] 写入代码前询问"May I write"
- [ ] 生成包含验证结论和建议的 `findings.md`
- [ ] 同名原型已存在时，呈现扩展/替换/归档三个选项
- [ ] 机制可行时判决为 PROTOTYPE COMPLETE，不可行时为 PROTOTYPE ABANDONED

---

## 覆盖说明

- 放宽的标准（允许硬编码的魔法数字、无需 ADR）适用于原型阶段，
  不适用于正式源代码；`/dev-story` 中会强制执行正式标准。
- 原型代码生命周期（测试后丢弃）是有意为之的设计——
  此规范不测试最终代码质量。
- 归档路径（`prototypes/archived/[机制名]/`）在技能主体中定义；
  此规范仅要求"归档"选项存在且可选。
