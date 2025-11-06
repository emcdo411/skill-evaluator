# Skill Evaluator - User Guide

**Version:** 1.0.0
**Last Updated:** November 2025

## Table of Contents

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [How It Works](#how-it-works)
5. [Evaluation Modes](#evaluation-modes)
6. [Understanding Reports](#understanding-reports)
7. [Use Cases](#use-cases)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)
10. [FAQ](#faq)

---

## Introduction

The **Skill Evaluator** is a comprehensive security and quality assessment toolkit for Claude skills. It helps you:

- ✅ **Evaluate skills before installation** - Assess third-party skills for safety
- 🔒 **Identify security vulnerabilities** - Detect injection risks, privilege escalation, and more
- 📊 **Assess quality** - Review code quality, documentation, and structure
- ✔️ **Validate compliance** - Ensure skills follow best practices and guidelines
- 📝 **Generate detailed reports** - Get actionable recommendations with scores

### Why Use Skill Evaluator?

Installing untrusted skills can be risky. Skills have access to your files, can execute code, and interact with your system. The Skill Evaluator provides:

- **Security analysis** with 5-layer defense-in-depth architecture
- **Automated vulnerability detection** for common attack patterns
- **Quality assessment** to ensure skills are well-built
- **Compliance validation** against skill-creator guidelines
- **Scored recommendations** (0-100) with clear install guidance

---

## Installation

### Prerequisites

- **Claude Code** installed and running
- **Python 3.7+** (for running evaluation scripts)
- **PyYAML** library (will be installed automatically)

### Installation Steps

#### Method 1: Install from Zip (Recommended)

1. **Download the skill**
   - Obtain `skill-evaluator.zip` from the distribution source

2. **Install the skill**

   **Option A: Via Claude Code UI**
   - Open Claude Code settings
   - Navigate to Skills/Plugins section
   - Click "Install Skill from Zip"
   - Select `skill-evaluator.zip`

   **Option B: Manual Installation**
   ```bash
   # Extract to your Claude Code plugins directory
   unzip skill-evaluator.zip -d ~/.claude/plugins/

   # Or on Windows:
   # Extract to: C:\Users\<YourName>\.claude\plugins\
   ```

3. **Install Python dependencies**
   ```bash
   cd ~/.claude/plugins/skill-evaluator
   pip install -r requirements.txt
   ```

4. **Restart Claude Code**
   - Close and reopen Claude Code to load the new skill

5. **Verify installation**
   - In Claude Code, ask: "Is the skill-evaluator installed?"
   - Claude should confirm the skill is available

#### Method 2: Install from Source Directory

1. **Copy the skill directory**
   ```bash
   cp -r /path/to/skill-evaluator ~/.claude/plugins/
   ```

2. **Install dependencies**
   ```bash
   cd ~/.claude/plugins/skill-evaluator
   pip install -r requirements.txt
   ```

3. **Restart Claude Code**

### Verifying Installation

Ask Claude Code:
```
"List my installed skills"
```

You should see `skill-evaluator` in the list with its description.

---

## Quick Start

### Your First Evaluation

Let's evaluate a skill for safety:

**Step 1: Ask Claude to evaluate a skill**
```
"Is the skill at /path/to/my-skill safe to install?"
```

**Step 2: Wait for analysis**
Claude will:
- Execute security scanner
- Check for vulnerabilities
- Assess quality and compliance
- Generate a report

**Step 3: Review the report**
You'll receive a markdown report with:
- Overall score (0-100)
- Recommendation (Install / Caution / Do Not Install)
- Security findings
- Quality assessment
- Actionable recommendations

### Example Session

**You:**
```
"I downloaded a skill called 'data-processor' from the internet.
Can you evaluate it for me? It's at ~/Downloads/data-processor/"
```

**Claude (using skill-evaluator):**
```
I'll evaluate the data-processor skill for security and quality.

[Executes evaluation scripts...]

# Evaluation Report

**Overall Score:** 45/100
**Recommendation:** ❌ DO NOT INSTALL
**Risk Level:** Critical

## Key Findings:
- ❌ 2 CRITICAL security vulnerabilities found
- ⚠️ Command injection in scripts/process.py:42
- ⚠️ Path traversal in scripts/loader.py:18

## Details:
[Full report follows...]

**Recommendation:** Do not install this skill. It contains
critical security vulnerabilities that could compromise your system.
```

---

## How It Works

### Evaluation Process

The Skill Evaluator follows a 5-step process:

#### Step 1: Skill Discovery & Extraction
- Accepts directory path or .zip file
- Extracts archives to temporary directory
- Identifies SKILL.md and bundled resources
- Validates basic structure

#### Step 2: Multi-Dimensional Analysis

**Security Analysis (35% weight)**
- 5-layer security architecture scan
- Pattern-based vulnerability detection
- Checks for injection, escalation, disclosure

**Quality Assessment (25% weight)**
- Code quality review
- Documentation completeness
- Structural organization
- Functionality validation

**Utility Evaluation (20% weight)**
- Practical value assessment
- Usability review
- Scope appropriateness
- Effectiveness check

**Compliance Validation (20% weight)**
- YAML frontmatter validation
- Guidelines adherence
- Writing style review
- Progressive disclosure check

#### Step 3: Score Calculation
```
Overall Score =
  (Security × 0.35) +
  (Quality × 0.25) +
  (Utility × 0.20) +
  (Compliance × 0.20)
```

**Override Rules:**
- Security < 50 → ❌ AUTO-FAIL
- Any CRITICAL vulnerability → ❌ AUTO-FAIL
- Compliance < 40 → ⚠️ NOT RECOMMENDED

#### Step 4: Report Generation
- Creates structured markdown report
- Includes executive summary
- Lists all findings by severity
- Provides actionable recommendations

#### Step 5: Output & Recommendations
- Saves report to file
- Presents summary to user
- Recommends install decision

### 5-Layer Security Architecture

The security scanner uses defense-in-depth:

**Layer 1: Input Validation & Sanitization**
- Detects command injection (subprocess, eval, exec)
- Identifies path traversal (../, directory escapes)
- Checks file operation safety

**Layer 2: Execution Environment Control**
- Detects privilege escalation (sudo, setuid)
- Checks environment variable manipulation
- Validates sandboxing and permissions

**Layer 3: Output Sanitization**
- Detects XSS in markdown output
- Identifies information disclosure (logging secrets)
- Checks for data exposure

**Layer 4: Privilege Management**
- Identifies hardcoded credentials
- Detects weak cryptography (MD5, SHA1)
- Checks authentication patterns

**Layer 5: Self-Protection**
- Detects DoS patterns (infinite loops)
- Identifies SSRF vulnerabilities
- Checks resource exhaustion risks

---

## Evaluation Modes

### Mode 1: Full Evaluation (Default)

**When to use:** Comprehensive assessment of any skill

**How to invoke:**
```
"Evaluate this skill at /path/to/skill"
"Evaluate the skill in ~/Downloads/skill.zip"
"Perform a full evaluation of my-skill"
```

**What you get:**
- Complete analysis across all 4 dimensions
- Overall score (0-100)
- Detailed findings for each dimension
- Comprehensive recommendations

**Report sections:**
- Executive Summary
- Security Analysis (with vulnerability details)
- Quality Assessment (code, docs, structure)
- Utility Evaluation
- Compliance Validation
- Priority Fixes
- Suggested Improvements

---

### Mode 2: Security-Focused Quick Check

**When to use:** Quick safety assessment before installation

**How to invoke:**
```
"Is /path/to/skill safe to install?"
"Check the security of this skill: ~/skill.zip"
"Security audit for my-skill"
```

**What you get:**
- Deep security analysis
- Brief quality/compliance check
- Install safety recommendation
- Critical vulnerability highlights

**Report focus:**
- Security score and risk level
- CRITICAL and HIGH vulnerabilities
- Security-specific recommendations
- Safe/Unsafe determination

**Example output:**
```
Security Score: 35/100
Risk Level: Critical
Recommendation: ❌ DO NOT INSTALL

Critical Issues:
- Command injection in scripts/handler.py:56
- Privilege escalation via sudo in scripts/setup.sh:12

This skill is NOT SAFE to install.
```

---

### Mode 3: Pre-Publication Review

**When to use:** You're creating a skill and want feedback before publishing

**How to invoke:**
```
"Review my skill before I publish it: /my-projects/my-skill"
"Help me improve my-skill for publication"
"Pre-publication check for /path/to/my-skill"
```

**What you get:**
- Full evaluation with author-focused guidance
- Prioritized improvements list
- Best practices recommendations
- Publication readiness assessment

**Report focus:**
- Detailed findings with explanations
- Specific code locations for issues
- How to fix each problem
- Best practices to adopt
- Publication readiness checklist

**Example output:**
```
Overall Score: 82/100
Status: Nearly Ready for Publication

Priority Improvements:
1. Add error handling to scripts/processor.py
2. Remove TODO placeholders from SKILL.md
3. Convert "you should" to imperative form in docs

Suggested Enhancements:
- Add usage examples
- Include type hints in Python code
- Expand documentation with edge cases

After these minor improvements, your skill will be
publication-ready with an estimated score of 90+.
```

---

## Understanding Reports

### Report Structure

Every evaluation report contains:

#### 1. Executive Summary
- **Overall Score** (0-100)
- **Recommendation** (Install decision)
- **Risk Level** (Low/Medium/High/Critical)
- **Key Findings** (3-5 main points)

#### 2. Security Analysis
- **Security Score** (0-100)
- **Vulnerabilities by Severity:**
  - Critical (auto-fail issues)
  - High (serious risks)
  - Medium (moderate concerns)
  - Low (minor issues)
- **Security Strengths**
- **Recommendations**

#### 3. Quality Assessment
- **Overall Quality Score** (0-100)
- **Breakdown:**
  - Code Quality (0-25)
  - Documentation (0-25)
  - Structure (0-25)
  - Functionality (0-25)
- **Strengths & Weaknesses**
- **Recommendations**

#### 4. Utility Evaluation
- **Utility Score** (0-100)
- **Value Assessment**
- **Use Cases**
- **Limitations**
- **Recommendations**

#### 5. Compliance Validation
- **Compliance Score** (0-100)
- **Standards Met** (checklist)
- **Violations Found**
- **Writing Style Review**
- **Recommendations**

#### 6. Overall Recommendations
- **Priority Fixes** (must-do items)
- **Suggested Improvements** (nice-to-have)
- **Best Practices** (general guidance)

#### 7. Conclusion
- Final assessment
- Install decision rationale

### Score Interpretation

#### Overall Score Ranges

**90-100: EXCELLENT ✅**
- Highly recommended for installation
- Exemplary quality across all dimensions
- No critical issues
- Follows best practices
- **Action:** Install with confidence

**75-89: GOOD ✅**
- Recommended for installation
- Solid quality with minor issues
- No major security concerns
- Generally well-implemented
- **Action:** Safe to install

**60-74: FAIR ⚠️**
- Use with caution
- Several issues to be aware of
- Review findings carefully
- May require monitoring
- **Action:** Install only if you understand the risks

**40-59: POOR ⚠️**
- Not recommended
- Significant problems present
- Security or quality concerns
- Needs major improvements
- **Action:** Do not install; wait for fixes

**0-39: CRITICAL ❌**
- Do not install
- Critical security vulnerabilities
- Fundamental quality issues
- Potentially dangerous
- **Action:** Do not install under any circumstances

### Vulnerability Severity Levels

#### CRITICAL (Auto-Fail)
- **Examples:** Command injection, arbitrary code execution, privilege escalation
- **Impact:** Full system compromise possible
- **Action:** Do not install
- **Score Impact:** Auto-fail (score < 25)

#### HIGH
- **Examples:** Path traversal, insecure deserialization, SSRF, hardcoded credentials
- **Impact:** Significant security risk
- **Action:** Do not install without fixes
- **Score Impact:** Major deduction (score < 50)

#### MEDIUM
- **Examples:** Information disclosure, weak crypto, XSS, missing input validation
- **Impact:** Moderate risk
- **Action:** Install with caution, monitor
- **Score Impact:** Moderate deduction (score < 75)

#### LOW
- **Examples:** Minor hardening opportunities, non-security improvements
- **Impact:** Minimal risk
- **Action:** Safe to install, improvements suggested
- **Score Impact:** Small deduction (score < 90)

### Reading the Security Section

**Example:**

```markdown
### Security Analysis

**Score:** 45/100
**Risk Level:** High
**Recommendation:** ❌ DO NOT INSTALL

#### ❌ Critical Issues (2 found)

1. **Command Injection** in `scripts/handler.py:42`
   - Description: subprocess.run() with shell=True and user input
   - Code: `subprocess.run(f"process {user_file}", shell=True)`
   - Recommendation: Use list arguments without shell=True
   - Risk: Attacker can execute arbitrary commands

2. **Privilege Escalation** in `scripts/setup.sh:12`
   - Description: Unnecessary sudo usage
   - Code: `sudo chmod 777 /tmp/output`
   - Recommendation: Remove sudo; use proper permissions
   - Risk: Could grant elevated privileges maliciously
```

**What this means:**
- The skill has 2 CRITICAL vulnerabilities
- These are NOT THEORETICAL - they are real attack vectors
- Score of 45 triggers auto-fail
- **Do not install** until these are fixed

**How to respond:**
1. Contact skill author with findings
2. Request fixes for critical issues
3. Re-evaluate after fixes
4. Only install if score improves above 75

---

## Use Cases

### Use Case 1: Evaluating Third-Party Skills

**Scenario:** You found a useful-looking skill on GitHub but don't know if it's safe.

**Steps:**

1. **Download the skill**
   ```bash
   git clone https://github.com/user/cool-skill.git ~/Downloads/cool-skill
   ```

2. **Evaluate before installation**
   ```
   "Is ~/Downloads/cool-skill safe to install?"
   ```

3. **Review the report**
   - Check overall score
   - Look for CRITICAL or HIGH issues
   - Read security recommendations

4. **Make decision**
   - Score ≥ 75: Safe to install
   - Score 60-74: Install with caution
   - Score < 60: Do not install

### Use Case 2: Pre-Publication Quality Check

**Scenario:** You created a skill and want to publish it.

**Steps:**

1. **Run pre-publication review**
   ```
   "Review my skill before I publish: ~/projects/my-skill"
   ```

2. **Address priority fixes**
   - Fix CRITICAL and HIGH issues first
   - Address compliance violations
   - Remove TODO placeholders

3. **Improve based on suggestions**
   - Enhance documentation
   - Add type hints
   - Follow best practices

4. **Re-evaluate**
   ```
   "Re-evaluate my-skill after my improvements"
   ```

5. **Publish when ready**
   - Target score: ≥ 90 for excellent
   - Minimum score: ≥ 75 for good

### Use Case 3: Auditing Installed Skills

**Scenario:** You want to audit skills you installed months ago.

**Steps:**

1. **Locate installed skill**
   ```bash
   ls ~/.claude/plugins/
   ```

2. **Evaluate each skill**
   ```
   "Audit the security of my installed skill: old-skill"
   ```

3. **Review findings**
   - Check if vulnerabilities exist
   - Assess if skill still meets standards

4. **Take action**
   - Update if new version available
   - Uninstall if security risks found
   - Contact author about issues

### Use Case 4: Comparing Multiple Skills

**Scenario:** Choosing between 3 similar skills.

**Steps:**

1. **Evaluate all candidates**
   ```
   "Evaluate skill-a, skill-b, and skill-c"
   ```

2. **Compare scores**
   | Skill   | Score | Security | Quality | Recommendation |
   |---------|-------|----------|---------|----------------|
   | skill-a | 92    | 95       | 88      | ✅ Excellent   |
   | skill-b | 78    | 82       | 75      | ✅ Good        |
   | skill-c | 55    | 45       | 62      | ❌ Do not use  |

3. **Choose the best**
   - skill-a: Best choice (highest scores)
   - skill-b: Acceptable alternative
   - skill-c: Avoid (security concerns)

### Use Case 5: Continuous Monitoring

**Scenario:** Monitor critical skills over time.

**Steps:**

1. **Establish baseline**
   ```
   "Evaluate critical-skill and save baseline report"
   ```

2. **Re-evaluate periodically**
   - Monthly: `"Re-evaluate critical-skill"`
   - After updates: `"Check security after update"`

3. **Track changes**
   - Compare scores over time
   - Identify regressions
   - Verify improvements

4. **Respond to changes**
   - Investigate score drops
   - Update documentation
   - Report new vulnerabilities

---

## Best Practices

### For Skill Users

#### Before Installing Any Skill

1. **Always evaluate first**
   ```
   "Is [skill-path] safe to install?"
   ```

2. **Check the source**
   - Official marketplaces: Generally safer
   - GitHub repos: Review commits and contributors
   - Unknown sources: Extra caution

3. **Review the report carefully**
   - Don't ignore CRITICAL or HIGH issues
   - Read recommendations
   - Understand the risks

4. **Follow recommendations**
   - Score ≥ 75: Generally safe
   - Score 60-74: Understand risks first
   - Score < 60: Do not install

5. **Monitor after installation**
   - Watch for unusual behavior
   - Re-evaluate after updates
   - Report issues you find

#### During Evaluation

1. **Use the right mode**
   - Quick check: Security-focused
   - Detailed review: Full evaluation
   - Comparison: Evaluate all candidates

2. **Save evaluation reports**
   ```
   "Save the evaluation report to ~/evaluations/"
   ```

3. **Share findings**
   - Report vulnerabilities to authors
   - Share reports with team
   - Contribute to community safety

#### After Installation

1. **Test in safe environment first**
   - Use test directory
   - Don't give access to sensitive files
   - Monitor behavior

2. **Keep skills updated**
   - Check for security patches
   - Re-evaluate after updates
   - Uninstall if unmaintained

3. **Report issues**
   - Contact skill authors
   - Share security concerns
   - Help improve the ecosystem

### For Skill Authors

#### Before Publishing

1. **Self-evaluate early**
   ```
   "Review my skill before publication"
   ```

2. **Aim for high scores**
   - Target: ≥ 90 (excellent)
   - Minimum: ≥ 75 (good)
   - Never publish: < 60

3. **Fix all CRITICAL and HIGH issues**
   - Security vulnerabilities first
   - Quality issues second
   - Compliance problems third

4. **Follow recommendations**
   - Address priority fixes
   - Implement suggested improvements
   - Adopt best practices

#### During Development

1. **Follow security best practices**
   - Never use subprocess with shell=True
   - Validate all inputs
   - Sanitize outputs
   - Use secure functions

2. **Write quality code**
   - Add type hints
   - Include docstrings
   - Handle errors properly
   - Test thoroughly

3. **Document comprehensively**
   - Clear SKILL.md
   - Usage examples
   - Reference documentation
   - Security considerations

4. **Follow guidelines**
   - Use imperative form
   - Proper YAML frontmatter
   - Progressive disclosure
   - Correct directory structure

#### After Publishing

1. **Monitor feedback**
   - Watch for security reports
   - Respond to issues quickly
   - Release patches promptly

2. **Encourage evaluation**
   - Tell users to evaluate your skill
   - Share your evaluation score
   - Be transparent about findings

3. **Improve continuously**
   - Re-evaluate after changes
   - Track your score over time
   - Aim for continuous improvement

---

## Troubleshooting

### Common Issues

#### Issue: "Cannot find skill to evaluate"

**Symptoms:**
```
Error: Skill directory does not exist: /path/to/skill
```

**Solutions:**
1. Check the path is correct
2. Use absolute paths, not relative
3. Ensure directory exists
4. For .zip files, use full path with extension

**Example:**
```
# Wrong
"Evaluate my-skill"

# Right
"Evaluate /home/user/Downloads/my-skill"
"Evaluate C:/Users/user/Downloads/my-skill.zip"
```

---

#### Issue: "SKILL.md not found"

**Symptoms:**
```
CRITICAL: SKILL.md file missing
Score: 0
Recommendation: INVALID SKILL STRUCTURE
```

**Cause:** The skill doesn't have a required SKILL.md file

**Solutions:**
1. Verify it's actually a Claude skill (not a regular Python package)
2. Check if SKILL.md is named correctly (case-sensitive)
3. Ensure SKILL.md is in the skill root directory

---

#### Issue: "Invalid YAML syntax"

**Symptoms:**
```
CRITICAL: Invalid YAML syntax in frontmatter
```

**Cause:** SKILL.md has malformed YAML frontmatter

**Solutions:**
1. Check YAML starts and ends with `---`
2. Verify indentation (spaces, not tabs)
3. Ensure proper YAML syntax
4. Test YAML at yamllint.com

**Example of correct YAML:**
```yaml
---
name: my-skill
description: This is a description of my skill. It should be clear and specific.
---
```

---

#### Issue: "Python dependencies missing"

**Symptoms:**
```
ModuleNotFoundError: No module named 'yaml'
```

**Cause:** PyYAML not installed

**Solution:**
```bash
pip install -r ~/.claude/plugins/skill-evaluator/requirements.txt

# Or directly:
pip install PyYAML>=6.0
```

---

#### Issue: "Permission denied when running scripts"

**Symptoms:**
```
Error: Permission denied: /path/to/evaluate_skill.py
```

**Solutions:**

**On Linux/Mac:**
```bash
chmod +x ~/.claude/plugins/skill-evaluator/scripts/*.py
```

**On Windows:**
- Run Claude Code as Administrator (if needed)
- Check file permissions in Properties

---

#### Issue: "Evaluation takes too long"

**Symptoms:**
- Evaluation runs for several minutes
- No output or progress shown

**Causes:**
- Very large skill (many files)
- Complex code patterns
- Slow file I/O

**Solutions:**
1. Be patient - large skills take time
2. Check if scripts are actually running
3. Use security-focused mode for faster results
4. Break large skills into smaller components

---

#### Issue: "Report not generated"

**Symptoms:**
- Evaluation completes but no report file

**Solutions:**
1. Check if Claude displayed report in chat
2. Look for report in skill directory
3. Specify output path explicitly
4. Check disk space and permissions

**Example:**
```
"Evaluate my-skill and save report to ~/reports/my-skill-eval.md"
```

---

### Getting Help

#### Self-Help Resources

1. **Re-read this guide** - Many answers are here
2. **Check SKILL.md** - Detailed technical documentation
3. **Review reference docs** - In `references/` directory
4. **Examine example reports** - Learn from examples

#### Reporting Issues

If you find a bug or problem:

1. **Gather information**
   - Skill being evaluated
   - Evaluation mode used
   - Error message (full text)
   - Expected vs actual behavior

2. **Check if it's a known issue**
   - Review FAQ below
   - Search existing issues

3. **Report the issue**
   - Contact skill maintainer
   - Include reproduction steps
   - Provide example skill (if possible)
   - Share error logs

#### False Positives/Negatives

**False Positive:** Evaluator flags safe code as vulnerable

**Example:**
```python
# Safe code flagged incorrectly
result = subprocess.run(['ls', '-la'], shell=False)  # Flagged but actually safe
```

**What to do:**
- Verify it's truly safe
- Report false positive with context
- Document in your own notes
- Consider refactoring to avoid pattern

**False Negative:** Evaluator misses a real vulnerability

**Example:**
```python
# Vulnerable code not detected
dangerous_func(user_input)  # Novel attack pattern
```

**What to do:**
- Report immediately with details
- Do not install the skill
- Contact skill author
- Help improve detection patterns

---

## FAQ

### General Questions

**Q: Do I need to evaluate every skill?**

A: Highly recommended for third-party skills. Official/trusted skills from verified sources are generally safe, but evaluation provides confidence.

**Q: How long does evaluation take?**

A: Usually 10-30 seconds for small skills, up to 2-3 minutes for large, complex skills.

**Q: Can I evaluate skills I already installed?**

A: Yes! Evaluating installed skills is a great security practice. Evaluate them periodically.

**Q: Does evaluation modify the skill?**

A: No. Evaluation is read-only static analysis. It never modifies skill files.

**Q: Can I evaluate skills written in languages other than Python?**

A: Yes, but security detection is optimized for Python and Bash. Other languages may have limited vulnerability detection.

---

### Security Questions

**Q: Is the skill-evaluator itself safe?**

A: Yes. The skill-evaluator:
- Uses only standard library functions (except PyYAML)
- Performs read-only analysis
- Doesn't execute evaluated skill code
- Follows its own security best practices
- Can be self-evaluated!

**Q: What if evaluation finds critical vulnerabilities?**

A: **Do not install the skill.** Contact the skill author with findings. Only install after fixes are released and re-evaluation shows safety.

**Q: Can evaluated skills detect they're being evaluated?**

A: No. Evaluation is static analysis only. Skill code is not executed during evaluation.

**Q: Does evaluation catch all vulnerabilities?**

A: No. Evaluation uses pattern-based detection for known vulnerability types. Novel attack vectors may not be detected. Use evaluation as one layer of defense.

**Q: What happens if I install a skill that scored 40?**

A: **Don't!** Scores below 60 indicate significant problems. Below 40 is critical. Installing such skills poses serious security risks.

---

### Scoring Questions

**Q: What's a "good" score?**

A:
- Excellent: 90-100
- Good: 75-89 (safe to install)
- Fair: 60-74 (caution advised)
- Poor: Below 60 (do not install)

**Q: Why does my skill have a low score?**

A: Common reasons:
- Security vulnerabilities detected
- Poor code quality
- Incomplete documentation
- Compliance violations
- Lack of functionality

Check the detailed report for specific issues.

**Q: Can I challenge a low score?**

A: Review the findings carefully. If you believe it's a false positive, you can document why the flagged code is actually safe. However, most findings are legitimate issues to fix.

**Q: My skill scored 85. How do I get to 90+?**

A: Review the "Priority Improvements" and "Suggested Improvements" sections. Common improvements:
- Add type hints
- Improve documentation
- Remove TODOs
- Enhance error handling
- Fix minor compliance issues

---

### Technical Questions

**Q: What Python version is required?**

A: Python 3.7+ (for dataclasses support). Most modern systems have this.

**Q: What are the dependencies?**

A: Only PyYAML (for parsing YAML frontmatter). Everything else is Python standard library.

**Q: Can I run the evaluation scripts manually?**

A: Yes!
```bash
cd ~/.claude/plugins/skill-evaluator
python scripts/evaluate_skill.py /path/to/skill
```

**Q: Can I customize the evaluation criteria?**

A: Yes, advanced users can modify:
- `references/security_patterns.md` - Add vulnerability patterns
- `references/quality_criteria.md` - Adjust scoring
- `scripts/*.py` - Modify detection logic

**Q: Where are reports saved?**

A: By default, in the current directory as `{skill_name}_evaluation_report.md`. You can specify custom paths.

**Q: Can I automate evaluations in CI/CD?**

A: Yes! Use the CLI:
```bash
python evaluate_skill.py /path/to/skill --output report.md --json results.json
```

Check exit codes:
- 0: Safe to install (score ≥ 75)
- 1: Do not install (score < 40 or critical issues)
- 2: Caution advised (score 40-74)

---

### Troubleshooting Questions

**Q: Evaluation fails with "ModuleNotFoundError: yaml"**

A: Install dependencies:
```bash
pip install PyYAML>=6.0
```

**Q: How do I update the skill-evaluator?**

A:
1. Download new version
2. Replace old version in plugins directory
3. Restart Claude Code

**Q: Can I use this offline?**

A: Yes, once installed. Evaluation is completely local—no internet required.

**Q: The skill-evaluator isn't working. How do I debug?**

A:
1. Verify installation: Check `~/.claude/plugins/skill-evaluator` exists
2. Check dependencies: `pip list | grep PyYAML`
3. Test manually: `python ~/.claude/plugins/skill-evaluator/scripts/evaluate_skill.py --help`
4. Review logs: Check Claude Code logs for errors

---

## Appendix

### Example: Complete Evaluation Session

```
You: "I found a skill called 'file-analyzer' on GitHub. Can you
evaluate it before I install it? The path is ~/Downloads/file-analyzer"

Claude: I'll evaluate the file-analyzer skill for security and quality.

[Runs evaluation...]

# Skill Evaluation Report

**Skill Name:** file-analyzer
**Evaluation Date:** 2025-11-05
**Overall Score:** 78/100

## Executive Summary

**Recommendation:** ✅ RECOMMENDED
**Risk Level:** Medium

### Key Findings
- ✅ No critical security vulnerabilities
- ⚠️ 2 medium-risk security issues identified
- ✅ Good code quality and documentation
- ⚠️ Minor compliance violations (writing style)

## Detailed Analysis

### 1. Security Analysis
**Score:** 75/100
**Risk Level:** Medium

#### Medium-Risk Issues (2 found)
1. **Information Disclosure** in `scripts/analyzer.py:89`
   - Logging potentially sensitive file paths
   - Recommendation: Use relative paths in logs

2. **Missing Input Validation** in `scripts/processor.py:34`
   - File size not checked before processing
   - Recommendation: Add max file size limit

#### Security Strengths
- No command injection vulnerabilities
- Proper path validation
- Safe file operations

### 2. Quality Assessment
**Score:** 82/100
- Code Quality: 21/25 (Excellent)
- Documentation: 20/25 (Good - missing some examples)
- Structure: 22/25 (Very Good)
- Functionality: 19/25 (Good)

### 3. Utility Evaluation
**Score:** 80/100
- Practical value: High
- Solves real file analysis needs
- Good usability

### 4. Compliance Validation
**Score:** 72/100

#### Violations Found
- Uses second-person language ("you should") in 3 places
- Missing reference to scripts in SKILL.md

## Overall Recommendations

### Priority Fixes
1. Add file size validation (Medium priority)
2. Reduce logging verbosity (Low priority)

### Suggested Improvements
1. Convert second-person language to imperative form
2. Add usage examples to documentation
3. Add type hints to Python functions

## Conclusion

This skill demonstrates good quality and security practices with
no critical issues. The medium-risk issues found are manageable
and don't pose immediate threats. Recommended for installation,
especially after the suggested improvements.

**Recommendation:** ✅ Safe to install

---

You: "Thanks! Those medium-risk issues seem minor. I'll install it and
monitor for any issues. Can you save this report for my records?"

Claude: I've saved the evaluation report to:
~/Downloads/file-analyzer_evaluation_report.md

The skill is safe to install. The medium-risk issues are indeed minor
and don't pose immediate security threats. Good practice to monitor
any new skills after installation!
```

---

### Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│          SKILL EVALUATOR QUICK REFERENCE                │
├─────────────────────────────────────────────────────────┤
│ EVALUATION MODES                                        │
│ • Full: "Evaluate [skill-path]"                         │
│ • Security: "Is [skill-path] safe?"                     │
│ • Pre-pub: "Review my skill: [path]"                    │
├─────────────────────────────────────────────────────────┤
│ SCORE INTERPRETATION                                    │
│ • 90-100: ✅ EXCELLENT - Highly recommended             │
│ • 75-89:  ✅ GOOD - Recommended                         │
│ • 60-74:  ⚠️  FAIR - Use caution                        │
│ • 40-59:  ⚠️  POOR - Not recommended                    │
│ • 0-39:   ❌ CRITICAL - Do not install                  │
├─────────────────────────────────────────────────────────┤
│ VULNERABILITY SEVERITY                                  │
│ • CRITICAL: Auto-fail (command injection, code exec)    │
│ • HIGH: Major risk (path traversal, SSRF)              │
│ • MEDIUM: Moderate (info disclosure, weak crypto)      │
│ • LOW: Minor (hardening opportunities)                 │
├─────────────────────────────────────────────────────────┤
│ INSTALLATION DECISION TREE                              │
│ Score ≥ 90:  Install immediately                        │
│ Score 75-89: Install (safe)                             │
│ Score 60-74: Review findings, proceed with caution      │
│ Score 40-59: Do not install                             │
│ Score < 40:  NEVER install                              │
├─────────────────────────────────────────────────────────┤
│ AUTO-FAIL CONDITIONS                                    │
│ • Any CRITICAL vulnerability found                      │
│ • Security score < 50                                   │
│ • Missing SKILL.md or required YAML fields              │
└─────────────────────────────────────────────────────────┘
```

---

## Version History

**v1.0.0** (November 2025)
- Initial release
- 5-layer security architecture
- Multi-dimensional evaluation
- Markdown report generation
- Three evaluation modes

---

## Support & Feedback

For issues, questions, or feedback about the Skill Evaluator:

1. Review this guide thoroughly
2. Check the FAQ section
3. Consult SKILL.md for technical details
4. Report issues to skill maintainer

---

**Remember:** The Skill Evaluator is a powerful tool for assessing Claude skills, but it's not a substitute for good judgment. Always:
- Review evaluation reports carefully
- Understand the risks before installing
- Monitor skills after installation
- Report vulnerabilities you discover
- Help make the Claude skill ecosystem safer for everyone

Stay safe and happy skill evaluation! 🛡️
