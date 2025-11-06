# CI/CD Troubleshooting Quick Reference

A rapid troubleshooting guide for common GitHub Actions CI/CD issues.

## Quick Diagnostics

```bash
# Run these commands locally to diagnose issues
python --version                    # Check Python version
pip --version                       # Check pip version
pytest --version                    # Check pytest version
flake8 --version                    # Check flake8 version
pytest --collect-only               # List all tests that will run
pytest -v                           # Run all tests with verbose output
flake8 . --count --statistics       # Count linting issues
```

## Common Issues → Solutions

### ❌ Issue: "No tests collected" (pytest exit code 5)

**Symptoms**: 
```
collected 0 items
ERROR: file or directory not found: tests
```

**Quick Fixes**:
```bash
# Verify test files exist
ls tests/test_*.py

# Check pytest configuration
cat setup.cfg

# Verify test naming convention
find tests/ -name "*.py" | grep test

# Run with verbose collection
pytest --collect-only -v
```

**Solutions**:
1. Ensure test files start with `test_` or end with `_test.py`
2. Add `__init__.py` to test directories
3. Check `setup.cfg` testpaths setting
4. Verify Python can import test modules

---

### ❌ Issue: Cache not restoring

**Symptoms**:
```
Cache not found for input keys: Linux-pip-abc123...
```

**Quick Fixes**:
```bash
# Check if requirements.txt exists
ls -l requirements.txt

# View cache key that will be generated
echo "Linux-pip-$(md5sum requirements.txt)"

# Clear local pip cache
rm -rf ~/.cache/pip
```

**Solutions**:
1. Verify `requirements.txt` exists and has content
2. Check cache key includes `hashFiles('**/requirements.txt')`
3. Cache may expire after 7 days of no use
4. Cache limit is 10GB per repository
5. Try clearing cache in GitHub Settings → Actions → Caches

---

### ❌ Issue: Python version not found

**Symptoms**:
```
Version 3.9 was not found in the local cache
```

**Quick Fixes**:
```yaml
# Use full version specifier
python-version: "3.9.18"  # Instead of "3.9"

# Or use version file
python-version-file: '.python-version'

# Or check available versions
- run: ls /opt/hostedtoolcache/Python/
```

