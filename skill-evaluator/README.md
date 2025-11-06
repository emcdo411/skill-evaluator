# skill-evaluator

**Version**: 1.2.1  
**Status**: Production Ready  
**License**: MIT (or your choice)

Comprehensive evaluation toolkit for analyzing Claude skills across security, quality, utility, and compliance dimensions.

## Quick Start

```bash
# Evaluate a skill
python scripts/evaluate_skill.py /path/to/skill

# Security-focused evaluation
python scripts/evaluate_skill.py --mode security /path/to/skill

# Pre-publication review
python scripts/evaluate_skill.py --mode pre-publish /path/to/skill

# Save report to file
python scripts/evaluate_skill.py -o report.md /path/to/skill
```

## Features

### v1.2.1 (Current)

✅ **4-Dimensional Evaluation**
- Security (35% weight) - 5-layer defense-in-depth architecture
- Quality (25% weight) - Code, documentation, structure, functionality
- Utility (20% weight) - Problem-solving value and usability
- Compliance (20% weight) - Skill-creator guidelines validation

✅ **Advanced Security Scanning**
- Hybrid scanner with zero false positives
- Pattern-based vulnerability detection
- Context-aware analysis with ignore markers
- Directory and file exclusions

✅ **Professional Reports**
- Detailed markdown reports with scores breakdown
- Executive summaries with recommendations
- Risk level assessment aligned with recommendations
- Comprehensive security disclaimers

✅ **Cross-Platform Support**
- Windows Unicode handling
- macOS and Linux compatible
- Graceful error handling

## Documentation

- **[SKILL.md](SKILL.md)** - Complete usage guide and reference
- **[VERSION_ROADMAP.md](VERSION_ROADMAP.md)** - Version history and v2.0 plans
- **[FUTURE_ENHANCEMENTS.md](FUTURE_ENHANCEMENTS.md)** - Detailed v2.0 designs
- **[DEVELOPMENT_NOTES.md](DEVELOPMENT_NOTES.md)** - Technical implementation notes

## Current Scores

Self-evaluation results for skill-evaluator v1.2.1:

| Dimension | Score | Grade |
|-----------|-------|-------|
| Security | 100.0/100 | Perfect ✅ |
| Quality | 90.3/100 | Excellent ✅ |
| Utility | 100.0/100 | Perfect ✅ |
| Compliance | 95.0/100 | Excellent ✅ |
| **Overall** | **96.9/100** | **HIGHLY RECOMMENDED** ✅ |

## What's Next?

### v2.0 (Planned Q2 2026)

🔮 **Community Trust Score** - 5th dimension incorporating:
- GitHub stars, forks, contributors
- Author reputation and track record
- Download counts and community ratings
- Maintenance activity and engagement

See [VERSION_ROADMAP.md](VERSION_ROADMAP.md) for complete v2.0 plans.


## Installation

### Prerequisites

- **Python 3.8+** (required for evaluation scripts)
- **PyYAML** library

Install PyYAML:
```bash
pip install pyyaml
```

### For Claude Code (CLI/Desktop)

**Recommended Method**: Install as a plugin

#### Option 1: Install from Directory

1. Clone or download this repository
2. Copy the skill to your Claude plugins directory:

**macOS/Linux**:
```bash
cp -r skill-evaluator ~/.claude/plugins/
```

**Windows**:
```powershell
xcopy /E /I skill-evaluator "%USERPROFILE%\.claude\plugins\skill-evaluator"
```

#### Option 2: Install from ZIP

1. Download `skill-evaluator.zip`
2. Extract to your Claude plugins directory:

**macOS/Linux**:
```bash
unzip skill-evaluator.zip -d ~/.claude/plugins/
```

**Windows**:
```powershell
# Using PowerShell
Expand-Archive -Path skill-evaluator.zip -DestinationPath "$env:USERPROFILE\.claude\plugins"
```

#### Verify Installation

After installation, Claude should recognize the skill. Test it:

```
"Evaluate the skill at ~/.claude/plugins/skill-evaluator"
```

