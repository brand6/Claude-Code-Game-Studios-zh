# Hook：post-merge-asset-validation

## 触发条件

在任何合并到 `develop` 或 `main` 分支且包含 `assets/` 目录变更后运行。

## 用途

验证合并分支中的所有资产是否符合命名规范、大小预算和格式要求，防止不合规资产在集成分支上积累。

## 实现

```bash
#!/bin/bash
# Post-merge hook：资产验证
# 检查已合并的资产是否符合项目标准

MERGED_ASSETS=$(git diff --name-only HEAD@{1} HEAD | grep -E '^assets/')

if [ -z "$MERGED_ASSETS" ]; then
    exit 0
fi

EXIT_CODE=0
WARNINGS=""

for file in $MERGED_ASSETS; do
    filename=$(basename "$file")

    # 检查命名规范（小写字母加下划线）
    if echo "$filename" | grep -qE '[A-Z[:space:]-]'; then
        WARNINGS="$WARNINGS\nNAMING: $file -- must be lowercase with underscores"
        EXIT_CODE=1
    fi

    # 检查纹理尺寸（必须为 2 的幂次方）
    if [[ "$file" == *.png || "$file" == *.jpg ]]; then
        # 需要 ImageMagick
        if command -v identify &> /dev/null; then
            dims=$(identify -format "%w %h" "$file" 2>/dev/null)
            if [ -n "$dims" ]; then
                w=$(echo "$dims" | cut -d' ' -f1)
                h=$(echo "$dims" | cut -d' ' -f2)
                if (( (w & (w-1)) != 0 || (h & (h-1)) != 0 )); then
                    WARNINGS="$WARNINGS\nSIZE: $file -- dimensions ${w}x${h} not power-of-2"
                fi
            fi
        fi
    fi

    # 检查文件大小预算
    size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
    if [ -n "$size" ]; then
        # 纹理：最大 4MB
        if [[ "$file" == assets/art/* ]] && [ "$size" -gt 4194304 ]; then
            WARNINGS="$WARNINGS\nBUDGET: $file -- ${size} bytes exceeds 4MB texture budget"
            EXIT_CODE=1
        fi
        # 音频：音乐最大 10MB，音效最大 512KB
        if [[ "$file" == assets/audio/sfx* ]] && [ "$size" -gt 524288 ]; then
            WARNINGS="$WARNINGS\nBUDGET: $file -- ${size} bytes exceeds 512KB SFX budget"
        fi
    fi
done

if [ -n "$WARNINGS" ]; then
    echo "=== Asset Validation Report ==="
    echo -e "$WARNINGS"
    echo "================================"
    echo "Run /asset-audit for a full report."
fi

exit $EXIT_CODE
```

## Agent 集成

当此 Hook 报告问题时：
1. 命名规范违规：手动修复，或调用 `art-director` 获取指导
2. 大小超限：调用 `technical-artist` 获取优化建议
3. 需要全面审查：运行 `/asset-audit` 技能
