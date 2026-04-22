# Skill Test Spec: /team-polish

## Skill 概述

编排六阶段打磨流水线：1. 性能分析（performance-analyst）→ 2. 技术打磨（technical-artist）→
3. 视觉打磨（technical-artist）和 4. 音频打磨（sound-designer）并行（与阶段 2 并行）→
5. 回归测试（qa-tester）→ 6. 最终验证（performance-analyst + lead-programmer）。
仅当阶段 1 发现引擎层根本原因时才派生 engine-programmer。
裁决：READY FOR RELEASE / NEEDS MORE WORK。
下一步：`/release-checklist`、`/sprint-plan update`、`/gate-check`。

---

## 静态断言（结构性）

- [ ] 包含必要的 frontmatter 字段：`name`、`description`、`argument-hint`、`user-invocable`、`allowed-tools`
- [ ] 明确包含六个阶段
- [ ] 阶段 3 和阶段 4 与阶段 2 并行执行
- [ ] engine-programmer 仅在阶段 1 发现引擎层根本原因时才条件派生
- [ ] 包含裁决关键字：READY FOR RELEASE、NEEDS MORE WORK
- [ ] 存在文件写入协议；编排者不直接写入文件
- [ ] 子 agent 在任何写入之前强制执行"May I write to [path]?"
- [ ] 存在错误恢复协议
- [ ] 步骤过渡前使用 `AskUserQuestion`
- [ ] 末尾包含下一步交接：`/release-checklist`、`/sprint-plan update`、`/gate-check`

---

## 测试用例

### 用例 1：正常路径——所有阶段完成，裁决 READY FOR RELEASE

**测试夹具：**
- 功能已完成实现
- 性能在预算内（帧率 ≥ 60fps，内存使用 < 80% 预算）
- 无引擎层根本原因
- 音频和视觉无重大问题

**输入：** `/team-polish combat-system`

**预期行为：**
1. 上下文收集：读取性能预算、现有 bug 报告、QA 测试结果
2. 阶段 1：派生 performance-analyst 进行基线分析（帧时间、内存、GC 压力）
3. 阶段 1 报告无引擎层根本原因；engine-programmer 不被派生
4. `AskUserQuestion` 批准分析结果后进行阶段 2+3+4
5. 阶段 2、3、4 并行启动：
   - 阶段 2：technical-artist 处理技术打磨（LOD、遮挡剔除、着色器优化）
   - 阶段 3：technical-artist 处理视觉打磨（视觉特效、材质细节、动画优化）
   - 阶段 4：sound-designer 处理音频打磨（混音平衡、SFX 细节、音频性能）
6. `AskUserQuestion` 批准打磨结果后进行阶段 5
7. 阶段 5：派生 qa-tester 进行回归测试——验证打磨未引入新问题
8. `AskUserQuestion` 批准回归测试后进行阶段 6
9. 阶段 6：派生 performance-analyst 和 lead-programmer 进行最终验证
10. 所有指标在预算内；裁决：READY FOR RELEASE
11. 下一步：`/release-checklist`、`/sprint-plan update`、`/gate-check`

**断言：**
- [ ] 阶段 1 未发现引擎层根本原因时不派生 engine-programmer
- [ ] 阶段 2、3、4 的 Task 调用同时发出（并行）
- [ ] 每次阶段过渡前使用 `AskUserQuestion`
- [ ] 编排者不直接写入任何文件
- [ ] 裁决为 READY FOR RELEASE
- [ ] 下一步引用 `/release-checklist`、`/sprint-plan update`、`/gate-check`

---

### 用例 2：帧预算违规未解决——裁决 NEEDS MORE WORK

**测试夹具：**
- 阶段 1 分析：战斗场景高峰期帧率为 45fps（低于 60fps 目标）
- 阶段 2 技术打磨后帧率提升至 52fps——仍低于目标
- 阶段 6 最终验证：performance-analyst 确认帧率目标未达成

**输入：** `/team-polish battle-scene`

**预期行为：**
1. 阶段 1：performance-analyst 报告帧率问题（45fps，低于 60fps 目标）
2. 无引擎层根本原因（非引擎 bug，而是场景复杂度问题）
3. 阶段 2–4 打磨后有所改善但未达标
4. 阶段 6：performance-analyst 最终确认 52fps < 60fps 目标
5. lead-programmer 评估后确认需要更多工作（可能需要削减场景复杂度或优化批处理）
6. 裁决：NEEDS MORE WORK
7. 报告包含具体指标（当前 52fps vs 目标 60fps）和推荐的优化方向

