#!/bin/bash
# CI Debug Script
# This script helps diagnose test collection issues in the CI pipeline
# by listing repository files, searching for test files, and running pytest --collect-only

set -e

echo "=== CI Debug: Repository structure ==="
echo "Working directory: $(pwd)"
echo ""

echo "=== Listing top-level files and directories ==="
ls -la
echo ""

echo "=== Searching for test files with git ==="
git ls-files | grep -E 'test.*\.py$' || echo "No test files found via git ls-files"
echo ""

echo "=== Searching for test files with find ==="
find . -name 'test*.py' -o -name '*_test.py' | grep -v '__pycache__' || echo "No test files found via find"
echo ""

echo "=== Running pytest --collect-only ==="
pytest --collect-only || exit_code=$?

if [ "${exit_code:-0}" -eq 5 ]; then
    echo ""
    echo "WARNING: pytest collected no tests (exit code 5)"
    exit 5
elif [ "${exit_code:-0}" -ne 0 ]; then
    echo ""
    echo "ERROR: pytest --collect-only failed with exit code ${exit_code}"
    exit "${exit_code}"
else
    echo ""
    echo "SUCCESS: pytest collected tests successfully"
    exit 0
fi
