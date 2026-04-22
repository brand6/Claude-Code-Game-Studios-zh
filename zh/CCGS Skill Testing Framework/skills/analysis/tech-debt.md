# 技能测试规范：/tech-debt

## 技能概要

`/tech-debt` 读取 `docs/tech-debt-register.md`（若存在）并扫描 `src/` 目录中的
内联 TODO/FIXME 注释。技能将两个来源合并，去重，按严重性排序，
并更新（或创建）技术债务登记册。

CRITICAL FIXME 条目会最先显示。若检测到之前存在但现在在源代码中已消失的条目
（表明债务已偿还），则将其标记为 RESOLVED 而非删除（保留审计追踪）。
技能在更新登记册前询问"May I write to `docs/tech-debt-register.md`?"。
无 director 门控。判定结果：REGISTER UPDATED（发现新债务并合并）
或 NO NEW DEBT FOUND（登记册内容未变化）。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判定关键词：REGISTER UPDATED、NO NEW DEBT FOUND
- [ ] 在更新技术债务登记册前包含"May I write"协作协议语言
- [ ] 包含下一步交接（例如 `/sprint-plan` 安排偿还债务）

---

## Director 门控检查

无。`/tech-debt` 是代码库维护技能，不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——内联 TODO + 现有登记册合并后更新，REGISTER UPDATED

**夹具：**
- `docs/tech-debt-register.md` 存在，包含 3 个已知债务条目（TD-001、TD-002、TD-003）
- `src/gameplay/combat/CombatSystem.gd` 包含：
  `# TODO: Replace hardcoded damage values with data-driven lookup`
- `src/core/SaveManager.gd` 包含：
  `# FIXME: Save file not encrypted — temporary for prototyping`

**输入：** `/tech-debt`

**预期行为：**
1. 技能读取现有登记册（TD-001 到 TD-003）
2. 技能扫描 `src/` 中的 TODO/FIXME 注释——发现 2 个
3. 技能与登记册进行交叉对比——2 个为新债务，未在 TD-001 到 TD-003 中
4. 技能按严重性排序（FIXME 通常高于 TODO）
5. 技能展示合并后的登记册并询问"May I write to `docs/tech-debt-register.md`?"
6. 写入更新后的登记册（TD-004、TD-005 追加）
7. 判定结果为 REGISTER UPDATED

**断言：**
- [ ] 读取现有登记册（不覆盖现有条目）
- [ ] 从 `src/` 中的内联注释发现 2 个新 TODO/FIXME
- [ ] 新条目去重（避免重复添加已知债务）
- [ ] 写入更新前询问"May I write"
- [ ] 判定结果为 REGISTER UPDATED

---

### 用例 2：登记册不存在——提供创建新登记册的选项

**夹具：**
- `docs/tech-debt-register.md` 不存在
- `src/` 中有 4 个 TODO/FIXME 注释

**输入：** `/tech-debt`

**预期行为：**
1. 技能尝试读取 `docs/tech-debt-register.md`——未找到
2. 技能报告："No tech debt register found. Found 4 TODO/FIXME items in src/."
3. 技能提供创建新登记册的选项
4. 技能询问"May I write a new `docs/tech-debt-register.md`?"
5. 批准后，用从 `src/` 扫描到的 4 个条目创建登记册
6. 判定结果为 REGISTER UPDATED

**断言：**
- [ ] 检测到登记册文件缺失
- [ ] 仍然扫描 `src/` 中的 TODO/FIXME
- [ ] 提供创建新登记册的选项
- [ ] 写入前询问"May I write a new tech-debt-register.md?"
- [ ] 判定结果为 REGISTER UPDATED

---

### 用例 3：已解决的条目——标记为 RESOLVED 而非删除

**夹具：**
- `docs/tech-debt-register.md` 包含 TD-002：
  `FIXME: Combat damage formula hardcoded in CombatSystem.gd`
- `src/gameplay/combat/CombatSystem.gd` 当前版本不再包含对应的 FIXME 注释
  （已修复）

**输入：** `/tech-debt`

**预期行为：**
1. 技能读取登记册——TD-002 标注在 CombatSystem.gd 中
2. 技能扫描 CombatSystem.gd——TD-002 对应的 FIXME 已消失
3. 技能将 TD-002 标记为 RESOLVED（而非从登记册中删除）
4. RESOLVED 状态保留审计追踪
5. 技能询问"May I write to `docs/tech-debt-register.md`?"更新状态
6. 判定结果为 REGISTER UPDATED

**断言：**
- [ ] 检测到 FIXME 注释已从源代码中消失
- [ ] TD-002 标记为 RESOLVED（而非删除）
- [ ] 更新后 RESOLVED 条目在登记册中仍然可见
- [ ] 写入前询问"May I write"
- [ ] 判定结果为 REGISTER UPDATED

---

### 用例 4：CRITICAL FIXME——最先显示

**夹具：**
- `src/core/NetworkManager.gd` 包含：
  `# FIXME: CRITICAL — No input validation on network packets, injection risk`
- `src/` 中还有 5 个其他常规 TODO

**输入：** `/tech-debt`

**预期行为：**
1. 技能扫描并发现 CRITICAL FIXME（以及其他 5 个 TODO）
2. CRITICAL FIXME 在报告和登记册中最先显示
3. 技能对 CRITICAL 条目进行特殊标注（与常规债务区分）
4. 询问"May I write to tech-debt-register.md?"；写入
5. 判定结果为 REGISTER UPDATED

**断言：**
- [ ] CRITICAL FIXME 在报告中首先列出（不仅按文件顺序排列）
- [ ] CRITICAL 条目与常规 TODO 有区分标注
- [ ] 在更新登记册前询问"May I write"

---

### 用例 5：门控合规性——无门控；/tech-debt 为代码库维护技能

**夹具：**
- `src/` 包含一些 TODO/FIXME 注释

**输入：** `/tech-debt`

**预期行为：**
1. 技能完成登记册更新
2. 未调用 director 门控
3. 在更新登记册前询问"May I write"

**断言：**
- [ ] 未调用任何 director 门控
- [ ] 写入登记册前询问"May I write"
- [ ] 判定结果为 REGISTER UPDATED 或 NO NEW DEBT FOUND

---

## 协议合规性

- [ ] 读取现有登记册（若存在）——不覆盖
- [ ] 扫描 `src/` 中的内联 TODO/FIXME 注释
- [ ] 将两个来源合并并去重
- [ ] CRITICAL FIXME 条目最先显示
- [ ] 已解决的条目标记为 RESOLVED 而非删除（保留审计追踪）
- [ ] 写入登记册前询问"May I write"
- [ ] 返回 REGISTER UPDATED 或 NO NEW DEBT FOUND 判定

---

## 覆盖说明

- 债务严重性分级（CRITICAL vs. HIGH vs. MEDIUM）的精确定义
  在技能正文中；此处对分级行为进行断言，但不对精确触发词进行断言。
- 跨 Git 历史追踪技术债务趋势（随时间的债务积累率）
  超出此技能范围，由回顾技能处理。
- 测试文件（`tests/`）中的 TODO 注释通常不应追踪为技术债务；
  此处假定技能会忽略 `tests/` 目录中的 TODO，但不进行断言测试。
