#!/usr/bin/env python3
"""
Compliance validator for checking adherence to skill-creator guidelines.
"""

import re
from yaml import safe_load
from pathlib import Path
from typing import Dict, List, Any, Tuple


class ComplianceValidator:
    """Validates skills against skill-creator guidelines."""

    def __init__(self, skill_dir: Path):
        """Initialize validator with skill directory."""
        self.skill_dir = skill_dir
        self.skill_md_path = skill_dir / "SKILL.md"
        self.violations = []

    def validate(self) -> Dict[str, Any]:
        """
        Run complete compliance validation.

        Returns:
            Dict with score, violations, and standards met
        """
        score = 100.0

        # 1. SKILL.md existence (10 points)
        skill_md_score, skill_md_valid = self._validate_skill_md_exists()
        score -= (10 - skill_md_score)

        if not skill_md_valid:
            return {
                'score': 0,
                'violations': ['Missing SKILL.md file (CRITICAL)'],
                'standards_met': [],
                'auto_fail': True
            }

        # 2. YAML frontmatter (20 points)
        yaml_score, yaml_data = self._validate_yaml_frontmatter()
        score -= (20 - yaml_score)

        if yaml_data is None:
            return {
                'score': max(0, score),
                'violations': self.violations,
                'standards_met': ['SKILL.md exists'],
                'auto_fail': True
            }

        # 3. Progressive disclosure (15 points)
        progressive_score = self._validate_progressive_disclosure()
        score -= (15 - progressive_score)

        # 4. Scripts usage (10 points)
        scripts_score = self._validate_scripts_usage()
        score -= (10 - scripts_score)

        # 5. References usage (10 points)
        refs_score = self._validate_references_usage()
        score -= (10 - refs_score)

        # 6. Assets usage (10 points)
        assets_score = self._validate_assets_usage()
        score -= (10 - assets_score)

        # 7. Writing style (10 points)
        style_score = self._validate_writing_style()
        score -= (10 - style_score)

        # 8. Trigger description (10 points)
        trigger_score = self._validate_trigger_description(yaml_data)
        score -= (10 - trigger_score)

        # 9. Overall adherence (5 points)
        overall_score = 5.0 if score >= 60 else 2.0
        score = max(0, score - (5 - overall_score))

        standards_met = self._list_standards_met()

        return {
            'score': max(0, score),
            'violations': self.violations,
            'standards_met': standards_met,
            'auto_fail': score < 40
        }

    def _validate_skill_md_exists(self) -> Tuple[float, bool]:
        """Validate SKILL.md exists (10 points)."""
        if not self.skill_md_path.exists():
            self.violations.append("CRITICAL: SKILL.md file missing")
            return 0.0, False

        try:
            content = self.skill_md_path.read_text(encoding='utf-8')
            if len(content.strip()) == 0:
                self.violations.append("CRITICAL: SKILL.md is empty")
                return 0.0, False
        except Exception as e:
            self.violations.append(f"CRITICAL: Cannot read SKILL.md: {e}")
            return 0.0, False

        return 10.0, True

    def _validate_yaml_frontmatter(self) -> Tuple[float, Dict]:
        """Validate YAML frontmatter (20 points)."""
        score = 20.0

        try:
            content = self.skill_md_path.read_text(encoding='utf-8')

            # Check for frontmatter
            if not content.startswith('---'):
                self.violations.append("CRITICAL: Missing YAML frontmatter")
                return 0.0, None

            # Extract frontmatter
            parts = content.split('---', 2)
            if len(parts) < 3:
                self.violations.append("CRITICAL: Invalid YAML frontmatter structure")
                return 0.0, None

            yaml_content = parts[1]

            # Parse YAML
            try:
                yaml_data = safe_load(yaml_content)
            except Exception as e:  # Catch all YAML parsing errors
                self.violations.append(f"CRITICAL: Invalid YAML syntax: {e}")
                return 0.0, None

            # Check required fields
            if 'name' not in yaml_data:
                self.violations.append("CRITICAL: Missing required 'name' field")
                score = 0
                return score, None

            if 'description' not in yaml_data:
                self.violations.append("CRITICAL: Missing required 'description' field")
                score = 0
                return score, None

            # Validate name format
            name = yaml_data['name']
            if not re.match(r'^[a-z0-9-]+$', name):
                self.violations.append("Name should use lowercase with hyphens (e.g., 'skill-name')")
                score -= 5

            # Check name matches directory
            if name != self.skill_dir.name:
                self.violations.append(f"Name '{name}' doesn't match directory '{self.skill_dir.name}'")
                score -= 5

            # Validate description
            description = yaml_data['description']
            if len(description) < 50:
                self.violations.append("Description is too short (minimum 50 characters)")
                score -= 5

            if len(description) > 500:
                self.violations.append("Description is too long (maximum 500 characters recommended)")
                score -= 2

            # Check for third-person perspective
            if re.search(r'\b(you|your|use this skill)\b', description, re.IGNORECASE):
                self.violations.append("Description should use third-person perspective (not 'you' or 'use this skill')")
                score -= 3

            return max(0, score), yaml_data

        except Exception as e:
            self.violations.append(f"Error reading SKILL.md: {e}")
            return 0.0, None

    def _validate_progressive_disclosure(self) -> float:
        """Validate progressive disclosure design (15 points)."""
        score = 15.0

        try:
            content = self.skill_md_path.read_text(encoding='utf-8')

            # Remove frontmatter
            if '---' in content:
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    body = parts[2]
                else:
                    body = content
            else:
                body = content

            word_count = len(body.split())

            # Check if SKILL.md is too long
            if word_count > 5000:
                self.violations.append("SKILL.md body exceeds 5,000 words (consider moving content to references/)")
                score -= 5

            # Check if content should be in references
            scripts_dir = self.skill_dir / "scripts"
            refs_dir = self.skill_dir / "references"

            has_scripts = scripts_dir.exists() and len(list(scripts_dir.glob("*.py"))) > 0
            has_refs = refs_dir.exists() and len(list(refs_dir.glob("*.md"))) > 0

            # If no references but long content, suggest moving
            if not has_refs and word_count > 2000:
                self.violations.append("Consider moving detailed content to references/ for progressive disclosure")
                score -= 3

            # Check if resources are referenced
            if has_scripts and 'script' not in body.lower():
                self.violations.append("Scripts exist but not referenced in SKILL.md")
                score -= 3

            if has_refs and 'reference' not in body.lower():
                self.violations.append("References exist but not mentioned in SKILL.md")
                score -= 3

        except Exception:
            score -= 5

        return max(0, score)

    def _validate_scripts_usage(self) -> float:
        """Validate scripts/ directory usage (10 points)."""
        score = 10.0

        scripts_dir = self.skill_dir / "scripts"
        if not scripts_dir.exists():
            return score  # N/A - no deductions

        scripts = list(scripts_dir.glob("*.py")) + list(scripts_dir.glob("*.sh"))

        if not scripts:
            return score  # N/A

        # Check for trivial scripts
        for script in scripts:
            try:
                content = script.read_text(encoding='utf-8')
                line_count = len([l for l in content.split('\n') if l.strip()])

                if line_count < 10:
                    self.violations.append(f"Script {script.name} is very short ({line_count} lines) - consider including as instructions")
                    score -= 3

                # Check for shebang
                if not content.startswith('#!'):
                    self.violations.append(f"Script {script.name} missing shebang line")
                    score -= 1

            except Exception:
                pass

        return max(0, score)

    def _validate_references_usage(self) -> float:
        """Validate references/ directory usage (10 points)."""
        score = 10.0

        refs_dir = self.skill_dir / "references"
        if not refs_dir.exists():
            return score  # N/A

        ref_files = list(refs_dir.glob("*.md"))

        if not ref_files:
            return score  # N/A

        # Check for appropriate content
        for ref_file in ref_files:
            try:
                content = ref_file.read_text(encoding='utf-8')

                # Check if it's too short (should have substance)
                if len(content.split()) < 100:
                    self.violations.append(f"Reference {ref_file.name} is too short - consider merging into SKILL.md")
                    score -= 2

                # Check for code (references should be docs, not code)
                if 'def ' in content or 'class ' in content:
                    self.violations.append(f"Reference {ref_file.name} contains code - should be in scripts/")
                    score -= 3

            except Exception:
                pass

        return max(0, score)

    def _validate_assets_usage(self) -> float:
        """Validate assets/ directory usage (10 points)."""
        score = 10.0

        assets_dir = self.skill_dir / "assets"
        if not assets_dir.exists():
            return score  # N/A

        asset_files = list(assets_dir.iterdir())

        if not asset_files:
            return score  # N/A

        # Check for misplaced files
        for asset_file in asset_files:
            if asset_file.suffix == '.md':
                self.violations.append(f"Asset {asset_file.name} is markdown - should be in references/")
                score -= 2

            if asset_file.suffix in ['.py', '.sh']:
                self.violations.append(f"Asset {asset_file.name} is a script - should be in scripts/")
                score -= 3

        return max(0, score)

    def _validate_writing_style(self) -> float:
        """Validate imperative/infinitive writing style (10 points)."""
        score = 10.0

        try:
            content = self.skill_md_path.read_text(encoding='utf-8')

            # Remove frontmatter
            if '---' in content:
                parts = content.split('---', 2)
                body = parts[2] if len(parts) >= 3 else content
            else:
                body = content

            # Count second-person usage
            second_person_count = len(re.findall(r'\b(you|your|yours)\b', body, re.IGNORECASE))

            # Count "should" usage (often indicates second-person)
            should_count = len(re.findall(r'\b(should|must|need to)\b', body, re.IGNORECASE))

            if second_person_count > 10:
                self.violations.append(f"Excessive second-person language ({second_person_count} instances) - use imperative form")
                score -= 5

            if second_person_count > 5:
                self.violations.append("Uses second-person language - should use imperative/infinitive form")
                score -= 3

        except Exception:
            pass

        return max(0, score)

    def _validate_trigger_description(self, yaml_data: Dict) -> float:
        """Validate trigger description quality (10 points)."""
        score = 10.0

        if not yaml_data or 'description' not in yaml_data:
            return 0.0

        description = yaml_data['description']

        # Check if it specifies when to use
        has_trigger = bool(re.search(
            r'(?:this skill should be used when|when users|when|use this)',
            description,
            re.IGNORECASE
        ))

        if not has_trigger:
            self.violations.append("Description doesn't clearly specify when to use the skill")
            score -= 5

        # Check if it's too generic
        generic_phrases = ['a skill for', 'helps with', 'useful for']
        is_generic = any(phrase in description.lower() for phrase in generic_phrases)

        if is_generic and len(description) < 100:
            self.violations.append("Description is too generic - be more specific about capabilities and triggers")
            score -= 3

        return max(0, score)

    def _list_standards_met(self) -> List[str]:
        """List standards that were met."""
        standards = []

        if self.skill_md_path.exists():
            standards.append("✓ SKILL.md exists")

            try:
                content = self.skill_md_path.read_text(encoding='utf-8')

                if content.startswith('---'):
                    standards.append("✓ YAML frontmatter present")

                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        yaml_data = safe_load(parts[1])

                        if 'name' in yaml_data:
                            standards.append("✓ Name field present")

                        if 'description' in yaml_data:
                            standards.append("✓ Description field present")

                            if yaml_data['name'] == self.skill_dir.name:
                                standards.append("✓ Name matches directory")

                # Check structure
                scripts_dir = self.skill_dir / "scripts"
                refs_dir = self.skill_dir / "references"
                assets_dir = self.skill_dir / "assets"

                if scripts_dir.exists():
                    standards.append("✓ Scripts directory exists")

                if refs_dir.exists():
                    standards.append("✓ References directory exists")

                if assets_dir.exists():
                    standards.append("✓ Assets directory exists")

            except Exception:
                pass

        return standards
