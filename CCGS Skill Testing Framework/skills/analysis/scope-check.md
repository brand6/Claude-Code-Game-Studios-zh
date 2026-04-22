# 技能测试规范：/scope-check

## 技能概要

`/scope-check` 通过将当前冲刺或故事文件与活跃里程碑目标进行比较，
来分析范围蔓延情况。技能读取活跃冲刺计划和当前里程碑定义，
标记冲刺计划中与里程碑目标没有可追踪关联的条目。
技能为只读——不写入任何文件，不修改故事或冲刺计划。

无 director 门控。判定结果：ON SCOPE（所有故事均可追踪至里程碑目标）、
CONCERNS（部分故事较弱或间接关联到里程碑）或
SCOPE CREEP DETECTED（故事与任何里程碑目标均无可追踪关联）。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判定关键词：ON SCOPE、CONCERNS、SCOPE CREEP DETECTED
- [ ] 不包含"May I write"语言（scope-check 为只读技能，不写入文件）
- [ ] 包含下一步交接（例如 `/sprint-plan` 调整范围，或 `/milestone-review` 更新里程碑目标）

---

## Director 门控检查

无。`/scope-check` 是只读分析技能，不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——所有故事均可追踪至里程碑目标，ON SCOPE

**夹具：**
- `production/milestones/alpha.md` 定义目标：战斗系统、玩家移动、基本 UI
- `production/sprints/sprint-05/sprint-plan.md` 包含 3 个故事：
  - 故事 1：实现近战攻击（→ 战斗系统）
  - 故事 2：实现奔跑机制（→ 玩家移动）
  - 故事 3：实现暂停菜单（→ 基本 UI）

**输入：** `/scope-check`

**预期行为：**
1. 技能读取里程碑目标（战斗、移动、UI）
2. 技能读取冲刺计划（3 个故事）
3. 技能将每个故事映射至里程碑目标——全部 3 个均匹配
4. 输出追踪矩阵：3/3 故事有里程碑依据
5. 判定结果为 ON SCOPE

**断言：**
- [ ] 从里程碑文件读取目标
- [ ] 将每个故事映射至里程碑目标
- [ ] 3/3 故事有可追踪关联 → 判定结果为 ON SCOPE
- [ ] 不写入任何文件

---

### 用例 2：2 个故事与里程碑无关联——SCOPE CREEP DETECTED

**夹具：**
- 里程碑目标：战斗系统、玩家移动、基本 UI（无音频目标）
- 冲刺包含 5 个故事：3 个可追踪至里程碑，2 个无关联
  （故事 4：实现背景音乐，故事 5：添加排行榜功能）

**输入：** `/scope-check`

**预期行为：**
1. 技能将所有 5 个故事映射至里程碑目标
2. 故事 4（背景音乐）：无对应里程碑目标
3. 故事 5（排行榜功能）：无对应里程碑目标
4. 技能报告：2 个故事没有里程碑依据
5. 判定结果为 SCOPE CREEP DETECTED

**断言：**
- [ ] 识别故事 4 和故事 5 与里程碑不匹配
- [ ] 报告中命名具体的范围蔓延条目
- [ ] 判定结果为 SCOPE CREEP DETECTED
- [ ] 不修改冲刺计划

---

### 用例 3：未定义里程碑——CONCERNS，建议 /milestone-review

**夹具：**
- `production/milestones/` 目录不存在或为空
- 冲刺计划存在

**输入：** `/scope-check`

**预期行为：**
1. 技能尝试读取里程碑定义——未找到
2. 技能报告："No milestone definition found. Cannot determine if sprint is in scope."
3. 建议 `/milestone-review` 定义里程碑目标
4. 判定结果为 CONCERNS（无法在没有基准的情况下验证范围）

**断言：**
- [ ] 检测到里程碑定义缺失
- [ ] 建议 `/milestone-review` 定义里程碑
- [ ] 判定结果为 CONCERNS（非 SCOPE CREEP DETECTED——缺少基准，并非明确的蔓延）
- [ ] 不写入任何文件

---

### 用例 4：故事间接关联里程碑——CONCERNS（弱追踪性）

**夹具：**
- 里程碑目标：战斗系统
- 故事：重构工具代码（内部工具，未被玩家看见，不直接实现战斗）

**输入：** `/scope-check`

**预期行为：**
1. 技能将"重构工具代码"映射至里程碑目标
2. 无直接匹配——故事与战斗、移动或 UI 无直接关联
3. 技能将其标记为弱/间接关联（技术债务 vs 里程碑交付物）
4. 建议与产品负责人确认是否在正确的冲刺中进行
5. 判定结果为 CONCERNS

**断言：**
- [ ] 检测到与里程碑的间接/弱关联
- [ ] 将其标记为 CONCERNS（而非 SCOPE CREEP DETECTED）
- [ ] 建议与产品负责人确认优先级
- [ ] 不写入任何文件

---

### 用例 5：门控合规性——无门控；scope-check 为只读

**夹具：**
- 里程碑和冲刺计划均已配置

**输入：** `/scope-check`

**预期行为：**
1. 技能完成范围分析
2. 未调用 director 门控
3. 不写入任何文件

**断言：**
- [ ] 未调用任何 director 门控
- [ ] 不写入任何文件
- [ ] 判定结果为 ON SCOPE、CONCERNS 或 SCOPE CREEP DETECTED

---

## 协议合规性

- [ ] 从里程碑定义读取范围目标（不硬编码）
- [ ] 将每个故事映射至里程碑目标
- [ ] 区分直接不匹配（SCOPE CREEP）与弱关联（CONCERNS）
- [ ] 从不写入任何文件（完全只读）
- [ ] 返回 ON SCOPE、CONCERNS 或 SCOPE CREEP DETECTED 判定

---

## 覆盖说明

- 跨多个活跃里程碑的范围检查（例如 Alpha + Beta 并行运行）遵循相同模式；
  此处仅对单一活跃里程碑进行测试。
- 范围蔓延的量化（例如"冲刺中 40% 的工作与里程碑无关"）
  在技能正文中定义；此处不对精确百分比门限进行断言。
- 技术债务故事（重构、基础设施改进）始终具有弱里程碑追踪性；
  此处在用例 4 中作为 CONCERNS 测试，而非 SCOPE CREEP DETECTED。