**断言：**
- [ ] 具体性能指标（当前 vs 目标）包含在报告中
- [ ] 裁决为 NEEDS MORE WORK（非 READY FOR RELEASE）
- [ ] 报告包含推荐的下一步优化行动
- [ ] `AskUserQuestion` 在最终验证后呈现裁决和建议

---

### 用例 3：无参数——使用指导

**测试夹具：**
- 任何项目状态

**输入：** `/team-polish`（无参数）

**预期行为：**
1. Skill 检测到未提供功能/区域名称
2. 输出使用指导，包含正确调用格式和示例
3. 不派生任何 agent

**断言：**
- [ ] 无参数时不派生任何 agent
- [ ] 使用信息包含带参数示例的正确格式
- [ ] 不使用 `AskUserQuestion`

---

### 用例 4：引擎层瓶颈——条件派生 engine-programmer

**测试夹具：**
- 阶段 1 性能分析发现：GC 停顿每帧 > 2ms，分析显示根本原因是引擎的场景树更新算法中存在内存分配模式问题（引擎层问题，不是游戏代码问题）

**输入：** `/team-polish ui-system`

**预期行为：**
1. 阶段 1：performance-analyst 报告 GC 停顿问题，并明确标记为"引擎层根本原因"
2. 编排者检测到"引擎层根本原因"标记
3. engine-programmer 被条件派生，与阶段 2+3+4 并行工作
4. engine-programmer 处理引擎层 GC 压力问题
5. 报告中明确说明 engine-programmer 是因引擎层根本原因而派生的
6. 所有阶段完成后进行回归测试和最终验证

**断言：**
- [ ] engine-programmer 仅在阶段 1 明确标记"引擎层根本原因"时才被派生
- [ ] engine-programmer 的派生与阶段 2+3+4 并行（不串行）
- [ ] 报告中说明派生 engine-programmer 的具体原因
- [ ] 无引擎层根本原因时，engine-programmer 不被派生（用例 1 已验证）

---

### 用例 5：阶段 5 发现回归——打磨引入新问题

**测试夹具：**
- 阶段 2–4 打磨已完成
- 阶段 5 回归测试：qa-tester 发现视觉打磨引入了新的玩家角色着色器问题——特定光照条件下角色变成全黑

**输入：** `/team-polish player-character`（阶段 5 场景）

**预期行为：**
1. 阶段 5：qa-tester 运行回归测试套件
2. 发现新回归：特定光照下角色全黑——在打磨之前不存在此问题
3. qa-tester 提交 bug 报告：`production/qa/bugs/BUG-[NNN]-player-shader-black.md`
4. 编排者显示回归发现，`AskUserQuestion` 呈现选项：
   - 立即修复着色器问题（由 technical-artist 处理）然后重新进行回归测试
   - 继续进行阶段 6 验证，将此 bug 标记为阻塞发布的已知问题
5. 裁决不能在未解决回归的情况下为 READY FOR RELEASE

**断言：**
- [ ] 回归问题在 bug 报告文件中记录
- [ ] bug 报告路径遵循 `production/qa/bugs/BUG-[NNN]-[slug].md` 模式
- [ ] `AskUserQuestion` 提供修复后重测或继续并标记为已知问题的选项
- [ ] 裁决在回归未解决时不为 READY FOR RELEASE

---

## 协议合规性

- [ ] 上下文收集（性能预算、现有 bug、QA 结果）在派生任何 agent 之前运行
- [ ] engine-programmer 仅在阶段 1 发现引擎层根本原因时条件派生
- [ ] 阶段 2、3、4 并行执行——Task 调用同时发出
- [ ] 每次阶段过渡前使用 `AskUserQuestion`
- [ ] 编排者不直接写入任何文件
- [ ] 子 agent 在任何写入之前强制执行"May I write to [path]?"
- [ ] 回归问题导致 NEEDS MORE WORK，不被静默忽略
- [ ] 裁决恰好为 READY FOR RELEASE 或 NEEDS MORE WORK
- [ ] 末尾包含下一步交接：`/release-checklist`、`/sprint-plan update`、`/gate-check`

---

## 覆盖率说明

- 当 technical-artist 同时参与阶段 2（技术打磨）和阶段 3（视觉打磨）时——
  同一 agent 类型在并行阶段被派生两次，其调度行为未独立测试。
- 性能预算文件的位置和格式（存储在何处？如何读取？）未在此
  spec 中独立断言。
