---
paths:
  - "assets/data/**"
---

# 数据文件规则

- 所有 JSON 文件必须是合法 JSON——格式损坏的 JSON 将阻断整个构建流水线
- 文件命名：仅使用小写字母和下划线，遵循 `[系统]_[名称].json` 模式
- 每个数据文件必须有已记录的 Schema（JSON Schema 或对应设计文档中的说明）
- 数值必须附有注释或配套文档，说明各数值的含义
- 使用统一的键命名规范：JSON 文件内的键使用驼峰命名（camelCase）
- 不得存在孤立数据条目——每个条目必须被代码或其他数据文件引用
- 进行破坏性 Schema 变更时，须为数据文件添加版本号
- 所有可选字段必须包含合理的默认值

## 示例

**正确** 命名和结构（`combat_enemies.json`）：

```json
{
  "goblin": {
    "baseHealth": 50,
    "baseDamage": 8,
    "moveSpeed": 3.5,
    "lootTable": "loot_goblin_common"
  },
  "goblin_chief": {
    "baseHealth": 150,
    "baseDamage": 20,
    "moveSpeed": 2.8,
    "lootTable": "loot_goblin_rare"
  }
}
```

**错误** （`EnemyData.json`）：

```json
{
  "Goblin": { "hp": 50 }
}
```

违规说明：文件名含大写、键名含大写、不符合 `[系统]_[名称]` 模式、缺少必填字段。
