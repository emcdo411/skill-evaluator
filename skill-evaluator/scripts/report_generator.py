#!/usr/bin/env python3
"""
Report generator for creating markdown evaluation reports.
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, Any


class ReportGenerator:
    """Generates formatted markdown reports from evaluation results."""

    VERSION = "1.0.0"

    def __init__(self, results: Dict[str, Any]):
        """Initialize generator with evaluation results."""
        self.results = results

    def generate(self) -> str:
        """
        Generate complete markdown report.

        Returns:
            Formatted markdown report as string
        """
        # Load template
        template_path = self._get_template_path()  # evaluator: ignore - safe internal path usage
        if template_path and template_path.exists():
            template = template_path.read_text(encoding='utf-8')
        else:
            # Fallback inline template
            template = self._get_inline_template()

        # Fill in all template variables
        report = self._fill_template(template)

        return report

    def _get_template_path(self) -> Path:  # evaluator: ignore - safe internal path usage
        """Get path to report template."""
        # Try to find template relative to this script
        script_dir = Path(__file__).parent  # evaluator: ignore - safe internal path usage
        skill_dir = script_dir.parent
        template_path = skill_dir / "assets" / "report_template.md"

        return template_path if template_path.exists() else None

    def _fill_template(self, template: str) -> str:
        """Fill template with evaluation results."""
        metadata = self.results.get('metadata', {})
        overall = self.results.get('overall', {})
        security = self.results.get('security', {})
        quality = self.results.get('quality', {})
        utility = self.results.get('utility', {})
        compliance = self.results.get('compliance', {})

        # Basic substitutions
        replacements = {
            '{skill_name}': metadata.get('skill_name', 'Unknown'),
            '{evaluation_date}': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '{evaluator_version}': self.VERSION,
            '{overall_score}': str(overall.get('overall_score', 0)),
            '{recommendation}': overall.get('recommendation', 'Unknown'),
            '{risk_level}': overall.get('risk_level', 'Unknown'),
            '{security_score}': str(security.get('score', 0)),
            '{security_risk_level}': self._get_security_risk_level(security),
            '{quality_score}': str(quality.get('score', 0)),
            '{code_quality_score}': str(quality.get('code_quality', 0)),
            '{documentation_score}': str(quality.get('documentation', 0)),
            '{structure_score}': str(quality.get('structure', 0)),
            '{functionality_score}': str(quality.get('functionality', 0)),
            '{utility_score}': str(utility.get('score', 0)),
            '{problem_solving_score}': str(utility.get('problem_solving', 0)),
            '{usability_score}': str(utility.get('usability', 0)),
            '{scope_score}': str(utility.get('scope', 0)),
            '{effectiveness_score}': str(utility.get('effectiveness', 0)),
            '{compliance_score}': str(compliance.get('score', 0)),
        }

        # Complex content generation
        replacements['{key_findings}'] = self._generate_key_findings()
        replacements['{security_vulnerabilities}'] = self._generate_security_vulnerabilities()
        replacements['{security_strengths}'] = self._generate_security_strengths()
        replacements['{security_recommendations}'] = self._generate_security_recommendations()
        replacements['{quality_strengths}'] = self._generate_quality_strengths()
        replacements['{quality_weaknesses}'] = self._generate_quality_weaknesses()
        replacements['{quality_recommendations}'] = self._generate_quality_recommendations()
        replacements['{value_assessment}'] = self._generate_value_assessment()
        replacements['{use_cases}'] = self._generate_use_cases()
        replacements['{limitations}'] = self._generate_limitations()
        replacements['{utility_recommendations}'] = self._generate_utility_recommendations()
        replacements['{standards_met}'] = self._generate_standards_met()
        replacements['{violations_found}'] = self._generate_violations()
        replacements['{progressive_disclosure}'] = self._generate_progressive_disclosure()
        replacements['{writing_style}'] = self._generate_writing_style()
        replacements['{compliance_recommendations}'] = self._generate_compliance_recommendations()
        replacements['{priority_fixes}'] = self._generate_priority_fixes()
        replacements['{suggested_improvements}'] = self._generate_suggested_improvements()
        replacements['{best_practices}'] = self._generate_best_practices()
        replacements['{conclusion}'] = self._generate_conclusion()

        # Apply replacements
        for key, value in replacements.items():
            template = template.replace(key, value)

        return template

    def _get_security_risk_level(self, security: Dict) -> str:
        """Determine security risk level from score."""
        score = security.get('score', 0)
        if score >= 90:
            return "Low"
        elif score >= 75:
            return "Medium"
        elif score >= 50:
            return "High"
        else:
            return "Critical"

    def _generate_key_findings(self) -> str:
        """Generate key findings bullet points."""
        findings = []

        overall = self.results.get('overall', {})
        security = self.results.get('security', {})
        quality = self.results.get('quality', {})
        compliance = self.results.get('compliance', {})

        # Security findings
        critical_count = security.get('critical_count', 0)
        high_count = security.get('high_count', 0)

        if critical_count > 0:
            findings.append(f"- ❌ **{critical_count} CRITICAL security vulnerabilities** found")
        elif high_count > 0:
            findings.append(f"- ⚠️ **{high_count} HIGH-risk security issues** identified")
        elif security.get('score', 0) >= 90:
            findings.append("- ✅ **Strong security posture** with no major vulnerabilities")

        # Quality findings
        if quality.get('score', 0) >= 90:
            findings.append("- ✅ **Excellent code quality** and documentation")
        elif quality.get('score', 0) < 60:
            findings.append("- ⚠️ **Quality improvements needed** in code and documentation")

        # Compliance findings
        if compliance.get('auto_fail', False):
            findings.append("- ❌ **Critical compliance violations** found")
        elif compliance.get('score', 0) >= 90:
            findings.append("- ✅ **Fully compliant** with skill-creator guidelines")

        # Overall recommendation
        findings.append(f"- **Overall Recommendation:** {overall.get('recommendation', 'Unknown')}")

        return '\n'.join(findings) if findings else "- No significant findings"

    def _generate_security_vulnerabilities(self) -> str:
        """Generate security vulnerabilities section."""
        security = self.results.get('security', {})
        issues = security.get('issues', [])

        if not issues:
            return "No security vulnerabilities detected."

        # Group by severity
        critical = [i for i in issues if i['severity'] == 'CRITICAL']
        high = [i for i in issues if i['severity'] == 'HIGH']
        medium = [i for i in issues if i['severity'] == 'MEDIUM']
        low = [i for i in issues if i['severity'] == 'LOW']

        sections = []

        if critical:
            sections.append("#### ❌ Critical Issues\n")
            for issue in critical:
                sections.append(f"- **{issue['category']}** in `{issue['file_path']}:{issue['line_number']}`")
                sections.append(f"  - {issue['description']}")
                sections.append(f"  - Recommendation: {issue['recommendation']}\n")

        if high:
            sections.append("#### ⚠️ High-Risk Issues\n")
            for issue in high[:5]:  # Limit to 5
                sections.append(f"- **{issue['category']}** in `{issue['file_path']}:{issue['line_number']}`")
                sections.append(f"  - {issue['description']}\n")

        if medium:
            sections.append(f"#### Medium-Risk Issues ({len(medium)} found)\n")
            sections.append(f"- {medium[0]['category']} and other issues found. Review security report for details.\n")

        if low:
            sections.append(f"#### Low-Risk Issues ({len(low)} found)\n")

        return '\n'.join(sections)

    def _generate_security_strengths(self) -> str:
        """Generate security strengths."""
        security = self.results.get('security', {})
        score = security.get('score', 0)
        issues = security.get('issues', [])

        if score >= 90:
            return "- No major security vulnerabilities detected\n- Follows security best practices\n- Implements safe coding patterns"
        elif score >= 75:
            return "- No critical vulnerabilities found\n- Generally follows security best practices"
        elif not issues:
            return "- Basic security checks passed"
        else:
            return "- Limited security issues detected"

    def _generate_security_recommendations(self) -> str:
        """Generate security recommendations."""
        security = self.results.get('security', {})
        issues = security.get('issues', [])

        if not issues:
            return "- Continue following security best practices\n- Regularly update dependencies\n- Stay informed about new vulnerabilities"

        recs = []
        categories = set(issue['category'] for issue in issues if issue['severity'] in ['CRITICAL', 'HIGH'])

        if categories:
            recs.append("**Priority Actions:**")
            for category in list(categories)[:5]:
                relevant_issue = next(i for i in issues if i['category'] == category)
                recs.append(f"- Fix {category}: {relevant_issue['recommendation']}")

        recs.append("\n**General Recommendations:**")
        recs.append("- Review all flagged security issues")
        recs.append("- Implement input validation and sanitization")
        recs.append("- Follow principle of least privilege")

        return '\n'.join(recs)

    def _generate_quality_strengths(self) -> str:
        """Generate quality strengths."""
        quality = self.results.get('quality', {})
        strengths = []

        if quality.get('code_quality', 0) >= 20:
            strengths.append("- Clean, well-structured code")

        if quality.get('documentation', 0) >= 20:
            strengths.append("- Comprehensive documentation")

        if quality.get('structure', 0) >= 20:
            strengths.append("- Proper directory organization")

        if quality.get('functionality', 0) >= 20:
            strengths.append("- Functional and practical implementation")

        return '\n'.join(strengths) if strengths else "- Basic quality standards met"

    def _generate_quality_weaknesses(self) -> str:
        """Generate quality weaknesses."""
        quality = self.results.get('quality', {})
        weaknesses = []

        if quality.get('code_quality', 0) < 15:
            weaknesses.append("- Code quality needs improvement")

        if quality.get('documentation', 0) < 15:
            weaknesses.append("- Documentation is incomplete or unclear")

        if quality.get('structure', 0) < 15:
            weaknesses.append("- Directory structure needs organization")

        if quality.get('functionality', 0) < 15:
            weaknesses.append("- Functionality or completeness issues")

        return '\n'.join(weaknesses) if weaknesses else "- No major quality weaknesses identified"

    def _generate_quality_recommendations(self) -> str:
        """Generate quality recommendations."""
        quality = self.results.get('quality', {})
        recs = []

        if quality.get('code_quality', 0) < 20:
            recs.append("- Improve code readability and error handling")
            recs.append("- Add type hints and docstrings")

        if quality.get('documentation', 0) < 20:
            recs.append("- Enhance documentation with clear examples")
            recs.append("- Remove TODO placeholders")

        if quality.get('structure', 0) < 20:
            recs.append("- Organize files into proper directories")
            recs.append("- Follow naming conventions")

        return '\n'.join(recs) if recs else "- Maintain current quality standards"

    def _generate_value_assessment(self) -> str:
        """Generate utility value assessment."""
        utility = self.results.get('utility', {})
        score = utility.get('score', 0)

        if score >= 90:
            return "This skill provides excellent practical value and solves real problems effectively."
        elif score >= 75:
            return "This skill provides good practical value with clear use cases."
        elif score >= 60:
            return "This skill provides moderate value but could be more impactful."
        else:
            return "This skill's practical value is limited or unclear."

    def _generate_use_cases(self) -> str:
        """Generate use cases."""
        return "- Refer to SKILL.md for documented use cases\n- Suitable for intended purpose as described"

    def _generate_limitations(self) -> str:
        """Generate limitations."""
        return "- Static analysis only (no runtime testing)\n- Pattern-based detection may have false positives/negatives"

    def _generate_utility_recommendations(self) -> str:
        """Generate utility recommendations."""
        utility = self.results.get('utility', {})
        score = utility.get('score', 0)

        if score < 75:
            return "- Clarify the specific problems this skill solves\n- Add concrete usage examples\n- Ensure functionality delivers real value"
        else:
            return "- Consider additional features to expand utility\n- Gather user feedback for improvements"

    def _generate_standards_met(self) -> str:
        """Generate standards met list."""
        compliance = self.results.get('compliance', {})
        standards = compliance.get('standards_met', [])

        return '\n'.join(standards) if standards else "- No compliance standards met"

    def _generate_violations(self) -> str:
        """Generate violations list."""
        compliance = self.results.get('compliance', {})
        violations = compliance.get('violations', [])

        if not violations:
            return "No compliance violations detected."

        return '\n'.join(f"- {v}" for v in violations)

    def _generate_progressive_disclosure(self) -> str:
        """Generate progressive disclosure assessment."""
        compliance = self.results.get('compliance', {})
        score = compliance.get('score', 0)

        if score >= 80:
            return "Skill follows progressive disclosure principles with appropriate separation of metadata, instructions, and bundled resources."
        else:
            return "Progressive disclosure could be improved by better organizing content across SKILL.md and bundled resources."

    def _generate_writing_style(self) -> str:
        """Generate writing style review."""
        compliance = self.results.get('compliance', {})
        violations = compliance.get('violations', [])

        style_violations = [v for v in violations if 'second-person' in v.lower() or 'imperative' in v.lower()]

        if not style_violations:
            return "Writing style follows imperative/infinitive form guidelines."
        else:
            return "Writing style needs adjustment:\n" + '\n'.join(f"  - {v}" for v in style_violations)

    def _generate_compliance_recommendations(self) -> str:
        """Generate compliance recommendations."""
        compliance = self.results.get('compliance', {})
        violations = compliance.get('violations', [])

        if not violations:
            return "- Maintain compliance with skill-creator guidelines\n- Keep structure and documentation up to date"

        recs = ["**Address the following violations:**"]
        for violation in violations[:5]:
            recs.append(f"- {violation}")

        if len(violations) > 5:
            recs.append(f"- ... and {len(violations) - 5} more violations")

        return '\n'.join(recs)

    def _generate_priority_fixes(self) -> str:
        """Generate priority fixes."""
        fixes = []

        # Security priority
        security = self.results.get('security', {})
        if security.get('critical_count', 0) > 0:
            fixes.append("1. **FIX CRITICAL SECURITY VULNERABILITIES** - Highest priority")

        # Compliance priority
        compliance = self.results.get('compliance', {})
        if compliance.get('auto_fail', False):
            fixes.append("2. **Address critical compliance violations** - Required for validity")

        # Quality priority
        quality = self.results.get('quality', {})
        if quality.get('score', 0) < 50:
            fixes.append("3. **Improve code and documentation quality** - Important for usability")

        return '\n'.join(fixes) if fixes else "No critical fixes required."

    def _generate_suggested_improvements(self) -> str:
        """Generate suggested improvements."""
        improvements = [
            "- Review and address all flagged issues",
            "- Enhance documentation with more examples",
            "- Follow security and quality best practices",
            "- Test thoroughly before distribution"
        ]

        return '\n'.join(improvements)

    def _generate_best_practices(self) -> str:
        """Generate best practices list."""
        practices = [
            "- Use subprocess with list arguments (not shell=True)",
            "- Validate and sanitize all inputs",
            "- Implement proper error handling",
            "- Write clear, imperative-form documentation",
            "- Follow progressive disclosure design",
            "- Use appropriate bundled resources (scripts, references, assets)"
        ]

        return '\n'.join(practices)

    def _generate_conclusion(self) -> str:
        """Generate conclusion."""
        overall = self.results.get('overall', {})
        recommendation = overall.get('recommendation', '')
        score = overall.get('overall_score', 0)

        if '❌ DO NOT INSTALL' in recommendation:
            return "This skill has critical issues that must be addressed before it can be safely used or distributed. Do not install until security and compliance issues are resolved."
        elif '⚠️' in recommendation:
            return "This skill has some issues that should be addressed. While usable, improvements are recommended before widespread distribution."
        elif score >= 90:
            return "This skill demonstrates excellent quality, security, and compliance. It is highly recommended for installation and use."
        else:
            return "This skill meets basic standards and is suitable for use. Minor improvements could enhance quality further."

    def _get_inline_template(self) -> str:
        """Fallback inline template."""
        return """# Skill Evaluation Report

