#!/usr/bin/env python3
"""
Translation Validation Tool for zh translations
Validates that Chinese translations are complete and correct
"""

import argparse
import json
import sys
from pathlib import Path
from fnmatch import fnmatch
from typing import Dict, List, Set, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import re


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class Issue:
    file: str
    severity: Severity
    category: str
    message: str
    line: int = 0


@dataclass
class ValidationResult:
    total_source_files: int = 0
    total_zh_files: int = 0
    passed: int = 0
    warnings: int = 0
    errors: int = 0
    issues: List[Issue] = field(default_factory=list)


class TranslationValidator:
    def __init__(self, config_path: Path, repo_root: Path):
        self.repo_root = repo_root
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        
        self.source_base = repo_root / self.config['source_base']
        self.translation_base = repo_root / self.config['translation_base']
        self.result = ValidationResult()
        
    def run(self, strict: bool = False) -> int:
        """Run all validations. Returns exit code."""
        print("=" * 80)
        print("Translation Validation Report")
        print(f"Repository: {self.repo_root}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print("=" * 80)
        print()
        
        # Build file mappings
        source_files = self._collect_source_files()
        zh_files = self._collect_zh_files()
        
        self.result.total_source_files = len(source_files)
        self.result.total_zh_files = len(zh_files)
        
        # File-level checks
        self._check_missing_translations(source_files, zh_files)
        self._check_unexpected_zh_files(source_files, zh_files)
        
        # Content-level checks
        for src_path in source_files:
            zh_path = self.translation_base / src_path
            if zh_path.exists():
                self._validate_file_pair(src_path, zh_path)
        
        # Generate reports
        self._print_summary()
        self._generate_reports()
        
        # Determine exit code
        if self.result.errors > 0:
            return 1
        if strict and self.result.warnings > 0:
            return 1
        return 0
    
    def _collect_source_files(self) -> Set[Path]:
        """Collect all source files that should be translated."""
        source_files = set()
        
        for pattern_config in self.config['path_patterns']:
            pattern = pattern_config['pattern']
            for path in self.source_base.rglob('*'):
                if path.is_file():
                    rel_path = path.relative_to(self.source_base)
                    # Skip zh directory itself
                    if str(rel_path).startswith('zh'):
                        continue
                    if self._matches_pattern(str(rel_path), pattern):
                        source_files.add(rel_path)
        
        return source_files
    
    def _collect_zh_files(self) -> Set[Path]:
        """Collect all translated files in zh directory."""
        zh_files = set()
        
        if not self.translation_base.exists():
            return zh_files
        
        for path in self.translation_base.rglob('*'):
            if path.is_file():
                rel_path = path.relative_to(self.translation_base)
                zh_files.add(rel_path)
        
        return zh_files
    
    def _matches_pattern(self, path: str, pattern: str) -> bool:
        """Check if path matches glob pattern."""
        # Normalize path separators
        path = path.replace('\\', '/')
        pattern = pattern.replace('\\', '/')

        # Patterns without a path separator are treated as root-level only.
        if '/' not in pattern:
            return '/' not in path and fnmatch(path, pattern)

        # Treat '/**/' as matching zero or more directories so direct children
        # are included alongside deeper descendants.
        if '/**/' in pattern and fnmatch(path, pattern.replace('/**/', '/')):
            return True

        return fnmatch(path, pattern)
    
    def _check_missing_translations(self, source_files: Set[Path], zh_files: Set[Path]):
        """Check for missing translation files."""
        missing = source_files - zh_files
        severity_name = self.config['severity_levels'].get('missing_translation', 'error')
        severity = Severity(severity_name)
        
        for path in sorted(missing):
            self._add_issue(
                str(path),
                severity,
                "missing_translation",
                f"Translation file missing"
            )
    
    def _check_unexpected_zh_files(self, source_files: Set[Path], zh_files: Set[Path]):
        """Check for unexpected files in zh that don't have source."""
        unexpected = zh_files - source_files
        whitelist = self.config.get('zh_only_whitelist', [])
        severity_name = self.config['severity_levels'].get('unexpected_zh_file', 'warning')
        severity = Severity(severity_name)
        
        for path in sorted(unexpected):
            # Check whitelist
            zh_full_path = f"zh/{path}"
            is_whitelisted = False
            for pattern in whitelist:
                if self._matches_pattern(zh_full_path, pattern):
                    is_whitelisted = True
                    break
            
            if not is_whitelisted:
                self._add_issue(
                    str(path),
                    severity,
                    "unexpected_zh_file",
                    f"Translation exists but no source file found (not whitelisted)"
                )
    
    def _validate_file_pair(self, rel_path: Path, zh_path: Path):
        """Validate a source/translation file pair."""
        src_path = self.source_base / rel_path
        
        # Determine file type
        if rel_path.suffix == '.md':
            self._validate_markdown_pair(rel_path, src_path, zh_path)
        elif rel_path.suffix in ['.yml', '.yaml']:
            self._validate_yaml_pair(rel_path, src_path, zh_path)
    
    def _validate_markdown_pair(self, rel_path: Path, src_path: Path, zh_path: Path):
        """Validate a markdown file pair."""
        try:
            with open(src_path, 'r', encoding='utf-8') as f:
                src_content = f.read()
            with open(zh_path, 'r', encoding='utf-8') as f:
                zh_content = f.read()
        except Exception as e:
            self._add_issue(
                str(rel_path),
                Severity.ERROR,
                "read_error",
                f"Failed to read file: {e}"
            )
            return
        
        if self.config['markdown_checks']['frontmatter']:
            self._check_frontmatter(rel_path, src_content, zh_content)
        
        if self.config['markdown_checks']['slash_commands']:
            self._check_slash_commands(rel_path, src_content, zh_content)
        
        if self.config['markdown_checks']['heading_count']:
            self._check_heading_count(rel_path, src_content, zh_content)
        
        if self.config['markdown_checks']['code_fences']:
            self._check_code_fences(rel_path, zh_content)
        
        if self.config['markdown_checks']['relative_links']:
            self._check_relative_links(rel_path, zh_path, zh_content)
        
        if self.config['markdown_checks']['truncation_heuristics']:
            self._check_truncation(rel_path, src_content, zh_content)
    
    def _check_frontmatter(self, rel_path: Path, src_content: str, zh_content: str):
        """Check frontmatter consistency."""
        src_fm = self._extract_frontmatter(src_content)
        zh_fm = self._extract_frontmatter(zh_content)
        
        # Check if source has frontmatter
        if src_fm is None and zh_fm is not None:
            # ZH has frontmatter but source doesn't - probably OK
            return
        
        if src_fm is not None and zh_fm is None:
            self._add_issue(
                str(rel_path),
                Severity(self.config['severity_levels']['frontmatter_missing']),
                "frontmatter_missing",
                "Source has frontmatter but translation doesn't"
            )
            return
        
        if src_fm is None and zh_fm is None:
            return  # Neither has frontmatter
        
        # Check if frontmatter is properly closed
        if not self._is_frontmatter_closed(zh_content):
            self._add_issue(
                str(rel_path),
                Severity(self.config['severity_levels']['frontmatter_unclosed']),
                "frontmatter_unclosed",
                "Frontmatter closing delimiter (---) missing or malformed"
            )
            return
        
        # Check key consistency
        src_keys = set(src_fm.keys())
        zh_keys = set(zh_fm.keys())
        
        if src_keys != zh_keys:
            missing = src_keys - zh_keys
            extra = zh_keys - src_keys
            msg_parts = []
            if missing:
                msg_parts.append(f"missing keys: {', '.join(sorted(missing))}")
            if extra:
                msg_parts.append(f"extra keys: {', '.join(sorted(extra))}")
            
            self._add_issue(
                str(rel_path),
                Severity(self.config['severity_levels']['frontmatter_key_mismatch']),
                "frontmatter_key_mismatch",
                "Frontmatter keys don't match: " + "; ".join(msg_parts)
            )
        
        # Check protected values
        rule_type = self._determine_frontmatter_rule_type(rel_path)
        if rule_type and rule_type in self.config['frontmatter_rules']:
            rule = self.config['frontmatter_rules'][rule_type]
            for key in rule.get('protected_keys', []):
                if key in src_fm and key in zh_fm:
                    if src_fm[key] != zh_fm[key]:
                        self._add_issue(
                            str(rel_path),
                            Severity(self.config['severity_levels']['protected_value_changed']),
                            "protected_value_changed",
                            f"Protected frontmatter key '{key}' was modified: '{src_fm[key]}' -> '{zh_fm[key]}'"
                        )
    
    def _extract_frontmatter(self, content: str) -> Dict[str, Any] | None:
        """Extract YAML frontmatter from markdown content."""
        if not content.startswith('---\n'):
            return None

        lines = content.split('\n')
        if not lines or lines[0].strip() != '---':
            return None

        fm_dict = {}
        current_key = None
        current_value_lines: List[str] = []

        def commit_current_key():
            nonlocal current_key, current_value_lines
            if current_key is None:
                return
            fm_dict[current_key] = '\n'.join(current_value_lines).rstrip()
            current_key = None
            current_value_lines = []

        for line in lines[1:]:
            if line.strip() == '---':
                commit_current_key()
                return fm_dict if fm_dict else None

            # Ignore standalone comments inside frontmatter.
            if line.startswith('#'):
                continue

            # Continuation lines belong to the current key.
            if current_key is not None and (
                line.startswith((' ', '\t')) or
                line.startswith('- ')
            ):
                current_value_lines.append(line)
                continue

            match = re.match(r'^([A-Za-z0-9_-]+):(?:\s*(.*))?$', line)
            if match:
                commit_current_key()
                current_key = match.group(1)
                value = match.group(2) or ''
                current_value_lines = [value] if value else []
                continue

            if current_key is not None:
                current_value_lines.append(line)

        return None
    
    def _is_frontmatter_closed(self, content: str) -> bool:
        """Check if frontmatter has both opening and closing delimiters."""
        if not content.startswith('---\n'):
            return True  # No frontmatter
        
        lines = content.split('\n')
        delimiter_count = 0
        for line in lines:
            if line.strip() == '---':
                delimiter_count += 1
                if delimiter_count == 2:
                    return True
        
        return False
    
    def _determine_frontmatter_rule_type(self, rel_path: Path) -> str | None:
        """Determine which frontmatter rule applies to this file."""
        path_str = str(rel_path).replace('\\', '/')

        if path_str.startswith('.claude/agents/') or '/.claude/agents/' in path_str:
            return 'agent'
        if path_str.startswith('.claude/skills/') or '/.claude/skills/' in path_str:
            return 'skill'
        if path_str.startswith('.claude/rules/') or '/.claude/rules/' in path_str:
            return 'rules'
        if path_str.startswith('.github/') or '/.github/' in path_str:
            return 'github'
        
        return None
    
    def _check_slash_commands(self, rel_path: Path, src_content: str, zh_content: str):
        """Check that slash commands from source appear in translation."""
        command_pattern = r'(?<![A-Za-z0-9._-])/(?:[a-z][a-z0-9-]*)(?![A-Za-z0-9_/.-])'

        src_commands = set(re.findall(command_pattern, src_content))
        zh_commands = set(re.findall(command_pattern, zh_content))
        
        missing = src_commands - zh_commands
        if missing:
            self._add_issue(
                str(rel_path),
                Severity(self.config['severity_levels']['slash_command_missing']),
                "slash_command_missing",
                f"Slash commands missing in translation: {', '.join(sorted(missing))}"
            )
    
    def _check_heading_count(self, rel_path: Path, src_content: str, zh_content: str):
        """Check that translation has similar number of level-2 headings."""
        src_h2 = len(re.findall(r'^## ', src_content, re.MULTILINE))
        zh_h2 = len(re.findall(r'^## ', zh_content, re.MULTILINE))
        
        if zh_h2 < src_h2:
            self._add_issue(
                str(rel_path),
                Severity(self.config['severity_levels']['heading_count_mismatch']),
                "heading_count_mismatch",
                f"Translation has fewer level-2 headings ({zh_h2}) than source ({src_h2})"
            )
    
    def _check_code_fences(self, rel_path: Path, content: str):
        """Check that code fences are properly closed."""
        fence_pattern = r'^```'
        fences = re.findall(fence_pattern, content, re.MULTILINE)
        
        if len(fences) % 2 != 0:
            self._add_issue(
                str(rel_path),
                Severity(self.config['severity_levels']['code_fence_broken']),
                "code_fence_broken",
                f"Unclosed code fence detected (found {len(fences)} fence markers)"
            )
    
    def _check_relative_links(self, rel_path: Path, zh_path: Path, content: str):
        """Check that relative markdown links point to existing files."""
        # Find markdown links: [text](path)
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        
        for link_text, link_target in links:
            # Skip absolute URLs and anchors
            if link_target.startswith(('http://', 'https://', '#', 'mailto:', 'file:', 'vscode:')):
                continue

            # Skip placeholder-style links used in examples or templates.
            if any(token in link_target for token in ('[', ']', '{', '}')):
                continue
            
            # Remove anchor part
            target_path = link_target.split('#')[0]
            if not target_path:
                continue
            
            # Resolve relative to zh file location
            target_full = (zh_path.parent / target_path).resolve()
            
            if not target_full.exists():
                self._add_issue(
                    str(rel_path),
                    Severity(self.config['severity_levels']['broken_link']),
                    "broken_link",
                    f"Broken relative link: [{link_text}]({link_target})"
                )
    
    def _check_truncation(self, rel_path: Path, src_content: str, zh_content: str):
        """Check for signs of truncated translation."""
        src_lines = src_content.count('\n')
        zh_lines = zh_content.count('\n')
        
        src_h2 = len(re.findall(r'^## ', src_content, re.MULTILINE))
        zh_h2 = len(re.findall(r'^## ', zh_content, re.MULTILINE))
        
        thresholds = self.config['truncation_thresholds']
        
        # Check heading loss
        heading_loss = src_h2 - zh_h2
        if heading_loss >= thresholds['heading_loss_threshold']:
            # Check line ratio
            line_ratio = zh_lines / src_lines if src_lines > 0 else 1.0
            
            if line_ratio < thresholds['line_ratio_min']:
                self._add_issue(
                    str(rel_path),
                    Severity(self.config['severity_levels']['truncation_suspected']),
                    "truncation_suspected",
                    f"Translation appears truncated: {heading_loss} headings missing, "
                    f"line ratio {line_ratio:.2f} (src: {src_lines}, zh: {zh_lines})"
                )
    
    def _validate_yaml_pair(self, rel_path: Path, src_path: Path, zh_path: Path):
        """Validate a YAML file pair."""
        try:
            with open(src_path, 'r', encoding='utf-8') as f:
                src_content = f.read()
            with open(zh_path, 'r', encoding='utf-8') as f:
                zh_content = f.read()
        except Exception as e:
            self._add_issue(
                str(rel_path),
                Severity.ERROR,
                "read_error",
                f"Failed to read file: {e}"
            )
            return
        
        # Simple YAML key extraction (not full parser)
        src_keys = self._extract_yaml_keys(src_content)
        zh_keys = self._extract_yaml_keys(zh_content)
        
        if src_keys != zh_keys:
            missing = src_keys - zh_keys
            extra = zh_keys - src_keys
            msg_parts = []
            if missing:
                msg_parts.append(f"missing keys: {', '.join(sorted(missing))}")
            if extra:
                msg_parts.append(f"extra keys: {', '.join(sorted(extra))}")
            
            self._add_issue(
                str(rel_path),
                Severity(self.config['severity_levels']['yaml_key_mismatch']),
                "yaml_key_mismatch",
                "YAML keys don't match: " + "; ".join(msg_parts)
            )
    
    def _extract_yaml_keys(self, content: str) -> Set[str]:
        """Extract top-level YAML keys."""
        keys = set()
        for line in content.split('\n'):
            # Match top-level keys (no leading whitespace)
            if ':' in line and not line.startswith((' ', '\t')):
                key = line.split(':')[0].strip()
                if key and not key.startswith('#'):
                    keys.add(key)
        return keys
    
    def _add_issue(self, file: str, severity: Severity, category: str, message: str, line: int = 0):
        """Add an issue to the result."""
        issue = Issue(file=file, severity=severity, category=category, message=message, line=line)
        self.result.issues.append(issue)
        
        if severity == Severity.ERROR:
            self.result.errors += 1
        elif severity == Severity.WARNING:
            self.result.warnings += 1
    
    def _print_summary(self):
        """Print summary to terminal."""
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Source files scanned:      {self.result.total_source_files}")
        print(f"Translation files found:   {self.result.total_zh_files}")
        print(f"Errors:                    {self.result.errors}")
        print(f"Warnings:                  {self.result.warnings}")
        print()
        
        # Category breakdown
        category_counts = {}
        for issue in self.result.issues:
            category_counts[issue.category] = category_counts.get(issue.category, 0) + 1
        
        if category_counts:
            print("Issues by category:")
            for category in sorted(category_counts.keys()):
                count = category_counts[category]
                print(f"  {category:30s} {count:4d}")
        
        print()
        
        # Show first few critical issues
        errors = [i for i in self.result.issues if i.severity == Severity.ERROR]
        if errors:
            print(f"First {min(10, len(errors))} errors:")
            for issue in errors[:10]:
                print(f"  [ERROR] {issue.file}")
                print(f"          {issue.category}: {issue.message}")
            if len(errors) > 10:
                print(f"  ... and {len(errors) - 10} more errors")
        
        print("=" * 80)
    
    def _generate_reports(self):
        """Generate markdown and JSON reports."""
        output_config = self.config['output']
        
        # Ensure reports directory exists
        reports_dir = self.repo_root / Path(output_config['markdown_report']).parent
        reports_dir.mkdir(parents=True, exist_ok=True)
        
        # Markdown report
        md_report_path = self.repo_root / output_config['markdown_report']
        self._generate_markdown_report(md_report_path)
        print(f"\nMarkdown report: {md_report_path.relative_to(self.repo_root)}")
        
        # JSON report
        json_report_path = self.repo_root / output_config['json_report']
        self._generate_json_report(json_report_path)
        print(f"JSON report:     {json_report_path.relative_to(self.repo_root)}")
    
    def _generate_markdown_report(self, path: Path):
        """Generate markdown report."""
        with open(path, 'w', encoding='utf-8') as f:
            f.write("# Translation Validation Report\n\n")
            f.write(f"**Generated:** {datetime.now().isoformat()}\n\n")
            f.write(f"**Repository:** `{self.repo_root}`\n\n")
            
            f.write("## Summary\n\n")
            f.write(f"- Source files scanned: {self.result.total_source_files}\n")
            f.write(f"- Translation files found: {self.result.total_zh_files}\n")
            f.write(f"- **Errors: {self.result.errors}**\n")
            f.write(f"- **Warnings: {self.result.warnings}**\n\n")
            
            # Group by severity
            errors = [i for i in self.result.issues if i.severity == Severity.ERROR]
            warnings = [i for i in self.result.issues if i.severity == Severity.WARNING]
            
            if errors:
                f.write(f"## Errors ({len(errors)})\n\n")
                for issue in sorted(errors, key=lambda x: (x.category, x.file)):
                    f.write(f"### {issue.file}\n\n")
                    f.write(f"- **Category:** `{issue.category}`\n")
                    f.write(f"- **Message:** {issue.message}\n\n")
            
            if warnings:
                f.write(f"## Warnings ({len(warnings)})\n\n")
                for issue in sorted(warnings, key=lambda x: (x.category, x.file)):
                    f.write(f"### {issue.file}\n\n")
                    f.write(f"- **Category:** `{issue.category}`\n")
                    f.write(f"- **Message:** {issue.message}\n\n")
    
    def _generate_json_report(self, path: Path):
        """Generate JSON report."""
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "repository": str(self.repo_root),
            "summary": {
                "total_source_files": self.result.total_source_files,
                "total_zh_files": self.result.total_zh_files,
                "errors": self.result.errors,
                "warnings": self.result.warnings
            },
            "issues": [
                {
                    "file": issue.file,
                    "severity": issue.severity.value,
                    "category": issue.category,
                    "message": issue.message,
                    "line": issue.line
                }
                for issue in self.result.issues
            ]
        }
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description='Validate zh translation completeness and correctness'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Treat warnings as errors (non-zero exit code)'
    )
    parser.add_argument(
        '--config',
        type=Path,
        default=Path('auto/translation_validation_config.json'),
        help='Path to configuration file'
    )
    parser.add_argument(
        '--repo-root',
        type=Path,
        default=Path.cwd(),
        help='Repository root directory'
    )
    
    args = parser.parse_args()
    
    # Validate paths
    config_path = args.repo_root / args.config
    if not config_path.exists():
        print(f"ERROR: Configuration file not found: {config_path}", file=sys.stderr)
        return 1
    
    # Run validation
    validator = TranslationValidator(config_path, args.repo_root)
    exit_code = validator.run(strict=args.strict)
    
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
