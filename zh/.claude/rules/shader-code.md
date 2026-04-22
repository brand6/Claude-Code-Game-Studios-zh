---
paths:
  - "assets/shaders/**"
---

# Shader 代码标准

`assets/shaders/` 中的所有 Shader 文件必须遵循以下标准，以维持视觉质量、性能和跨平台兼容性。

## 命名规范
- 文件命名：`[类型]_[分类]_[名称].[扩展名]`
  - `spatial_env_water.gdshader`（Godot）
  - `SG_Env_Water`（Unity Shader Graph）
  - `M_Env_Water`（Unreal Material）
- 使用能体现材质用途的描述性名称
- 以 Shader 类型作为前缀：`spatial_`、`canvas_`、`particles_`、`post_`

## 代码质量
- 所有 uniform/参数必须有描述性名称和适当的提示信息
- 对相关参数进行分组（Godot：`group_uniforms`；Unity：`[Header]`；Unreal：Category）
- 对不显而易见的计算添加注释（尤其是数学密集型部分）
- 不使用魔法数字——使用具名常量或已记录的 uniform 值
- 每个 Shader 文件顶部须包含作者和用途注释

## 性能要求
- 记录每个 Shader 的目标平台和复杂度预算
- 使用合适的精度：移动端在不需要全精度时使用 `half`/`mediump`
- 在 Fragment Shader 中尽量减少纹理采样次数
- 避免在 Fragment Shader 中使用动态分支——改用 `step()`、`mix()`、`smoothstep()`
- 循环内不得进行纹理读取
- 模糊效果采用两遍方案（水平 → 垂直）

## 跨平台
- 在最低配置目标硬件上测试 Shader
- 为低质量档位提供降级/简化版本
- 说明 Shader 面向的渲染管线（Forward/Deferred、URP/HDRP、Forward+/Mobile/Compatibility）
- 同一目录不得混用来自不同渲染管线的 Shader

## 变体管理
- 尽量减少 Shader 变体——每个变体都是独立编译的 Shader
- 记录所有关键字/变体及其用途
- 尽可能使用功能剥离以减小构建体积
- 记录并监控每个 Shader 的变体总数
