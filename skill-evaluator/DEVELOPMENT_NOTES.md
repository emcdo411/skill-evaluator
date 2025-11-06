# Development Notes

## Version Management Best Practices

### Key Finding: Synchronize Fallback VERSION with SKILL.md

**Date**: 2025-11-06
**Version**: 1.2.1

#### Implementation

The skill-evaluator uses a **dynamic version system** with fallback:

1. **Primary Source**: `SKILL.md` YAML frontmatter
   ```yaml
   ---
   name: skill-evaluator
   version: 1.2.1
   description: ...
   ---
   ```

2. **Fallback**: `scripts/report_generator.py`
   ```python
   class ReportGenerator:
       VERSION = "1.2.1"  # Fallback version
   ```

#### Critical Best Practice

**ALWAYS keep the fallback VERSION constant synchronized with SKILL.md version field.**

- The fallback should match the current working version
- If dynamic reading fails, reports will still show the correct version
- Don't let fallback drift to outdated versions (e.g., 1.0.0 when actual version is 1.2.1)

#### Version Update Checklist

When updating to a new version:

- [ ] Update `version:` field in `SKILL.md`
- [ ] Update `VERSION = "x.x.x"` constant in `scripts/report_generator.py`
- [ ] Verify both match by running:
  ```python
  from report_generator import ReportGenerator
  gen = ReportGenerator({...})
  assert gen.version == gen.VERSION  # Should be True
  ```
- [ ] Commit changes with version number in commit message
- [ ] Update release notes if applicable

#### How It Works

1. `ReportGenerator.__init__()` calls `self._get_version()`
2. `_get_version()` attempts to read `SKILL.md` and parse YAML frontmatter
3. If successful, returns version from SKILL.md
4. If any error occurs (file missing, malformed YAML, etc.), returns `self.VERSION` fallback
5. Result is stored in `self.version` and used in all reports

#### Benefits

- **Single source of truth**: SKILL.md is the canonical version location
- **Safe fallback**: If reading fails, still shows correct version (not outdated)
- **No code changes needed**: Just update SKILL.md for normal version bumps
- **Development flexibility**: Fallback allows testing even if SKILL.md is temporarily broken


## Windows Unicode Support

### Key Finding: Handle Unicode Gracefully on Windows

**Date**: 2025-11-06
**Version**: 1.2.2

#### Problem

Windows console (cmd.exe, PowerShell) uses cp1252 encoding by default, which cannot display Unicode characters like ✅, ❌, ⚠️, ✓. This caused `UnicodeEncodeError` when printing evaluation reports containing these characters.

#### Solution

Added multi-layered Unicode handling in `scripts/evaluate_skill.py`:

1. **Stdout Reconfiguration** (lines 25-33)
   ```python
   # Configure stdout encoding for Unicode support on Windows
   if sys.platform == 'win32':
       try:
           sys.stdout.reconfigure(encoding='utf-8')
       except (AttributeError, OSError):
           import codecs
           sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')
   ```

2. **Safe Print Function** (lines 36-50)
   ```python
   def safe_print(text: str) -> None:
       """Print text with Unicode, falling back to ASCII if needed."""
       try:
           print(text)
       except UnicodeEncodeError:
           # Replace Unicode with ASCII equivalents
           replacements = {
               '✅': '[OK]',
               '❌': '[X]',
               '⚠️': '[!]',
               '✓': '[+]',
           }
           for uni, asc in replacements.items():
               text = text.replace(uni, asc)
           print(text)
   ```

3. **Updated Print Calls**
   - Changed `print(report)` → `safe_print(report)`
   - Changed `print(json.dumps(...))` → `safe_print(json.dumps(...))`

#### Benefits

- **Cross-platform compatibility**: Works on Windows, Linux, macOS
- **Graceful degradation**: Falls back to ASCII if UTF-8 fails
- **User-friendly**: No error messages, just works
- **Professional appearance**: Unicode displays correctly when terminal supports it

#### Testing

Verified on Windows with:
```bash
python scripts/evaluate_skill.py path/to/skill
```

Result: Clean output with Unicode characters, exit code 0, no errors.

#### Unicode Characters Used

Reports contain these Unicode characters:
- ✅ `U+2705` - White Heavy Check Mark (success)
- ❌ `U+274C` - Cross Mark (error/failure)  
- ⚠️ `U+26A0` - Warning Sign (caution)
- ✓ `U+2713` - Check Mark (verified)

All handled gracefully with ASCII fallbacks: `[OK]`, `[X]`, `[!]`, `[+]`