**Skill Name:** `{skill_name}`
**Evaluation Date:** {evaluation_date}
**Evaluator Version:** {evaluator_version}

---

## Executive Summary

### Overall Score: {overall_score}/100

**Recommendation:** {recommendation}

**Risk Level:** {risk_level}

### Key Findings

{key_findings}

---

## Detailed Analysis

### 1. Security Analysis

**Score:** {security_score}/100
**Risk Level:** {security_risk_level}

#### Vulnerabilities Found

{security_vulnerabilities}

#### Security Strengths

{security_strengths}

#### Security Recommendations

{security_recommendations}

---

### 2. Quality Assessment

**Score:** {quality_score}/100

#### Breakdown
- **Code Quality:** {code_quality_score}/25
- **Documentation:** {documentation_score}/25
- **Structure & Organization:** {structure_score}/25
- **Functionality:** {functionality_score}/25

#### Strengths

{quality_strengths}

#### Weaknesses

{quality_weaknesses}

#### Quality Recommendations

{quality_recommendations}

---

### 3. Utility Evaluation

**Score:** {utility_score}/100

#### Value Assessment

{value_assessment}

---

### 4. Compliance Validation

**Score:** {compliance_score}/100

#### Standards Met

{standards_met}

#### Violations Found

{violations_found}

---

## Overall Recommendations

### Priority Fixes

{priority_fixes}

### Suggested Improvements

{suggested_improvements}

---

## Conclusion

{conclusion}

---

*Report generated by skill-evaluator v{evaluator_version}*
"""
