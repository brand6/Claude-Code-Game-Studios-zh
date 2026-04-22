---
paths:
  - "tests/**"
---

# 测试标准

- 测试命名：遵循 `test_[系统]_[场景]_[预期结果]` 模式
- 每个测试必须具有清晰的 排列（Arrange）/ 执行（Act）/ 断言（Assert）结构
- 单元测试不得依赖外部状态（文件系统、网络、数据库）
- 集成测试必须在执行后进行清理
- 性能测试必须指定可接受的阈值，并在超出时失败
- 测试数据必须在测试内部或专用固件（fixtures）中定义，禁止使用共享可变状态
- 模拟外部依赖——测试应快速且具有确定性
- 每次 Bug 修复必须附有能捕获原始 Bug 的回归测试

## 示例

**正确**（正确命名 + 排列/执行/断言）：

```gdscript
func test_health_system_take_damage_reduces_health() -> void:
    # 排列
    var health := HealthComponent.new()
    health.max_health = 100
    health.current_health = 100

    # 执行
    health.take_damage(25)

    # 断言
    assert_eq(health.current_health, 75)
```

**错误**：

```gdscript
func test1() -> void:  # 违规：无描述性名称
    var h := HealthComponent.new()
    h.take_damage(25)  # 违规：无排列步骤，无明确断言
    assert_true(h.current_health < 100)  # 违规：断言不精确
```
