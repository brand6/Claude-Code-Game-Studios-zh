# Skill Test Spec: /design-system

## Skill 概述

引导骨架优先的 GDD 逐节编写，共 8 个必需章节。
CD-GDD-ALIGN 门控在完整模式和精简模式下均运行（仅独立模式跳过）。
支持改造模式。
裁决：APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED。
下一步：`/review-all-gdds` 或 `/map-systems next`。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 明确包含 8 个必需章节
- [ ] CD-GDD-ALIGN 门控在完整模式和精简模式下均运行
- [ ] 仅独立模式跳过 CD-GDD-ALIGN 并注明
- [ ] 骨架文件在内容讨论之前创建（含所有 8 个章节标题）
- [ ] 按章节询问"May I write section [N]?"
- [ ] MAJOR REVISION 阻塞章节写入直至解决
- [ ] 仅写入已批准的非空章节
- [ ] 裁决关键字：APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED
- [ ] 末尾包含下一步交接：`/review-all-gdds` 或 `/map-systems next`

---

## 门控检查

### CD-GDD-ALIGN 门控（创意总监 GDD 对齐审查）

**触发条件：** 完整模式和精简模式下，每个章节起草后

**派生 agent：** creative-director（内部门控 ID：CD-GDD-ALIGN）

**预期行为：**
- creative-director 评审章节草稿，检查是否与游戏核心愿景和设计支柱对齐
- 返回裁决：APPROVED / NEEDS REVISION / MAJOR REVISION NEEDED

**断言：**
- [ ] 完整模式和精简模式均派生 CD-GDD-ALIGN
- [ ] 仅独立模式跳过 CD-GDD-ALIGN
- [ ] MAJOR REVISION NEEDED 阻塞当前章节写入，直至用户解决

---

## 测试用例

### 用例 1：正常路径——精简模式，骨架优先

**测试夹具：**
- 精简模式：`production/session-state/review-mode.txt` 为 `lean`
- 目标系统：战斗系统
- CD-GDD-ALIGN 返回 APPROVED

**输入：** `/design-system combat`

**预期行为：**
1. 立即创建包含所有 8 个章节标题的骨架文件（内容为空）
2. 子 agent 询问"May I write the skeleton to `design/gdd/combat.md`?"
3. 按章节逐节引导：
   - 第一章节：提出引导问题（例如："战斗系统的核心机制是什么？"）
   - 讨论并起草内容
   - 派生 CD-GDD-ALIGN 门控（精简模式也要运行）
   - 门控返回 APPROVED
   - 询问"May I write section [概述]?"
   - 用户批准后写入该章节
4. 所有 8 个章节按此模式完成
5. 裁决：APPROVED
6. 下一步：`/review-all-gdds` 或 `/map-systems next`

**断言：**
- [ ] 骨架文件在任何内容讨论之前立即创建
- [ ] 精简模式下每节均运行 CD-GDD-ALIGN 门控
- [ ] 按章节逐节询问"May I write section [N]?"（不是整个文档一次询问）
- [ ] 门控 APPROVED 后方写入章节
- [ ] 裁决为 APPROVED（所有章节完成）

---

### 用例 2：改造模式——现有 GDD

**测试夹具：**
- `design/gdd/crafting.md` 已存在，包含部分章节（3/8 完整）

**输入：** `/design-system crafting`

**预期行为：**
1. Skill 读取现有 `design/gdd/crafting.md`
2. 编排者注明："发现现有 GDD——进入改造模式"
3. 分析现有内容，识别完整章节 vs 缺失章节
4. `AskUserQuestion` 提供：
   - 仅补充缺失的 5 个章节
   - 修订特定章节（用户指定）
5. 改造过程中每节仍运行 CD-GDD-ALIGN 门控（完整或精简模式）
6. 仅写入新增/修订且通过门控的章节

**断言：**
- [ ] 发现现有 GDD 时不被静默覆盖
- [ ] 改造模式中已完整的章节不被重写（除非用户指定）
- [ ] 改造过程中 CD-GDD-ALIGN 门控仍正常运行

---

### 用例 3：CD-GDD-ALIGN 返回 MAJOR REVISION——阻塞写入

