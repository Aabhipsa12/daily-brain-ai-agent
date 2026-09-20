# Daily Brain Development & Contribution Guide

Guidelines for contributing, local testing, and building the Daily Brain ecosystem.

---

## 🛠️ Development Environment

### 1. Requirements
- Python 3.10+
- Node.js (optional, for web asset tools)
- Android Studio Iguana+ (for Android native)
- Xcode 15+ (for iOS native)

### 2. Local Setup
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
pip install pytest flake8 pyinstaller pywebview
```

---

## 🧪 Testing & Validation

### Run Syntax & Linting Checks
```bash
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

### Run Multi-Platform Build Pipeline
```bash
python build_all.py
```

---

## 🚢 Release Process

1. Ensure all local tests pass.
2. Commit changes following conventional commits (`feat:`, `fix:`, `docs:`, `ci:`).
3. Create a semantic version tag:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
4. GitHub Actions will automatically compile the release assets and publish them to GitHub Releases.
