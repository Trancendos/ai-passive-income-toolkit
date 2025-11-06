# Contributing to CI/CD

This guide helps contributors understand and work with the CI/CD pipeline in this repository.

## Quick Start

### Running Tests Locally

Before pushing code, run tests locally to catch issues early:

```bash
# Install dependencies
pip install -r requirements.txt
pip install flake8 pytest

# Run linting
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# Run tests
pytest -v

# Or use the CI debug script
chmod +x scripts/ci_debug.sh
./scripts/ci_debug.sh
```

### Understanding CI Status

The CI runs automatically on:
- Every push to `main` branch
- Every pull request to `main` branch

**Matrix Testing**: Tests run on Python 3.9, 3.10, and 3.11 in parallel.

## CI Workflow Overview

```
┌─────────────────┐
│  Code Push/PR   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Checkout Code   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Setup Python    │
│ (3.9/3.10/3.11) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Restore Cache   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│Install Deps     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Lint (flake8)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Test (pytest)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  ✓ Success or   │
│  ✗ Failure      │
└─────────────────┘
```

## Common CI Tasks

### Adding a New Dependency

1. Add to `requirements.txt`
2. Update cache key if needed (done automatically via hash)
3. Test locally
4. Push and verify CI passes

### Adding a New Test

1. Create test file in `tests/` directory
2. Follow naming convention: `test_*.py` or `*_test.py`
3. Use pytest conventions
4. Run `pytest --collect-only` to verify collection
5. Run full test suite: `pytest -v`

### Updating Python Version Matrix

Edit `.github/workflows/python-package.yml`:

```yaml
matrix:
  python-version: ["3.9", "3.10", "3.11", "3.12"]  # Add new version
```

### Debugging CI Failures

1. **Check the logs** in GitHub Actions tab
2. **Look for**:
   - Dependency installation errors
   - Test failures
   - Linting errors
   - Timeout issues

3. **Common solutions**:
   ```bash
   # Recreate CI environment locally
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install --upgrade pip
   pip install flake8 pytest
   pip install -r requirements.txt
   
   # Run same commands as CI
   flake8 .
   pytest
   ```

4. **Enable debug mode**: Set repository secret `ACTIONS_STEP_DEBUG=true`

## Linting Standards

### What Gets Checked

1. **Critical Errors** (must pass):
   - E9: Syntax errors
   - F63: Invalid print statements
   - F7: Syntax errors in type comments
   - F82: Undefined names

2. **Style Warnings** (informational):
   - Max line length: 127 characters
   - Max complexity: 10
   - All other PEP 8 style issues

### Fixing Linting Issues

```bash
# Check for critical errors
flake8 . --select=E9,F63,F7,F82

# Check all issues
flake8 . --max-line-length=127 --max-complexity=10

# Auto-fix some issues (install autopep8)
pip install autopep8
autopep8 --in-place --aggressive --aggressive <filename>
```

## Testing Guidelines

### Test Structure

```python
# tests/test_feature.py
import pytest
from your_module import YourClass

class TestYourClass:
    """Test suite for YourClass"""
    
    def test_basic_functionality(self):
        """Test basic functionality"""
        obj = YourClass()
        assert obj.method() == expected_result
    
    def test_edge_case(self):
        """Test edge case handling"""
        obj = YourClass()
        with pytest.raises(ValueError):
            obj.method(invalid_input)
```

### Mocking External APIs

Always mock external API calls in tests:

```python
from unittest.mock import Mock, patch

def test_api_call(self):
    """Test API interaction"""
    with patch('module.api_client') as mock_api:
        mock_api.return_value = {'status': 'success'}
        result = function_that_calls_api()
        assert result['status'] == 'success'
```

### Running Specific Tests

```bash
# Run specific test file
pytest tests/test_feature.py

# Run specific test class
pytest tests/test_feature.py::TestYourClass

# Run specific test method
pytest tests/test_feature.py::TestYourClass::test_method

# Run tests matching pattern
pytest -k "test_api"

# Run with verbose output
pytest -v

# Run with coverage
pip install pytest-cov
pytest --cov=your_module --cov-report=html
```

## Performance Optimization

### Speed Up CI Runs

1. **Cache is key**: Dependency caching saves 30-60 seconds per run
2. **Run tests in parallel** (if you have many):
   ```bash
   pip install pytest-xdist
   pytest -n auto
   ```
