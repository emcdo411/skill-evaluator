# Evaluation Methodology

This reference document explains the comprehensive evaluation process and scoring system.

## Overview

The skill evaluator uses a multi-dimensional assessment framework with four core dimensions:

1. **Security** (0-100 points) - Vulnerability analysis and risk assessment
2. **Quality** (0-100 points) - Code quality, documentation, structure
3. **Utility** (0-100 points) - Practical value and effectiveness
4. **Compliance** (0-100 points) - Adherence to skill-creator guidelines

Each dimension is scored independently, then combined into an overall score with weighted recommendations.

---

## Evaluation Process

### Phase 1: Skill Discovery & Extraction

**Objective:** Locate and prepare the skill for analysis

**Steps:**
1. Accept skill path (directory or .zip file)
2. Extract .zip files to temporary directory
3. Validate basic structure (SKILL.md exists)
4. Parse YAML frontmatter
5. Identify bundled resources (scripts, references, assets)

**Output:** Skill manifest with file inventory

---

### Phase 2: Security Analysis

**Objective:** Identify vulnerabilities and security risks

**Process:**
1. **Static code analysis** of all scripts
   - Scan for vulnerability patterns from `security_patterns.md`
   - Check for command injection, path traversal, etc.
   - Analyze privilege escalation risks

2. **Configuration review**
   - Check for hardcoded credentials
   - Validate environment variable usage
   - Review permission requirements

3. **Input/output validation**
   - Assess user input handling
   - Check output sanitization
   - Verify file operation safety

4. **Resource access analysis**
   - File system access patterns
   - Network requests
   - System command execution

5. **5-Layer security check** (see security_patterns.md)
   - Layer 1: Input validation
   - Layer 2: Execution control
   - Layer 3: Output sanitization
   - Layer 4: Privilege management
   - Layer 5: Self-protection

**Scoring:**
- **CRITICAL vulnerability found:** 0-25 points
- **HIGH risk issues:** 25-50 points
- **MEDIUM risks:** 50-75 points
- **LOW risks or minor issues:** 75-90 points
- **No security issues:** 90-100 points

**Weight in overall score:** 35%

---

### Phase 3: Quality Assessment

**Objective:** Evaluate code quality, documentation, and structure

**Process:**
1. **Code quality analysis** (25 points)
   - Readability and style
   - Error handling
   - Modularity
   - Dependencies
   - Best practices

2. **Documentation quality** (25 points)
   - Purpose clarity
   - Usage instructions
   - Resource references
   - Writing quality
   - Completeness

3. **Structure & organization** (25 points)
   - Directory structure
   - File naming
   - YAML frontmatter
   - Proper organization

4. **Functionality & utility** (25 points)
   - Practical value
   - Tool appropriateness
   - Reusability
   - Completeness

**Scoring:** See `quality_criteria.md` for detailed rubric

**Weight in overall score:** 25%

---

### Phase 4: Utility Evaluation

**Objective:** Assess practical value and effectiveness

**Criteria:**

1. **Problem-solving value** (25 points)
   - Addresses real user needs
   - Saves significant time/effort
   - Solves non-trivial problems
   - Clear value proposition

2. **Usability** (25 points)
   - Clear instructions
   - Easy to understand
   - Well-structured workflow
   - Good examples provided

3. **Scope appropriateness** (25 points)
   - Not too broad or narrow
   - Appropriate complexity
   - Well-defined boundaries
   - Focused purpose

4. **Effectiveness** (25 points)
   - Actually works as described
   - Produces expected results
   - Handles edge cases
   - Reliable performance

**Scoring:**
- **Excellent utility:** 90-100 points
- **Good utility:** 75-89 points
- **Moderate utility:** 60-74 points
- **Limited utility:** 40-59 points
- **Minimal/no utility:** 0-39 points

**Weight in overall score:** 20%

---

### Phase 5: Compliance Validation

**Objective:** Verify adherence to skill-creator guidelines

**Process:**
1. Check required components (SKILL.md, YAML)
2. Validate YAML frontmatter structure
3. Assess progressive disclosure design
4. Review bundled resource usage
5. Check writing style (imperative form)
6. Evaluate trigger description quality

**Scoring:** See `compliance_checklist.md` for detailed criteria

**Critical violations (auto-fail):**
- Missing SKILL.md
- Missing required YAML fields
- Invalid YAML syntax
- Empty content
- Fundamentally wrong structure

**Weight in overall score:** 20%

---

## Overall Score Calculation

### Weighted Formula

```
Overall Score = (Security × 0.35) + (Quality × 0.25) + (Utility × 0.20) + (Compliance × 0.20)
```

