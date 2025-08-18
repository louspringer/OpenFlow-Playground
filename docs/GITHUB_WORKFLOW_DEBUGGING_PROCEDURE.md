# GitHub Workflow Debugging Procedure

## 🎯 Overview
This document outlines the systematic procedure for diagnosing and fixing GitHub Actions workflow failures. This procedure was developed and tested while fixing the Quality Gates workflow in PR #23.

## 🚨 When to Use This Procedure
- GitHub Actions workflows are failing (red X status)
- CI/CD pipelines are not completing successfully
- Workflow runs are timing out or erroring
- You need to understand why a workflow is failing

## 🔍 Step-by-Step Debugging Procedure

### **Step 1: Identify the Failing Workflow**
```bash
# List recent workflow runs to see which ones are failing
gh run list --limit 10

# Look for workflows with X status (failed) or * status (running)
# Note the workflow name and run ID for investigation
```

**Example Output:**
```
STATUS  TITLE          WORKFLOW     BRANCH       EVENT        ID           ELAPSED  AGE
X       Feature/co...  Quality ...  feature/...  pull_req...  17054078454  13s      less tha...
✓       Feature/co...  Copilot ...  feature/...  pull_req...  17054077622  15s      less tha...
```

### **Step 2: Examine the Workflow Run Logs**
```bash
# Get detailed logs for the failing workflow run
gh run view <RUN_ID> --log

# Look for error messages, failed steps, and exit codes
# Focus on sections marked with ##[error] or ##[warning]
```

**Key Things to Look For:**
- **Exit codes**: `Process completed with exit code 2`
- **Error messages**: `##[error]` sections
- **Warning messages**: `##[warning]` sections
- **Command failures**: `command not found`, `unrecognized arguments`
- **Deprecated actions**: `deprecated version` warnings

### **Step 3: Identify the Root Cause**
Based on the logs, categorize the issue:

#### **A. Deprecated Action Versions**
**Symptoms:**
- `This request has been automatically failed because it uses a deprecated version`
- `Learn more: https://github.blog/changelog/...`

**Common Deprecated Actions:**
- `actions/upload-artifact@v3` → `actions/upload-artifact@v4`
- `actions/setup-python@v4` → `actions/setup-python@v5`
- `actions/checkout@v3` → `actions/checkout@v4`

#### **B. CLI Argument Errors**
**Symptoms:**
- `unrecognized arguments: --project-path`
- `cli.py: error: unrecognized arguments`
- `Process completed with exit code 2`

#### **C. Missing Dependencies**
**Symptoms:**
- `command not found`
- `ModuleNotFoundError`
- `ImportError`

#### **D. Configuration Issues**
**Symptoms:**
- `Invalid configuration`
- `Missing required field`
- `YAML parsing errors`

### **Step 4: Fix the Issue**

#### **Fix Deprecated Actions**
```yaml
# Before (deprecated)
- name: Upload artifact
  uses: actions/upload-artifact@v3

# After (current)
- name: Upload artifact
  uses: actions/upload-artifact@v4
```

#### **Fix CLI Arguments**
```yaml
# Before (incorrect)
- name: Run analysis
  run: |
    python -m src.module.cli --project-path . --verbose

# After (correct)
- name: Run analysis
  run: |
    python -m src.module.cli
```

#### **Fix Missing Dependencies**
```yaml
# Add missing setup steps
- name: Install dependencies
  run: |
    pip install -r requirements.txt
    # or
    uv sync
```

### **Step 5: Test the Fix Locally**
```bash
# Test the command that was failing in the workflow
python -m src.code_quality_system.cli ci

# Check for any local errors or missing dependencies
# Verify the command works as expected
```

### **Step 6: Commit and Push the Fix**
```bash
# Add the modified workflow file
git add .github/workflows/workflow-name.yml

# Commit with descriptive message
git commit -m "fix: Fix workflow issue - [Brief description of what was fixed]"

# Push to trigger new workflow run
git push
```

### **Step 7: Monitor the New Workflow Run**
```bash
# Check if new workflow run started
gh run list --limit 5

# Monitor the run in real-time
gh run watch <NEW_RUN_ID>

# Check final status
gh run view <NEW_RUN_ID> --json conclusion,status
```

## 🛠️ Tools and Commands

