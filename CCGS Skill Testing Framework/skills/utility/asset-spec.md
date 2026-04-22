# 技能测试规范：/asset-spec

## 技能概要

`/asset-spec` 从设计需求中生成每个资产的视觉规格文档。
它读取相关 GDD、美术圣经和设计系统，生成一份结构化的资产规格表，
定义：尺寸、动画状态（如适用）、调色板引用、风格说明、技术约束
（格式、文件大小预算）以及交付物清单。

规格表在"May I write"确认后写入 `assets/specs/[资产名]-spec.md`。
若规格已存在，技能提供更新选项。当单次调用请求多个资产时，
每个资产单独发出一次"May I write"询问。不适用 director 门控。
所有请求的规格均写入完成后，判决为 COMPLETE。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需夹具。

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含至少 2 个阶段标题
- [ ] 包含判决关键词：COMPLETE
- [ ] 包含"May I write"协作协议语言（每个资产各一次）
- [ ] 包含下一步交接（例如，分配给美术师，或稍后运行 `/asset-audit`）

---

## Director 门控检查

无。`/asset-spec` 是设计文档工具。技术美术师可以单独审查规格，
但这不是本技能内部的门控步骤。

---

## 测试用例

### 用例 1：正常路径——包含完整 GDD 和美术圣经的敌人精灵规格

**夹具：**
- `design/gdd/enemies.md` 存在，定义了敌人变体
- `design/art-bible.md` 存在，包含调色板和风格说明
- "goblin-enemy"尚无资产规格

**输入：** `/asset-spec goblin-enemy`

**预期行为：**
1. 技能读取敌人 GDD 和美术圣经
2. 技能为哥布林敌人精灵生成规格：
   - 尺寸：从引擎默认值推断或直接从 GDD 获取
   - 动画状态：idle、walk、attack、hurt、death
   - 调色板引用：链接到美术圣经调色板章节
   - 风格说明：来自美术圣经角色设计规则
   - 技术约束：格式（PNG）、大小预算
   - 交付物清单
3. 技能询问"May I write to `assets/specs/goblin-enemy-spec.md`?"
4. 批准后写入文件；判决为 COMPLETE

**断言：**
- [ ] 所有 6 个规格组成部分均存在（尺寸、动画、调色板、风格、技术、清单）
- [ ] 调色板引用链接到美术圣经（而非复制内容）
- [ ] 动画状态来自 GDD（而非凭空捏造）
- [ ] "May I write"询问包含正确路径
- [ ] 判决为 COMPLETE

---

### 用例 2：未找到美术圣经——规格包含占位风格说明，依赖项已标记

**夹具：**
- `design/gdd/player.md` 存在
- `design/art-bible.md` 不存在

**输入：** `/asset-spec player-sprite`

**预期行为：**
1. 技能读取玩家 GDD，但找不到美术圣经
2. 技能生成包含占位风格说明的规格："DEPENDENCY GAP: art bible
   not found — style notes are placeholders"
3. 调色板章节使用："TBD — see art bible when created"
4. 技能询问"May I write to `assets/specs/player-sprite-spec.md`?"
5. 文件写入，带有占位符和依赖项标记；判决为 COMPLETE 并附有建议说明

**断言：**
- [ ] 为缺失的美术圣经标记 DEPENDENCY GAP
- [ ] 规格仍然生成（未被阻塞）
- [ ] 风格说明包含占位符标记，而非捏造的风格
- [ ] 判决为 COMPLETE 并附有建议说明

---

### 用例 3：资产规格已存在——提供更新选项

**夹具：**
- `assets/specs/goblin-enemy-spec.md` 已存在
- 自规格写入后 GDD 已更新（新增了攻击动画）

**输入：** `/asset-spec goblin-enemy`

**预期行为：**
1. 技能检测到现有规格文件
2. 技能报告："Asset spec already exists for goblin-enemy — checking for updates"
3. 技能对比 GDD 与现有规格，发现：GDD 中新增了"charge-attack"动画状态但规格中没有
4. 技能呈现差异："1 new animation state found — offering to update spec"
5. 技能询问"May I update `assets/specs/goblin-enemy-spec.md`?"（而非覆写）
6. 规格已更新；判决为 COMPLETE

**断言：**
- [ ] 检测到现有规格并提供"更新"路径
- [ ] 显示 GDD 与现有规格之间的差异
- [ ] 使用"May I update"语言（而非"May I write"）
- [ ] 保留现有规格内容；仅应用差异
- [ ] 判决为 COMPLETE

---

### 用例 4：请求多个资产——每个资产单独询问"May I write"

**夹具：**
- GDD 和美术圣经存在
- 用户请求 3 个资产的规格：goblin-enemy、orc-enemy、treasure-chest

**输入：** `/asset-spec goblin-enemy orc-enemy treasure-chest`

**预期行为：**
1. 技能按顺序生成全部 3 个规格
2. 对每个资产，技能展示草稿并分别询问"May I write to
   `assets/specs/[名称]-spec.md`?"
3. 用户可以批准全部 3 个，或跳过个别资产
4. 所有已批准的规格均已写入；判决为 COMPLETE

**断言：**
- [ ] "May I write"被询问 3 次（每个资产各一次），而非一次性确认全部
- [ ] 用户可以拒绝某个资产而不阻塞其他资产
- [ ] 已批准的 3 个规格文件均已写入
- [ ] 所有已批准规格写入完成后判决为 COMPLETE

---

### 用例 5：Director 门控检查——无门控；asset-spec 是设计工具

**夹具：**
- GDD 和美术圣经存在

**输入：** `/asset-spec goblin-enemy`

**预期行为：**
1. 技能生成并写入资产规格
2. 未调用任何 director agent
3. 输出中无门控 ID

**断言：**
- [ ] 未调用 director 门控
- [ ] 输出中无门控跳过消息
- [ ] 技能在不经过任何门控检查的情况下达到 COMPLETE

---

## 协议合规

- [ ] 生成规格前读取 GDD、美术圣经和设计系统
- [ ] 包含所有 6 个规格组成部分（尺寸、动画、调色板、风格、技术、清单）
- [ ] 用 DEPENDENCY GAP 注释标记缺失的依赖项（美术圣经、GDD）
- [ ] 每个资产单独询问"May I write"（或"May I update"）
- [ ] 多资产时使用独立的写入确认处理
- [ ] 所有已批准规格写入完成后判决为 COMPLETE

---

## 覆盖说明

- 音频资产规格（音效、音乐）遵循相同结构，但字段不同（时长、采样率、循环），
  不单独测试。
- UI 资产规格（图标、按钮状态）遵循相同流程，交互状态需求与 UX 规格对齐。
- GDD 和美术圣经均缺失的情况（两者都不存在）不单独测试；规格会生成，
  同时标记两个依赖项差距。
