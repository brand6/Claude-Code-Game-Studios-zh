# 技能测试规范：/content-audit

## 技能概要

`/content-audit` 读取 `design/gdd/` 中的 GDD，检查其中指定的所有内容项（敌人、物品、关卡等）是否都在 `assets/` 中有对应实现。它会生成一张缺口表：Content Type → Specified Count → Found Count → Missing Items。无 director 门控。未经用户批准，技能不会写入文件。判定结果：COMPLETE、GAPS FOUND 或 MISSING CRITICAL CONTENT。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证，无需夹具。

- [ ] 包含所需的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判定关键词：COMPLETE、GAPS FOUND、MISSING CRITICAL CONTENT
- [ ] 不要求包含 "May I write" 语言（只读输出；写入是可选报告）
- [ ] 包含下一步交接（缺口表审阅后该做什么）

---

## Director 门控检查

无。内容审计是只读分析技能；不调用任何门控。

---

## 测试用例

### 用例 1：正常路径——所有指定内容都已存在

**夹具：**
- `design/gdd/enemies.md` 指定 4 种敌人类型：Grunt、Sniper、Tank、Boss
- `assets/art/characters/` 包含目录：`grunt/`、`sniper/`、`tank/`、`boss/`
- `design/gdd/items.md` 指定 3 种物品类型；在 `assets/data/items/` 中都能找到这 3 种物品

**输入：** `/content-audit`

**预期行为：**
1. 技能读取 `design/gdd/` 中的全部 GDD
2. 技能针对每个被指定的内容项扫描 `assets/`
3. 全部 4 种敌人和 3 种物品都能找到
4. 缺口表显示：所有行都满足 Found Count = Specified Count，且没有缺失项
5. 判定结果为 COMPLETE

**断言：**
- [ ] 缺口表覆盖 GDD 中找到的所有内容类型
- [ ] 每一行都显示 Specified Count 与 Found Count
- [ ] 当数量匹配时，不应出现缺失项
- [ ] 判定结果为 COMPLETE
- [ ] 不写入任何文件

---

### 用例 2：发现缺口——资产中缺少一种敌人类型

**夹具：**
- `design/gdd/enemies.md` 指定 3 种敌人类型：Grunt、Sniper、Boss
- `assets/art/characters/` 仅包含：`grunt/`、`sniper/`（缺少 Boss 文件夹）

**输入：** `/content-audit`

**预期行为：**
1. 技能读取 GDD，发现共指定 3 种敌人
2. 技能扫描 `assets/art/characters/`，只找到 2 种
3. 缺口表的敌人一行显示：Specified 3、Found 2、Missing: Boss
4. 判定结果为 GAPS FOUND

**断言：**
- [ ] 缺口表行会按名称指出缺失项是 "Boss"
- [ ] 同时显示 Specified Count（3）和 Found Count（2）
- [ ] 只要有任一内容项缺失，判定结果就是 GAPS FOUND
- [ ] 技能不会假定该资产以后会补齐，而是立即标记缺口

---

### 用例 3：未找到 GDD 内容规格——给出指引

**夹具：**
- `design/gdd/` 中只有 `core-loop.md`，其中没有内容清单章节
- 不存在其他包含内容规格的 GDD

**输入：** `/content-audit`

**预期行为：**
1. 技能读取全部 GDD，但没有发现内容清单章节
2. 输出："No content specifications found in GDDs — run /design-system first to define content lists"
3. 不生成缺口表
4. 判定结果为 GAPS FOUND（因为没有规格，无法确认完整性）

**断言：**
- [ ] 当 GDD 中不存在内容规格时，技能不会生成缺口表
- [ ] 输出建议运行 `/design-system`
- [ ] 判定结果要体现“无法确认完整性”

---

### 用例 4：边界情况——资产格式不符合目标平台要求

**夹具：**
- `design/gdd/audio.md` 指定音频资产使用 OGG 格式
- `assets/audio/sfx/jump.wav` 存在（WAV 格式，而不是 OGG）
- `assets/audio/sfx/land.ogg` 存在（格式正确）
- `technical-preferences.md` 指定音频格式为 OGG

**输入：** `/content-audit`

**预期行为：**
1. 技能读取 GDD 音频规格，以及 technical preferences 中的格式要求
2. 找到 `jump.wav`，确认它存在，但格式不正确
3. 音频一行缺口表显示：Specified 2、Found 2（按名称），但 `jump.wav` 标记为 FORMAT ISSUE
4. 判定结果为 GAPS FOUND（格式合规性属于内容完整性的一部分）

**断言：**
- [ ] 如果 GDD 或 technical preferences 指定了格式，技能会检查资产格式
- [ ] `jump.wav` 会被标记为 FORMAT ISSUE，并注明期望格式（OGG）
- [ ] 格式问题在缺口表中要与“内容缺失”区分开
- [ ] 只要存在格式问题，判定结果就是 GAPS FOUND

---

### 用例 5：门控合规性——只读；无门控；缺口表供人工审阅

**夹具：**
- GDD 共指定 10 个内容项；资产中找到 9 个，缺 1 个
- `review-mode.txt` 内容为 `full`

**输入：** `/content-audit`

**预期行为：**
1. 技能读取 GDD 并扫描资产，生成缺口表
2. 无论 review mode 如何，都不调用 director 门控
3. 技能将缺口表作为只读输出展示给用户
4. 判定结果为 GAPS FOUND
5. 技能会提供可选的审计报告写入，但不会自动写入

**断言：**
- [ ] 任意 review mode 下都不调用 director 门控
- [ ] 直接展示缺口表，不会自动写入任何文件
- [ ] 可选报告写入会被提供，但不是强制流程
- [ ] 技能不会修改任何资产文件

---

## 协议合规性

- [ ] 在生成缺口表前读取 GDD 和资产目录
- [ ] 缺口表显示 Content Type、Specified Count、Found Count、Missing Items
- [ ] 不在未经用户明确批准的情况下写入文件
- [ ] 不调用 director 门控
- [ ] 判定结果严格为：COMPLETE、GAPS FOUND、MISSING CRITICAL CONTENT 之一

---

## 覆盖说明

- MISSING CRITICAL CONTENT（相对于 GAPS FOUND）会在 GDD 将缺失项标记为关键内容时触发；这里未显式单测，但沿用相同的检测路径。
- `assets/` 目录不存在的情况未在这里测试；这种情况下，技能会对所有被指定项给出 MISSING CRITICAL CONTENT 判定。
