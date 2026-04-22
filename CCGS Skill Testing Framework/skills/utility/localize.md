# 技能测试规范：/localize

## 技能概要

`/localize` 管理完整的本地化流水线：从源文件中提取玩家可见字符串，
在 `assets/localization/` 中维护翻译文件，
并验证所有语言区域文件的完整性。

对于新语言区域，技能创建包含所有键（值为空）的骨架翻译文件，
并询问"May I write"。对于现有语言区域，技能生成差异报告（新增/删除/变更的字符串），
允许翻译人员了解需要更新的内容。

判决为 LOCALIZATION COMPLETE（所有字符串已翻译）或 GAPS FOUND（存在缺失条目）。
不适用 director 门控。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判决关键词：LOCALIZATION COMPLETE、GAPS FOUND
- [ ] 在写入翻译文件前包含"May I write"协作协议语言
- [ ] 区分"新语言区域"和"现有语言区域"两种工作流路径

---

## Director 门控检查

无。`/localize` 是内容流水线工具。不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——新语言区域，创建骨架翻译文件

**夹具：**
- `assets/localization/en.json` 存在，包含 50 个字符串键
- `assets/localization/fr.json` 不存在

**输入：** `/localize fr`（法语）

**预期行为：**
1. 技能读取 `assets/localization/en.json`（源语言文件）以获取键列表
2. 技能生成 `fr.json` 骨架文件，包含所有 50 个键，值为空字符串
3. 技能询问"May I write to `assets/localization/fr.json`?"
4. 文件写入后，技能输出摘要：50 个字符串待翻译
5. 判决为 GAPS FOUND（骨架文件存在空值）

**断言：**
- [ ] `fr.json` 包含来自 `en.json` 的所有键
- [ ] 所有值为空字符串（不是"TODO"或占位符文本）
- [ ] 写入前询问"May I write"
- [ ] 因存在空值，判决为 GAPS FOUND

---

### 用例 2：现有语言区域——生成差异报告（新增/删除/变更）

**夹具：**
- `assets/localization/en.json` 包含 55 个键（自上次本地化后新增 5 个键，删除 2 个）
- `assets/localization/de.json` 存在，包含 52 个键（部分已翻译，部分为空）

**输入：** `/localize de`（德语）

**预期行为：**
1. 技能读取 `en.json`（55 个键）和 `de.json`（52 个键）
2. 技能生成差异报告：
   - 新增：5 个新键（de.json 中缺失）
   - 删除：2 个已废弃键（de.json 中存在但 en.json 中已删除）
   - 现有：50 个键（已有翻译）
3. 技能询问"May I update `assets/localization/de.json`?"以同步更改
4. 更新文件后，技能输出 GAPS FOUND（若有空值）或 LOCALIZATION COMPLETE（若全部翻译完成）

**断言：**
- [ ] 差异报告识别所有 3 种变更类型（新增/删除/现有）
- [ ] 修改文件前询问"May I update"
- [ ] 已废弃键从 `de.json` 中删除（不保留孤儿键）
- [ ] 若存在空值则判决为 GAPS FOUND，否则为 LOCALIZATION COMPLETE

---

### 用例 3：语言区域中缺少字符串——GAPS FOUND 并列出缺失键

**夹具：**
- `assets/localization/en.json` 包含 20 个键（全部有值）
- `assets/localization/ja.json` 存在，包含 15 个键（缺少 5 个）

**输入：** `/localize ja`（日语）

**预期行为：**
1. 技能读取两个文件
2. 技能识别出 ja.json 中缺少的 5 个键
3. 缺失的键在输出中明确列出（按键名列举）
4. 技能询问是否将缺失的键（值为空）添加至 ja.json
5. 判决为 GAPS FOUND

**断言：**
- [ ] 缺失的键按名称明确列出（不仅说"某些缺失"）
- [ ] 判决为 GAPS FOUND
- [ ] 在翻译人员填写缺失的键之前，判决不为 LOCALIZATION COMPLETE

---

### 用例 4：翻译文件语法错误——技能报告错误并停止

**夹具：**
- `assets/localization/es.json` 存在，但包含无效 JSON（例如，缺少结束括号）

**输入：** `/localize es`（西班牙语）

**预期行为：**
1. 技能尝试读取 `es.json`
2. 技能检测到 JSON 解析错误
3. 技能报告："Parse error in `assets/localization/es.json`: [错误详情]"
4. 技能停止处理（不继续修改损坏的文件）
5. 技能建议用户先修复语法错误

**断言：**
- [ ] 技能不覆盖包含语法错误的文件
- [ ] 错误报告中包含文件名
- [ ] 技能建议先修复语法
- [ ] 损坏文件情况下不发出 LOCALIZATION COMPLETE 或 GAPS FOUND 判决

---

### 用例 5：Director 门控检查——无门控；localize 为内容流水线工具

**夹具：**
- 标准本地化设置

**输入：** `/localize`

**预期行为：**
1. 技能执行本地化流水线
2. 未调用任何 director agent
3. 输出中无门控 ID

**断言：**
- [ ] 未调用 director 门控
- [ ] 输出中无门控跳过消息
- [ ] 技能在不经过任何门控检查的情况下达到 LOCALIZATION COMPLETE / GAPS FOUND

---

## 协议合规

- [ ] 读取源语言文件（通常为 `en.json`）以确定键的完整集合
- [ ] 对现有语言区域生成三类差异报告（新增/删除/现有）
- [ ] 对新语言区域生成所有键为空值的骨架文件
- [ ] 写入或更新文件前询问"May I write"或"May I update"
- [ ] 所有键翻译完成时判决为 LOCALIZATION COMPLETE
- [ ] 存在空值或缺失键时判决为 GAPS FOUND

---

## 覆盖说明

- 多语言区域批量运行（同时处理 de、fr、ja）不在此规范覆盖范围内；
  逐语言区域依次运行，每次运行对应一个语言区域的技能实例。
- 翻译记忆（重用之前的翻译内容）是进阶功能，不在此测试用例范围内。
- 本地化键的实际格式（扁平 JSON vs. 嵌套 JSON）在技能主体中定义，
  不在此规范中硬编码。
