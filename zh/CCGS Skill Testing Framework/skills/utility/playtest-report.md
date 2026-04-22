# 技能测试规范：/playtest-report

## 技能概要

`/playtest-report` 从会话备注或用户输入生成结构化的游戏测试报告。
报告分为四个章节：
1. **Feel & Accessibility**（游戏体验与无障碍）
2. **Bugs Observed**（观察到的缺陷）
3. **Design Feedback**（设计反馈）
4. **Next Steps**（后续行动）

若有多名测试员，技能聚合反馈并标注多数/少数意见。
若缺陷与现有缺陷报告匹配，技能生成交叉引用链接，
而不是重复列出相同问题。

不适用 director 门控（CD-PLAYTEST 门控是独立调用，非本技能的一部分）。
判决始终为 COMPLETE。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判决关键词：COMPLETE
- [ ] 记录四个必要报告章节：Feel & Accessibility、Bugs Observed、Design Feedback、Next Steps
- [ ] 在写入报告前包含"May I write"协作协议语言
- [ ] 包含下一步交接（例如 `/bug-report` 处理新发现的缺陷，`/design-review` 处理设计反馈）

---

## Director 门控检查

无。`/playtest-report` 是文档工具。CD-PLAYTEST 是通过独立会话调用的独立门控，
不由本技能触发。

---

## 测试用例

### 用例 1：正常路径——用户提供备注，生成结构化报告

**夹具：**
- 无现有游戏测试报告
- `production/bugs/` 为空（无现有缺陷）

**输入：** `/playtest-report`（用户提供："Movement felt sluggish,
  controls took 10 mins to learn, found a bug where double jump doesn't work
  near walls, overall fun but boss fight too hard"）

**预期行为：**
1. 技能解析用户备注，提取相关内容
2. 技能生成包含四个章节的结构化报告：
   - Feel & Accessibility：行动迟缓，操控需要 10 分钟学习
   - Bugs Observed：双段跳在靠近墙壁时失效
   - Design Feedback：游戏有趣，但 Boss 战难度过高
   - Next Steps：建议对缺陷运行 `/bug-report`，对设计反馈运行 `/design-review`
3. 技能询问"May I write?"并写入报告
4. 判决为 COMPLETE

**断言：**
- [ ] 报告包含全部四个章节
- [ ] 每条反馈归入对应章节
- [ ] 双段跳问题归入 Bugs Observed 章节
- [ ] 判决为 COMPLETE

---

### 用例 2：空输入——逐章节引导用户填写

**夹具：**
- 无游戏测试备注

**输入：** `/playtest-report`（无附加内容）

**预期行为：**
1. 技能检测到无输入内容
2. 技能通过结构化提问引导：
   - "How did the game feel overall?"
   - "Did you observe any bugs?"
   - "What design feedback do you have?"
   - "What are the next steps you'd recommend?"
3. 技能将用户回答汇总为结构化报告
4. 技能询问"May I write?"；判决为 COMPLETE

**断言：**
- [ ] 技能针对四个章节各提至少一个引导问题
- [ ] 所有章节均收集到后才生成报告
- [ ] 判决为 COMPLETE

---

### 用例 3：多名测试员——聚合反馈，标注多数/少数意见

**夹具：**
- 用户提供 3 名测试员的备注：
  - 测试员 A："Controls felt great, boss fight too easy"
  - 测试员 B："Controls felt great, boss fight too hard"
  - 测试员 C："Controls a bit stiff, boss fight too hard"

**输入：** `/playtest-report`（用户粘贴全部 3 份备注）

**预期行为：**
1. 技能识别出 3 名测试员的独立备注
2. 聚合后的结果：
   - 操控顺畅（多数，3 人中 2 人认为顺畅，1 人认为略显僵硬）
   - Boss 难度过高（多数，3 人中 2 人认为，1 人认为太简单）
3. 技能标注多数意见（大多数测试员）和少数意见（异议意见）
4. 写入报告；判决为 COMPLETE

**断言：**
- [ ] 报告区分多数意见和少数意见
- [ ] 结论基于聚合结果，而非仅使用最后一名测试员的备注
- [ ] 判决为 COMPLETE

---

### 用例 4：缺陷匹配现有报告——生成链接而非重复列出

**夹具：**
- `production/bugs/bug-2026-03-22-double-jump-near-walls.md` 已存在

**输入：** `/playtest-report`（用户备注包含："double jump broken near walls"）

**预期行为：**
1. 技能扫描 `production/bugs/` 查找相关现有报告
2. 技能找到匹配报告：bug-2026-03-22-double-jump-near-walls.md
3. 在 Bugs Observed 章节中，技能链接至现有报告：
   "See existing bug report: bug-2026-03-22-double-jump-near-walls.md"
4. 不为相同问题创建重复报告
5. 判决为 COMPLETE

**断言：**
- [ ] 技能链接至现有缺陷报告，而不是创建新报告
- [ ] 未为已存在的缺陷建议运行 `/bug-report`
- [ ] 现有缺陷报告文件名（链接）出现在 Bugs Observed 章节中
- [ ] 判决为 COMPLETE

---

### 用例 5：Director 门控检查——无门控；报告为文档工具

**夹具：**
- 标准游戏测试输入

**输入：** `/playtest-report`

**预期行为：**
1. 技能生成游戏测试报告
2. 未调用任何 director agent
3. 输出中无门控 ID

**断言：**
- [ ] 未调用 director 门控（包括 CD-PLAYTEST）
- [ ] 输出中无门控跳过消息
- [ ] 技能在不经过任何门控检查的情况下达到 COMPLETE

---

## 协议合规

- [ ] 报告包含所有四个章节：Feel & Accessibility、Bugs Observed、Design Feedback、Next Steps
- [ ] 多名测试员时聚合反馈并区分多数/少数意见
- [ ] 扫描现有缺陷报告以交叉引用，避免重复
- [ ] 在写入前询问"May I write?"
- [ ] 所有情况下判决均为 COMPLETE

---

## 覆盖说明

- 此技能不会自动创建缺陷报告——仅创建游戏测试报告并链接至现有缺陷报告。
  新缺陷的发现需要单独运行 `/bug-report`。
- 多名测试员的聚合启发式方法（通过相似措辞分组）在技能主体中定义；
  此规范仅要求区分多数/少数意见。
- CD-PLAYTEST 门控（creative-director 游戏测试设计审查）是通过独立会话调用的，
  不在此技能范围内。
