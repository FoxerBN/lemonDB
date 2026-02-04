# 🍋 LemonDB - PyPI Publishing Guide

## Prerequisites

Before publishing to PyPI, you need:

1. **PyPI Account** - Create account at https://pypi.org/account/register/
2. **API Token** - Generate at https://pypi.org/manage/account/token/
3. **GitHub Repository** - Your code on GitHub
4. **GitHub Secrets** - Add PyPI token to repository secrets

---

## Step 1: Update Package Info

Edit `setup.cfg` and update:

```ini
[metadata]
name = lemondb
version = 1.0.0
author = Your Name
author_email = your.email@example.com
url = https://github.com/YOUR_USERNAME/lemonDB
```

---

## Step 2: Create PyPI API Token

1. Go to https://pypi.org/manage/account/token/
2. Click "Add API token"
3. Name: `lemondb-github-actions`
4. Scope: `Entire account` or `Project: lemondb`
5. Copy the token (starts with `pypi-`)

---

## Step 3: Add Token to GitHub Secrets

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `PYPI_API_TOKEN`
5. Value: Paste your PyPI token
6. Click "Add secret"

---

## Step 4: Push to GitHub

```bash
# Add GitHub remote (replace YOUR_USERNAME)
git remote add github https://github.com/YOUR_USERNAME/lemonDB.git

# Push to GitHub
git push github master

# Push workflows
git push github master --force
```

---

## Step 5: Create Release (Automatic Publish)

### Option A: Via GitHub Web Interface

1. Go to your repository on GitHub
2. Click "Releases" → "Create a new release"
3. Tag: `v1.0.0`
4. Release title: `🍋 LemonDB v1.0.0 - Auto-Increment IDs`
5. Description:
   ```
   First stable release of LemonDB!
   
   Features:
   - Auto-increment ID generation
   - Schema validation with constraints
   - Simple CRUD operations
   - Custom storage paths
   - Comprehensive logging
   
   Install: `pip install lemondb`
   ```
6. Click "Publish release"
7. GitHub Actions will automatically publish to PyPI!

### Option B: Via Command Line

```bash
# Create and push tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push github v1.0.0

# Then create release on GitHub web interface
```

---

## Step 6: Manual Publish (Optional)

If you want to publish manually without GitHub Actions:

```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Check package
twine check dist/*

# Upload to PyPI
twine upload dist/*
# Enter username: __token__
# Enter password: <your-pypi-token>
```

---

## Step 7: Verify Installation

After publishing, test installation:

```bash
# Create new virtual environment
python -m venv test_env
source test_env/bin/activate  # On Windows: test_env\Scripts\activate

# Install from PyPI
pip install lemondb

# Test it
python -c "from app import LemonDB; print('✅ LemonDB installed successfully!')"
```

---

## Project Information for PyPI

**Project Name:** `lemondb`  
**Owner:** Richard Tekula (update in setup.cfg)  
**Repository:** `https://github.com/YOUR_USERNAME/lemonDB`  
**Workflow Name:** `publish-to-pypi.yml`  
**Environment:** Not required (uses secrets directly)

---

## GitHub Workflows

### 1. `publish-to-pypi.yml`
- Triggers on: Release published
- Action: Builds and publishes to PyPI
- Requires: `PYPI_API_TOKEN` secret

### 2. `tests.yml`
- Triggers on: Push to master/main
- Action: Runs all tests on Python 3.8-3.11
- No secrets required

---

## Troubleshooting

### Build fails
```bash
# Check setup.cfg syntax
python setup.py check

# Test build locally
python -m build
```

### Upload fails
- Check PyPI token is correct
- Verify package name is available on PyPI
- Ensure version number is incremented

### Tests fail
```bash
# Run tests locally
python run_all_tests.py

# Check Python version
python --version
```

---

## Version Bumping

For future releases:

1. Update version in `setup.cfg`: `version = 1.1.0`
2. Commit changes: `git commit -am "Bump version to 1.1.0"`
3. Create new tag: `git tag -a v1.1.0 -m "Release v1.1.0"`
4. Push: `git push github master --tags`
5. Create release on GitHub

---

## Quick Reference

```bash
# Current setup
Project: lemondb
Version: 1.0.0
Python: >=3.8
License: MIT

# Workflows
.github/workflows/publish-to-pypi.yml  # PyPI publishing
.github/workflows/tests.yml            # Automated testing

# Required Secrets
PYPI_API_TOKEN  # Your PyPI token

# Installation after publish
pip install lemondb
```

---

**Ready to publish! 🍋**
