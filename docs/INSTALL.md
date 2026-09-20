# Daily Brain Installation & Deployment Guide

This guide covers deployment and installation across all supported platforms.

---

## 🌐 1. Web & Cloud Deployment (Streamlit Community Cloud)

1. Fork or push your Daily Brain repository to GitHub.
2. Visit [share.streamlit.io](https://share.streamlit.io).
3. Connect your repository (`main` branch) and set the main file to `app.py`.
4. In **App Settings ➡️ Secrets**, add:
   ```toml
   GEMINI_API_KEY = "your-api-key-here"
   ```
5. Click **Deploy**. The app will be live and auto-sync on every git push.

---

## 💻 2. Windows Desktop App Installation

### Option A: Run directly from source
```cmd
DailyBrain.bat
```

### Option B: Install Desktop & Start Menu Shortcuts
Double-click `Install_Desktop_Shortcut.bat`.

### Option C: Build Standalone Executable
```cmd
python build_desktop.py
```
Outputs standalone package to `dist/DailyBrain/DailyBrain.exe`.

---

## 📱 3. Android Installation

### Option A: PWA Installation (Instant)
1. Open `https://daily-brain-agent.streamlit.app` in Chrome on Android.
2. Tap the top-right menu `⋮` and select **"Install app"**.

### Option B: Native APK Build
1. Open the `android/` directory in **Android Studio**.
2. Connect your Android device or start an emulator.
3. Click **Run** or **Build ➡️ Build APK(s)**.

---

## 🍏 4. iOS Installation

### Option A: PWA Installation (Instant)
1. Open `https://daily-brain-agent.streamlit.app` in Safari on iPhone.
2. Tap the **Share** button (box with upward arrow).
3. Scroll down and tap **"Add to Home Screen"**.

### Option B: Native Xcode Build
1. Open `ios/DailyBrain.xcodeproj` in **Xcode** on macOS.
2. Select your development team in **Signing & Capabilities**.
3. Select your iPhone or simulator and click **Run**.
