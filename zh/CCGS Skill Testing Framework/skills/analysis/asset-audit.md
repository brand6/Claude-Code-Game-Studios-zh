# 技能测试规范：/asset-audit

## 技能概要

`/asset-audit` 审计 `assets/` 目录，检查命名规范合规性、缺失的元数据、
文件格式标准和资产大小预算。技能读取 `technical-preferences.md` 获取
引擎特定规范（命名规则、格式、大小限制），并遍历 `assets/` 目录与
GDD 中引用的资产对比。

技能可选择询问"May I write the audit report to `production/qa/asset-audit-[日期].md`?"。
不应用修复——仅发现并报告。
无 director 门控。判定结果：COMPLIANT（全部检查通过）、WARNINGS（存在小问题）
或 NON-COMPLIANT（存在命名/大小/格式违规）。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判定关键词：COMPLIANT、WARNINGS、NON-COMPLIANT
- [ ] 在写入审计报告前包含"May I write"协作协议语言
- [ ] 包含下一步交接（例如 `/code-review` 或 `/content-audit`）

---

## Director 门控检查

无。`/asset-audit` 是只读分析技能，不适用 director 门控。

---

## 测试用例

### 用例 1：正常路径——所有资产符合命名和大小规范，COMPLIANT

**夹具：**
- `technical-preferences.md`：引擎为 Godot 4，纹理最大 2048×2048，音频格式为 .ogg，snake_case 命名
- `assets/textures/`：所有文件均为 snake_case .png，尺寸 ≤ 2048×2048
- `assets/audio/`：所有文件均为 .ogg
- `assets/data/`：资产 YAML 文件存在，无孤立引用

**输入：** `/asset-audit`

**预期行为：**
1. 技能读取规范（snake_case、.ogg、≤2048）
2. 技能遍历所有 `assets/` 子目录
3. 技能检查每个文件的命名、格式和大小——全部通过
4. 技能询问"May I write the asset audit report to `production/qa/asset-audit-[date].md`?"
5. 写入报告；判定结果为 COMPLIANT

**断言：**
- [ ] 检查命名规范（snake_case）
- [ ] 检查文件格式（纹理用 .png，音频用 .ogg）
- [ ] 检查尺寸预算（≤ 2048×2048）
- [ ] 0 个违规 → 判定结果为 COMPLIANT
- [ ] 写入报告前询问"May I write"

---

### 用例 2：纹理超过大小预算，NON-COMPLIANT

**夹具：**
- `technical-preferences.md` 纹理上限为 2048×2048
- `assets/textures/boss_dragon.png`：4096×4096（超出预算两倍）
- `assets/textures/player_idle.png`：1024×1024（合规）

**输入：** `/asset-audit`

**预期行为：**
1. 技能扫描纹理
2. 检测到 `boss_dragon.png` 超出大小预算（4096 > 2048）
3. `player_idle.png` 通过
4. 报告标记 `boss_dragon.png` 为 HIGH 严重性违规
5. 判定结果为 NON-COMPLIANT

**断言：**
- [ ] 以文件名标识 `boss_dragon.png` 为违规项
- [ ] 违规报告为 HIGH 严重性
- [ ] `player_idle.png` 在报告中标记为通过
- [ ] 判定结果为 NON-COMPLIANT（非 WARNINGS）

---

### 用例 3：音频文件格式错误——使用了 .mp3 而非 .ogg，WARNINGS

**夹具：**
- `technical-preferences.md` 指定音频格式为 .ogg
- `assets/audio/ambient_forest.mp3`（格式错误——应为 .ogg）
- `assets/audio/player_jump.ogg`（正确格式）

**输入：** `/asset-audit`

**预期行为：**
1. 技能扫描音频文件
2. 检测到 `ambient_forest.mp3` 使用了错误格式
3. 将此标记为 MEDIUM 严重性（格式问题通常可修复但不致命）
4. `player_jump.ogg` 通过
5. 判定结果为 WARNINGS

**断言：**
- [ ] 识别格式违规（.mp3 而非 .ogg）
- [ ] 标记为 MEDIUM 严重性
- [ ] 判定结果为 WARNINGS（非 NON-COMPLIANT，因为无大小或命名违规）

---

### 用例 4：GDD 引用了不存在的资产，NON-COMPLIANT

**夹具：**
- GDD 引用了 `assets/textures/boss_frost_golem.png`
- 该文件在 `assets/textures/` 中不存在

**输入：** `/asset-audit`

**预期行为：**
1. 技能读取 GDD 以获取预期资产引用
2. 技能扫描 `assets/textures/` 目录
3. 技能检测到 `boss_frost_golem.png` 被 GDD 引用但在磁盘上缺失
4. 将此标记为 HIGH 严重性（缺失资产会破坏 GDD 实现）
5. 判定结果为 NON-COMPLIANT

**断言：**
- [ ] 将 GDD 引用与磁盘上实际存在的资产进行对比
- [ ] 检测到缺失的 GDD 引用资产（`boss_frost_golem.png`）
- [ ] 标记为 HIGH 严重性
- [ ] 判定结果为 NON-COMPLIANT

---

### 用例 5：门控合规性——无门控；可选报告写入

**夹具：**
- `assets/` 目录存在且有内容，规范已配置

**输入：** `/asset-audit`

**预期行为：**
1. 技能完成完整的审计
2. 未调用 director 门控
3. 可选写入审计报告时询问"May I write"

**断言：**
- [ ] 未调用任何 director 门控
- [ ] 写入报告时（若选择写入）询问"May I write"
- [ ] 报告可选——若用户拒绝仍返回判定结果

---

## 协议合规性

- [ ] 从 `technical-preferences.md` 读取规范（不硬编码）
- [ ] 检查命名规范、格式和大小预算
- [ ] 扫描时将 GDD 引用与磁盘上的资产对比
- [ ] 写入审计报告前询问"May I write"（报告为可选）
- [ ] 仅报告——不修改、重命名或删除任何资产文件
- [ ] 返回 COMPLIANT、WARNINGS 或 NON-COMPLIANT 判定

---

## 覆盖说明

- 孤立资产（磁盘上存在但无 GDD 引用）的行为此处未测试。
  技能可将其报告为 WARNINGS，但这不属于 NON-COMPLIANT 范畴。
- Unity 和 Unreal 的资产命名规范与 Godot snake_case 有所不同。
  技能应从 `technical-preferences.md` 读取规范，而非假定使用 Godot 规范。
- 资产管道工具（AssetPostprocessor 等）生成的元数据文件审计
  此处未测试，超出基础审计范围。
