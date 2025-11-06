#!/usr/bin/env python3
"""
Security scanner implementing 5-layer security architecture.
Performs deep vulnerability analysis on Claude skills.
"""

import re
import ast
from pathlib import Path
from typing import Dict, List, Any, Set
from dataclasses import dataclass, field


@dataclass
class SecurityIssue:
    """Represents a security vulnerability."""
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    category: str  # Command Injection, Path Traversal, etc.
    description: str
    file_path: str
    line_number: int = 0
    code_snippet: str = ""
    recommendation: str = ""


@dataclass
class LayerResult:
    """Results for a single security layer."""
    layer_name: str
    passed: bool
    issues: List[SecurityIssue] = field(default_factory=list)
    score: float = 100.0


class SecurityScanner:
    """
    Comprehensive security scanner with 5-layer defense-in-depth analysis.
    """

    # Vulnerability patterns from references/security_patterns.md
    PATTERNS = {
        'command_injection': [
            # Python patterns
            (r'os\.system\s*\(', 'CRITICAL', 'os.system() with potential user input'),
            (r'subprocess\.(call|run|Popen).*shell\s*=\s*True', 'CRITICAL', 'subprocess with shell=True'),
            (r'\beval\s*\(', 'CRITICAL', 'eval() allows arbitrary code execution'),
            (r'\bexec\s*\(', 'CRITICAL', 'exec() allows arbitrary code execution'),
            (r'__import__\s*\(', 'HIGH', '__import__() with dynamic module names'),
            (r'compile\s*\(', 'HIGH', 'compile() with external code'),
            # Bash patterns
            (r'\$\([^)]*\$', 'HIGH', 'Command substitution with variables'),
            (r'`[^`]*\$', 'HIGH', 'Backtick command substitution'),
            (r'bash\s+-c\s+["\'].*\$', 'CRITICAL', 'bash -c with variable expansion'),
        ],
        'path_traversal': [
            (r'\.\./', 'HIGH', 'Directory traversal sequence'),
            (r'%2e%2e%2f', 'HIGH', 'URL-encoded traversal'),
            (r'\.\.\\\\', 'HIGH', 'Windows directory traversal'),
            (r'open\s*\([^)]*\)', 'MEDIUM', 'File open without validation'),
            (r'Path\s*\([^)]*\)\s*(?!\.resolve\(\))', 'MEDIUM', 'Path without resolve()'),
        ],
        'arbitrary_file_ops': [
            (r'shutil\.(copy|move|rmtree)', 'HIGH', 'File operations without validation'),
            (r'os\.(remove|unlink|rmdir)', 'MEDIUM', 'File deletion without checks'),
            (r'open\s*\([^)]*[,\s]+["\']w["\']', 'MEDIUM', 'File write without validation'),
        ],
        'privilege_escalation': [
            (r'\bsudo\b', 'CRITICAL', 'Privilege elevation with sudo'),
            (r'\bsu\b(?!\w)', 'CRITICAL', 'Switching to superuser'),
            (r'os\.setuid', 'CRITICAL', 'Changing user ID'),
            (r'os\.chmod\s*\([^)]*0o777', 'HIGH', 'Setting world-writable permissions'),
            (r'runas\s*\(', 'CRITICAL', 'Windows privilege elevation'),
        ],
        'env_var_manipulation': [
            (r'os\.environ\s*\[\s*["\']PATH["\']', 'HIGH', 'Modifying PATH environment variable'),
            (r'os\.environ\s*\[\s*["\']LD_PRELOAD["\']', 'CRITICAL', 'Setting LD_PRELOAD'),
            (r'os\.environ\s*\[\s*["\']PYTHONPATH["\']', 'HIGH', 'Modifying PYTHONPATH'),
        ],
        'dos_patterns': [
            (r'while\s+True\s*:', 'MEDIUM', 'Infinite loop without timeout'),
            (r'def\s+\w+\s*\([^)]*\)\s*:.*\1\s*\(', 'HIGH', 'Potential recursive call'),
            (r'for\s+\w+\s+in\s+range\s*\(\s*[0-9]{7,}', 'MEDIUM', 'Very large iteration'),
        ],
        'information_disclosure': [
            (r'print\s*\(.*(?:api[_-]?key|password|token|secret)', 'MEDIUM', 'Logging sensitive data'),
            (r'logging\..*\(.*(?:api[_-]?key|password|token|secret)', 'MEDIUM', 'Logging credentials'),
            (r'traceback\.print_exc\s*\(\)', 'LOW', 'Exposing stack traces'),
        ],
        'insecure_deserialization': [
            (r'pickle\.loads\s*\(', 'HIGH', 'Unsafe pickle deserialization'),
            (r'yaml\.load\s*\([^)]*\)(?!.*Loader\s*=)', 'HIGH', 'yaml.load without SafeLoader'),
            (r'marshal\.loads\s*\(', 'HIGH', 'Unsafe marshal deserialization'),
        ],
        'hardcoded_credentials': [
            (r'(?:api[_-]?key|password|token|secret)\s*=\s*["\'][^"\']{8,}["\']', 'HIGH', 'Hardcoded credentials'),
            (r'(?:sk_live|pk_live)_[a-zA-Z0-9]{20,}', 'HIGH', 'Hardcoded API key pattern'),
            (r'Bearer\s+[a-zA-Z0-9_-]{20,}', 'HIGH', 'Hardcoded bearer token'),
        ],
        'weak_crypto': [
            (r'hashlib\.md5\s*\(', 'MEDIUM', 'Weak hashing algorithm MD5'),
            (r'hashlib\.sha1\s*\(', 'MEDIUM', 'Weak hashing algorithm SHA1'),
            (r'\brandom\.(?:randint|choice|random)\s*\(', 'LOW', 'Insecure random for security'),
        ],
        'ssrf': [
            (r'requests\.(?:get|post)\s*\([^)]*\)', 'MEDIUM', 'HTTP request without URL validation'),
            (r'urllib\.request\.urlopen\s*\(', 'MEDIUM', 'URL fetch without validation'),
            (r'(?:localhost|127\.0\.0\.1|169\.254\.169\.254)', 'HIGH', 'Internal network access'),
        ],
        'xss_output': [
            (r'<script[^>]*>', 'MEDIUM', 'Script tag in output'),
            (r'javascript:', 'MEDIUM', 'JavaScript protocol in URL'),
            (r'onerror\s*=', 'MEDIUM', 'Event handler in output'),
        ],
    }

    def __init__(self, skill_dir: Path):
        """Initialize scanner with skill directory."""
        self.skill_dir = skill_dir
        self.issues: List[SecurityIssue] = []
        self.layer_results: List[LayerResult] = []

    def analyze(self) -> Dict[str, Any]:
        """
        Run complete 5-layer security analysis.

        Returns:
            Dict with score, issues, and layer results
        """
        # Layer 1: Input Validation & Sanitization
        self.analyze_layer1_input_validation()

        # Layer 2: Execution Environment Control
        self.analyze_layer2_execution_control()

        # Layer 3: Output Sanitization
        self.analyze_layer3_output_sanitization()

        # Layer 4: Privilege Management
        self.analyze_layer4_privilege_management()

        # Layer 5: Self-Protection
        self.analyze_layer5_self_protection()

        # Calculate overall security score
        score = self.calculate_security_score()

        # Categorize issues by severity
        critical = [i for i in self.issues if i.severity == 'CRITICAL']
        high = [i for i in self.issues if i.severity == 'HIGH']
        medium = [i for i in self.issues if i.severity == 'MEDIUM']
        low = [i for i in self.issues if i.severity == 'LOW']

        return {
            'score': score,
            'critical_count': len(critical),
            'high_count': len(high),
            'medium_count': len(medium),
            'low_count': len(low),
            'issues': [self._issue_to_dict(i) for i in self.issues],
            'layers': [self._layer_to_dict(l) for l in self.layer_results],
        }

    def analyze_layer1_input_validation(self):
        """Layer 1: Check input validation and sanitization."""
        layer_issues = []

        # Scan for command injection vulnerabilities
        layer_issues.extend(self._scan_patterns('command_injection'))

        # Scan for path traversal
        layer_issues.extend(self._scan_patterns('path_traversal'))

        # Scan for file operation issues
        layer_issues.extend(self._scan_patterns('arbitrary_file_ops'))

        passed = len([i for i in layer_issues if i.severity in ['CRITICAL', 'HIGH']]) == 0
        score = self._calculate_layer_score(layer_issues)

        self.layer_results.append(LayerResult(
            layer_name="Layer 1: Input Validation & Sanitization",
            passed=passed,
            issues=layer_issues,
            score=score
        ))
        self.issues.extend(layer_issues)

    def analyze_layer2_execution_control(self):
        """Layer 2: Check execution environment controls."""
        layer_issues = []

        # Check for privilege escalation
        layer_issues.extend(self._scan_patterns('privilege_escalation'))

        # Check for environment variable manipulation
        layer_issues.extend(self._scan_patterns('env_var_manipulation'))

        # Check for insecure deserialization
        layer_issues.extend(self._scan_patterns('insecure_deserialization'))

        passed = len([i for i in layer_issues if i.severity in ['CRITICAL', 'HIGH']]) == 0
        score = self._calculate_layer_score(layer_issues)

        self.layer_results.append(LayerResult(
            layer_name="Layer 2: Execution Environment Control",
            passed=passed,
            issues=layer_issues,
            score=score
        ))
        self.issues.extend(layer_issues)

    def analyze_layer3_output_sanitization(self):
        """Layer 3: Check output sanitization."""
        layer_issues = []

        # Check for XSS in output
        layer_issues.extend(self._scan_patterns('xss_output'))

        # Check for information disclosure
        layer_issues.extend(self._scan_patterns('information_disclosure'))

        passed = len([i for i in layer_issues if i.severity in ['CRITICAL', 'HIGH']]) == 0
        score = self._calculate_layer_score(layer_issues)

        self.layer_results.append(LayerResult(
            layer_name="Layer 3: Output Sanitization",
            passed=passed,
            issues=layer_issues,
            score=score
        ))
        self.issues.extend(layer_issues)

    def analyze_layer4_privilege_management(self):
        """Layer 4: Check privilege management."""
        layer_issues = []

        # Check for hardcoded credentials
        layer_issues.extend(self._scan_patterns('hardcoded_credentials'))

        # Check for weak cryptography
        layer_issues.extend(self._scan_patterns('weak_crypto'))

        passed = len([i for i in layer_issues if i.severity in ['CRITICAL', 'HIGH']]) == 0
        score = self._calculate_layer_score(layer_issues)

        self.layer_results.append(LayerResult(
            layer_name="Layer 4: Privilege Management",
            passed=passed,
            issues=layer_issues,
            score=score
        ))
        self.issues.extend(layer_issues)

    def analyze_layer5_self_protection(self):
        """Layer 5: Check self-protection mechanisms."""
        layer_issues = []

        # Check for DoS patterns
        layer_issues.extend(self._scan_patterns('dos_patterns'))

        # Check for SSRF
        layer_issues.extend(self._scan_patterns('ssrf'))

        passed = len([i for i in layer_issues if i.severity in ['CRITICAL', 'HIGH']]) == 0
        score = self._calculate_layer_score(layer_issues)

        self.layer_results.append(LayerResult(
            layer_name="Layer 5: Self-Protection",
            passed=passed,
            issues=layer_issues,
            score=score
        ))
        self.issues.extend(layer_issues)

    def _scan_patterns(self, category: str) -> List[SecurityIssue]:
        """Scan for specific vulnerability patterns."""
        issues = []
        patterns = self.PATTERNS.get(category, [])

        # Scan all Python and Bash scripts
        script_files = list(self.skill_dir.rglob('*.py'))
        script_files.extend(self.skill_dir.rglob('*.sh'))
        script_files.extend(self.skill_dir.rglob('*.bash'))

        # Directories to exclude from scanning (dependencies, build artifacts)
        excluded_dirs = {'node_modules', 'venv', '.venv', '__pycache__', 
                        '.git', 'dist', 'build', '.eggs', '.tox'}
        
        # Files to exclude from scanning (contain pattern definitions)
        excluded_files = {'security_scanner.py', 'quality_checker.py'}

        for script_path in script_files:
            # Skip files in excluded directories
            path_parts = set(script_path.relative_to(self.skill_dir).parts)
            if path_parts.intersection(excluded_dirs):
                continue
            # Skip files that contain pattern definitions
            if script_path.name in excluded_files:
                continue

            try:
                content = script_path.read_text(encoding='utf-8', errors='ignore')
                lines = content.split('\n')

                for line_num, line in enumerate(lines, 1):
                    for pattern, severity, description in patterns:
                        match = re.search(pattern, line, re.IGNORECASE)
                        if match:
                            # Check for ignore markers (skill authors can suppress false positives)
                            if '# evaluator: ignore' in line or '# noqa' in line:
                                continue
                            
                            # Basic string literal detection - skip if match is likely inside a string
                            # Count quotes before the match position
                            before_match = line[:match.start()]
                            single_quotes = before_match.count("'")
                            double_quotes = before_match.count('"')
                            
                            # If odd number of quotes before match, we're likely inside a string
                            if (single_quotes % 2 == 1) or (double_quotes % 2 == 1):
                                continue
                            
                            issues.append(SecurityIssue(
                                severity=severity,
                                category=category.replace('_', ' ').title(),
                                description=description,
                                file_path=str(script_path.relative_to(self.skill_dir)),
                                line_number=line_num,
                                code_snippet=line.strip()[:100],
                                recommendation=self._get_recommendation(category)
                            ))
            except Exception as e:
                # Skip files that can't be read
                pass

        return issues

    def _get_recommendation(self, category: str) -> str:
        """Get security recommendation for category."""
        recommendations = {
            'command_injection': 'Use subprocess with list arguments and shell=False. Validate all inputs.',
            'path_traversal': 'Use Path.resolve() and validate paths are within allowed directories.',
            'arbitrary_file_ops': 'Validate file paths and use temporary directories for untrusted operations.',
            'privilege_escalation': 'Remove privilege elevation. Run with least necessary privileges.',
            'env_var_manipulation': 'Avoid modifying system environment variables. Use configuration files.',
            'dos_patterns': 'Add timeouts, resource limits, and iteration bounds.',
            'information_disclosure': 'Never log credentials or sensitive data. Use proper error handling.',
            'insecure_deserialization': 'Use json or yaml.safe_load(). Never deserialize untrusted data.',
            'hardcoded_credentials': 'Use environment variables or secure secret management.',
            'weak_crypto': 'Use SHA-256 or stronger. Use secrets module for random values.',
            'ssrf': 'Validate and allowlist URLs. Restrict access to internal networks.',
            'xss_output': 'Escape HTML output. Sanitize user content before rendering.',
        }
        return recommendations.get(category, 'Review and apply security best practices.')

    def _calculate_layer_score(self, issues: List[SecurityIssue]) -> float:
        """Calculate score for a security layer."""
        if not issues:
            return 100.0

        deductions = 0
        for issue in issues:
            if issue.severity == 'CRITICAL':
                deductions += 40
            elif issue.severity == 'HIGH':
                deductions += 20
            elif issue.severity == 'MEDIUM':
                deductions += 10
            elif issue.severity == 'LOW':
                deductions += 5

        return max(0.0, 100.0 - deductions)

    def calculate_security_score(self) -> float:
        """Calculate overall security score from all layers."""
        if not self.issues:
            return 100.0

        # Count by severity
        critical = sum(1 for i in self.issues if i.severity == 'CRITICAL')
        high = sum(1 for i in self.issues if i.severity == 'HIGH')
        medium = sum(1 for i in self.issues if i.severity == 'MEDIUM')
        low = sum(1 for i in self.issues if i.severity == 'LOW')

        # Critical issues = auto-fail
        if critical > 0:
            return min(25.0, 25.0 - (critical * 5))

        # High issues = poor score
        if high > 0:
            return min(50.0, 50.0 - (high * 5))

        # Medium issues = moderate score
        if medium > 0:
            return min(75.0, 75.0 - (medium * 3))

        # Low issues = good score
        if low > 0:
            return min(90.0, 90.0 - (low * 2))

        return 100.0

    def _issue_to_dict(self, issue: SecurityIssue) -> Dict:
        """Convert SecurityIssue to dict."""
        return {
            'severity': issue.severity,
            'category': issue.category,
            'description': issue.description,
            'file_path': issue.file_path,
            'line_number': issue.line_number,
            'code_snippet': issue.code_snippet,
            'recommendation': issue.recommendation,
        }

    def _layer_to_dict(self, layer: LayerResult) -> Dict:
        """Convert LayerResult to dict."""
        return {
            'name': layer.layer_name,
            'passed': layer.passed,
            'score': layer.score,
            'issue_count': len(layer.issues),
        }
