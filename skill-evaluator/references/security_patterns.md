# Security Patterns Database

This reference document contains comprehensive security vulnerability patterns for evaluating Claude skills.

## 5-Layer Security Architecture

The skill evaluator implements a defense-in-depth approach with five security layers:

### Layer 1: Input Validation & Sanitization
- Path traversal detection
- Command injection prevention
- File type validation
- Size limit enforcement

### Layer 2: Execution Environment Control
- Sandboxing detection
- Permission verification
- Resource limit checks
- Temporary directory usage

### Layer 3: Output Sanitization
- Cross-site scripting (XSS) prevention
- Markdown injection detection
- File content validation
- Data exposure checks

### Layer 4: Privilege Management
- Least privilege principle
- Credential handling
- API key security
- Permission escalation detection

### Layer 5: Self-Protection
- Meta-injection prevention
- Skill manipulation detection
- Recursive execution limits
- Chain-of-trust validation

## Critical Vulnerability Patterns

### Command Injection

**High Risk Patterns:**
```python
# Direct user input in shell commands
os.system(user_input)
subprocess.call(user_input, shell=True)
subprocess.run(f"command {user_input}", shell=True)
eval(user_input)
exec(user_input)

# Bash command concatenation
bash -c "command $USER_INPUT"
sh -c "echo $1"
```

**Detection Criteria:**
- Use of `shell=True` without sanitization
- String concatenation in shell commands
- `eval()` or `exec()` with external input
- Backticks or `$()` in bash scripts with variables

**Risk Level:** CRITICAL

---

### Path Traversal

**High Risk Patterns:**
```python
# Unrestricted path operations
open(user_provided_path)
os.path.join(base, user_input)  # Without validation
Path(user_input)  # Without checking

# Directory traversal sequences
"../"
"../../"
"%2e%2e%2f"  # URL encoded
"..%5c"  # Windows backslash
```

**Detection Criteria:**
- File operations without path validation
- Missing `os.path.abspath()` or `Path.resolve()`
- No checks for `..` sequences
- Unrestricted file system access

**Risk Level:** CRITICAL

---

### Arbitrary File Write/Read

**High Risk Patterns:**
```python
# Writing user content to arbitrary locations
with open(user_path, 'w') as f:
    f.write(data)

# Reading without validation
file_contents = open(path).read()

# Overwriting system files
shutil.copy(src, "/etc/")
```

**Detection Criteria:**
- File writes outside designated directories
- No validation of target paths
- Ability to overwrite existing files
- Reading sensitive system files

**Risk Level:** CRITICAL

---

### Code Injection

**High Risk Patterns:**
```python
# Dynamic code execution
compile(user_code, '<string>', 'exec')
exec(open(user_file).read())
__import__(user_module)

# Template injection
eval(f"function({user_input})")
jinja2_template.render(user_data)  # Without autoescape
```

**Detection Criteria:**
- Use of `compile()`, `eval()`, `exec()`
- Dynamic imports from user paths
- Template rendering without escaping
- `pickle.loads()` with untrusted data

**Risk Level:** CRITICAL

---

### Privilege Escalation

**High Risk Patterns:**
```python
# Running commands as root/admin
subprocess.run(['sudo', 'command'])
os.setuid(0)
runas('Administrator', command)

# Modifying permissions
os.chmod(file, 0o777)
subprocess.run(['chmod', '+x', user_file])
```

**Detection Criteria:**
- Use of `sudo`, `su`, or privilege elevation
- Permission modifications (chmod, chown)
- setuid/setgid operations
- Windows `runas` commands

**Risk Level:** CRITICAL

---

### Environment Variable Manipulation

**High Risk Patterns:**
```python
# Setting dangerous env vars
os.environ['PATH'] = user_path
os.environ['LD_PRELOAD'] = user_lib
os.environ['PYTHONPATH'] = user_input

# Loading env vars without validation
api_key = os.getenv(user_variable)
```

**Detection Criteria:**
- Modifying PATH, LD_PRELOAD, LD_LIBRARY_PATH
- Setting PYTHONPATH, NODE_PATH
- Loading env vars by user-specified names
- Exposing credentials via environment

**Risk Level:** HIGH

---

### Denial of Service (DoS)

**High Risk Patterns:**
```python
# Infinite loops
while True:
    heavy_operation()

# Resource exhaustion
data = []
for i in range(999999999):
    data.append(large_object)

# Recursive bombs
def recurse():
    recurse()
```

**Detection Criteria:**
- Unbounded loops or recursion
- No timeout mechanisms
- Unlimited resource allocation
- Fork bombs or process spawning

**Risk Level:** HIGH

---

### Information Disclosure

**High Risk Patterns:**
```python
# Exposing sensitive data
print(f"API Key: {api_key}")
logging.info(f"Password: {password}")
error_message = str(exception)  # May contain paths/secrets

# Verbose error messages
traceback.print_exc()  # In production
sys.exc_info()  # Exposed to user
```

