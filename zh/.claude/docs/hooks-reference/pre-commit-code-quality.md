# Hook：pre-commit-code-quality

## 触发条件

在任何修改 `src/` 目录中文件的提交之前运行。

## 用途

在代码进入版本控制前强制执行编码规范。捕获风格违规、缺失文档、方法过于复杂，以及应由数据驱动的硬编码数值。

## 实现

```bash
#!/bin/bash
# Pre-commit hook：代码质量检查
# 请根据你的语言和工具链调整具体检查项

CODE_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '^src/')

EXIT_CODE=0

if [ -n "$CODE_FILES" ]; then
    for file in $CODE_FILES; do
        # 检查游戏代码中的硬编码魔法数字
        if [[ "$file" == src/gameplay/* ]]; then
            # 查找可能是平衡数值的数字字面量
            # 请根据你的语言调整匹配模式
            if grep -nE '(damage|health|speed|rate|chance|cost|duration)[[:space:]]*[:=][[:space:]]*[0-9]+' "$file"; then
                echo "WARNING: $file may contain hardcoded gameplay values. Use data files."
                # 仅警告，不阻断
            fi
        fi

        # 检查没有指定负责人的 TODO/FIXME
        if grep -nE '(TODO|FIXME|HACK)[^(]' "$file"; then
            echo "WARNING: $file has TODO/FIXME without owner tag. Use TODO(name) format."
        fi

        # 运行语言专用 linter（取消注释对应行）
        # GDScript：gdlint "$file" || EXIT_CODE=1
        # C#：dotnet format --check "$file" || EXIT_CODE=1
        # C++：clang-format --dry-run -Werror "$file" || EXIT_CODE=1
    done

    # 对修改的系统运行单元测试
    # 请取消注释并根据你的测试框架调整
    # python -m pytest tests/unit/ -x --quiet || EXIT_CODE=1
fi

exit $EXIT_CODE
```

## Agent 集成

当此 Hook 失败时：
1. 风格违规：用格式化工具自动修复，或调用 `lead-programmer`
2. 硬编码数值：调用 `gameplay-programmer` 将数值外部化
3. 测试失败：调用 `qa-tester` 诊断，调用 `gameplay-programmer` 或相关程序员修复
