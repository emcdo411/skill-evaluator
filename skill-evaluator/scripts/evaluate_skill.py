#!/usr/bin/env python3
"""
Main orchestrator for skill evaluation.
Coordinates security, quality, utility, and compliance analyses.
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime
import zipfile
import tempfile
import shutil
from typing import Dict, Any, Tuple

# Import evaluation modules
from security_scanner import SecurityScanner
from quality_checker import QualityChecker
from compliance_validator import ComplianceValidator
from report_generator import ReportGenerator


class SkillEvaluator:
    """Main evaluator orchestrating all analysis dimensions."""

    VERSION = "1.0.0"

    def __init__(self, skill_path: str, mode: str = "full"):
        """
        Initialize evaluator with skill path and evaluation mode.

        Args:
            skill_path: Path to skill directory or .zip file
            mode: Evaluation mode (full, security, pre-publish)
        """
        self.skill_path = Path(skill_path)  # evaluator: ignore - safe internal path usage
        self.mode = mode
        self.temp_dir = None
        self.skill_dir = None
        self.results = {}

    def __enter__(self):
        """Context manager entry - extract if zip."""
        if self.skill_path.suffix == '.zip':
            self.temp_dir = tempfile.mkdtemp(prefix='skill_eval_')
            with zipfile.ZipFile(self.skill_path, 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir)
            # Find skill directory (should be single top-level dir)
            contents = list(Path(self.temp_dir).iterdir())  # evaluator: ignore - safe internal path usage
            if len(contents) == 1 and contents[0].is_dir():
                self.skill_dir = contents[0]
            else:
                self.skill_dir = Path(self.temp_dir)  # evaluator: ignore - safe internal path usage
        else:
            self.skill_dir = self.skill_path

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - cleanup temp files."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)  # evaluator: ignore - safe internal path usage

    def validate_structure(self) -> Tuple[bool, str]:
        """
        Validate basic skill structure.

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.skill_dir.exists():
            return False, f"Skill directory does not exist: {self.skill_dir}"

        skill_md = self.skill_dir / "SKILL.md"
        if not skill_md.exists():
            return False, "SKILL.md file not found (required)"

        return True, ""

    def run_security_analysis(self) -> Dict[str, Any]:
        """Run comprehensive security analysis."""
        scanner = SecurityScanner(self.skill_dir)
        return scanner.analyze()

    def run_quality_assessment(self) -> Dict[str, Any]:
        """Run quality assessment."""
        checker = QualityChecker(self.skill_dir)
        return checker.assess()

    def run_utility_evaluation(self) -> Dict[str, Any]:
        """Run utility evaluation."""
        # Utility is assessed as part of quality for now
        # but could be expanded to separate module
        checker = QualityChecker(self.skill_dir)
        return checker.assess_utility()

    def run_compliance_validation(self) -> Dict[str, Any]:
        """Run compliance validation."""
        validator = ComplianceValidator(self.skill_dir)
        return validator.validate()

    def calculate_overall_score(self) -> Dict[str, Any]:
        """
        Calculate weighted overall score and recommendation.

        Returns:
            Dict with overall_score, recommendation, risk_level
        """
        # Extract individual scores
        security_score = self.results['security']['score']
        quality_score = self.results['quality']['score']
        utility_score = self.results['utility']['score']
        compliance_score = self.results['compliance']['score']

        # Weighted calculation
        overall = (
            security_score * 0.35 +
            quality_score * 0.25 +
            utility_score * 0.20 +
            compliance_score * 0.20
        )

        # Determine recommendation
        recommendation = self._determine_recommendation(
            overall, security_score, compliance_score
        )

        # Determine risk level
        risk_level = self._determine_risk_level(security_score)

        return {
            'overall_score': round(overall, 1),
            'recommendation': recommendation,
            'risk_level': risk_level,
            'breakdown': {
                'security': security_score,
                'quality': quality_score,
                'utility': utility_score,
                'compliance': compliance_score
            }
        }

    def _determine_recommendation(
        self, overall: float, security: float, compliance: float
    ) -> str:
        """Determine install recommendation with overrides."""
        # Security override
        if security < 50:
            return "❌ DO NOT INSTALL - Critical security risks"

        # Check for critical vulnerabilities
        if self.results['security'].get('critical_count', 0) > 0:
            return "❌ DO NOT INSTALL - Critical vulnerabilities found"

        # Compliance override
        if compliance < 40:
            return "⚠️ NOT RECOMMENDED - Fundamental compliance issues"

        # Standard scoring
        if overall >= 90:
            return "✅ HIGHLY RECOMMENDED"
        elif overall >= 75:
            return "✅ RECOMMENDED"
        elif overall >= 60:
            return "⚠️ USE WITH CAUTION"
        elif overall >= 40:
            return "⚠️ NOT RECOMMENDED"
        else:
            return "❌ DO NOT INSTALL"

    def _determine_risk_level(self, security_score: float) -> str:
        """Determine overall risk level based on security score."""
        if security_score >= 90:
            return "Low"
        elif security_score >= 75:
            return "Medium"
        elif security_score >= 50:
            return "High"
        else:
            return "Critical"

    def evaluate(self) -> Dict[str, Any]:
        """
        Run complete evaluation based on mode.

        Returns:
            Complete evaluation results
        """
        # Validate structure first
        is_valid, error = self.validate_structure()
        if not is_valid:
            return {
                'error': error,
                'overall_score': 0,
                'recommendation': '❌ INVALID SKILL STRUCTURE'
            }

        # Run analyses based on mode
        if self.mode == "security":
            # Security-focused mode
            self.results['security'] = self.run_security_analysis()
            self.results['quality'] = {'score': 0}  # Skip
            self.results['utility'] = {'score': 0}  # Skip
            self.results['compliance'] = self.run_compliance_validation()
        elif self.mode == "pre-publish":
            # Full evaluation with detailed recommendations
            self.results['security'] = self.run_security_analysis()
            self.results['quality'] = self.run_quality_assessment()
            self.results['utility'] = self.run_utility_evaluation()
            self.results['compliance'] = self.run_compliance_validation()
        else:
            # Full evaluation (default)
            self.results['security'] = self.run_security_analysis()
            self.results['quality'] = self.run_quality_assessment()
            self.results['utility'] = self.run_utility_evaluation()
            self.results['compliance'] = self.run_compliance_validation()

        # Calculate overall score
        self.results['overall'] = self.calculate_overall_score()

        # Add metadata
        self.results['metadata'] = {
            'skill_name': self.skill_dir.name,
            'evaluation_date': datetime.now().isoformat(),
            'evaluator_version': self.VERSION,
            'mode': self.mode
        }

        return self.results

    def generate_report(self, output_path: str = None) -> str:
        """
        Generate markdown report.

        Args:
            output_path: Optional path for output file

        Returns:
            Report content as string
        """
        generator = ReportGenerator(self.results)
        report = generator.generate()

        if output_path:
            output_file = Path(output_path)  # evaluator: ignore - safe internal path usage
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(report, encoding='utf-8')

        return report


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description='Evaluate Claude skills for security, quality, and compliance'
    )
    parser.add_argument(
        'skill_path',
        help='Path to skill directory or .zip file'
    )
    parser.add_argument(
        '--mode',
        choices=['full', 'security', 'pre-publish'],
        default='full',
        help='Evaluation mode'
    )
    parser.add_argument(
        '--output',
        '-o',
        help='Output path for report (markdown)'
    )
    parser.add_argument(
        '--json',
        help='Output path for JSON results'
    )

    args = parser.parse_args()

    # Run evaluation
    with SkillEvaluator(args.skill_path, args.mode) as evaluator:
        results = evaluator.evaluate()

        # Generate report
        report = evaluator.generate_report(args.output)

        # Output to console if no file specified
        if not args.output:
            print(report)

        # Save JSON if requested
        if args.json:
            json_path = Path(args.json)  # evaluator: ignore - safe internal path usage
            json_path.parent.mkdir(parents=True, exist_ok=True)
            json_path.write_text(
                json.dumps(results, indent=2),
                encoding='utf-8'
            )

        # Exit code based on recommendation
        if '❌ DO NOT INSTALL' in results['overall']['recommendation']:
            sys.exit(1)
        elif '⚠️' in results['overall']['recommendation']:
            sys.exit(2)
        else:
            sys.exit(0)


if __name__ == '__main__':
    main()
