---
paths:
  - "src/gameplay/**"
---

# 玩法代码规则

- 所有玩法数值必须来自外部配置/数据文件，绝不硬编码
- 所有与时间相关的计算必须使用 delta time（帧率无关性）
- 禁止直接引用 UI 代码——跨系统通信使用事件/信号
- 每个玩法系统必须实现清晰的接口
- 状态机必须具有显式转换表，并对所有状态进行文档说明
- 为所有玩法逻辑编写单元测试——将逻辑与表现层分离
- 在代码注释中记录每个功能对应实现的设计文档
- 游戏状态不使用静态单例——采用依赖注入

## 示例

**正确**（数据驱动）：

```gdscript
var damage: float = config.get_value("combat", "base_damage", 10.0)
var speed: float = stats_resource.movement_speed * delta
```

**错误**（硬编码）：

```gdscript
var damage: float = 25.0   # 违规：硬编码玩法数值
var speed: float = 5.0      # 违规：非配置来源，未使用 delta
```
