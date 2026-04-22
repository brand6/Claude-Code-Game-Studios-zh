# 技能测试规范：/consistency-check

## 技能概要

`/consistency-check` 扫描所有 GDD，交叉对比 `design/registry/entities.yaml`
（实体注册表），以发现不同文档之间的冲突：公式不匹配、竞争性所有权、
失效引用和依赖缺口。技能优先使用 grep 搜索而非全文档读取，
先读取注册表，再仅针对冲突部分读取 GDD。

技能可选择询问"May I write the consistency report to `production/qa/consistency-[日期].md`?"。
不应用修复——仅报告冲突。无 director 门控。
判定结果：CONSISTENT（无冲突）、CONFLICTS FOUND（存在直接冲突）
或 DEPENDENCY GAP（依赖的 GDD 缺失）。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判定关键词：CONSISTENT、CONFLICTS FOUND、DEPENDENCY GAP
- [ ] 在写入一致性报告前包含"May I write"协作协议语言
- [ ] 包含下一步交接（例如 `/design-review` 审查冲突的 GDD，或 `/propagate-design-change`）

---

## Director 门控检查

无。`/consistency-check` 是只读分析技能，不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——4 个 GDD 无冲突，CONSISTENT

**夹具：**
- `design/registry/entities.yaml` 包含 player、enemy、weapon、item 实体
- 4 个 GDD 文件（combat.md、player.md、enemy.md、items.md）相互引用一致
- 公式无冲突，所有权清晰

**输入：** `/consistency-check`

**预期行为：**
1. 技能读取实体注册表
2. 技能 grep 所有 GDD 查找跨文档引用
3. 检查所有公式和属性值——无冲突
4. 技能询问"May I write the consistency report?"
5. 写入报告；判定结果为 CONSISTENT

**断言：**
- [ ] 先读取实体注册表（优先于全文档读取）
- [ ] 0 个公式冲突 → 判定结果为 CONSISTENT
- [ ] 写入报告前询问"May I write"
- [ ] 不修改任何 GDD 文件

---

### 用例 2：伤害公式冲突——CONFLICTS FOUND（HIGH）

**夹具：**
- `design/gdd/combat.md`：`damage = base_attack × 1.5`
- `design/gdd/enemy.md`：`damage = base_attack × 2.0`（与 combat.md 冲突）

**输入：** `/consistency-check`

**预期行为：**
1. 技能 grep GDD 查找"damage ="定义
2. 检测到冲突：combat.md 定义乘数 1.5，enemy.md 定义乘数 2.0
3. 将此标记为 HIGH 严重性冲突（核心公式不一致）
4. 报告列出具体冲突（引用两个文件及其各自定义）
5. 判定结果为 CONFLICTS FOUND

**断言：**
- [ ] 检测到公式冲突（×1.5 vs ×2.0）
- [ ] 报告中列出两个冲突文件
- [ ] 标记为 HIGH 严重性
- [ ] 判定结果为 CONFLICTS FOUND

---

### 用例 3：依赖 GDD 缺失——DEPENDENCY GAP（MEDIUM）

**夹具：**
- `design/gdd/items.md` 引用了"crafting-system GDD"
- `design/gdd/crafting.md` 不存在

**输入：** `/consistency-check`

**预期行为：**
1. 技能读取 items GDD
2. 检测到对 crafting-system 的引用
3. 技能检查 `design/gdd/crafting.md` 是否存在——未找到
4. 将此标记为 DEPENDENCY GAP，MEDIUM 严重性
5. 建议运行 `/design-system crafting` 创建缺失的 GDD
6. 判定结果为 DEPENDENCY GAP

**断言：**
- [ ] 检测到 items GDD 中的依赖引用
- [ ] 检查被引用的 GDD 是否存在
- [ ] 检测到缺失 GDD 后标记为 DEPENDENCY GAP
- [ ] 建议 `/design-system crafting` 作为下一步
- [ ] 判定结果为 DEPENDENCY GAP

---

### 用例 4：未找到 GDD——报告错误，建议 /design-system

**夹具：**
- `design/gdd/` 目录为空或不存在

**输入：** `/consistency-check`

**预期行为：**
1. 技能扫描 GDD 目录——未找到 GDD 文件
2. 技能报告："No GDD files found. Run `/design-system [name]` to create system designs."
3. 不进行一致性检查（无可比较内容）
4. 技能礼貌退出

**断言：**
- [ ] 检测到无 GDD 文件
- [ ] 建议 `/design-system` 创建设计文档
- [ ] 不生成部分报告
- [ ] 技能以清晰的错误信息退出

---

### 用例 5：门控合规性——无门控；不读取 review-mode.txt

**夹具：**
- GDD 存在于标准位置

**输入：** `/consistency-check`

**预期行为：**
1. 技能完成完整的一致性检查
2. 未调用 director 门控
3. 技能不读取 `review-mode.txt` 或类似环境标志

**断言：**
- [ ] 未调用任何 director 门控
- [ ] 不读取或引用任何 `review-mode.txt` 文件
- [ ] 写入报告时询问"May I write"

---

## 协议合规性

- [ ] 先读取实体注册表，再针对冲突 grep GDD 章节
- [ ] 检查公式冲突、所有权冲突和依赖缺口
- [ ] 按严重性（HIGH/MEDIUM/LOW）对冲突进行分类
- [ ] 写入报告前询问"May I write"（报告为可选）
- [ ] 不修改任何 GDD 文件
- [ ] 返回 CONSISTENT、CONFLICTS FOUND 或 DEPENDENCY GAP 判定

---

## 覆盖说明

- 本技能检查 GDD 之间的结构一致性；深度设计理论分析（支柱偏移、主导策略等）
  由 `/review-all-gdds` 处理。
- 技能通过 grep 优先模式而非逐文档全文读取来检测冲突——这是一种优化，
  以避免在大型项目中消耗过多 token。此处不对 grep 搜索行为进行断言。
- 实体属性的所有权冲突（两个 GDD 都声称拥有同一属性的规范定义）
  此处未单独测试，但在 CONFLICTS FOUND 判定下涵盖。
- 命名风格不一致（不同 GDD 使用不同大小写或单数/复数）报告为 LOW 严重性，
  此处未单独测试。
