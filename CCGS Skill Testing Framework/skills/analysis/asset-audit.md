# 技能测试规范：/asset-audit

## 技能概要

`/asset-audit` 审计 `assets/` 目录，检查其是否符合命名规范、是否缺少元数据，以及是否存在格式/大小问题。它会依据 `technical-preferences.md` 中定义的规范与预算读取资产文件。无 director 门控。未经用户批准，技能不会写入文件。判定结果：COMPLIANT、WARNINGS 或 NON-COMPLIANT。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证，无需夹具。

- [ ] 包含所需的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判定关键词：COMPLIANT、WARNINGS、NON-COMPLIANT
- [ ] 不要求包含 "May I write" 语言（只读；可选报告写入仍需批准）
- [ ] 包含下一步交接（审计结果出来后该做什么）

---

## Director 门控检查

无。资产审计是只读分析技能；不调用任何门控。

---

## 测试用例

### 用例 1：正常路径——所有资产都遵循命名规范

**夹具：**
- `technical-preferences.md` 指定命名规范为 `snake_case`，例如 `enemy_grunt_idle.png`
- `assets/art/characters/` 包含：`enemy_grunt_idle.png`、`enemy_sniper_run.png`
- `assets/audio/sfx/` 包含：`sfx_jump_land.ogg`、`sfx_item_pickup.ogg`
- 所有文件均在大小预算内（纹理 ≤2MB，音频 ≤500KB）

**输入：** `/asset-audit`

**预期行为：**
1. 技能从 `technical-preferences.md` 读取命名规范与大小预算
2. 递归扫描 `assets/`
3. 所有文件都符合 `snake_case` 规范，且都在预算内
4. 审计表的所有行均显示 PASS
5. 判定结果为 COMPLIANT

**断言：**
- [ ] 审计覆盖美术和音频资产目录
- [ ] 每个文件都根据命名规范和大小预算进行检查
- [ ] 合规时所有行都显示 PASS
- [ ] 判定结果为 COMPLIANT
- [ ] 不写入任何文件

---

### 用例 2：不合规——纹理超出大小预算

**夹具：**
- `assets/art/environment/` 包含 5 个纹理文件
- 其中 3 个纹理文件各为 4MB（预算：≤2MB）
- 其余 2 个纹理文件在预算内

**输入：** `/asset-audit`

**预期行为：**
1. 技能从 `technical-preferences.md` 读取大小预算（纹理 2MB）
2. 扫描 `assets/art/environment/`，发现 3 个超大纹理
3. 审计表列出每个超大文件的实际大小与预算
4. 判定结果为 NON-COMPLIANT
5. 技能为被标记文件建议压缩或降低分辨率

**断言：**
- [ ] 3 个超大文件都按名称列出，并显示实际大小与预算大小
- [ ] 只要任一文件超出预算，判定结果就是 NON-COMPLIANT
- [ ] 为超大文件给出优化建议
- [ ] 为保证完整性，也列出预算内文件（显示 PASS）

---

### 用例 3：格式问题——音频格式错误

**夹具：**
- `technical-preferences.md` 指定音频格式为 OGG
- `assets/audio/music/theme_main.wav` 存在（WAV 格式）
- `assets/audio/sfx/sfx_footstep.ogg` 存在（正确的 OGG 格式）

**输入：** `/asset-audit`

**预期行为：**
1. 技能读取音频格式要求：OGG
2. 扫描 `assets/audio/`，发现 `theme_main.wav` 格式不对
3. 审计表将 `theme_main.wav` 标记为 FORMAT ISSUE（期望 OGG，实际 WAV）
4. `sfx_footstep.ogg` 显示 PASS
5. 判定结果为 WARNINGS（格式问题可修复）

**断言：**
- [ ] `theme_main.wav` 被标记为 FORMAT ISSUE，并注明期望与实际格式
- [ ] 对于可修复的格式问题，判定结果为 WARNINGS（而不是 NON-COMPLIANT）
- [ ] 正确格式的资产显示为 PASS
- [ ] 技能不修改或转换任何资产文件

---

### 用例 4：缺失资产——GDD 引用了 assets/ 中不存在的资产

**夹具：**
- `design/gdd/enemies.md` 引用了 `enemy_boss_idle.png`
- `assets/art/characters/boss/` 目录为空，该文件不存在

**输入：** `/asset-audit`

**预期行为：**
1. 技能读取 GDD 中的资产引用，找出预期资产（与 `/content-audit` 的范围交叉）
2. 扫描 `assets/art/characters/boss/`，未找到该文件
3. 审计表将 `enemy_boss_idle.png` 标记为 MISSING ASSET
4. 判定结果为 NON-COMPLIANT（关键美术资产缺失）

**断言：**
- [ ] 技能会检查 GDD 引用以识别预期资产
- [ ] 缺失资产会标记为 MISSING ASSET，并注明对应的 GDD 引用
- [ ] 当关键资产缺失时，判定结果为 NON-COMPLIANT
- [ ] 技能不创建或添加占位资产

---

### 用例 5：门控合规性——无门控；可单独建议 technical-artist 参与

**夹具：**
- 2 个文件违反命名规范（CamelCase 而不是 snake_case）
- `review-mode.txt` 内容为 `full`

**输入：** `/asset-audit`

**预期行为：**
1. 技能扫描资产并找到 2 个命名违规
2. 无论 review mode 如何，都不调用 director 门控
3. 判定结果为 WARNINGS
4. 输出提示："Consider having a Technical Artist review naming conventions"
5. 技能展示发现结果；可选提供写入审计报告
6. 如果用户选择写入：询问 "May I write to `production/qa/asset-audit-[date].md`?"

**断言：**
- [ ] 任意 review mode 下都不调用 director 门控
- [ ] 只是建议 technical-artist 参与，而不是强制要求
- [ ] 在任何写入提示之前先展示发现表
- [ ] 可选的审计报告写入在真正写入前会询问 "May I write"

---

## 协议合规性

- [ ] 从 `technical-preferences.md` 读取命名规范、格式与大小预算
- [ ] 递归扫描 `assets/` 目录
- [ ] 审计表显示文件名、检查类型、期望值、实际值和结果
- [ ] 不修改任何资产文件
- [ ] 不调用 director 门控
- [ ] 判定结果严格为：COMPLIANT、WARNINGS、NON-COMPLIANT 之一

---

## 覆盖说明

- 元数据检查（例如 Godot `.import` 文件中缺失纹理导入设置）未在这里单独测试；它们沿用相同的 FORMAT ISSUE 标记模式。
- `/asset-audit` 与 `/content-audit` 都会检查 GDD 引用和资产的对应关系，这是有意的重叠；`/asset-audit` 关注合规性，`/content-audit` 关注完整性。
