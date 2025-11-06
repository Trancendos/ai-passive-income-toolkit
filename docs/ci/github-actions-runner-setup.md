# GitHub Actions Runner Setup Documentation

## Overview

This document provides comprehensive information about the GitHub Actions runner environment used in this repository's CI/CD pipeline. It includes runner specifications, software inventory, setup process, and troubleshooting guidance.

## Runner Specifications

### Runner Environment
- **Runner Version**: 2.329.0
- **Commit**: 8ab8ac8bfd662a3739dab9fe09456aba92132568
- **Build Date**: 2025-10-15
- **Operating System**: Ubuntu 24.04.3 LTS
- **Image**: ubuntu-24.04
- **Image Version**: 20251030.96.2

### Hardware Resources
- **CPU**: 4-core
- **RAM**: 16 GB
- **Disk Space**: 14 GB (SSD storage)

### Official Documentation Links
- **Included Software**: [Ubuntu 24.04 Software Inventory](https://github.com/actions/runner-images/blob/ubuntu24/20251030.96/images/ubuntu/Ubuntu2404-Readme.md)
- **Image Release Notes**: [Release ubuntu24/20251030.96](https://github.com/actions/runner-images/releases/tag/ubuntu24%2F20251030.96)

## Pre-installed Software Highlights

The Ubuntu 24.04 runner image comes with extensive pre-installed software. Key packages relevant to this project include:

### Language Runtimes
- **Python**: 3.9, 3.10, 3.11, 3.12 (multiple versions available)
- **Node.js**: Multiple LTS versions
- **Ruby**: Multiple versions
- **Go**: Latest stable version
- **Java**: JDK 8, 11, 17, 21

### Development Tools
- **Git**: Latest version with Git LFS
- **Docker**: Docker Engine with Docker Compose
- **Build Tools**: gcc, g++, make, cmake
- **Package Managers**: pip, npm, yarn, gem, cargo

### Python Ecosystem
- **pip**: Latest version
- **virtualenv**: Pre-installed
- **setuptools**: Pre-installed
- **wheel**: Pre-installed

### Databases
- **PostgreSQL**: Client and server
- **MySQL**: Client and server
- **SQLite**: Latest version
- **Redis**: Latest version

### Cloud Tools
- **AWS CLI**: v2
- **Azure CLI**: Latest
- **Google Cloud SDK**: Latest

## CI Pipeline Setup Process

### Job Setup Phase

The GitHub Actions runner executes several initialization steps before running your workflow jobs:

1. **Environment Preparation**
   ```
   - Initialize workspace directory
   - Set environment variables
   - Configure runner context
   - Set up job container (if specified)
   ```

2. **Repository Checkout**
   ```yaml
   - uses: actions/checkout@v4
   ```
   - Clones repository to `$GITHUB_WORKSPACE`
   - Fetches git history (configurable depth)
   - Checks out specified branch/commit

3. **Python Environment Setup**
   ```yaml
   - uses: actions/setup-python@v3
     with:
       python-version: ${{ matrix.python-version }}
   ```
   - Downloads and installs specified Python version
   - Configures PATH to use selected Python
   - Sets up pip and setuptools
   - Configures virtual environment if needed

4. **Dependency Caching**
   ```yaml
   - uses: actions/cache@v4
     with:
       path: ~/.cache/pip
       key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}-flake8-pytest
   ```
   - Generates cache key from requirements file hash
   - Restores cached dependencies if available
   - Saves cache after successful installation

5. **Dependency Installation**
   ```bash
   python -m pip install --upgrade pip
   python -m pip install flake8 pytest
   pip install -r requirements.txt
   ```
   - Upgrades pip to latest version
   - Installs test and lint tools
   - Installs project dependencies

### Debug Output Analysis

The CI setup phase generates detailed debug logs that include:

- **Environment Variables**: System and custom variables
- **Runner Context**: Operating system, architecture, runner details
- **Path Configuration**: Binary paths, workspace location
- **Action Downloads**: GitHub Actions being used
- **Cache Operations**: Cache hits/misses, restoration status
- **Command Execution**: Each command with timing information

#### Key Debug Markers

```
##[debug]Starting: Set up job
##[debug]Runner name: 'Hosted Agent'
##[debug]Runner group name: 'GitHub Actions'
##[debug]Machine name: 'fv-az...'
##[debug]Finishing: Set up job
```

## Workflow Configuration

### Current Workflow: `python-package.yml`

```yaml
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
      fail-fast: false
      matrix:
        python-version: ["3.9", "3.10", "3.11"]

    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Cache pip dependencies
      uses: actions/cache@v4
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}-flake8-pytest
        restore-keys: |
          ${{ runner.os }}-pip-
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        python -m pip install flake8 pytest
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    
    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    
    - name: CI self-debug: list tests and run pytest --collect-only
      run: |
        chmod +x scripts/ci_debug.sh || true
        ./scripts/ci_debug.sh
    
    - name: Test with pytest (only run if tests collected)
      run: |
        pytest || rc=$?
        if [ "${rc:-0}" -eq 5 ]; then
          echo "No tests collected; skipping pytest run (treated as success for CI)."
          exit 0
        elif [ "${rc:-0}" -ne 0 ]; then
          echo "pytest failed with exit code ${rc}"
          exit "${rc}"
        fi
```

### Workflow Features

1. **Matrix Strategy**: Tests against multiple Python versions (3.9, 3.10, 3.11)
2. **Fail-fast Disabled**: All matrix jobs run even if one fails
3. **Dependency Caching**: Speeds up builds by caching pip packages
4. **Multi-stage Testing**: Linting, test collection, and test execution
5. **Error Handling**: Graceful handling of "no tests collected" scenario

## CI Setup Best Practices

### For Contributors

When setting up similar CI pipelines, follow these best practices:

#### 1. Python Version Matrix
```yaml
strategy:
  fail-fast: false
  matrix:
    python-version: ["3.9", "3.10", "3.11", "3.12"]
```
- Test against all supported Python versions
- Use `fail-fast: false` to see all version failures

#### 2. Dependency Caching
```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```
- Include requirements file hash in cache key
- Use restore-keys for partial cache matches
- Cache location: `~/.cache/pip` for pip

#### 3. Upgrade pip First
```bash
python -m pip install --upgrade pip
```
- Always upgrade pip before installing dependencies
- Ensures latest pip features and bug fixes

#### 4. Install Test Tools Explicitly
```bash
python -m pip install flake8 pytest pytest-cov
```
- Don't rely on pre-installed versions
- Pin versions in requirements-dev.txt if needed

#### 5. Use Proper Linting Configuration
```bash
# Critical errors only
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# All issues as warnings
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
```
- Fail on syntax errors and undefined names
- Report all style issues without failing

#### 6. Handle Test Collection Gracefully
```bash
pytest || rc=$?
if [ "${rc:-0}" -eq 5 ]; then
  echo "No tests collected"
  exit 0
fi
```
- Exit code 5 means no tests collected
- Decide if this should fail or pass

## Troubleshooting Guide

### Common Issues and Solutions

#### Issue: Cache Not Restoring

**Symptoms**: Dependencies reinstall on every run

**Solutions**:
1. Verify cache key includes `hashFiles('**/requirements.txt')`
2. Check cache size limits (10 GB per repository)
3. Ensure cache path is correct for your OS
4. Review cache hit/miss in job logs

**Debug**:
```yaml
- name: Debug cache
  run: |
    echo "Cache key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}"
    ls -la ~/.cache/pip || echo "Cache directory not found"
```

#### Issue: Python Version Not Found

**Symptoms**: `setup-python` action fails to find version

**Solutions**:
1. Use exact version specifier (e.g., "3.9" not "3.9.x")
2. Check [Python versions available](https://github.com/actions/python-versions/releases)
3. Use `python-version-file` option if you have `.python-version`

**Example**:
```yaml
- uses: actions/setup-python@v5
  with:
    python-version-file: '.python-version'
```

#### Issue: Import Errors in Tests

**Symptoms**: Tests fail with `ModuleNotFoundError`

**Solutions**:
1. Ensure all dependencies are in `requirements.txt`
2. Install package in editable mode: `pip install -e .`
3. Check PYTHONPATH configuration
4. Verify package structure has `__init__.py` files

**Debug**:
```bash
- name: Debug Python environment
  run: |
    python -m pip list
    python -c "import sys; print(sys.path)"
    find . -name "__init__.py"
```

#### Issue: Out of Memory

**Symptoms**: Job killed due to memory limits

**Solutions**:
1. Use ubuntu-latest-m or ubuntu-latest-l for more memory
2. Limit parallel test execution: `pytest -n auto --maxprocesses=2`
3. Reduce matrix size
4. Split tests into multiple jobs

#### Issue: Tests Pass Locally, Fail in CI

**Symptoms**: Tests work on local machine but fail in GitHub Actions

**Solutions**:
1. Check environment variables and secrets
2. Verify file paths are platform-independent
3. Check timezone assumptions
4. Review differences in pre-installed software versions
5. Use `act` to test GitHub Actions locally

**Local Testing**:
```bash
# Install act
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run workflow locally
act -j build
```

#### Issue: Slow CI Runs

**Symptoms**: CI takes longer than expected

**Solutions**:
1. Implement dependency caching (saves 30-60 seconds)
2. Use cache for pip, npm, etc.
3. Minimize matrix dimensions
4. Remove unnecessary test runs
5. Parallelize independent jobs

**Optimization Example**:
```yaml
- name: Install dependencies
  run: |
    pip install --no-cache-dir -r requirements.txt  # Don't cache during install
    
- name: Run tests in parallel
  run: |
    pytest -n auto  # Use pytest-xdist for parallel execution
```

### Debug Mode

Enable debug logging for detailed troubleshooting:

1. **Repository Secrets**: Set `ACTIONS_STEP_DEBUG` to `true`
2. **Runner Diagnostic Logs**: Set `ACTIONS_RUNNER_DEBUG` to `true`

These settings enable verbose logging for all workflow runs.

## Optimization Recommendations

### Current Workflow Optimizations

1. **Dependency Caching**: ✅ Implemented
   - Caches pip packages based on requirements.txt hash
   - Reduces install time by 30-60 seconds

2. **Matrix Strategy**: ✅ Optimized
   - Tests multiple Python versions in parallel
   - `fail-fast: false` ensures all versions tested

3. **Test Collection Check**: ✅ Implemented
   - Custom script validates test collection
   - Prevents pytest exit code 5 failures

### Additional Optimization Opportunities

1. **Action Version Updates**
   ```yaml
   # Current: actions/setup-python@v3
   # Recommended: actions/setup-python@v5
   - uses: actions/setup-python@v5  # Faster, better caching
   ```

2. **Built-in Python Caching**
   ```yaml
   - uses: actions/setup-python@v5
     with:
       python-version: ${{ matrix.python-version }}
       cache: 'pip'  # Automatic pip caching
   ```

3. **Concurrent Job Execution**
   ```yaml
   jobs:
     lint:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - run: flake8 .
     
     test:
       runs-on: ubuntu-latest
       strategy:
         matrix:
           python-version: ["3.9", "3.10", "3.11"]
       steps:
         - uses: actions/checkout@v4
         - run: pytest
   ```

4. **Test Parallelization**
   ```bash
   pip install pytest-xdist
   pytest -n auto  # Parallel test execution
   ```

5. **Conditional Steps**
   ```yaml
   - name: Upload coverage
     if: matrix.python-version == '3.11'  # Only once
     uses: codecov/codecov-action@v3
   ```

## Environment Variables

### Standard GitHub Variables

```bash
GITHUB_WORKSPACE=/home/runner/work/ai-passive-income-toolkit/ai-passive-income-toolkit
GITHUB_REPOSITORY=Trancendos/ai-passive-income-toolkit
GITHUB_RUN_ID=<unique-run-id>
GITHUB_SHA=<commit-sha>
GITHUB_REF=refs/heads/main
RUNNER_OS=Linux
RUNNER_TEMP=/home/runner/work/_temp
```

### Python-specific Variables

```bash
pythonLocation=/opt/hostedtoolcache/Python/3.9.*/x64
Python_ROOT_DIR=/opt/hostedtoolcache/Python/3.9.*/x64
Python3_ROOT_DIR=/opt/hostedtoolcache/Python/3.9.*/x64
```

## CI Checklist for Contributors

When setting up or modifying CI workflows:

- [ ] Python version matrix includes all supported versions
- [ ] Dependency caching is configured correctly
- [ ] All required dependencies are in requirements.txt
- [ ] Linting rules are defined and enforced
- [ ] Tests are discovered and run correctly
- [ ] Error handling for edge cases (no tests, API errors)
- [ ] Job timeouts are reasonable (default: 6 hours)
- [ ] Secrets are properly configured for external APIs
- [ ] Documentation is updated to reflect CI changes
- [ ] CI badge is added to README.md

### Example CI Badge

```markdown
![Python package](https://github.com/Trancendos/ai-passive-income-toolkit/workflows/Python%20package/badge.svg)
```

## References

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Python Setup Action](https://github.com/actions/setup-python)
- [Cache Action](https://github.com/actions/cache)
- [Virtual Environments](https://github.com/actions/runner-images)
- [Ubuntu 24.04 Image](https://github.com/actions/runner-images/blob/ubuntu24/20251030.96/images/ubuntu/Ubuntu2404-Readme.md)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## Version History

- **2025-11-06**: Initial documentation created
  - Documented runner version 2.329.0
  - Ubuntu 24.04.3 LTS (Image version 20251030.96.2)
  - Python 3.9, 3.10, 3.11 matrix testing

---

**Last Updated**: 2025-11-06  
**Maintainer**: Repository Contributors  
**Related Files**:
- `.github/workflows/python-package.yml`
- `scripts/ci_debug.sh`
- `requirements.txt`
- `setup.cfg`
