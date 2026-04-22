# 技能测试规范：/content-audit

## 技能测试规范：/content-audit

## 技能概要

`/content-audit` 读取 GDD 中的内容规格（角色数量、关卡数量、物品类型等），
并对照 `assets/` 目录检查已实现的内容，识别规划内容与已构建内容之间的差距。
技能生成差距表，列出：内容类型、GDD 指定数量、已发现数量和缺失的具体条目。

技能不自动写入报告——但可选询问"May I write the audit report to `production/qa/content-audit-[日期].md`?"。
不应用修复——仅报告缺口。
无 director 门控。判定结果：COMPLETE（所有规格内容均已构建）、
GAPS FOUND（内容存在但数量不足或格式不对）
或 MISSING CRITICAL CONTENT（缺少重要游戏内容，可能阻碍里程碑达成）。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判定关键词：COMPLETE、GAPS FOUND、MISSING CRITICAL CONTENT
- [ ] 在写入审计报告前包含"May I write"协作协议语言
- [ ] 包含下一步交接（例如 `/asset-spec` 规格制作缺失内容，或 `/sprint-plan` 安排内容）

---

## Director 门控检查

无。`/content-audit` 是只读分析技能，不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——所有指定内容均已构建，COMPLETE

**夹具：**
- `design/gdd/enemies.md` 指定：5 种敌人类型（哥布林、巨魔、史莱姆、弓箭手、首领）
- `assets/enemies/` 包含 5 个目录（goblin/、troll/、slime/、archer/、boss/）
- 所有 5 个目录均包含各自的资产

**输入：** `/content-audit`

**预期行为：**
1. 技能读取敌人 GDD 获取规格数量（5 种类型）
2. 技能扫描 `assets/enemies/` 目录
3. 找到全部 5 种类型，均带有各自的资产文件
4. 差距表：全部 5/5 完整
5. 判定结果为 COMPLETE

**断言：**
- [ ] 从 GDD 读取指定数量（5 种敌人类型）
- [ ] 将 `assets/` 内容与 GDD 规格进行比对
- [ ] 差距表准确（5/5 完整）
- [ ] 判定结果为 COMPLETE
- [ ] 不修改任何资产文件

---

### 用例 2：缺少一种敌人类型——GAPS FOUND

**夹具：**
- `design/gdd/enemies.md` 指定 5 种敌人类型
- `assets/enemies/` 仅包含 4 个目录（缺少 boss/）

**输入：** `/content-audit`

**预期行为：**
1. 技能读取 GDD——5 种类型规格
2. 技能扫描 `assets/enemies/`——发现 4 种
3. 检测到差距：boss 类型缺失
4. 差距表：4/5 完整；缺失：boss
5. 判定结果为 GAPS FOUND

**断言：**
- [ ] 差距表显示 4/5 完整
- [ ] 在差距报告中将"boss"标识为缺失内容
- [ ] 判定结果为 GAPS FOUND

---

### 用例 3：GDD 无内容规格——GAPS FOUND，建议 /design-system

**夹具：**
- GDD 存在但不包含具体内容规格（例如仅有叙述性描述，无"5 种敌人类型"列表）

**输入：** `/content-audit`

**预期行为：**
1. 技能读取 GDD——无结构化内容规格
2. 技能无法比对内容（无参考数量）
3. 技能报告："No content specifications found in GDDs.
   Run `/design-system [name]` to add content specs."
4. 判定结果为 GAPS FOUND（无法验证完整性）

**断言：**
- [ ] 检测到 GDD 中缺少内容规格
- [ ] 建议 `/design-system` 添加规格
- [ ] 判定结果为 GAPS FOUND（非 COMPLETE——无法确认完整性）

---

### 用例 4：资产格式错误——GAPS FOUND

**夹具：**
- `design/gdd/items.md` 指定物品图标为 `.png` 格式
- `assets/items/icons/sword_icon.jpg`（格式错误——应为 .png）

**输入：** `/content-audit`

**预期行为：**
1. 技能读取 GDD 内容规格（需要 .png 图标）
2. 技能扫描 `assets/items/icons/`
3. 检测到 `sword_icon.jpg`——格式错误（jpg 而非 png）
4. 将此标记为内容存在但格式不符
5. 判定结果为 GAPS FOUND（内容已规划且存在，但未满足格式要求）

**断言：**
- [ ] 检测到格式不符（.jpg 而非 .png）
- [ ] 文件被标记为 GAPS FOUND（非 COMPLETE——格式错误）
- [ ] 报告列出格式差距

---

### 用例 5：门控合规性——无门控；可选报告写入

**夹具：**
- GDD 和资产目录均已配置

**输入：** `/content-audit`

**预期行为：**
1. 技能完成完整的内容审计
2. 未调用 director 门控
3. 询问"May I write"写入可选报告

**断言：**
- [ ] 未调用任何 director 门控
- [ ] 写入报告时询问"May I write"
- [ ] 报告为可选

---

## 协议合规性

- [ ] 从 GDD 读取内容规格数量（不硬编码期望值）
- [ ] 将资产目录与 GDD 规格进行比对
- [ ] 报告在差距表中列出缺失条目的名称
- [ ] 写入报告前询问"May I write"（报告为可选）
- [ ] 不修改任何资产文件
- [ ] 返回 COMPLETE、GAPS FOUND 或 MISSING CRITICAL CONTENT 判定

---

## 覆盖说明

- MISSING CRITICAL CONTENT（而非 GAPS FOUND）的门限标准——例如缺少 50% 以上的关键内容——
  在技能正文中定义；此处不对该门限进行断言测试。
- 跨多个内容类别（敌人、物品、关卡等）的批量审计遵循相同的逐类别检查模式；
  此处针对单个类别测试。
- 孤立资产（磁盘上存在但 GDD 无规格的内容）可报告为 GAPS FOUND，
  但此处不进行断言测试。
