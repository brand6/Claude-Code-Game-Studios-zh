---
paths:
  - "src/core/**"
---

# 引擎代码规则

- 热路径（更新循环、渲染、物理）中零内存分配——预分配、对象池、重复利用
- 所有引擎 API 必须线程安全，或明确标注为仅限单线程使用
- 每次优化前后均需性能剖析——记录实测数据
- 引擎代码绝不得依赖玩法代码（严格依赖方向：引擎 ← 玩法）
- 每个公开 API 必须在文档注释中提供使用示例
- 修改公开接口须经历废弃期，并提供迁移指南
- 所有资源使用 RAII / 确定性清理
- 所有引擎系统必须支持优雅降级
- 编写引擎 API 代码前，须查阅 `docs/engine-reference/` 中对应的引擎版本文档，并核对 API 与参考文档的一致性

## 示例

**正确**（零分配热路径）：

```gdscript
# 预分配数组，每帧复用
var _nearby_cache: Array[Node3D] = []

func _physics_process(delta: float) -> void:
    _nearby_cache.clear()  # 复用，不重新分配
    _spatial_grid.query_radius(position, radius, _nearby_cache)
```

**错误**（热路径中分配内存）：

```gdscript
func _physics_process(delta: float) -> void:
    var nearby: Array[Node3D] = []  # 违规：每帧分配内存
    nearby = get_tree().get_nodes_in_group("enemies")  # 违规：每帧遍历场景树
```
