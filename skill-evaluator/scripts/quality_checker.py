#!/usr/bin/env python3
"""
Quality checker for evaluating code quality, documentation, structure, and utility.
"""

import re
import ast
from pathlib import Path
from typing import Dict, List, Any, Tuple


class QualityChecker:
    """Assesses skill quality across multiple dimensions."""

    def __init__(self, skill_dir: Path):
        """Initialize checker with skill directory."""
        self.skill_dir = skill_dir
        self.skill_md_path = skill_dir / "SKILL.md"

    def assess(self) -> Dict[str, Any]:
        """
        Run complete quality assessment.

        Returns:
            Dict with overall score and dimension scores
        """
        code_quality = self.assess_code_quality()
        documentation = self.assess_documentation()
        structure = self.assess_structure()
        functionality = self.assess_functionality()

        total_score = code_quality + documentation + structure + functionality

        return {
            'score': total_score,
            'code_quality': code_quality,
            'documentation': documentation,
            'structure': structure,
            'functionality': functionality,
            'breakdown': {
                'code_quality_max': 25,
                'documentation_max': 25,
                'structure_max': 25,
                'functionality_max': 25
            }
        }

    def assess_code_quality(self) -> float:
        """
        Assess code quality (25 points max).
        - Clean, readable code: 5 points
        - Error handling: 5 points
        - Modularity: 5 points
        - Dependencies: 5 points
        - Best practices: 5 points
        """
        score = 25.0

        script_dir = self.skill_dir / "scripts"
        if not script_dir.exists():
            return score  # No scripts = no deductions

        python_scripts = list(script_dir.glob("*.py"))
        if not python_scripts:
            return score  # No Python scripts = no deductions

        for script_path in python_scripts:
            try:
                content = script_path.read_text(encoding='utf-8')

                # Check readability (5 points)
                score -= self._check_readability(content)

                # Check error handling (5 points)
                score -= self._check_error_handling(content)

                # Check modularity (5 points)
                score -= self._check_modularity(content, script_path)

                # Check dependencies (5 points)
                score -= self._check_dependencies(content)

                # Check best practices (5 points)
                score -= self._check_best_practices(content)

            except Exception:
                score -= 2  # Penalty for unreadable files

        return max(0.0, score)

    def _check_readability(self, content: str) -> float:
        """Check code readability (max 5 points deduction)."""
        deductions = 0.0

        # Check for commented-out code
        commented_lines = [l for l in content.split('\n') if l.strip().startswith('#') and len(l.strip()) > 2]
        if len(commented_lines) > 10:
            deductions += 1.0

        # Check for very long lines (>120 chars)
        long_lines = [l for l in content.split('\n') if len(l) > 120]
        if len(long_lines) > 5:
            deductions += 1.0

        # Check for meaningful names (detect many single-char variables)
        single_char_vars = len(re.findall(r'\b[a-z]\s*=', content))
        if single_char_vars > 10:
            deductions += 1.5

        return min(5.0, deductions)

    def _check_error_handling(self, content: str) -> float:
        """Check error handling (max 5 points deduction)."""
        deductions = 0.0

        # Check for bare except clauses
        if re.search(r'except\s*:', content):
            deductions += 2.0

        # Check if try-except exists at all
        has_try = 'try:' in content
        has_file_ops = bool(re.search(r'open\s*\(|Path\s*\(', content))

        if has_file_ops and not has_try:
            deductions += 3.0

        return min(5.0, deductions)

    def _check_modularity(self, content: str, script_path: Path) -> float:
        """Check code modularity (max 5 points deduction)."""
        deductions = 0.0

        try:
            tree = ast.parse(content)

            # Check for very long functions (>50 lines)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_length = node.end_lineno - node.lineno
                    if func_length > 50:
                        deductions += 0.5

            # Check for duplicate code patterns
            lines = content.split('\n')
            line_counts = {}
            for line in lines:
                stripped = line.strip()
                if len(stripped) > 20:  # Only check substantial lines
                    line_counts[stripped] = line_counts.get(stripped, 0) + 1

            duplicates = [l for l, count in line_counts.items() if count > 2]
            if len(duplicates) > 3:
                deductions += 1.5

        except SyntaxError:
            deductions += 2.0  # Syntax errors are bad

        return min(5.0, deductions)

    def _check_dependencies(self, content: str) -> float:
        """Check dependency management (max 5 points deduction)."""
        deductions = 0.0

        # Count imports
        import_lines = [l for l in content.split('\n') if l.strip().startswith('import ') or l.strip().startswith('from ')]

        # Check for excessive dependencies
        if len(import_lines) > 20:
            deductions += 1.0

        # Check for unusual/heavy dependencies
        heavy_deps = ['tensorflow', 'torch', 'pandas']
        for dep in heavy_deps:
            if dep in content:
                deductions += 1.0

        return min(5.0, deductions)

    def _check_best_practices(self, content: str) -> float:
        """Check Python best practices (max 5 points deduction)."""
        deductions = 0.0

        # Check for type hints
        has_type_hints = '->' in content or ': str' in content or ': int' in content
        if not has_type_hints and len(content) > 100:
            deductions += 1.0

        # Check for docstrings
        has_docstrings = '"""' in content or "'''" in content
        if not has_docstrings and len(content) > 200:
            deductions += 1.5

        # Check for magic numbers (numbers > 1 without explanation)
        magic_numbers = re.findall(r'\b([2-9][0-9]+)\b', content)
        if len(magic_numbers) > 10:
            deductions += 0.5

        return min(5.0, deductions)

    def assess_documentation(self) -> float:
        """
        Assess documentation quality (25 points max).
        - Clear purpose: 5 points
        - Usage instructions: 5 points
        - Bundled resource references: 5 points
        - Writing quality: 5 points
        - Completeness: 5 points
        """
        score = 25.0

        if not self.skill_md_path.exists():
            return 0.0  # No SKILL.md = 0 points

        try:
            content = self.skill_md_path.read_text(encoding='utf-8')

            # Clear purpose (5 points)
            score -= self._check_purpose_clarity(content)

            # Usage instructions (5 points)
            score -= self._check_usage_instructions(content)

            # Resource references (5 points)
            score -= self._check_resource_references(content)

            # Writing quality (5 points)
            score -= self._check_writing_quality(content)

            # Completeness (5 points)
            score -= self._check_completeness(content)

        except Exception:
            return 0.0

        return max(0.0, score)

    def _check_purpose_clarity(self, content: str) -> float:
        """Check if purpose is clear (max 5 deductions)."""
        deductions = 0.0

        # Check for purpose/overview section
        has_purpose = bool(re.search(r'(?i)(purpose|overview|about|what)', content[:500]))
        if not has_purpose:
            deductions += 2.0

        # Check description length (should be descriptive)
        intro_section = content[:1000]
        if len(intro_section.split()) < 50:
            deductions += 2.0

        return min(5.0, deductions)

    def _check_usage_instructions(self, content: str) -> float:
        """Check usage instructions quality (max 5 deductions)."""
        deductions = 0.0

        # Check for usage/how-to section
        has_usage = bool(re.search(r'(?i)(usage|how to|getting started|instructions)', content))
        if not has_usage:
            deductions += 3.0

        # Check for examples
        has_examples = bool(re.search(r'(?i)(example|for instance)', content))
        if not has_examples:
            deductions += 2.0

        return min(5.0, deductions)

    def _check_resource_references(self, content: str) -> float:
        """Check bundled resource documentation (max 5 deductions)."""
        deductions = 0.0

        # Check if scripts/ exists and is referenced
        scripts_dir = self.skill_dir / "scripts"
        if scripts_dir.exists() and list(scripts_dir.glob("*.py")):
            if 'script' not in content.lower():
                deductions += 2.0

        # Check if references/ exists and is referenced
        refs_dir = self.skill_dir / "references"
        if refs_dir.exists() and list(refs_dir.glob("*.md")):
            if 'reference' not in content.lower():
                deductions += 2.0

        # Check if assets/ exists and is referenced
        assets_dir = self.skill_dir / "assets"
        if assets_dir.exists() and len(list(assets_dir.iterdir())) > 0:
            if 'asset' not in content.lower():
                deductions += 1.0

        return min(5.0, deductions)

    def _check_writing_quality(self, content: str) -> float:
        """Check overall writing quality (max 5 deductions)."""
        deductions = 0.0

        # Check for second-person usage (should be imperative)
        second_person = len(re.findall(r'\byou\b|\byour\b', content, re.IGNORECASE))
        if second_person > 5:
            deductions += 1.0

        # Check for extremely short sections
        sections = content.split('\n##')
        short_sections = [s for s in sections if len(s.split()) < 20]
        if len(short_sections) > len(sections) / 2:
            deductions += 1.5

        return min(5.0, deductions)

    def _check_completeness(self, content: str) -> float:
        """Check documentation completeness (max 5 deductions)."""
        deductions = 0.0

        # Check for TODO placeholders
        todos = len(re.findall(r'TODO|FIXME|XXX|\\[\\s*\\]', content, re.IGNORECASE))
        if todos > 0:
            deductions += min(3.0, todos * 1.0)

        # Check if too short
        word_count = len(content.split())
        if word_count < 100:
            deductions += 2.0

        return min(5.0, deductions)

    def assess_structure(self) -> float:
        """
        Assess structure and organization (25 points max).
        - Proper organization: 8 points
        - File naming: 7 points
        - YAML frontmatter: 10 points
        """
        score = 25.0

        # Proper organization (8 points)
        score -= self._check_organization()

        # File naming (7 points)
        score -= self._check_file_naming()

        # YAML frontmatter (10 points) - handled by compliance, light check here
        score -= self._check_yaml_structure()

        return max(0.0, score)

    def _check_organization(self) -> float:
        """Check directory organization (max 8 deductions)."""
        deductions = 0.0

        # Check for misplaced files in root
        root_files = [f for f in self.skill_dir.iterdir() if f.is_file() and f.name != 'SKILL.md']
        if len(root_files) > 2:  # Allow README, LICENSE, etc.
            deductions += 2.0

        # Check for proper subdirectories usage
        scripts_dir = self.skill_dir / "scripts"
        refs_dir = self.skill_dir / "references"
        assets_dir = self.skill_dir / "assets"

        # If scripts exist outside scripts/
        scripts_in_root = [f for f in root_files if f.suffix in ['.py', '.sh', '.bash']]
        if scripts_in_root:
            deductions += 3.0

        return min(8.0, deductions)

    def _check_file_naming(self) -> float:
        """Check file naming conventions (max 7 deductions)."""
        deductions = 0.0

        all_files = list(self.skill_dir.rglob('*'))
        all_files = [f for f in all_files if f.is_file()]

        # Check for spaces in filenames
        spaces_in_names = [f for f in all_files if ' ' in f.name]
        if spaces_in_names:
            deductions += 2.0

        # Check for uppercase in Python scripts
        py_files = [f for f in all_files if f.suffix == '.py']
        uppercase_py = [f for f in py_files if any(c.isupper() for c in f.stem)]
        if uppercase_py:
            deductions += 1.5

        return min(7.0, deductions)

    def _check_yaml_structure(self) -> float:
        """Light YAML check for quality (max 10 deductions)."""
        deductions = 0.0

        if not self.skill_md_path.exists():
            return 10.0

        try:
            content = self.skill_md_path.read_text(encoding='utf-8')

            # Check for frontmatter presence
            if not content.startswith('---'):
                deductions += 5.0

            # Check for description quality (length)
            desc_match = re.search(r'description:\s*(.+?)(?=\n---|$)', content, re.DOTALL)
            if desc_match:
                desc = desc_match.group(1).strip()
                if len(desc) < 50:
                    deductions += 3.0
            else:
                deductions += 5.0

        except Exception:
            deductions += 10.0

        return min(10.0, deductions)

    def assess_functionality(self) -> float:
        """
        Assess functionality and utility (25 points max).
        - Practical value: 8 points
        - Appropriate tools: 7 points
        - Reusability: 5 points
        - Completeness: 5 points
        """
        score = 25.0

        # This is somewhat subjective, so we do basic checks
        score -= self._check_practical_value()
        score -= self._check_tool_appropriateness()
        score -= self._check_reusability()
        score -= self._check_completeness_functionality()

        return max(0.0, score)

    def _check_practical_value(self) -> float:
        """Check if skill provides practical value (max 8 deductions)."""
        deductions = 0.0

        # Check if skill is too trivial (very minimal content)
        scripts_dir = self.skill_dir / "scripts"
        refs_dir = self.skill_dir / "references"
        assets_dir = self.skill_dir / "assets"

        has_scripts = scripts_dir.exists() and len(list(scripts_dir.glob("*.py"))) > 0
        has_refs = refs_dir.exists() and len(list(refs_dir.glob("*.md"))) > 0
        has_assets = assets_dir.exists() and len(list(assets_dir.iterdir())) > 0

        if not (has_scripts or has_refs or has_assets):
            deductions += 5.0  # No bundled resources = likely trivial

        return min(8.0, deductions)

    def _check_tool_appropriateness(self) -> float:
        """Check if tools are appropriately used (max 7 deductions)."""
        deductions = 0.0

        scripts_dir = self.skill_dir / "scripts"
        if scripts_dir.exists():
            scripts = list(scripts_dir.glob("*.py"))

            # Check for overly simple scripts (< 20 lines)
            for script in scripts:
                try:
                    content = script.read_text()
                    if len(content.split('\n')) < 20:
                        deductions += 1.0
                except Exception:
                    pass

        return min(7.0, deductions)

    def _check_reusability(self) -> float:
        """Check reusability (max 5 deductions)."""
        deductions = 0.0

        # Check if skill appears overly specific
        if self.skill_md_path.exists():
            content = self.skill_md_path.read_text(encoding='utf-8', errors='ignore')

            # Look for overly specific language
            specific_indicators = ['my company', 'our team', 'internal only']
            for indicator in specific_indicators:
                if indicator.lower() in content.lower():
                    deductions += 1.5

        return min(5.0, deductions)

    def _check_completeness_functionality(self) -> float:
        """Check functional completeness (max 5 deductions)."""
        deductions = 0.0

        # Check for broken file references
        if self.skill_md_path.exists():
            content = self.skill_md_path.read_text(encoding='utf-8', errors='ignore')

            # Find file references
            file_refs = re.findall(r'(?:scripts|references|assets)/[\\w/-]+\\.\\w+', content)

            for ref in file_refs:
                ref_path = self.skill_dir / ref
                if not ref_path.exists():
                    deductions += 1.0

        return min(5.0, deductions)

    def assess_utility(self) -> Dict[str, Any]:
        """
        Assess utility separately for utility evaluation mode.
        Returns similar structure but focused on practical value.
        """
        problem_solving = self._assess_problem_solving()
        usability = self._assess_usability()
        scope = self._assess_scope()
        effectiveness = self._assess_effectiveness()

        total = problem_solving + usability + scope + effectiveness

        return {
            'score': total,
            'problem_solving': problem_solving,
            'usability': usability,
            'scope': scope,
            'effectiveness': effectiveness
        }

    def _assess_problem_solving(self) -> float:
        """Assess problem-solving value (25 points max)."""
        # Use similar logic to practical value
        return 25.0 - self._check_practical_value() * 3

    def _assess_usability(self) -> float:
        """Assess usability (25 points max)."""
        # Based on documentation quality
        return 25.0 - (self._check_usage_instructions(
            self.skill_md_path.read_text(encoding='utf-8') if self.skill_md_path.exists() else ''
        ) * 5)

    def _assess_scope(self) -> float:
        """Assess scope appropriateness (25 points max)."""
        return 25.0 - self._check_reusability() * 5

    def _assess_effectiveness(self) -> float:
        """Assess effectiveness (25 points max)."""
        return 25.0 - self._check_completeness_functionality() * 5
