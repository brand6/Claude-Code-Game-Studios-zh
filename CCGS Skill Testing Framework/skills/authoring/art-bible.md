# Skill Test Spec: /art-bible

## Skill 概述

引导逐节编写美术圣经。骨架优先。必需章节：视觉风格（Visual Style）、色彩方案（Color Palette）、
字体设计（Typography）、角色设计规则（Character Design Rules）、环境风格（Environment Style）、
UI 视觉语言（UI Visual Language）。
完整模式：所有章节起草完成后运行 AD-ART-BIBLE 门控。
精简/独立模式：门控跳过。
输出：`design/art-bible.md`。
裁决：COMPLETE。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 明确列出 6 个必需章节
- [ ] 完整模式下所有章节起草后运行 AD-ART-BIBLE 门控
- [ ] 精简和独立模式下跳过 AD-ART-BIBLE 并注明
- [ ] 骨架文件在讨论内容之前创建（含所有章节标题）
- [ ] 按章节询问"May I write section [N]?"
- [ ] 输出路径为 `design/art-bible.md`
- [ ] 裁决为 COMPLETE
- [ ] 末尾包含下一步交接（如 `/asset-spec` 或 `/design-system`）

---

## 门控检查

### AD-ART-BIBLE 门控（美术总监审查）

**触发条件：** 完整模式下所有 6 个章节均已起草后

**派生 agent：** art-director（内部门控 ID：AD-ART-BIBLE）

**预期行为：**
- art-director 评审完整美术圣经草稿，检查视觉一致性、风格定义清晰度和可实施性
- 返回裁决：APPROVED / CONCERNS / REJECTED

**断言：**
- [ ] 仅在完整模式下派生 art-director
- [ ] 精简和独立模式中不派生 AD-ART-BIBLE 门控
- [ ] 门控在所有 6 个章节起草完成后才运行（不是逐章节运行）

---

## 测试用例

### 用例 1：正常路径——完整模式，门控 APPROVED，裁决 COMPLETE

**测试夹具：**
- 完整模式：`production/session-state/review-mode.txt` 为 `full`
- 无现有美术圣经
- AD-ART-BIBLE 门控返回 APPROVED

**输入：** `/art-bible`

**预期行为：**
1. 立即创建骨架文件 `design/art-bible.md`，包含所有 6 个章节标题（但内容为空）
2. 子 agent 询问"May I write the skeleton to `design/art-bible.md`?"
3. 逐节引导：
   - 为每个章节提供上下文问题（例如："这款游戏的整体视觉风格定位是什么？"）
   - 讨论并起草内容
   - 询问"May I write section [视觉风格]?"
   - 用户批准后写入该章节
4. 所有 6 个章节完成后，派生 AD-ART-BIBLE 门控
5. art-director 返回 APPROVED
6. 裁决：COMPLETE
7. 引用下一步：`/asset-spec` 生产准备

**断言：**
- [ ] 骨架文件在任何内容讨论之前立即创建
- [ ] 按章节逐节引导，每节有独立的"May I write"询问
- [ ] AD-ART-BIBLE 门控在所有 6 个章节完成后运行
- [ ] 门控 APPROVED 后裁决为 COMPLETE
- [ ] 输出路径为 `design/art-bible.md`

---

### 用例 2：完整模式，AD-ART-BIBLE 返回 CONCERNS——修订章节

**测试夹具：**
- 完整模式
- 所有 6 个章节已起草
- AD-ART-BIBLE 返回 CONCERNS：色彩方案章节中主色和辅助色的对比度比值未说明，无障碍合规性存疑

**输入：** `/art-bible`（门控评审场景）

**预期行为：**
1. 所有 6 个章节起草完成
2. 派生 AD-ART-BIBLE 门控
3. art-director 返回 CONCERNS：色彩方案无障碍问题
4. 编排者显示具体 CONCERNS 内容
5. 因有 CONCERNS，不直接写入最终文件（或若已写入则需修订）
6. `AskUserQuestion` 提供选项：
   - 修订色彩方案章节以添加对比度比值后，重新请求 AD-ART-BIBLE 审查
   - 记录此问题为待解决事项，先完成美术圣经再处理

**断言：**
- [ ] CONCERNS 具体内容（色彩方案无障碍问题）在输出中列出
- [ ] `AskUserQuestion` 提供修订特定章节并重评审的选项
- [ ] Skill 不在 CONCERNS 未解决的情况下以 COMPLETE 状态输出最终版本（除非用户明确接受）

---

### 用例 3：精简模式——AD-ART-BIBLE 跳过，状态 COMPLETE

**测试夹具：**
- 精简模式：`production/session-state/review-mode.txt` 为 `lean`

**输入：** `/art-bible`

**预期行为：**
1. 骨架文件创建
2. 逐节引导完成所有 6 个章节
3. 所有章节完成后，无门控派生
4. 输出注明："[AD-ART-BIBLE] 跳过——精简模式"
5. 裁决：COMPLETE

**断言：**
- [ ] 精简模式下不派生 AD-ART-BIBLE 门控
- [ ] 跳过明确注明并含"精简模式"标签
- [ ] 无门控输出
- [ ] 裁决为 COMPLETE

---

### 用例 4：独立模式——AD-ART-BIBLE 跳过，Skill 注明

**测试夹具：**
- `production/session-state/review-mode.txt` 为 `solo`

**输入：** `/art-bible`

**预期行为：**
1. 骨架文件创建；逐节完成所有 6 个章节
2. 独立模式：AD-ART-BIBLE 门控跳过
3. 输出注明："[AD-ART-BIBLE] 跳过——独立模式"
4. 裁决：COMPLETE（独立模式下 COMPLETE 是正常结果）

**断言：**
- [ ] 独立模式下不派生 AD-ART-BIBLE 门控
- [ ] 跳过注明含"独立模式"标签
- [ ] 裁决为 COMPLETE

---

### 用例 5（适配版）：现有美术圣经——改造模式

**测试夹具：**
- `design/art-bible.md` 已存在，包含部分章节
- 用户希望更新或补充缺失章节

**输入：** `/art-bible`

**预期行为：**
1. Skill 读取现有 `design/art-bible.md`
2. 编排者注明："发现现有美术圣经——进入改造模式"
3. 编排者分析现有内容，识别完整章节 vs 空/缺失章节
4. `AskUserQuestion` 提供选项：
   - 仅补充缺失/空章节
   - 从头重写整个美术圣经
5. 根据选择，按需引导用户

**断言：**
- [ ] 发现现有美术圣经时不被静默覆盖
- [ ] 编排者识别哪些章节已完整、哪些需要补充
- [ ] `AskUserQuestion` 提供改造选项

---

## 协议合规性

- [ ] 骨架文件在讨论任何内容之前立即创建
- [ ] 逐节讨论和起草，一次一个章节
- [ ] AD-ART-BIBLE 门控在完整模式下所有章节起草后运行
- [ ] 精简和独立模式中 AD-ART-BIBLE 跳过并明确注明
- [ ] 按章节询问"May I write section [N]?"
- [ ] 裁决为 COMPLETE（无论门控结果如何，完成写作即为 COMPLETE）

---

## 覆盖率说明

- AD-ART-BIBLE 返回 REJECTED（而非仅 CONCERNS）的情况未独立测试；
  Skill 会阻塞写入并询问用户如何处理（修订或覆盖）。
- 字体设计章节被列为必需章节，但其具体内容要求未在此 spec 中独立断言。
- 美术圣经为 `/asset-spec` 提供输入——此关系在交接部分中注明，
  但不作为本 Skill spec 的测试内容。
