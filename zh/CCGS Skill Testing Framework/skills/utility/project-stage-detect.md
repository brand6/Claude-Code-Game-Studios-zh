# 技能测试规范：/project-stage-detect

## 技能概要

`/project-stage-detect` 自动分析项目制品，判断当前开发阶段。
它识别以下 7 个阶段：Concept、Systems Design、Technical Setup、
Pre-Production、Production、Polish、Release。

技能始终报告置信度（HIGH/MEDIUM/LOW）。若 `production/stage.txt` 存在，
技能读取该文件并与制品分析进行交叉验证，
标记已记录阶段与实际项目状态之间的任何差异。

技能不写入 `stage.txt`——设置 stage.txt 是 `/gate-check` 的职责。
不适用 director 门控。判决为"检测到的阶段"，无固定判决词。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 定义 7 个开发阶段（Concept 至 Release）
- [ ] 报告置信度等级（HIGH/MEDIUM/LOW）
- [ ] 不包含写入 `production/stage.txt` 的说明（这是 `/gate-check` 的职责）
- [ ] 包含下一步交接（例如 `/gate-check` 以正式推进阶段）

---

## Director 门控检查

无。`/project-stage-detect` 是诊断工具。不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——stage.txt 存在，交叉验证

**夹具：**
- `production/stage.txt` 内容为 `production`
- 源代码文件存在（`src/` 目录）
- 活跃冲刺（`production/sprints/sprint-010.md`）存在
- GDD 和 architecture.md 均存在

**输入：** `/project-stage-detect`

**预期行为：**
1. 技能读取 `production/stage.txt` → `production`
2. 技能读取制品：源代码、冲刺文件、GDD
3. 技能将已记录阶段与制品进行交叉验证——结果一致
4. 技能输出："Detected stage: Production (matches stage.txt)"
5. 报告置信度：HIGH（stage.txt 与制品相符）
6. 推荐的下一步：继续使用 `/sprint-plan` 或 `/dev-story`

**断言：**
- [ ] 检测到的阶段为 Production
- [ ] 输出注明"matches stage.txt"
- [ ] 置信度为 HIGH
- [ ] 未写入任何文件

---

### 用例 2：无 stage.txt，但有 GDD 和 Epic——推断为 Production

**夹具：**
- 不存在 `production/stage.txt`
- `design/gdd/` 中存在 4 个已批准的 GDD 文件
- 存在 Epic 文件（`production/epics/`）
- 不存在源代码文件

**输入：** `/project-stage-detect`

**预期行为：**
1. 技能尝试读取 `production/stage.txt`——未找到
2. 技能扫描项目制品：GDD（✓）、Epics（✓）、源代码（✗）、冲刺（✗）
3. 技能推断："有 GDD 和 Epics 但无源代码——处于 Pre-Production 阶段"
4. 置信度：MEDIUM（无 stage.txt 确认）
5. 建议运行 `/gate-check` 以设置 `stage.txt`

**断言：**
- [ ] 检测到的阶段为 Pre-Production（不是 Production 或 Systems Design）
- [ ] 置信度为 MEDIUM
- [ ] 建议运行 `/gate-check` 设置 stage.txt
- [ ] 未写入任何文件

---

### 用例 3：无 stage.txt，无文档，无源代码——推断为 Concept

**夹具：**
- 不存在任何项目文件（新建仓库，仅有 CLAUDE.md）

**输入：** `/project-stage-detect`

**预期行为：**
1. 技能扫描项目——除 CLAUDE.md 外无制品
2. 技能推断："无 GDD、无 Epics、无源代码——处于 Concept 阶段"
3. 置信度：HIGH（缺少制品是 Concept 阶段的有力证据）
4. 建议运行 `/start` 开始引导流程

**断言：**
- [ ] 检测到的阶段为 Concept
- [ ] 置信度为 HIGH（缺少制品是 Concept 的有力证据）
- [ ] 建议运行 `/start` 作为下一步
- [ ] 未写入任何文件

---

### 用例 4：stage.txt 显示 Production，但无源代码——置信度 LOW，标记差异

**夹具：**
- `production/stage.txt` 内容为 `production`
- 不存在源代码文件（`src/` 目录为空或不存在）
- 存在 GDD 和 architecture.md

**输入：** `/project-stage-detect`

**预期行为：**
1. 技能读取 `production/stage.txt` → `production`
2. 技能扫描制品——未找到源代码
3. 技能标记差异："stage.txt says Production but no source code files found"
4. 置信度：LOW（已记录阶段与实际制品不符）
5. 建议运行 `/gate-check` 以更新阶段状态

**断言：**
- [ ] 差异消息出现在输出中
- [ ] 置信度为 LOW
- [ ] 建议运行 `/gate-check` 或 `/project-stage-detect`（重新评估）
- [ ] 未写入任何文件

---

### 用例 5：Director 门控检查——无门控；stage detect 为诊断工具

**夹具：**
- 任意项目状态

**输入：** `/project-stage-detect`

**预期行为：**
1. 技能检测并报告开发阶段
2. 未调用任何 director agent
3. 未写入任何文件

**断言：**
- [ ] 未调用 director 门控
- [ ] 未写入任何文件
- [ ] 输出中无门控跳过消息

---

## 协议合规

- [ ] 识别所有 7 个阶段（Concept 至 Release）
- [ ] 报告置信度（HIGH/MEDIUM/LOW）
- [ ] 若 stage.txt 存在，则与制品进行交叉验证
- [ ] 在已记录阶段与实际制品存在差异时标记
- [ ] 不写入 `production/stage.txt`（这是 `/gate-check` 的职责）
- [ ] 所有情况下均不写入任何文件

---

## 覆盖说明

- 7 个阶段之间的精确阈值（例如，几个 GDD 意味着 Systems Design 阶段结束）
  在技能主体中定义，不在此规范中硬编码；仅对整体阶段推断进行断言。
- 存在多个差异的情况（例如，stage.txt 显示 Release 但无 GDD）
  与用例 4 相同处理：置信度 LOW 并列出所有差异。
- 置信度等级（HIGH/MEDIUM/LOW）基于制品的存在性和 stage.txt 是否确认；
  不基于制品的质量。