### **GitHub CLI Commands**
```bash
# List workflow runs
gh run list [--limit N] [--json fields]

# View specific run details
gh run view <RUN_ID> [--log] [--json fields]

# Watch running workflow
gh run watch <RUN_ID>

# Rerun failed workflow
gh run rerun <RUN_ID>
```

### **Workflow File Locations**
```
.github/workflows/
├── quality-gates.yml          # Quality gate checks
├── copilot-review.yml         # Copilot automation
├── cloud-build.yml            # Cloud Build integration
├── diversity-hypothesis-check.yml  # Diversity validation
└── copilot-validation.yml     # Copilot validation
```

### **Common Workflow Patterns**
```yaml
# Standard workflow structure
name: Workflow Name
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  job-name:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Setup environment
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Run command
        run: |
          echo "Command here"
```

## 📋 Debugging Checklist

### **Before Starting**
- [ ] Identify which workflow is failing
- [ ] Note the run ID and workflow name
- [ ] Understand what the workflow is supposed to do

### **During Investigation**
- [ ] Examine the full workflow run logs
- [ ] Look for error messages and exit codes
- [ ] Identify the specific step that's failing
- [ ] Understand why that step is failing

### **During Fixing**
- [ ] Update deprecated action versions
- [ ] Fix CLI argument mismatches
- [ ] Add missing dependencies
- [ ] Test the fix locally if possible

### **After Fixing**
- [ ] Commit and push the changes
- [ ] Monitor the new workflow run
- [ ] Verify the fix resolves the issue
- [ ] Document what was fixed for future reference

## 🚨 Common Issues and Solutions

### **Issue: Deprecated Action Versions**
**Solution:** Update to current versions
```yaml
# Update these actions regularly
actions/checkout@v4
actions/setup-python@v5
actions/upload-artifact@v4
actions/setup-node@v4
```

### **Issue: CLI Argument Mismatches**
**Solution:** Check the actual CLI interface
```bash
# Test the command locally
python -m src.module.cli --help

# Verify the expected arguments
# Update workflow to match actual CLI interface
```

### **Issue: Missing Dependencies**
**Solution:** Add proper setup steps
```yaml
- name: Install dependencies
  run: |
    uv sync --all-extras
    # or
    pip install -r requirements.txt
```

### **Issue: Environment Variables**
**Solution:** Check environment setup
```yaml
env:
  VARIABLE_NAME: ${{ secrets.VARIABLE_NAME }}
  # or
  VARIABLE_NAME: ${{ vars.VARIABLE_NAME }}
```

## 📊 Example: Quality Gates Workflow Fix

### **Problem Identified**
- Workflow failing with `Process completed with exit code 2`
- CLI error: `unrecognized arguments: --project-path`

### **Root Cause**
- Workflow calling CLI with incorrect arguments
- CLI expected: `python -m src.code_quality_system.cli ci`
- Workflow was calling: `python -m src.code_quality_system.cli ci --project-path . --verbose`

### **Fix Applied**
```yaml
# Before
- name: Run quality analysis
  run: |
    python -m src.code_quality_system.cli ci --project-path . --verbose

# After
- name: Run quality analysis
  run: |
    python -m src.code_quality_system.cli ci
```

### **Result**
- Workflow now executes without CLI argument errors
- Quality analysis step completes successfully
- CI pipeline can proceed to next steps

## 🎯 Best Practices

### **1. Always Check Logs First**
- Don't guess what's wrong
- Use `gh run view <ID> --log` to see actual errors
- Look for specific error messages and exit codes

### **2. Test Locally When Possible**
- Run the failing command locally
- Verify dependencies and configuration
- Ensure the command works as expected

### **3. Use Descriptive Commit Messages**
```bash
git commit -m "fix: Fix workflow issue - [Specific description]"
```

### **4. Monitor After Fixing**
- Watch the new workflow run
- Verify the fix resolves the issue
- Check for any new problems introduced

### **5. Document the Fix**
- Update this procedure if you discover new patterns
- Note common issues and solutions
- Share knowledge with the team

## 🚀 Conclusion

This debugging procedure provides a systematic approach to resolving GitHub Actions workflow issues. By following these steps, you can:

1. **Quickly identify** what's causing workflow failures
2. **Efficiently fix** common issues like deprecated actions and CLI errors
3. **Prevent future failures** by understanding common patterns
4. **Maintain reliable CI/CD** pipelines for the project

Remember: **Always check the logs first, don't guess!** The actual error messages will tell you exactly what's wrong and how to fix it.
