# Hook：pre-commit-design-check

## 触发条件

在任何修改 `design/` 或 `assets/data/` 目录中文件的提交之前运行。

## 用途

在设计文档进入版本控制前强制执行设计文档规范。确保 GDD 包含所有必需章节，并验证数据文件的 JSON 格式正确。

## 实现

```bash
#!/bin/bash
# Pre-commit hook：设计文档检查

DESIGN_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '^design/')
DATA_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '^assets/data/')

EXIT_CODE=0

# 检查 GDD 是否包含必需章节
for file in $DESIGN_FILES; do
    if [[ "$file" == *.md ]]; then
        MISSING_SECTIONS=""

        if ! grep -q "## Overview" "$file"; then
            MISSING_SECTIONS="$MISSING_SECTIONS Overview"
        fi
        if ! grep -q "## Detailed Design" "$file"; then
            MISSING_SECTIONS="$MISSING_SECTIONS 'Detailed Design'"
        fi
        if ! grep -q "## Edge Cases" "$file"; then
            MISSING_SECTIONS="$MISSING_SECTIONS 'Edge Cases'"
        fi
        if ! grep -q "## Dependencies" "$file"; then
            MISSING_SECTIONS="$MISSING_SECTIONS Dependencies"
        fi
        if ! grep -q "## Acceptance Criteria" "$file"; then
            MISSING_SECTIONS="$MISSING_SECTIONS 'Acceptance Criteria'"
        fi

        if [ -n "$MISSING_SECTIONS" ]; then
            echo "FAIL: $file missing required sections:$MISSING_SECTIONS"
            EXIT_CODE=1
        fi
    fi
done

# 验证数据文件的 JSON 合法性
for file in $DATA_FILES; do
    if [[ "$file" == *.json ]]; then
        if ! python3 -c "import json,sys; json.load(open('$file'))" 2>/dev/null; then
            echo "FAIL: $file contains invalid JSON"
            EXIT_CODE=1
        fi
    fi
done

exit $EXIT_CODE
```

## Agent 集成

当此 Hook 失败时：
1. GDD 缺少章节：调用 `game-designer` 补全文档
2. JSON 格式错误：调用 `tools-programmer` 修复语法