3. **Skip unnecessary matrix combinations**:
   ```yaml
   matrix:
     python-version: ["3.9", "3.11"]  # Test min and max only
   ```

### Monitoring CI Performance

Check workflow run times in GitHub Actions:
- Target: < 5 minutes per job
- Warning: > 10 minutes per job
- Action needed: > 15 minutes per job

## Troubleshooting Checklist

When CI fails, check in this order:

- [ ] Does it pass locally? (`pytest` and `flake8`)
- [ ] Are all dependencies in `requirements.txt`?
- [ ] Is the Python version compatible?
- [ ] Are there file path issues? (use `pathlib` for cross-platform)
- [ ] Are there timezone/locale issues?
- [ ] Are environment variables/secrets configured?
- [ ] Is there a syntax error in workflow YAML?
- [ ] Is the cache corrupted? (clear and retry)

## CI Configuration Files

### Key Files to Know

| File | Purpose |
|------|---------|
| `.github/workflows/python-package.yml` | Main CI workflow |
| `scripts/ci_debug.sh` | Debug script for test collection |
| `requirements.txt` | Python dependencies |
| `setup.cfg` | pytest configuration |
| `.gitignore` | Files excluded from git |

### Workflow Configuration

```yaml
# .github/workflows/python-package.yml
name: Python package

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11"]
    steps:
      # Steps defined here
```

### pytest Configuration

```ini
# setup.cfg
[tool:pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
```

## Best Practices

### Before Committing

```bash
# Run pre-commit checks
flake8 . --select=E9,F63,F7,F82
pytest -v
git status  # Verify only intended files
```

### Writing CI-Friendly Code

1. **Avoid hardcoded paths**: Use `pathlib` and relative paths
2. **Mock external dependencies**: No real API calls in tests
3. **Handle missing resources gracefully**: Check file existence
4. **Use environment variables**: For configuration
5. **Write deterministic tests**: Same input = same output

### Pull Request Checklist

- [ ] All tests pass locally
- [ ] New tests added for new features
- [ ] Linting passes
- [ ] Documentation updated
- [ ] CI badge shows passing
- [ ] No secrets or API keys in code

## Getting Help

### Resources

- **Full Documentation**: See `docs/ci/github-actions-runner-setup.md`
- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **pytest Docs**: https://docs.pytest.org/
- **flake8 Docs**: https://flake8.pycqa.org/

### Common Questions

**Q: Why does CI pass on one Python version but fail on another?**  
A: Different Python versions have different behaviors. Test locally with the failing version.

**Q: How do I skip CI for a commit?**  
A: Add `[skip ci]` or `[ci skip]` to commit message.

**Q: Can I run CI on my fork?**  
A: Yes! GitHub Actions work on forks automatically.

**Q: How do I add secrets for API testing?**  
A: Go to Settings → Secrets and variables → Actions → New repository secret

## Examples

### Adding a New Feature with Tests

```bash
# 1. Create feature branch
git checkout -b feature/new-feature

# 2. Write your code
vim your_module/new_feature.py

# 3. Write tests
vim tests/test_new_feature.py

# 4. Run tests locally
pytest tests/test_new_feature.py -v

# 5. Run linting
flake8 your_module/new_feature.py

# 6. Commit and push
git add your_module/new_feature.py tests/test_new_feature.py
git commit -m "Add new feature with tests"
git push origin feature/new-feature

# 7. Create pull request
# CI will run automatically
```

### Fixing a Failing Test

```bash
# 1. Pull latest changes
git pull origin main

# 2. Run failing test locally
pytest tests/test_feature.py::test_failing_test -v

# 3. Fix the issue
vim your_module/feature.py

# 4. Verify fix
pytest tests/test_feature.py::test_failing_test -v

# 5. Run full test suite
pytest -v

# 6. Commit fix
git commit -am "Fix failing test in feature"
git push
```

## Continuous Improvement

### Suggesting CI Improvements

If you have ideas to improve the CI pipeline:

1. Open an issue with label `ci/cd`
2. Describe the improvement
3. Include examples if possible
4. Estimate impact (time saved, errors prevented, etc.)

### Monitoring CI Health

Keep an eye on:
- Average run time per job
- Success rate over time
- Cache hit rate
- Flaky tests (pass/fail inconsistently)

---

**Questions?** Open an issue with the `ci/cd` label or ask in discussions.

**Last Updated**: 2025-11-06
