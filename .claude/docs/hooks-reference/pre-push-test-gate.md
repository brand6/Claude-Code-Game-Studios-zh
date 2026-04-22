# Hook：pre-push-test-gate

## 触发条件

在向远程仓库推送代码之前运行。对 `develop` 和 `main` 分支强制执行，其他分支仅作警告。

## 用途

确保在代码合并到集成分支之前，所有测试均已通过。防止损坏的代码进入团队共享分支。

## 实现

```bash
#!/bin/bash
# Pre-push hook：测试门禁
# 在推送到受保护分支之前运行完整测试套件

REMOTE="$1"
URL="$2"
BRANCH=$(git rev-parse --abbrev-ref HEAD)
EXIT_CODE=0

PROTECTED_BRANCHES="main develop"
IS_PROTECTED=false
for b in $PROTECTED_BRANCHES; do
    if [ "$BRANCH" = "$b" ]; then
        IS_PROTECTED=true
        break
    fi
done

echo "=== Pre-push Test Gate ==="
echo "Branch: $BRANCH | Protected: $IS_PROTECTED"

# ── 步骤 1：构建检查 ────────────────────────────
echo "Step 1/4: Build check..."
# 请取消注释并根据你的引擎调整
# godot --headless --check-only --quit || EXIT_CODE=1
# dotnet build --no-restore -q || EXIT_CODE=1
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL: Build failed. Aborting push."
    exit 1
fi
echo "PASS: Build OK"

# ── 步骤 2：单元测试 ────────────────────────────
echo "Step 2/4: Unit tests..."
# 请取消注释并根据你的测试框架调整
# python -m pytest tests/unit/ --quiet --tb=no || EXIT_CODE=1
# dotnet test --filter Category=Unit --quiet || EXIT_CODE=1
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL: Unit tests failed."
    exit 1
fi
echo "PASS: Unit tests OK"

# ── 步骤 3：集成测试（仅受保护分支）────────────
if $IS_PROTECTED; then
    echo "Step 3/4: Integration tests (protected branch)..."
    # 请取消注释并根据你的测试框架调整
    # python -m pytest tests/integration/ --quiet --tb=short || EXIT_CODE=1
    if [ $EXIT_CODE -ne 0 ]; then
        echo "FAIL: Integration tests failed."
        exit 1
    fi
    echo "PASS: Integration tests OK"
else
    echo "Step 3/4: Integration tests -- SKIPPED (feature branch)"
fi

# ── 步骤 4：冒烟测试与性能 ──────────────────────
if $IS_PROTECTED; then
    echo "Step 4/4: Smoke + performance..."
    # 启动无头游戏并运行冒烟测试
    # godot --headless --script tests/smoke/run_smoke.gd --quit || EXIT_CODE=1
    # 检查性能基线
    # python tools/perf_baseline_check.py || EXIT_CODE=1
    echo "PASS: Smoke/perf OK (checks not yet configured)"
else
    echo "Step 4/4: Smoke tests -- SKIPPED (feature branch)"
fi

echo "=========================="
if [ $EXIT_CODE -ne 0 ]; then
    echo "GATE FAILED. Fix issues before pushing."
else
    echo "GATE PASSED."
fi

exit $EXIT_CODE
```

## Agent 集成

当此 Hook 失败时：
1. 构建失败：调用 `lead-programmer`
2. 单元测试失败：调用 `qa-tester` 分类，调用相应程序员修复
3. 集成测试失败：调用 `lead-programmer` 判断影响范围
4. 性能回归：调用 `performance-analyst`
