# Quality Assessment Criteria

This reference document defines quality standards for evaluating Claude skills.

## Quality Dimensions

### 1. Code Quality (25 points)

#### Script Quality
- **Clean, readable code** (5 points)
  - Consistent formatting and style
  - Meaningful variable names
  - Appropriate comments
  - No commented-out code

- **Error handling** (5 points)
  - Try-except blocks for expected failures
  - Graceful degradation
  - Clear error messages
  - No bare except clauses

- **Modularity** (5 points)
  - Functions with single responsibilities
  - Reusable components
  - Appropriate abstraction levels
  - No code duplication

- **Dependencies** (5 points)
  - Minimal external dependencies
  - Standard library preference
  - Clear requirements.txt if needed
  - Compatible versions

- **Best practices** (5 points)
  - Type hints in Python
  - Linting compliance
  - Consistent coding style
  - Performance considerations

---

### 2. Documentation Quality (25 points)

#### SKILL.md Quality
- **Clear purpose** (5 points)
  - Concise description of what skill does
  - When to use the skill
  - What problems it solves
  - Target audience clear

- **Usage instructions** (5 points)
  - Step-by-step procedures
  - Examples of invocation
  - Expected outcomes
  - Common use cases

- **Bundled resource references** (5 points)
  - Scripts documented
  - References explained
  - Assets described
  - Integration points clear

- **Writing quality** (5 points)
  - Imperative/infinitive form used consistently
  - Clear, concise language
  - Proper grammar and spelling
  - Well-organized sections

- **Completeness** (5 points)
  - No TODO placeholders left
  - All features documented
  - Edge cases mentioned
  - Limitations acknowledged

#### Reference Documentation
- Comprehensive and accurate
- Well-organized sections
- Examples provided
- Easy to search/grep

---

### 3. Structure & Organization (25 points)

#### Directory Structure
- **Proper organization** (8 points)
  - Scripts in `scripts/`
  - References in `references/`
  - Assets in `assets/`
  - No misplaced files

- **File naming** (7 points)
  - Descriptive, lowercase names
  - Hyphens for multi-word (skill-name)
  - Appropriate extensions
  - Consistent conventions

- **YAML frontmatter** (10 points)
  - Valid YAML syntax
  - Required fields present (name, description)
  - Name matches directory name
  - Description is specific and actionable
  - Third-person perspective

---

### 4. Functionality & Utility (25 points)

#### Practical Value
- **Solves real problems** (8 points)
  - Addresses genuine use cases
  - Saves time or effort
  - Not trivial functionality
  - Clear value proposition

- **Appropriate tool usage** (7 points)
  - Scripts for repeated tasks
  - References for knowledge
  - Assets for templates
  - Not over-engineered

- **Reusability** (5 points)
  - Applicable to multiple scenarios
  - Configurable where appropriate
  - Not overly specific
  - Generalizable approach

- **Completeness** (5 points)
  - All promised functionality works
  - No broken references
  - Dependencies available
  - No missing components

---

## Quality Score Calculation

### Total Score: 100 points (4 dimensions × 25 points)

**Score Ranges:**
- **90-100**: Excellent - Production-ready, exemplary quality
- **75-89**: Good - Minor improvements needed
- **60-74**: Fair - Several improvements recommended
- **40-59**: Poor - Significant issues to address
- **0-39**: Critical - Major rework required

### Scoring Guidelines

#### Code Quality Deductions
- Poor formatting: -2 to -5 points
- Missing error handling: -3 to -5 points
- Code duplication: -2 to -4 points
- Overly complex code: -2 to -5 points
- Unnecessary dependencies: -1 to -3 points
- No type hints (Python): -1 to -2 points

#### Documentation Deductions
- Unclear purpose: -3 to -5 points
- Missing usage examples: -3 to -5 points
- TODO placeholders: -2 to -5 points
- Poor writing quality: -2 to -4 points
- Incomplete documentation: -3 to -5 points
- Wrong voice (not imperative): -1 to -2 points

#### Structure Deductions
- Misplaced files: -2 to -5 points
- Poor naming conventions: -2 to -4 points
- Invalid YAML: -5 to -10 points
- Missing required fields: -5 points each
- Name mismatch: -5 points
- Generic description: -3 to -5 points

#### Functionality Deductions
- Trivial/no real value: -5 to -8 points
- Inappropriate tool choice: -2 to -5 points
- Over-engineered: -2 to -4 points
- Missing functionality: -3 to -5 points
- Broken references: -2 to -5 points
- Missing dependencies: -3 to -5 points

---

## Quality Checks

### Automated Checks
1. **YAML validation** - Parse frontmatter
2. **Required fields** - name, description present
3. **File structure** - Correct directories
4. **No TODOs** - Grep for TODO placeholders
5. **Script syntax** - Python/bash syntax check
6. **Broken links** - Check file references

### Manual Review Points
1. **Code readability** - Human judgment required
2. **Documentation clarity** - Comprehension check
3. **Practical utility** - Value assessment
4. **Appropriate complexity** - Over/under-engineering

---

## Red Flags

### Critical Quality Issues
- ❌ Missing or invalid YAML frontmatter
- ❌ Empty or placeholder SKILL.md
- ❌ Scripts with syntax errors
- ❌ Broken file references
- ❌ No actual functionality
- ❌ Generic/vague description

### Warning Signs
- ⚠️ Overly complex for task
- ⚠️ Poor code organization
- ⚠️ Minimal documentation
- ⚠️ Unclear purpose
- ⚠️ Too many dependencies
- ⚠️ No examples provided

---

## Best Practices Checklist

### Code
- [ ] Functions are focused and single-purpose
- [ ] Error handling covers expected failures
- [ ] Code is readable without excessive comments
- [ ] No hardcoded paths or credentials
- [ ] Dependencies are justified
- [ ] Type hints used (Python)

### Documentation
- [ ] Purpose is clear in 2-3 sentences
- [ ] Usage examples provided
- [ ] Imperative form used throughout
- [ ] All bundled resources explained
- [ ] No TODO placeholders
- [ ] Grammar and spelling checked

### Structure
- [ ] Files in correct directories
- [ ] Naming conventions followed
- [ ] YAML frontmatter valid
- [ ] Name matches directory
- [ ] Description is specific
- [ ] Third-person perspective in description

### Functionality
- [ ] Solves a real problem
- [ ] Scripts are necessary (not trivial)
- [ ] References contain useful knowledge
- [ ] Assets are appropriate
- [ ] Everything works as documented
- [ ] Value is clear to users
