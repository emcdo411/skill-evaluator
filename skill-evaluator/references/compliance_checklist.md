# Compliance Checklist

This reference document validates skills against skill-creator guidelines and best practices.

## Skill Creator Guidelines Compliance

### Required Components

#### 1. SKILL.md File (REQUIRED)
- [ ] SKILL.md file exists at skill root
- [ ] File is readable and valid markdown
- [ ] YAML frontmatter present
- [ ] Markdown content present after frontmatter

**Scoring:**
- Missing SKILL.md: **0 points (FAIL)**
- Present and valid: **10 points**

---

#### 2. YAML Frontmatter (REQUIRED)

**Required Fields:**
- [ ] `name:` field present
- [ ] `description:` field present

**Name Requirements:**
- [ ] Name matches directory name
- [ ] Uses lowercase with hyphens (e.g., `skill-name`)
- [ ] No spaces or special characters
- [ ] Descriptive and clear

**Description Requirements:**
- [ ] Describes what the skill does (not generic)
- [ ] Explains when to use it
- [ ] Uses third-person perspective
- [ ] Specific and actionable (not vague)
- [ ] Between 50-300 words

**Scoring:**
- Missing required fields: **0 points (FAIL)**
- Invalid name format: **-5 points**
- Name mismatch: **-5 points**
- Generic description: **-5 to -10 points**
- Wrong perspective (not third-person): **-3 points**
- Full compliance: **20 points**

---

#### 3. Progressive Disclosure Design

**Metadata (Always Loaded):**
- [ ] Name is concise (~2-4 words)
- [ ] Description is clear and focused (~100 words)
- [ ] Frontmatter is minimal

**SKILL.md Body (Loaded When Triggered):**
- [ ] Under 5,000 words preferred
- [ ] Focuses on procedures and workflows
- [ ] References bundled resources
- [ ] Not duplicating reference content

**Bundled Resources (Loaded As Needed):**
- [ ] Scripts in `scripts/` directory
- [ ] References in `references/` directory
- [ ] Assets in `assets/` directory
- [ ] Resources are actually used

**Scoring:**
- Excellent separation: **15 points**
- Good separation: **10 points**
- Poor separation (everything in SKILL.md): **5 points**
- Violations: **0 points**

---

### Bundled Resources Standards

#### Scripts Directory (`scripts/`)

**Purpose:** Executable code for tasks requiring deterministic reliability or repeatedly rewritten.

**Compliance Checks:**
- [ ] Scripts are executable (.py, .sh, .js, etc.)
- [ ] Scripts have proper shebang lines
- [ ] Scripts handle errors gracefully
- [ ] Scripts are documented in SKILL.md
- [ ] Scripts solve real problems (not trivial)

**Anti-patterns:**
- ❌ Scripts that should be in SKILL.md instructions
- ❌ One-liner scripts with no complexity
- ❌ Scripts that are never referenced
- ❌ Overly complex scripts that are hard to maintain

**Scoring:**
- Appropriate use: **10 points**
- Minor issues: **5-8 points**
- Misuse: **0-4 points**

---

#### References Directory (`references/`)

**Purpose:** Documentation and reference material loaded as needed into context.

**Compliance Checks:**
- [ ] Contains documentation/knowledge (not code)
- [ ] Files are markdown or readable text
- [ ] Referenced in SKILL.md
- [ ] Provides value beyond SKILL.md
- [ ] Not duplicating SKILL.md content

**Good Examples:**
- ✅ Database schemas
- ✅ API documentation
- ✅ Company policies
- ✅ Domain-specific knowledge
- ✅ Detailed workflow guides

**Anti-patterns:**
- ❌ Duplicating SKILL.md instructions
- ❌ Trivial content that should be in SKILL.md
- ❌ Binary files
- ❌ Unreferenced files

**Scoring:**
- Excellent use: **10 points**
- Good use: **7-9 points**
- Minimal value: **4-6 points**
- Misuse: **0-3 points**
- Not applicable (no references): **N/A**

---

#### Assets Directory (`assets/`)

**Purpose:** Files used in output (templates, images, fonts, boilerplate).

**Compliance Checks:**
- [ ] Files are used in skill output
- [ ] Not intended to be read into context
- [ ] Appropriate file types (images, templates, etc.)
- [ ] Referenced in SKILL.md
- [ ] Provide clear value

**Good Examples:**
- ✅ Logo images
- ✅ PowerPoint templates
- ✅ HTML/React boilerplate
- ✅ Font files
- ✅ Sample documents

**Anti-patterns:**
- ❌ Documentation files (should be in references)
- ❌ Scripts (should be in scripts)
- ❌ Unused files
- ❌ Files that should be generated dynamically

