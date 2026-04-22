# Agent 测试规格：unity-addressables-specialist

## Agent 概述
职责领域：Addressable 资源系统——分组管理、异步加载/卸载、句柄生命周期管理、内存预算、内容目录，以及远程内容分发。
不负责：渲染系统（engine-programmer）、使用已加载资源的游戏逻辑（gameplay-programmer）。
模型层级：Sonnet（默认）。
未分配关卡 ID。

---

## 静态断言（结构检查）

- [ ] `description:` 字段存在且领域明确（引用 Addressables / 资源加载 / 内容目录 / 远程分发）
- [ ] `allowed-tools:` 列表包含 Read、Write、Edit、Bash、Glob、Grep
- [ ] 模型层级为 Sonnet（专员的默认层级）
- [ ] Agent 定义未主张对渲染系统或使用已加载资源的游戏玩法拥有权

---

## 测试用例

### 用例 1：领域内请求——合适的输出
**输入**："异步加载一个角色纹理，并在角色销毁时释放它。"
**预期行为**：
- 产出 `Addressables.LoadAssetAsync<Texture2D>()` 调用模式
- 将返回的 `AsyncOperationHandle<Texture2D>` 存储在请求对象中
- 在角色销毁时（`OnDestroy()`），使用存储的句柄调用 `Addressables.Release(handle)`
- 不使用 `Resources.Load()` 作为加载机制
- 注明用空值或未初始化句柄调用 Release 会导致错误——包含有效性检查
- 注明释放句柄与释放资源的区别（释放句柄是正确做法）

### 用例 2：领域外重定向
**输入**："实现将加载的纹理应用到角色网格的渲染系统。"
**预期行为**：
- 不产出渲染或网格材质赋值代码
- 明确声明渲染系统实现属于 `engine-programmer` 的职责范围
- 将请求重定向给 `engine-programmer`
- 可描述将提供的资源类型和 API 接口（如句柄完成后的 `Texture2D` 引用）作为交接规格

### 用例 3：内存泄漏——未释放的句柄
**输入**："每次关卡加载后内存占用持续攀升。我们使用 Addressables 加载关卡资源。"
**预期行为**：
- 诊断可能原因：`AsyncOperationHandle` 对象在使用后未被释放
- 识别句柄泄漏模式：将资源加载到局部变量，丢失引用，从不调用 `Addressables.Release()`
- 提出审计方案：搜索所有 `LoadAssetAsync` / `LoadSceneAsync` 调用，验证是否有对应的 `Release()` 调用
- 提供修正模式：使用跟踪句柄列表（`List<AsyncOperationHandle>`）和 `ReleaseAll()` 清理方法
- 在没有证据的情况下，不假设泄漏发生在其他位置

### 用例 4：远程内容分发——目录版本管理
**输入**："我们需要支持可下载的内容更新，而不要求完整的应用重装。"
**预期行为**：
- 产出远程目录更新模式：
  - 启动时调用 `Addressables.CheckForCatalogUpdates()`
  - 检测到更新后调用 `Addressables.UpdateCatalogs()`
  - 使用 `Addressables.DownloadDependenciesAsync()` 预热更新内容
- 注明用于变更检测的目录哈希校验
- 处理边缘用例：玩家开始游戏会话后目录在会话中途更新——定义行为（使用旧目录完成当前会话，下次启动时重新加载）
- 不设计服务端 CDN 基础设施（委托给 devops-engineer）

### 用例 5：上下文传递——平台内存约束
**输入**：平台上下文：目标平台为 Nintendo Switch，4GB RAM，实际资源内存上限 512MB。请求："为大型开放世界关卡设计 Addressables 加载策略。"
**预期行为**：
- 在设计依据中明确引用 512MB 内存上限
- 设计流式加载策略：
  - 将世界划分为可寻址区域，根据玩家距离加载/卸载
  - 定义每个活跃区域的内存预算（如每区 128MB，最多 4 个区同时活跃）
  - 指定异步预加载触发距离和卸载距离（滞后区间）
- 注明 Switch 专属约束：SD 卡加载时间较慢，建议预热相邻区域
- 不产出会超过所述 512MB 上限的加载策略（若超出须明确标记）

---

## 协议合规性

- [ ] 保持在声明的职责范围内（Addressables 加载、句柄生命周期、内存、目录、远程分发）
- [ ] 将渲染和使用资源的游戏玩法代码重定向给 engine-programmer 和 gameplay-programmer
- [ ] 返回结构化输出（加载模式、句柄生命周期代码、流式区域设计）
- [ ] 始终将 `LoadAssetAsync` 与对应的 `Release()` 配对——将句柄泄漏标记为内存 bug
- [ ] 根据提供的内存上限设计加载策略
- [ ] 不设计 CDN/服务器基础设施——将服务端交委托给 devops-engineer

---

## 覆盖说明
- 句柄生命周期（用例 1）必须包含验证释放后内存被回收的测试
- 句柄泄漏诊断（用例 3）应产出适合作为 bug 工单的发现报告
- 平台内存用例（用例 5）验证 Agent 应用了上下文中的硬性约束，而非默认假设