### For Claude on the Web (claude.ai)

**Note**: Claude on the web does not currently support custom plugins/skills. You can:

1. **Use via Claude Desktop/Code** - Install Claude Code CLI for full skill support
2. **Manual Execution** - Copy the Python scripts and run them locally:
   ```bash
   git clone <this-repo>
   cd skill-evaluator
   python scripts/evaluate_skill.py /path/to/skill
   ```
3. **Copy Prompts** - Use the evaluation criteria from `references/` as context in web conversations

### For Enterprise/Team Use

#### Shared Installation

Place skill in a shared location and symlink:

**macOS/Linux**:
```bash
ln -s /shared/skills/skill-evaluator ~/.claude/plugins/skill-evaluator
```

**Windows** (as Administrator):
```powershell
mklink /D "%USERPROFILE%\.claude\plugins\skill-evaluator" "C:\Shared\Skills\skill-evaluator"
```

#### Custom Plugin Directory

Set custom plugin location via environment variable:
```bash
export CLAUDE_PLUGINS_DIR=/custom/path/to/plugins
```

### Troubleshooting Installation

#### Skill Not Recognized

1. Check the plugin directory exists:
   ```bash
   ls ~/.claude/plugins/skill-evaluator
   ```

2. Verify SKILL.md exists:
   ```bash
   cat ~/.claude/plugins/skill-evaluator/SKILL.md
   ```

3. Restart Claude Code/Desktop

#### Python Dependencies

If evaluation fails with import errors:

```bash
# Check Python version
python --version  # Should be 3.8+

# Install PyYAML
pip install pyyaml

# If using virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install pyyaml
```

#### Permission Issues

**macOS/Linux**:
```bash
chmod -R 755 ~/.claude/plugins/skill-evaluator
```

**Windows**:
Right-click folder → Properties → Security → Ensure your user has Read & Execute permissions

### Plugin Directory Locations

Default plugin directories by platform:

| Platform | Path |
|----------|------|
| **macOS** | `~/.claude/plugins/` |
| **Linux** | `~/.claude/plugins/` |
| **Windows** | `%USERPROFILE%\.claude\plugins\` |

Full path examples:
- macOS: `/Users/username/.claude/plugins/skill-evaluator`
- Linux: `/home/username/.claude/plugins/skill-evaluator`
- Windows: `C:\Users\username\.claude\plugins\skill-evaluator`

## Requirements

- Python 3.8+
- PyYAML

```bash
pip install pyyaml
```


## Usage Examples

### Example 1: Quick Security Check
```bash
python scripts/evaluate_skill.py --mode security ~/downloads/new-skill.zip
```

### Example 2: Pre-Publication Review
```bash
python scripts/evaluate_skill.py --mode pre-publish ~/my-skill/
```

### Example 3: Full Evaluation with JSON
```bash
python scripts/evaluate_skill.py \
  -o report.md \
  --json results.json \
  ~/skills/my-skill/
```

## Important Disclaimers

⚠️ **This evaluation CANNOT determine with certainty that a skill is safe.**

This tool provides **pattern-based static analysis** as ONE input into your security decision. You are responsible for:

1. Manual code review
2. Testing in isolated environments
3. Following organizational security policies
4. Assessing your specific risk tolerance
5. Ongoing monitoring after installation

See report disclaimers for complete limitations.

## Contributing

Contributions welcome! Please:

1. Review [FUTURE_ENHANCEMENTS.md](FUTURE_ENHANCEMENTS.md) for v2.0 plans
2. Open issues for bugs or feature requests
3. Submit PRs with clear descriptions
4. Follow existing code style

## License

MIT License - See [LICENSE](LICENSE) file for details.

Copyright (c) 2025 skill-evaluator contributors

## Credits

Developed for the Claude Code community.

Special thanks to:
- Claude skill-creator guidelines
- Security analysis best practices
- Community feedback and testing

---

**Evaluate responsibly. Trust, but verify. 🔍**
