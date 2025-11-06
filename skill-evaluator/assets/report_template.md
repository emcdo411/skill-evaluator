# Skill Evaluation Report

**Skill Name:** `{skill_name}`
**Evaluation Date:** {evaluation_date}
**Evaluator Version:** {evaluator_version}

---

## Executive Summary

### Overall Score: {overall_score}/100

**Recommendation:** {recommendation}

**Risk Level:** {risk_level}

### Score Breakdown

| Dimension | Score | Weight |
|-----------|-------|--------|
| **Security** | {security_score}/100 | 35% |
| **Quality** | {quality_score}/100 | 25% |
| **Utility** | {utility_score}/100 | 20% |
| **Compliance** | {compliance_score}/100 | 20% |
| **Overall** | **{overall_score}/100** | **100%** |

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

#### Breakdown
- **Problem-Solving Value:** {problem_solving_score}/25
- **Usability:** {usability_score}/25
- **Scope Appropriateness:** {scope_score}/25
- **Effectiveness:** {effectiveness_score}/25

#### Value Assessment

{value_assessment}

#### Use Cases

{use_cases}

#### Limitations

{limitations}

#### Utility Recommendations

{utility_recommendations}

---

### 4. Compliance Validation

**Score:** {compliance_score}/100

#### Standards Met

{standards_met}

#### Violations Found

{violations_found}

#### Progressive Disclosure Assessment

{progressive_disclosure}

#### Writing Style Review

{writing_style}

#### Compliance Recommendations

{compliance_recommendations}

---

## Overall Recommendations

### Priority Fixes

{priority_fixes}

### Suggested Improvements

{suggested_improvements}

### Best Practices to Adopt

{best_practices}

---

## Conclusion

{conclusion}

---

## ⚠️ Important Disclaimers

**READ CAREFULLY BEFORE ACTING ON THIS EVALUATION**

### No Guarantee of Safety

This evaluation **CANNOT determine with certainty that a skill is safe.** Security analysis has inherent limitations:

- **Cannot prove absence of vulnerabilities** - Static analysis detects known patterns but cannot prove a skill is vulnerability-free
- **False negatives are possible** - Novel attacks, obfuscated code, or sophisticated malicious techniques may evade detection
- **Static analysis limitations** - Cannot assess runtime behavior, dynamic execution, or context-dependent security risks
- **Time-bound assessment** - New vulnerabilities may be discovered after this evaluation was performed

### Use as ONE Input Only

**This evaluation should be used as ONE input into your security decision, not the sole determining factor.**

### Your Responsibilities

Before installing ANY skill, regardless of evaluation score:

1. **Manual code review** - Read and understand the skill's code yourself
2. **Test in isolation** - Run in sandboxed or test environments before production use
3. **Follow organizational policies** - Security policies override any recommendation in this report
4. **Assess your risk** - Consider your specific threat model, data sensitivity, and risk tolerance
5. **Monitor ongoing** - Continue monitoring skill behavior after installation

### You Are Responsible

- **YOU are responsible for skills you install** - Not this evaluator, not the skill author
- **Security policies take precedence** - If your organization prohibits certain actions, this report doesn't override that
- **"HIGHLY RECOMMENDED" ≠ "SAFE"** - Even top-scoring skills require review and may contain undiscovered vulnerabilities
- **When uncertain, consult experts** - If unsure about a skill's safety, seek guidance from security professionals

### Limitations of This Analysis

This tool performs **pattern-based static code analysis** with known limitations:

**✅ Can Detect:**
- Common vulnerability patterns (injection, traversal, etc.)
- Structural and organizational issues
- Compliance violations with skill-creator guidelines
- Code quality and documentation problems

**❌ Cannot Detect:**
- Zero-day exploits or novel attack vectors
- Logic bombs or time-delayed malicious behavior
- Social engineering or supply chain attacks
- Backdoors triggered by specific conditions
- Malicious intent disguised as legitimate functionality

**❌ Cannot Assess:**
- Author trustworthiness or reputation
- Long-term maintenance and support
- Runtime performance or behavior
- Compatibility with your specific environment

### Legal Disclaimer

**NO WARRANTIES**: This evaluation is provided "as-is" without warranties of any kind, express or implied. The authors and contributors of this tool assume NO LIABILITY for any damages, losses, security breaches, or other consequences resulting from:

- Use of this evaluation tool
- Reliance on evaluation results
- Installation of evaluated skills
- Any actions taken based on this report

**USE AT YOUR OWN RISK**: By using this evaluation, you acknowledge and accept all risks associated with skill installation and use.


---

*Report generated by skill-evaluator v{evaluator_version}*
