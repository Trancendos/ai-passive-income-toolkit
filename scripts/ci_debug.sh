#!/usr/bin/env bash
set -euo pipefail

echo "CI self-debug: listing repository top-level files and tests/*"
ls -la .
echo
echo "Looking for test files matching pytest naming patterns..."
# First try to list tracked files matching common test patterns
TEST_FILES=$(git ls-files -- "tests/test_*.py" "test_*.py" || true)
# fallback: use find to locate possible test files
if [ -z "${TEST_FILES}" ]; then
  TEST_FILES=$(find . -maxdepth 4 -type f \( -name 'test_*.py' -o -name 'tests.py' \) -print || true)
fi

if [ -z "${TEST_FILES}" ]; then
  echo "No test files found by git/find."
else
  echo "Found test files:"
  echo "${TEST_FILES}"
fi

echo
echo "Running pytest collection to show what pytest would collect..."
# Collect-only; pytest returns exit code 5 when no tests are collected
set +e
pytest --maxfail=1 --collect-only -q
rc=$?
set -e

if [ "$rc" -eq 5 ]; then
  echo "pytest collected no tests (exit code 5)."
  exit 5
elif [ "$rc" -ne 0 ]; then
  echo "pytest collection failed with exit code $rc"
  exit $rc
else
  echo "pytest collected tests successfully."
  exit 0
fi