**Detection Criteria:**
- Logging credentials or API keys
- Exposing stack traces to users
- Including file paths in errors
- Verbose debugging in production

**Risk Level:** MEDIUM

---

### Cross-Site Scripting (XSS) in Output

**High Risk Patterns:**
```markdown
# Unescaped user input in markdown
<script>alert('xss')</script>
<img src=x onerror="alert('xss')">
[link](javascript:alert('xss'))

# HTML injection
<iframe src="evil.com">
<object data="payload">
```

**Detection Criteria:**
- Raw HTML in markdown output
- Unescaped user content
- JavaScript URLs in links
- Inline event handlers

**Risk Level:** MEDIUM

---

### Insecure Deserialization

**High Risk Patterns:**
```python
# Unsafe deserialization
pickle.loads(user_data)
yaml.load(user_yaml)  # Without SafeLoader
marshal.loads(user_input)

# Eval-based parsing
json_data = eval(user_string)
```

**Detection Criteria:**
- Use of `pickle`, `marshal` with untrusted data
- `yaml.load()` without `Loader=yaml.SafeLoader`
- Custom deserialization without validation
- Eval-based parsing

**Risk Level:** HIGH

---

### Hardcoded Credentials

**High Risk Patterns:**
```python
# Credentials in code
api_key = "sk_live_abc123xyz"
password = "admin123"
conn = psycopg2.connect("postgresql://user:pass@host/db")

# Tokens in scripts
headers = {"Authorization": "Bearer token123"}
```

**Detection Criteria:**
- API keys, passwords, tokens in source
- Database connection strings with credentials
- SSH keys or certificates embedded
- No use of environment variables or secret management

**Risk Level:** HIGH

---

### Weak Cryptography

**High Risk Patterns:**
```python
# Weak algorithms
hashlib.md5(password)
hashlib.sha1(data)

# Insecure random
random.randint(0, 999999)  # For security tokens

# No encryption
password = request.form['password']  # Stored plaintext
```

**Detection Criteria:**
- Use of MD5, SHA1 for passwords
- `random` module for cryptographic purposes
- Plaintext password storage
- Weak key derivation

**Risk Level:** MEDIUM

---

### Server-Side Request Forgery (SSRF)

**High Risk Patterns:**
```python
# Unvalidated URL fetching
requests.get(user_url)
urllib.request.urlopen(user_input)

# Internal network access
requests.get(f"http://localhost:{port}")
requests.get("http://169.254.169.254/")  # Cloud metadata
```

**Detection Criteria:**
- Fetching user-provided URLs
- No URL validation or allowlisting
- Access to private IP ranges
- Cloud metadata endpoint access

**Risk Level:** HIGH

---

### Regex Denial of Service (ReDoS)

**High Risk Patterns:**
```python
# Catastrophic backtracking
re.match(r'(a+)+b', user_input)
re.search(r'(a|a)*b', malicious_string)
re.match(r'(a|ab)*c', evil_input)
```

**Detection Criteria:**
- Nested quantifiers in regex
- Overlapping alternatives
- No timeout on regex matching
- User-controlled regex patterns

**Risk Level:** MEDIUM

---

## Secure Coding Patterns (Good Examples)

### Safe Command Execution
```python
# Use list form, no shell=True
subprocess.run(['ls', '-la', validated_dir])

# Validate and sanitize input
allowed_chars = set(string.ascii_letters + string.digits + '._-')
if not all(c in allowed_chars for c in user_input):
    raise ValueError("Invalid characters")
```

### Safe Path Handling
```python
# Validate and restrict paths
base_dir = Path("/safe/directory").resolve()
user_path = Path(user_input).resolve()

if not user_path.is_relative_to(base_dir):
    raise ValueError("Path outside allowed directory")
```

### Safe File Operations
```python
# Write to temporary directory
with tempfile.TemporaryDirectory() as tmpdir:
    safe_path = Path(tmpdir) / sanitized_filename
    with open(safe_path, 'w') as f:
        f.write(sanitized_content)
```

### Safe Output Handling
```python
# Escape markdown/HTML
import html
safe_output = html.escape(user_content)

# Use allowlists for markdown
allowed_tags = ['p', 'strong', 'em', 'code']
sanitized = bleach.clean(user_html, tags=allowed_tags)
```

---

## Scoring Guidelines

### Security Score Calculation

**Critical Issues (0-25 points each):**
- Command injection vulnerabilities
- Path traversal vulnerabilities
- Arbitrary code execution
- Privilege escalation

**High Issues (25-50 points each):**
- Weak authentication/authorization
- Information disclosure
- Insecure deserialization
- SSRF vulnerabilities

**Medium Issues (50-75 points each):**
- Missing input validation
- Weak cryptography
- Verbose error messages
- XSS in output

**Low Issues (75-90 points each):**
- Minor security improvements
- Hardcoded non-sensitive config
- Missing security headers

**Excellent (90-100 points):**
- No security issues found
- Implements defense-in-depth
- Follows secure coding practices
- Includes security documentation
