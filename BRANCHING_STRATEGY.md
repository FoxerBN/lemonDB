# 🌳 Git Branching Strategy

## Branch Structure

```
lemonDB/
├── develop   → Development branch (your daily work)
├── publish   → Production/Release branch (triggers PyPI publish)
└── master    → Legacy/unused (can be deleted or kept as redirect)
```

---

## Branch Purposes

### 🔧 `develop` - Development Branch
**Purpose:** All development work happens here

**Use for:**
- Adding new features
- Bug fixes
- Experiments
- Testing
- Documentation updates

**Workflow:**
```bash
# Switch to develop
git checkout develop

# Make changes
# ... edit files ...

# Commit
git add .
git commit -m "Add new feature"

# Push to GitHub
git push github develop
```

---

### 🚀 `publish` - Production Branch
**Purpose:** Stable releases only, triggers automatic PyPI publishing

**Use for:**
- Stable releases ready for PyPI
- Tested and verified code only
- Version-tagged releases

**Workflow:**
```bash
# When develop is ready for release:

# 1. Switch to publish branch
git checkout publish

# 2. Merge from develop
git merge develop

# 3. Update version in setup.cfg
# version = 1.1.0

# 4. Commit version bump
git add setup.cfg
git commit -m "Bump version to 1.1.0"

# 5. Push to GitHub (triggers PyPI publish!)
git push github publish

# 6. Optionally create tag
git tag -a v1.1.0 -m "Release v1.1.0"
git push github v1.1.0
```

---

## Initial Setup

### Step 1: Create Branches

```bash
cd /home/richardtekula/Documents/python-projects/lemonDB

# Rename master to develop
git branch -m master develop

# Create publish branch from current state
git checkout -b publish

# Go back to develop
git checkout develop
```

### Step 2: Add GitHub Remote

```bash
# Add GitHub remote (replace YOUR_USERNAME)
git remote add github https://github.com/YOUR_USERNAME/lemonDB.git

# Verify
git remote -v
```

### Step 3: Push Both Branches

```bash
# Push develop
git push -u github develop

# Push publish
git checkout publish
git push -u github publish

# Back to develop for work
git checkout develop
```

---

## GitHub Actions Triggers

### Tests Workflow (`tests.yml`)
**Triggers on:**
- Push to `develop` branch
- Push to `master` branch  
- Pull request to `develop`
- Pull request to `publish`

**What it does:**
- Runs all tests
- Tests on Python 3.8, 3.9, 3.10, 3.11
- No publish, just testing

### Publish Workflow (`publish-to-pypi.yml`)
**Triggers on:**
- Push to `publish` branch ⚠️ **Automatically publishes to PyPI!**
- Manual workflow dispatch
- GitHub release published

**What it does:**
- Builds package
- Publishes to PyPI
- Users can install with `pip install lemondb`

---

## Typical Development Workflow

### Day-to-day Development

```bash
# Always work on develop
git checkout develop

# Make changes
vim app/core.py

# Test locally
python run_all_tests.py

# Commit
git add .
git commit -m "Add awesome feature"

# Push to GitHub (runs tests, no publish)
git push github develop
```

### When Ready for Release

```bash
# 1. Make sure develop is clean and tested
git checkout develop
python run_all_tests.py  # All tests pass

# 2. Switch to publish
git checkout publish

# 3. Merge develop into publish
git merge develop

# 4. Update version
nano setup.cfg  # Change version = 1.1.0

# 5. Commit version
git add setup.cfg
git commit -m "Release v1.1.0"

# 6. Push (THIS TRIGGERS PYPI PUBLISH!)
git push github publish

# 7. Create tag (optional but recommended)
git tag -a v1.1.0 -m "Release v1.1.0"
git push github v1.1.0

# 8. Back to develop
git checkout develop
```

---

## Protection Rules (Optional)

On GitHub, you can protect branches:

### For `publish` branch:
1. Go to Settings → Branches
2. Add rule for `publish`
3. Enable:
   - Require pull request reviews
   - Require status checks (tests must pass)
   - Prevent force push

This ensures only tested code gets published to PyPI!

---

## Version Numbering

Follow Semantic Versioning:

```
MAJOR.MINOR.PATCH

1.0.0 → Initial release
1.0.1 → Bug fix
1.1.0 → New feature (backward compatible)
2.0.0 → Breaking change
```

Update in `setup.cfg`:
```ini
[metadata]
version = 1.1.0
```

---

## Quick Reference

```bash
# Create branches
git branch -m master develop
git checkout -b publish
git checkout develop

# Push to GitHub
git remote add github https://github.com/YOUR_USERNAME/lemonDB.git
git push -u github develop
git push -u github publish

# Daily work (develop)
git checkout develop
# ... make changes ...
git commit -am "Add feature"
git push github develop  # ← Tests run, no publish

# Release (publish)
git checkout publish
git merge develop
# update version in setup.cfg
git commit -am "Release v1.1.0"
git push github publish  # ← PUBLISHES TO PYPI!
```

---

## Important Notes

⚠️ **WARNING:** Pushing to `publish` branch automatically publishes to PyPI!

✅ **SAFE:** Pushing to `develop` only runs tests, does not publish

💡 **TIP:** Always test on `develop` first before merging to `publish`

🔒 **RECOMMENDED:** Set up branch protection on `publish` branch

---

**Made with 🍋 by lemonDB**
