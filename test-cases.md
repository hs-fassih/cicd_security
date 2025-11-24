# Pre-commit Hook Testing

## Test Case 1: Black Code Formatter Hook

**Objective:** Verify that Black hook automatically formats Python code during commit

**Setup:**
1. Ensure pre-commit hooks are installed: `pre-commit install`
2. Create a new Python file with poorly formatted code

**Steps:**
1. Create a test file `test_format.py` with intentionally bad formatting:
```python
# Badly formatted python code example
def hello(    ):
    x=1
    y =2
    z= 3
    return x+y+z
```

2. Stage the file: `git add test_format.py`

3. Attempt to commit: `git commit -m "Test black formatter"`

**Expected Result:**
- ✓ Black hook runs automatically
- ✓ Code is reformatted to PEP 8 standards
- ✓ One of two outcomes:
  - **Option A**: Commit succeeds and file is auto-formatted
  - **Option B**: Commit fails, Black shows the changes needed, then re-run commit

**Formatted Output Example:**
```python
# After Black formatting
def hello():
    x = 1
    y = 2
    z = 3
    return x + y + z
```

**Pass Criteria:**
- ✓ Code is properly formatted (spaces, indentation, line length)
- ✓ File follows PEP 8 standards
- ✓ Line length respects 120-character limit

---

## Test Case 2: Gitleaks Secret Detection Hook

**Objective:** Verify that Gitleaks hook prevents committing hardcoded secrets

**Setup:**
1. Ensure pre-commit hooks are installed: `pre-commit install`
2. Create a test Python file with fake credentials

**Steps:**
1. Create a test file `test_secrets.py` with hardcoded secrets (PLACEHOLDER EXAMPLE):
```python
# DO NOT USE REAL CREDENTIALS - TEST ONLY
import os

# Hardcoded API Key
API_KEY = "[STRIPE_TEST_KEY_PLACEHOLDER]"

# Hardcoded Password
DB_PASSWORD = "[PASSWORD_PLACEHOLDER]"

# Hardcoded AWS Secret
AWS_SECRET = "[AWS_SECRET_PLACEHOLDER]"

# Hardcoded Slack Token
SLACK_TOKEN = "[SLACK_TOKEN_PLACEHOLDER]"
```

2. Stage the file: `git add test_secrets.py`

3. Attempt to commit: `git commit -m "Test gitleaks detector"`

**Expected Result:**
- ✓ Gitleaks hook runs automatically
- ✓ Hook detects hardcoded secrets
- ✓ Commit is BLOCKED with warning message
- ✓ Output shows detected secrets:
```
Gitleaks Report:
- Potential API Key found
- Potential AWS Secret found
- Potential Password found
- Potential Slack Token found
```

**Pass Criteria:**
- ✓ Commit is REJECTED (blocked)
- ✓ Gitleaks identifies all exposed credentials
- ✓ Clear error message prevents accidental push
- ✓ File must be modified/cleaned before commit succeeds

**Resolution Steps:**
To allow commit after fixing secrets:
1. Remove hardcoded credentials from file
2. Use environment variables instead:
```python
import os

# Correct way - using environment variables
API_KEY = os.getenv("API_KEY")
DB_PASSWORD = os.getenv("DB_PASSWORD")
AWS_SECRET = os.getenv("AWS_SECRET")
SLACK_TOKEN = os.getenv("SLACK_TOKEN")
```
3. Re-stage file: `git add test_secrets.py`
4. Commit again: `git commit -m "Test gitleaks detector - fixed secrets"`

**Cleanup:**
After testing, delete test files:
```bash
git rm test_format.py
git rm test_secrets.py
git commit -m "Remove test files"
```

---

## Summary of Hook Validation

| Hook | Test Case | Expected Behavior | Status |
|------|-----------|-------------------|--------|
| Black | Format Python code | Auto-formats or blocks commit until formatted | ✓ Pass |
| Gitleaks | Detect hardcoded secrets | Blocks commit with security warnings | ✓ Pass |

Both hooks successfully protect code quality and security! 🎉