**测试夹具：**
- 完整模式
- "核心循环"章节草稿已完成
- CD-GDD-ALIGN 返回 MAJOR REVISION NEEDED：核心循环与游戏设计支柱"探索优先"相矛盾——当前设计强制玩家完成战斗才能推进，限制了探索自由度

**输入：** `/design-system exploration`（章节评审场景）

**预期行为：**
1. "核心循环"章节起草完成
2. 派生 CD-GDD-ALIGN 门控
3. creative-director 返回 MAJOR REVISION NEEDED
4. 编排者立即显示：**MAJOR REVISION NEEDED——章节写入已阻塞**
5. 具体问题列出（与"探索优先"支柱相矛盾）
6. 该章节不被写入文件
7. `AskUserQuestion` 提供选项：
   - 修订核心循环章节以解除强制战斗限制
   - 在此停止，重新讨论设计方向
8. 直到用户修订并重新获得 CD-GDD-ALIGN APPROVED 后，才写入该章节

**断言：**
- [ ] MAJOR REVISION NEEDED 时章节不被写入文件
- [ ] 具体矛盾（与"探索优先"支柱冲突）在输出中列出
- [ ] Skill 不写入"TBD"或占位符内容
- [ ] `AskUserQuestion` 提供修订并重评审的选项

---

### 用例 4：独立模式——CD-GDD-ALIGN 跳过，明确注明

**测试夹具：**
- `production/session-state/review-mode.txt` 为 `solo`

**输入：** `/design-system inventory`

**预期行为：**
1. 骨架文件创建；逐节引导
2. 每个章节起草后：CD-GDD-ALIGN 门控跳过
3. 每节输出注明："[CD-GDD-ALIGN] 跳过——独立模式"
4. 无创意总监 agent 派生
5. 仅需用户批准即可写入章节
6. 裁决：APPROVED（独立模式下完成即视为 APPROVED，但注明未经门控审查）

**断言：**
- [ ] 独立模式下每节均不派生 CD-GDD-ALIGN
- [ ] 每节跳过均明确注明（含"独立模式"标签）
- [ ] 裁决为 APPROVED（独立模式）

---

### 用例 5：空章节不被写入

**测试夹具：**
- 精简模式
- 编写"边缘案例处理"章节时，用户表示此章节暂无内容，跳过

**输入：** `/design-system skill-tree`（章节空内容场景）

**预期行为：**
1. 引导到"边缘案例处理"章节
2. 用户表示暂无内容，不提供任何实质内容
3. Skill 不写入该章节（不写空内容、不写"TBD"、不写占位符）
4. 骨架文件中该章节的标题保留（结构完整）
5. 继续进行下一章节
6. 会话末尾列出所有未完成章节，提醒用户补充：
   "以下章节未完成，请稍后返回填写：[边缘案例处理]"

**断言：**
- [ ] 空章节或未批准章节不被写入文件
- [ ] 骨架文件中该章节标题保留
- [ ] Skill 追踪并在末尾列出所有未完成章节
- [ ] Skill 不写入"TBD"或占位符内容（需用户明确批准才能写入）

---

## 协议合规性

- [ ] 骨架文件在任何章节内容讨论之前创建（含所有 8 个章节标题）
- [ ] CD-GDD-ALIGN 在完整模式和精简模式下均运行（不仅仅是完整模式）
- [ ] 仅独立模式跳过 CD-GDD-ALIGN——每节明确注明
- [ ] 按章节逐节询问"May I write [章节]?"（不是整个文档一次）
- [ ] MAJOR REVISION NEEDED 阻塞当前章节写入直至解决
- [ ] 仅写入已批准的非空章节
- [ ] 末尾包含下一步交接：`/review-all-gdds` 或 `/map-systems next`

---

## 覆盖率说明

- 必需的 8 个章节根据项目设计文档标准在 `CLAUDE.md` 中定义——
  未在此 spec 中重新枚举。
- Skill 内部的章节顺序逻辑（首先撰写哪个章节）未独立测试——
  顺序遵循标准 GDD 模板。
- CD-GDD-ALIGN 中支柱对齐检查由门控 agent 整体评估——
  具体支柱检查未在此 spec 中独立测试。
