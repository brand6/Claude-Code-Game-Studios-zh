# Agent 测试规格：unity-shader-specialist

## Agent 概述
职责领域：Unity Shader Graph、自定义 HLSL、VFX Graph、URP/HDRP 渲染管线定制，以及后处理效果。
不负责：游戏玩法代码、美术风格方向。
模型层级：Sonnet（默认）。
未分配关卡 ID。

---

## 静态断言（结构检查）

- [ ] `description:` 字段存在且领域明确（引用 Shader Graph / HLSL / VFX Graph / URP / HDRP）
- [ ] `allowed-tools:` 列表包含 Read、Write、Edit、Glob、Grep
- [ ] 模型层级为 Sonnet（专员的默认层级）
- [ ] Agent 定义未主张对游戏玩法代码或美术方向拥有权

---

## 测试用例

### 用例 1：领域内请求——合适的输出
**输入**："在 URP 中使用 Shader Graph 为角色创建描边效果。"
**预期行为**：
- 产出 Shader Graph 节点设置描述：
  - 反转法线外壳法：缩放法线 → 顶点阶段的顶点偏移，Cull Front
  - 或使用深度/法线边缘检测的屏幕空间后处理描边
- 根据 URP 能力推荐合适方案（URP 兼容性用反转外壳法，HDRP 用后处理）
- 注明 URP 限制：不支持几何着色器（排除几何着色器描边方案）
- 不在未确认渲染管线的情况下产出 HDRP 专属节点

### 用例 2：领域外重定向
**输入**："用代码实现角色生命值条 UI。"
**预期行为**：
- 不产出 UI 实现代码
- 明确声明 UI 实现属于 `ui-programmer`（或 `unity-ui-specialist`）的职责范围
- 将请求适当重定向
- 可注明：基于着色器的生命值条填充效果（如溶解/渐变填充）若本身是着色器驱动的视觉效果，则在其职责范围内

### 用例 3：HDRP 自定义 Pass 描边
**输入**："我们使用 HDRP，想将描边效果作为后处理实现。"
**预期行为**：
- 产出 HDRP `CustomPassVolume` 模式：
  - 继承 `CustomPass` 的 C# 类
  - 使用 `CoreUtils.SetRenderTarget()` 和全屏 shader blit 的 `Execute()` 方法
  - 用于边缘检测的深度/法线缓冲采样
- 注明 CustomPass 需要 HDRP 包，不适用于 URP
- 在提供 HDRP 专属代码前确认项目使用 HDRP

### 用例 4：VFX Graph 性能——GPU 事件批处理
**输入**："爆炸 VFX Graph 每次事件生成 10000 个粒子，20 个同时爆炸导致 GPU 帧率尖刺。"
**预期行为**：
- 识别 GPU 粒子生成为主要性能消耗（20万个粒子同时生成）
- 提出 GPU 事件批处理：将生成事件分散到多帧，错开初始化
- 建议每个活跃爆炸设置粒子预算上限（如每次爆炸 3000 个，多余的排队等待）
- 注明 VFX Graph Event Batcher 模式和跨帧分发的 Output Event API
- 不改变游戏玩法事件系统——提出 VFX 侧的预算解决方案

### 用例 5：上下文传递——渲染管线（URP 或 HDRP）
**输入**：项目上下文：URP 渲染管线，Unity 2022.3。请求："添加景深后处理效果。"
**预期行为**：
- 使用 URP Volume 框架：`DepthOfField` Volume Override 组件
- 不使用 HDRP Volume 组件（如参数名不同的 HDRP `DepthOfField`）
- 注明 URP 专属的景深限制（如 vs HDRP 的焦外散景质量差异）
- 产出与 Unity 2022.3 URP 包版本兼容的 C# Volume Profile 设置代码

---

## 协议合规性

- [ ] 保持在声明的职责范围内（Shader Graph、HLSL、VFX Graph、URP/HDRP 定制）
- [ ] 将游戏玩法和 UI 代码重定向给相应的 Agent
- [ ] 返回结构化输出（节点图描述、HLSL 代码、CustomPass 模式）
- [ ] 区分 URP 和 HDRP 方案——绝不混用管线专属 API
- [ ] 在适用时标记几何着色器方案与 URP 不兼容
- [ ] 产出的 VFX 优化不改变游戏玩法行为

---

## 覆盖说明
- 描边效果（用例 1）应搭配 `production/qa/evidence/` 中的视觉截图测试
- HDRP CustomPass（用例 3）确认 Agent 产出正确的 Unity 模式，而非通用后处理方案
- 管线分离（用例 5）验证 Agent 在无上下文时不假设渲染管线类型
