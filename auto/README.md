# Automation Scripts

This directory contains automation scripts and tools for the Claude Code Game Studios project.

## Translation Validation

### validate_translation.py

Validates the completeness and correctness of Chinese (zh) translations against source files.

**Usage:**

```bash
# Run validation (default mode: errors cause non-zero exit, warnings don't)
python auto/validate_translation.py

# Strict mode: warnings also cause non-zero exit
python auto/validate_translation.py --strict

# Custom config location
python auto/validate_translation.py --config path/to/config.json

# Custom repository root
python auto/validate_translation.py --repo-root /path/to/repo
```

**What it checks:**

- Missing translation files
- Unexpected zh-only files (with whitelist support)
- Frontmatter consistency (keys, protected values)
- Slash commands (/command) presence
- Heading count mismatches (level-2 headings)
- Code fence completeness (``` markers)
- Relative link validity
- Truncation detection (heuristic-based)
- YAML key stability

**Output:**

- Terminal summary with error/warning counts and category breakdown
- Markdown report: `auto/reports/validation_report.md`
- JSON report: `auto/reports/validation_report.json`

**Configuration:**

Edit `auto/translation_validation_config.json` to customize:
- Path patterns to scan
- Frontmatter rules per file type
- Severity levels per check type
- Truncation thresholds
- zh-only file whitelist

**Exit codes:**

- `0`: Success (no errors, or warnings only in non-strict mode)
- `1`: Validation failed (errors found, or warnings in strict mode)

**Integration:**

This tool can be integrated into CI/CD pipelines or pre-commit hooks to ensure translation quality before merging.

## Reports

Validation reports are written to `auto/reports/` (gitignored by default).
