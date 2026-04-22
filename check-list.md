# Translation Quality Checklist

## Automated Validation

### Translation Completeness Validator

Run the automated translation validation tool before committing zh translations:

```bash
python auto/validate_translation.py
```

This checks:
- Missing translation files
- Frontmatter consistency (keys, protected values)
- Slash commands presence
- Heading count mismatches
- Code fence completeness
- Broken relative links
- Truncation detection

See `auto/README.md` for detailed usage and configuration options.

### Strict Mode (for CI/CD)

Use strict mode to treat warnings as errors:

```bash
python auto/validate_translation.py --strict
```

## Manual Review

Before marking a translation as complete:

1. ✅ All source files have corresponding zh files
2. ✅ Frontmatter keys match source (protected values unchanged)
3. ✅ All /slash-commands preserved
4. ✅ Level-2 headings complete (no truncation)
5. ✅ Code blocks properly closed
6. ✅ Relative links point to valid files
7. ✅ Technical terms use GLOSSARY.md consistently

## Reports

Validation reports are generated in `auto/reports/`:
- `validation_report.md` - Human-readable summary
- `validation_report.json` - Machine-readable details
