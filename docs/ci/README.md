# CI/CD Documentation

Welcome to the CI/CD documentation for the AI Passive Income Toolkit. This directory contains comprehensive guides for understanding and working with the GitHub Actions continuous integration pipeline.

## 📖 Documentation Index

### 1. [GitHub Actions Runner Setup](./github-actions-runner-setup.md)
**Complete reference for the CI/CD environment**

This is the main documentation file covering:
- Runner specifications and version information
- Pre-installed software inventory
- Detailed setup process walkthrough
- Environment variables and configuration
- Optimization recommendations
- Best practices for Python CI/CD

**When to use**: Understanding the CI environment, investigating runner capabilities, or optimizing workflows.

### 2. [Contributing to CI/CD](./CONTRIBUTING-CI.md)
**Quick start guide for developers**

A practical guide for contributors covering:
- Running tests locally
- Understanding CI workflow
- Adding dependencies and tests
- Debugging CI failures
- Linting and testing guidelines
- Performance optimization tips

**When to use**: Before making your first contribution, when adding tests, or when CI fails.

### 3. [Troubleshooting Guide](./TROUBLESHOOTING.md)
**Quick reference for common issues**

Fast solutions for frequent problems:
- No tests collected errors
- Cache restoration issues
- Module import problems
- Linting failures
- Flaky tests
- Emergency fixes

**When to use**: When CI is failing and you need a quick solution.

## 🚀 Quick Start

### For Contributors

1. **First time?** Read [CONTRIBUTING-CI.md](./CONTRIBUTING-CI.md)
2. **CI failing?** Check [TROUBLESHOOTING.md](./TROUBLESHOOTING.md)
3. **Need details?** See [github-actions-runner-setup.md](./github-actions-runner-setup.md)

### Common Tasks

#### Run tests locally
```bash
pip install -r requirements.txt
pip install flake8 pytest
pytest -v
flake8 .
```

#### Debug test collection
```bash
pytest --collect-only -v
./scripts/ci_debug.sh
```

#### Fix linting issues
```bash
flake8 . --select=E9,F63,F7,F82  # Critical only
pip install autopep8
autopep8 --in-place --aggressive --aggressive <file>
```

## 🏗️ CI Architecture

```
┌─────────────────────────────────────────┐
│         GitHub Actions Trigger          │
│    (Push to main / Pull Request)        │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│       Matrix Strategy (Parallel)        │
│   Python 3.9  │  3.10  │  3.11          │
└────────┬───────┴────────┴────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│          Setup Environment              │
│  • Checkout code                        │
│  • Setup Python version                 │
│  • Restore cache                        │
│  • Install dependencies                 │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│          Quality Checks                 │
│  • Lint with flake8                     │
│  • Collect tests (debug)                │
│  • Run pytest                           │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│            Results                      │
│  ✓ Success → Merge allowed              │
│  ✗ Failure → Review required            │
└─────────────────────────────────────────┘
```

## 📊 CI Metrics

### Performance Targets
- **Job Duration**: < 5 minutes
- **Cache Hit Rate**: > 80%
- **Test Success Rate**: > 95%
- **Flaky Test Rate**: < 5%

### Current Setup
- **Python Versions**: 3.9, 3.10, 3.11
- **Test Count**: 23 tests
- **Linting**: flake8 (PEP 8 compliance)
- **Cache**: pip dependencies

## 🔍 Runner Environment

### Ubuntu 24.04 Runner
- **Image**: ubuntu-24.04 (20251030.96.2)
- **Runner**: v2.329.0
- **CPU**: 4 cores
- **RAM**: 16 GB
- **Disk**: 14 GB SSD

### Key Pre-installed Software
- Python 3.9, 3.10, 3.11, 3.12
- Docker & Docker Compose
- Git with Git LFS
- AWS, Azure, Google Cloud CLIs
- Build tools (gcc, make, cmake)

See [complete software list](https://github.com/actions/runner-images/blob/ubuntu24/20251030.96/images/ubuntu/Ubuntu2404-Readme.md).

## 🛠️ Workflow Files

### Main Workflow
**File**: `.github/workflows/python-package.yml`

```yaml
name: Python package
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v3
      - uses: actions/cache@v4
      - run: pip install -r requirements.txt
      - run: flake8 .
      - run: pytest
```

### Debug Script
**File**: `scripts/ci_debug.sh`

Helper script for diagnosing test collection issues:
- Lists repository structure
- Searches for test files
- Runs pytest --collect-only
- Reports collection status

## 📚 Additional Resources

### GitHub Documentation
- [GitHub Actions Overview](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Virtual Environments](https://github.com/actions/runner-images)

### Python Testing
- [pytest Documentation](https://docs.pytest.org/)
- [flake8 Rules](https://www.flake8rules.com/)
- [PEP 8 Style Guide](https://pep8.org/)

### Actions Used
- [actions/checkout](https://github.com/actions/checkout)
- [actions/setup-python](https://github.com/actions/setup-python)
- [actions/cache](https://github.com/actions/cache)

## 🆘 Getting Help

### Troubleshooting Steps
1. Check [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) for common issues
2. Review CI logs in GitHub Actions tab
3. Reproduce locally using same Python version
4. Enable debug mode (set `ACTIONS_STEP_DEBUG=true`)
5. Ask in GitHub Issues with `ci/cd` label

### Debug Commands
```bash
# View recent workflow runs
gh run list

# View specific run
gh run view <run-id>

# Download logs
gh run download <run-id>

# Rerun failed jobs
gh run rerun <run-id> --failed
```

## 📝 Documentation Maintenance

### Update Checklist
- [ ] Runner version changes
- [ ] Python version changes
- [ ] New dependencies added
- [ ] Workflow modifications
- [ ] Image updates
- [ ] New troubleshooting patterns

### Version History
- **2025-11-06**: Initial documentation
  - Runner v2.329.0
  - Ubuntu 24.04.3 LTS
  - Image 20251030.96.2
  - Python 3.9, 3.10, 3.11

## 🤝 Contributing to Documentation

Improvements to this documentation are welcome!

1. Fork the repository
2. Update documentation
3. Test any code examples
4. Submit pull request
5. Add `documentation` label

## 📞 Contact

- **Issues**: [GitHub Issues](https://github.com/Trancendos/ai-passive-income-toolkit/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Trancendos/ai-passive-income-toolkit/discussions)
- **CI/CD Label**: Use `ci/cd` label for CI-related issues

---

**Last Updated**: 2025-11-06  
**Maintained by**: Repository Contributors  
**Version**: 1.0

---

*This documentation is part of the [AI Passive Income Toolkit](https://github.com/Trancendos/ai-passive-income-toolkit)*
