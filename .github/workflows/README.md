# AI Passive Income Toolkit - Workflow Documentation

## Active Workflows

### python-package.yml
**Purpose:** Framework-compliant Python CI/CD pipeline

**Gates Implemented:**
- Gate 6-7: Testing with 90% coverage target
- Gate 9: Security scanning (Trivy + safety)
- Gate 10: Cost governance (Doris validation)

**Triggers:**
- Push to main/develop
- Pull requests
- Manual dispatch

**Framework Compliance:**
- ✅ Zero-cost mandate
- ✅ NO Copilot tokens used
- ✅ Multi-version Python testing (3.9-3.12)
- ✅ Security scanning integrated

---

## Removed Workflows

### auto-fix-deprecated-actions.yml
**Reason:** Redundant - functionality integrated into main CI pipeline
**Date Removed:** 2025-11-09

---

## Testing

**Coverage Requirements:** 90% minimum (Framework requirement)
**Test Discovery:** Automatic via pytest
**Failure Handling:** Graceful for projects without tests

---

**Last Updated:** 2025-11-09 00:08 GMT
**Framework:** [Trancendos Unified Framework](https://www.notion.so/2a56dc80116981c59556f9b0a34d6960)