**Scoring:**
- Excellent use: **10 points**
- Good use: **7-9 points**
- Minimal value: **4-6 points**
- Misuse: **0-3 points**
- Not applicable (no assets): **N/A**

---

### Writing Style Compliance

#### Imperative/Infinitive Form (Required)

**Correct Style:**
- ✅ "To accomplish X, do Y"
- ✅ "Load the reference file"
- ✅ "Execute the script"
- ✅ "When users request X, perform Y"

**Incorrect Style:**
- ❌ "You should do X"
- ❌ "Claude should perform Y"
- ❌ "The user wants X"
- ❌ "We will do Y"

**Compliance Checks:**
- [ ] SKILL.md uses imperative form throughout
- [ ] No second-person language ("you", "your")
- [ ] Objective, instructional tone
- [ ] Consistent voice

**Scoring:**
- Perfect compliance: **10 points**
- Minor violations: **7-9 points**
- Frequent violations: **4-6 points**
- Non-compliant: **0-3 points**

---

### Skill Trigger Description

**Description Must Specify:**
- [ ] What the skill does (capabilities)
- [ ] When to use it (trigger conditions)
- [ ] Who it's for (use cases)

**Good Description Example:**
```yaml
description: Comprehensive evaluation toolkit for analyzing Claude skills
across security, quality, utility, and compliance dimensions. This skill
should be used when users need to evaluate a skill before installation,
review a skill before publishing, or assess overall skill quality and
safety.
```

**Poor Description Examples:**
```yaml
description: A skill for evaluating skills.
# ❌ Too vague

description: Use this skill to check skills for problems.
# ❌ Wrong perspective (not third-person)

description: Skill evaluator.
# ❌ Not descriptive enough
```

**Scoring:**
- Excellent description: **10 points**
- Good description: **7-9 points**
- Adequate: **4-6 points**
- Poor: **0-3 points**

---

## Compliance Score Calculation

### Total Compliance: 100 points

**Component Breakdown:**
1. SKILL.md existence: **10 points**
2. YAML frontmatter: **20 points**
3. Progressive disclosure: **15 points**
4. Scripts usage: **10 points**
5. References usage: **10 points**
6. Assets usage: **10 points**
7. Writing style: **10 points**
8. Trigger description: **10 points**
9. Overall adherence: **5 points**

**Score Ranges:**
- **90-100**: Fully compliant - Exemplary adherence
- **75-89**: Mostly compliant - Minor improvements
- **60-74**: Partially compliant - Several violations
- **40-59**: Non-compliant - Major violations
- **0-39**: Severely non-compliant - Fundamental issues

---

## Critical Violations (Auto-Fail)

These violations result in an automatic FAIL regardless of other scores:

1. **Missing SKILL.md** - Core requirement
2. **Missing required YAML fields** - name or description
3. **Invalid YAML syntax** - Cannot be parsed
4. **Empty SKILL.md** - No actual content
5. **Completely wrong structure** - No proper organization

---

## Compliance Validation Process

### Automated Checks
1. Check SKILL.md exists
2. Parse YAML frontmatter
3. Validate required fields
4. Check name matches directory
5. Verify directory structure
6. Check file placements
7. Scan for second-person language
8. Validate writing style

### Manual Review
1. Assess description quality
2. Evaluate progressive disclosure
3. Review bundled resource appropriateness
4. Check trigger clarity
5. Verify overall adherence to guidelines

---

## Recommendation Thresholds

### Compliance-Based Recommendations

**90-100 points:**
- Status: ✅ **COMPLIANT**
- Recommendation: Excellent adherence to guidelines
- Action: Ready for distribution

**75-89 points:**
- Status: ⚠️ **MOSTLY COMPLIANT**
- Recommendation: Minor improvements recommended
- Action: Address minor issues before distribution

**60-74 points:**
- Status: ⚠️ **PARTIALLY COMPLIANT**
- Recommendation: Several compliance issues to fix
- Action: Revision needed before distribution

**Below 60 points:**
- Status: ❌ **NON-COMPLIANT**
- Recommendation: Major rework required
- Action: Do not distribute until fixed

---

## Common Compliance Issues

### Frequent Violations
1. Generic descriptions that don't specify when to use
2. Using second-person ("you should") instead of imperative
3. Putting documentation in assets/ instead of references/
4. Overly complex SKILL.md that should use references/
5. Scripts that are trivial and should be instructions
6. Name doesn't match directory name
7. Missing references to bundled resources in SKILL.md
8. No clear trigger conditions in description

### Quick Fixes
- Rewrite description to third-person, specify triggers
- Convert "you should do X" to "Do X" or "To do X"
- Move files to correct directories
- Extract large content blocks to references/
- Remove trivial scripts, add instructions instead
- Rename skill or directory to match
- Add "Usage" section explaining bundled resources
- Enhance description with "This skill should be used when..."
