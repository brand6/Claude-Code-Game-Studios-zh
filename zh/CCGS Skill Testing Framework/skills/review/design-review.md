# Skill 测试规范：/design-review

## Skill 摘要

`/design-review design/gdd/[system].md` 对游戏设计文档（GDD）进行评估，检查其是否符合 8 节标准：概述、游戏支柱对齐、机制规范、公式与数值、验收标准、依赖关系、引擎注意事项和未解决问题。Skill 为只读操作（`context: fork`），评估文档的完整性、内部一致性和可实现性。

Verdict 为：APPROVED、NEEDS REVISION、MAJOR REVISION NEEDED。无 Director 门控——此 Skill 本身就是评审，不委派给 Director 代理。

---

## 静态断言（结构性）

由 `/skill-test static` 自动验证——无需 Fixture。

- [ ] 包含必填 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 包含 ≥2 个阶段标题
- [ ] 包含 verdict 关键词：APPROVED、NEEDS REVISION、MAJOR REVISION NEEDED
- [ ] 不包含"May I write"语言（只读 Skill）
- [ ] 末尾包含适合对应 verdict 的下一步交接
- [ ] 说明无 Director 门控（不读取 review-mode.txt）

---

## Director 门控检查

无 Director 门控——该 Skill 无论审核模式如何均不生成任何 Director 门控代理。该 Skill 本身就是设计评审；不将评审委派给 Director。

---

## 测试用例

### 用例 1：正常路径——完整 GDD，全部 8 个章节

**Fixture：**
- `design/gdd/[system].md` 存在，包含所有 8 个必需章节
- 机制规范引用了核心游戏支柱
- 所有验收标准均具体、可测试

**输入：** `/design-review design/gdd/[system].md`

**预期行为：**
1. Skill 读取 GDD 并检查所有 8 个章节
2. 验证内部一致性（无相互矛盾的规则）
3. 验证可实现性（机制已完整定义）
4. 输出包含完整性、内部一致性、可实现性章节
5. Verdict 为 APPROVED

**断言：**
- [ ] Verdict 为 APPROVED
- [ ] 输出包含完整性评估（8/8 章节）
- [ ] 输出包含内部一致性评估
- [ ] 输出包含可实现性评估
- [ ] 不写入任何文件

---

### 用例 2：失败路径——不完整 GDD（8 节中缺少 4 节）

**Fixture：**
- `design/gdd/[system].md` 存在，只有 4 个必需章节

**输入：** `/design-review design/gdd/[system].md`

**预期行为：**
1. Skill 读取 GDD 并检查章节完整性
2. 检测到 4 个缺少的章节
3. 按名称列出每个缺少的章节
4. Verdict 为 MAJOR REVISION NEEDED

**断言：**
- [ ] Verdict 为 MAJOR REVISION NEEDED（不是 APPROVED 或 NEEDS REVISION）
- [ ] 缺少的章节均在输出中按名称列出
- [ ] 输出提供明确的修复指导

---

### 用例 3：部分失败——7/8 个章节，有内部不一致

**Fixture：**
- `design/gdd/[system].md` 存在，包含 7 个章节（缺少公式章节）
- 一个现有章节中验收标准措辞模糊（"系统应该感觉正确"）

**输入：** `/design-review design/gdd/[system].md`

**预期行为：**
1. Skill 读取 GDD，注意到缺少公式章节
2. Skill 标记不明确的验收标准作为可实现性问题
3. Verdict 为 NEEDS REVISION（不是 MAJOR REVISION NEEDED，仅缺少 1 节）
4. 每个标记的问题均有具体、可操作的修复建议

**断言：**
- [ ] Verdict 为 NEEDS REVISION（不是 APPROVED 或 MAJOR REVISION NEEDED），7/8 且有问题
- [ ] 输出中具体标注缺少公式章节
- [ ] 输出将模糊的验收标准标记为可实现性缺口
- [ ] 每个标记的问题均有具体、可操作的修复建议

---

### 用例 4：边缘情况——文件未找到

**Fixture：**
- 提供的路径在项目中不存在

**输入：** `/design-review design/gdd/nonexistent.md`

**预期行为：**
1. Skill 尝试读取该文件
2. 文件未找到
3. Skill 输出错误消息，指出缺少的文件名
4. Skill 建议检查路径或列出 `design/gdd/` 中的文件
5. Skill 不生成 verdict

**断言：**
- [ ] 文件未找到时 Skill 输出明确错误
- [ ] 文件缺少时 Skill 不输出 APPROVED、NEEDS REVISION 或 MAJOR REVISION NEEDED
- [ ] Skill 建议纠正措施（检查路径、列出可用 GDD）

---

### 用例 5：Director 门控——无论审核模式如何均不生成门控

**Fixture：**
- `design/gdd/[system].md` 存在，包含全部 8 个章节
- `production/session-state/review-mode.txt` 存在，内容为 `full`

**输入：** `/design-review design/gdd/[system].md`（full 审核模式活跃）

**预期行为：**
1. Skill 读取 GDD 文档
2. Skill 不读取 `review-mode.txt`——此 Skill 无 Director 门控
3. Skill 正常生成评审输出
4. 全程不生成任何 Director 门控代理
5. Verdict 为 APPROVED（Fixture 中 8 个章节均存在）

**断言：**
- [ ] Skill 不生成任何 Director 门控代理（无 CD-、TD-、PR-、AD- 前缀的代理）
- [ ] Skill 不读取 `review-mode.txt` 或等效模式文件
- [ ] `--review` 标志或 `full` 模式状态对是否生成 Director 门控无影响
- [ ] 输出不包含任何"Gate: [GATE-ID]"条目
- [ ] Skill 本身就是评审——不将评审委派给 Director

---

## 协议合规

- [ ] 不使用 Write 或 Edit 工具（只读 Skill）
- [ ] 发布 verdict 前展示完整结论
- [ ] 不请求批准（无文件写入需要批准）
- [ ] 末尾包含推荐的下一步（例如修复问题后重新运行，或进入 `/map-systems`）

---

## 覆盖率说明

- 跨系统一致性检查（技能自身阶段列表中的用例 3）未在此直接测试，
  因为它需要多个 GDD 文件进行比较；该测试由 `/review-all-gdds` 规范覆盖。
- 技能的 `context: fork` 行为（作为子 agent 运行）未在规范级别测试——这是需要手动验证的运行时行为。
- 非常大的 GDD 文件的性能和边界情况不在测试范围内。