**Rationale:**
- **Security (35%)** - Highest weight due to critical importance
- **Quality (25%)** - Important for maintainability and usability
- **Utility (20%)** - Practical value matters
- **Compliance (20%)** - Ensures consistency and best practices

### Score Ranges & Interpretation

**90-100: EXCELLENT**
- ✅ Highly recommended for installation
- All dimensions score well
- No critical issues
- Exemplary implementation

**75-89: GOOD**
- ✅ Recommended for installation
- Minor improvements possible
- No major concerns
- Solid implementation

**60-74: FAIR**
- ⚠️ Use with caution
- Several issues to address
- May require fixes
- Consider alternatives

**40-59: POOR**
- ⚠️ Not recommended
- Significant problems
- Major improvements needed
- Risky to use

**0-39: CRITICAL**
- ❌ Do not install
- Critical issues present
- Fundamental problems
- Potentially dangerous

---

## Special Considerations

### Security Override

If **Security score < 50**, overall recommendation is automatically:
- ❌ **DO NOT INSTALL** (regardless of other scores)
- Rationale: Security risks outweigh other benefits

### Critical Vulnerability Override

If **ANY critical vulnerability** is found:
- ❌ **DO NOT INSTALL** (regardless of overall score)
- Examples: Command injection, arbitrary code execution, privilege escalation

### Compliance Failure Override

If **Compliance score < 40**:
- ⚠️ **NOT RECOMMENDED** (even if other scores are high)
- Rationale: Fundamental structural problems indicate quality issues

---

## Report Structure

### Executive Summary Section
1. **Overall Score** (0-100)
2. **Recommendation** (Install / Use with Caution / Do Not Install)
3. **Key Findings** (3-5 bullet points)
4. **Risk Level** (Low / Medium / High / Critical)

### Detailed Analysis Sections

#### 1. Security Analysis
- Score: X/100
- Risk level: Low/Medium/High/Critical
- Vulnerabilities found (if any):
  - Critical issues
  - High-risk issues
  - Medium-risk issues
  - Low-risk issues
- Security strengths
- Recommendations

#### 2. Quality Assessment
- Score: X/100
- Code quality: X/25
- Documentation: X/25
- Structure: X/25
- Functionality: X/25
- Strengths
- Weaknesses
- Recommendations

#### 3. Utility Evaluation
- Score: X/100
- Problem-solving value: X/25
- Usability: X/25
- Scope: X/25
- Effectiveness: X/25
- Value assessment
- Use cases
- Limitations
- Recommendations

#### 4. Compliance Validation
- Score: X/100
- Standards met
- Violations found
- Progressive disclosure assessment
- Writing style review
- Recommendations

### Recommendations Section
- Priority fixes (if any)
- Suggested improvements
- Best practices to adopt
- Overall guidance

---

## Evaluation Modes

### Mode 1: Full Evaluation
**Usage:** "Evaluate this skill"

**Process:** Complete analysis across all four dimensions

**Output:** Comprehensive report with detailed findings

**Use case:** Thorough assessment before installation or publication

---

### Mode 2: Security-Focused Quick Check
**Usage:** "Is this skill safe to install?"

**Process:** Deep security analysis, brief quality/utility/compliance check

**Output:** Security-focused report with install recommendation

**Use case:** Quick safety verification before installation

---

### Mode 3: Pre-Publication Review
**Usage:** "Review my skill before I publish it"

**Process:** Full evaluation with actionable improvement suggestions

**Output:** Detailed report with prioritized recommendations for authors

**Use case:** Skill authors preparing for distribution

---

## Continuous Improvement

### Pattern Database Updates

The evaluation methodology relies on up-to-date pattern databases:

1. **Security patterns** - Add new vulnerability types as discovered
2. **Quality criteria** - Refine based on skill ecosystem evolution
3. **Compliance rules** - Update when skill-creator guidelines change

### Scoring Calibration

Regular calibration ensures consistent scoring:

1. Test against known good/bad skills
2. Adjust weights if needed
3. Refine thresholds based on ecosystem standards
4. Document scoring rationale changes

---

## Limitations

### What This Evaluation Can Assess
- ✅ Static code analysis
- ✅ Structure and organization
- ✅ Documentation quality
- ✅ Compliance with guidelines
- ✅ Common vulnerability patterns

### What This Evaluation Cannot Assess
- ❌ Runtime behavior (requires execution)
- ❌ Performance at scale
- ❌ Integration with specific environments
- ❌ Novel attack vectors not in pattern database
- ❌ Subjective user satisfaction

### Recommendations
- Use evaluation as a strong signal, not absolute truth
- Test skills in safe environments before production use
- Stay updated on new security vulnerabilities
- Report false positives/negatives to improve the evaluator
- Combine automated evaluation with human review for critical skills