**Solutions**:
1. Use major.minor version format: `"3.9"`, `"3.10"`, `"3.11"`
2. Check [available versions](https://github.com/actions/python-versions/releases)
3. Update `actions/setup-python` to latest version (v5)
4. Use `python-version-file` for consistency

---

### ❌ Issue: Module not found in tests

**Symptoms**:
```
ModuleNotFoundError: No module named 'your_module'
```

**Quick Fixes**:
```bash
# Install in editable mode
pip install -e .

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"

# Verify package structure
find . -name "__init__.py"

# List installed packages
pip list | grep your-package
```

**Solutions**:
1. Add `__init__.py` files to all package directories
2. Install package: `pip install -e .` or add to requirements.txt
3. Ensure PYTHONPATH includes project root
4. Use absolute imports in tests
5. Check that package name matches directory name

---

### ❌ Issue: Linting failures

**Symptoms**:
```
./your_module/file.py:42:1: E302 expected 2 blank lines, found 1
```

**Quick Fixes**:
```bash
# Fix automatically (safe changes)
pip install autopep8
autopep8 --in-place --aggressive --aggressive file.py

# Or use black formatter
pip install black
black file.py

# Check what will be fixed
autopep8 --diff file.py
```

**Common Violations**:
- `E302`: Need 2 blank lines between functions
- `E501`: Line too long (max 127 in this project)
- `F401`: Imported but unused
- `W291`: Trailing whitespace
- `E305`: Need 2 blank lines after class/function

**Solutions**:
1. Run `autopep8` for auto-fixes
2. Use editor with linting enabled (VS Code, PyCharm)
3. Configure pre-commit hooks
4. Check `.flake8` or `setup.cfg` for project rules

---

### ❌ Issue: Tests pass locally, fail in CI

**Possible Causes & Fixes**:

#### 1. **File Paths**
```python
# ❌ Bad: Hardcoded path
with open('/Users/me/data.txt') as f:
    data = f.read()

# ✅ Good: Relative path
from pathlib import Path
data_file = Path(__file__).parent / 'data.txt'
with open(data_file) as f:
    data = f.read()
```

#### 2. **Environment Variables**
```python
# ❌ Bad: Assumes env var exists
api_key = os.environ['API_KEY']

# ✅ Good: Default or skip
api_key = os.getenv('API_KEY', 'test-key')
if not api_key:
    pytest.skip("API_KEY not set")
```

#### 3. **Timezone Issues**
```python
# ❌ Bad: Assumes local timezone
now = datetime.now()

# ✅ Good: Explicit timezone
from datetime import timezone
now = datetime.now(timezone.utc)
```

#### 4. **External Dependencies**
```python
# ✅ Mock external calls
from unittest.mock import patch

@patch('requests.get')
def test_api_call(mock_get):
    mock_get.return_value.json.return_value = {'status': 'ok'}
    result = my_function()
    assert result == {'status': 'ok'}
```

---

### ❌ Issue: Dependency installation fails

**Symptoms**:
```
ERROR: Could not find a version that satisfies the requirement package==1.0.0
```

**Quick Fixes**:
```bash
# Update pip
python -m pip install --upgrade pip

# Check package exists
pip search package-name  # (deprecated, use Google)

# Install without version pin
pip install package-name

# Check for typos in requirements.txt
cat requirements.txt | grep package
```

**Solutions**:
1. Verify package name spelling
2. Check if package supports your Python version
3. Update outdated version pins
4. Remove version constraints if compatible
5. Check for platform-specific packages

---

### ❌ Issue: Timeout (job exceeds 6 hours)

**Symptoms**:
```
The job running on runner Hosted Agent has exceeded the maximum execution time of 360 minutes.
```

**Quick Fixes**:
```yaml
# Set shorter timeout
jobs:
  build:
    timeout-minutes: 30  # Default is 360

# Or for specific step
- name: Run tests
  run: pytest
  timeout-minutes: 10
```

**Solutions**:
1. Reduce test scope or split into jobs
2. Use pytest-xdist for parallel testing
3. Check for infinite loops or hangs
4. Optimize slow tests
5. Skip long-running integration tests in CI

---

### ❌ Issue: Out of memory

**Symptoms**:
```
Killed
```
or
```
MemoryError
```

**Quick Fixes**:
```yaml
# Use larger runner (GitHub paid plans)
runs-on: ubuntu-latest-l  # 4 cores, 16GB RAM

# Limit parallel execution
- run: pytest -n 2  # Instead of -n auto
```

**Solutions**:
1. Reduce memory usage in tests
2. Use `pytest-xdist` with limited workers
3. Split tests into separate jobs
4. Clean up large objects in tests
5. Use generators instead of lists for large datasets

---

### ❌ Issue: Flaky tests (intermittent failures)

**Symptoms**: Tests pass sometimes, fail randomly

**Diagnosis**:
```bash
# Run test multiple times
pytest tests/test_flaky.py -v --count=10

# With pytest-repeat
pip install pytest-repeat
pytest tests/test_flaky.py --count=100
```

**Common Causes**:
1. **Race conditions**: Use proper synchronization
2. **Random data**: Use fixed seeds `random.seed(42)`
3. **Timing issues**: Add retries or increase timeouts
4. **External API**: Mock all external calls
5. **Shared state**: Isolate tests with fixtures

**Solutions**:
```python
# Use fixtures for isolation
@pytest.fixture
def clean_state():
    # Setup
    state = {}
    yield state
    # Teardown
    state.clear()

# Use retries for flaky operations
import pytest
from pytest import mark

@mark.flaky(reruns=3, reruns_delay=1)
def test_flaky_operation():
    assert external_api_call()
```

---

## Quick Command Reference

### Local Testing Commands

```bash
# Full CI simulation
python -m pip install --upgrade pip
python -m pip install flake8 pytest
pip install -r requirements.txt
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
pytest -v

# Fast check (critical errors only)
flake8 . --select=E9,F63,F7,F82 && pytest

# Debug test collection
pytest --collect-only -v

# Run specific test
pytest tests/test_file.py::test_function -v

# Run with coverage
pytest --cov=your_module --cov-report=term

# Parallel execution
pytest -n auto
```

### GitHub Actions Commands

```bash
# View workflow runs
gh run list

# View specific run
gh run view <run-id>

# Download logs
gh run download <run-id>

# Rerun failed jobs
gh run rerun <run-id> --failed

# Watch run in real-time
gh run watch
```

### Cache Management

```bash
# List caches (requires gh CLI)
gh cache list

# Delete specific cache
gh cache delete <cache-id>

# Delete all caches (use with caution)
gh cache delete --all
```

## Debug Mode

### Enable GitHub Actions Debug Logging

**Repository Settings**:
1. Go to Settings → Secrets and variables → Actions
2. Add secret `ACTIONS_STEP_DEBUG` = `true`
3. Add secret `ACTIONS_RUNNER_DEBUG` = `true`

**In Workflow**:
```yaml
- name: Enable debug
  run: |
    echo "::debug::Debug message"
    echo "ACTIONS_STEP_DEBUG=true" >> $GITHUB_ENV
```

## Emergency Fixes

### Skip CI for a commit
```bash
git commit -m "WIP: Quick fix [skip ci]"
```

### Disable failing workflow temporarily
```yaml
# Add to workflow file
on:
  push:
    branches-ignore:
      - '**'  # Disable temporarily
```

### Force cache refresh
```yaml
# Change cache key to force refresh
key: ${{ runner.os }}-pip-v2-${{ hashFiles('**/requirements.txt') }}
#                            ^^^ increment version
```

## Health Check Script

Create this script to verify CI readiness:

```bash
#!/bin/bash
# ci-health-check.sh

echo "🔍 CI Health Check"
echo "==================="

# Check Python
python --version || echo "❌ Python not found"

# Check pip
pip --version || echo "❌ pip not found"

# Check requirements
if [ -f requirements.txt ]; then
    echo "✅ requirements.txt found"
else
    echo "❌ requirements.txt missing"
fi

# Check test directory
if [ -d tests ]; then
    echo "✅ tests/ directory found"
    test_count=$(find tests -name "test_*.py" | wc -l)
    echo "   Found $test_count test files"
else
    echo "❌ tests/ directory missing"
fi

# Check test collection
pytest --collect-only -q 2>&1 | grep "test session" || echo "❌ No tests collected"

# Check for syntax errors
flake8 . --select=E9,F63,F7,F82 --count || echo "❌ Syntax errors found"

echo ""
echo "Health check complete!"
```

Usage:
```bash
chmod +x ci-health-check.sh
./ci-health-check.sh
```

## Getting More Help

### Log Analysis

Look for these keywords in CI logs:
- `ERROR:` - Critical failures
- `FAILED` - Test failures  
- `ImportError` - Module import issues
- `ModuleNotFoundError` - Missing dependencies
- `AssertionError` - Test assertion failures
- `##[error]` - GitHub Actions errors
- `##[warning]` - GitHub Actions warnings

### Useful Links

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [pytest Documentation](https://docs.pytest.org/)
- [flake8 Rules](https://www.flake8rules.com/)
- [Full CI Documentation](./github-actions-runner-setup.md)

### Support Channels

1. Check existing [GitHub Issues](https://github.com/Trancendos/ai-passive-income-toolkit/issues)
2. Review [Discussions](https://github.com/Trancendos/ai-passive-income-toolkit/discussions)
3. Open new issue with `ci/cd` label

---

**Quick Tip**: 90% of CI issues are reproducible locally. Always test locally first!

**Last Updated**: 2025-11-06
