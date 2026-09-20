# 🧠 Daily Brain — Comprehensive Ecosystem Audit & Productionization Roadmap

**Document Version:** 1.0.0  
**Generated:** September 20, 2026  
**Author:** Lead Software Architect & Product Engineering Team

---

## Executive Summary

**Daily Brain** is an AI-powered autonomous task management agent built around Google Gemini (Gemini 3.6 Flash) that translates natural language conversation and voice recordings into scheduled tasks, structured subtask checklists, category tags, and urgency tracking.

The core conversational agent, deadline computation, speech-to-text, and web presentation are working. However, the ecosystem currently operates as a collection of wrappers around a single Streamlit web deployment. To transform Daily Brain into a single, cohesive, installable multi-platform product across Web, Desktop, Android, and iOS, we have conducted an end-to-end audit of all assets, codebases, and configurations.

---

## A. Ecosystem Audit (What Exists Right Now)

| Platform / Target | Technology Stack | Current Location | Working Features | Missing / Incomplete Items |
| :--- | :--- | :--- | :--- | :--- |
| **Agent Engine / Core** | Python 3.10+, `google-genai` SDK | [`main.py`](file:///D:/Daily-brain/main.py) | • 8 native Python function tools (`save_task`, `list_tasks`, `get_current_date`, `complete_task`, `delete_task`, `add_checklist_item`, `update_task_category`, `get_urgent_tasks`)<br>• Gemini 3.6 Flash multimodal STT audio transcription<br>• Regex date/urgency engine | • No standalone REST/WebSocket API layer (embedded in local script)<br>• Single-user JSON storage<br>• No multi-device sync or user auth |
| **Web Application** | Streamlit 1.40+, HTML5/CSS | [`app.py`](file:///D:/Daily-brain/app.py) | • Theme-adaptive UI (Dark/Light)<br>• Multi-turn chat session with auto-recovery<br>• Interactive checklists with progress bars<br>• Category pills & urgency banners<br>• Voice recording via `st.audio_input` | • State is coupled to Streamlit server session<br>• Relies on server-side Python runtime for all UI changes |
| **Cloud Deployment** | Streamlit Community Cloud | Live at [daily-brain-agent.streamlit.app](https://daily-brain-agent.streamlit.app) | • Automatic GitHub deployment on `main`<br>• Secrets management for `GEMINI_API_KEY`<br>• Accessible from desktop & mobile browsers | • Ephemeral server environment (tasks reset on container rebuild unless external store is connected) |
| **Desktop Application** | Python, `pywebview` (Edge WebView2), Batch Script | [`desktop_app.py`](file:///D:/Daily-brain/desktop_app.py), [`DailyBrain.bat`](file:///D:/Daily-brain/DailyBrain.bat) | • Standalone frameless desktop window (1280x820)<br>• Background Streamlit daemon management<br>• Clean process termination on close | • Requires Python runtime on host machine<br>• No Windows installer (`.msi` / `.exe` setup)<br>• No Start Menu integration or uninstaller |
| **Android Application** | Android Native (Kotlin), WebView, Gradle | [`android/`](file:///D:/Daily-brain/android) | • Clean Android Studio project layout<br>• `AndroidManifest.xml` with permissions (`RECORD_AUDIO`, `INTERNET`)<br>• Hardware acceleration & pull-to-refresh | • Needs Gradle wrapper (`gradlew`) generated<br>• Needs production adaptive & vector icon system<br>• Needs signed Release APK & AAB build workflows |
| **iOS Application** | SwiftUI, `WKWebView`, WebKit | [`ios/DailyBrain/`](file:///D:/Daily-brain/ios/DailyBrain) | • Modern SwiftUI app lifecycle (`DailyBrainApp.swift`)<br>• Safe area insets & dark mode theming<br>• `Info.plist` with `NSMicrophoneUsageDescription` | • Needs `.xcodeproj` container for direct Xcode builds<br>• Needs App Store asset catalog & TestFlight configuration |
| **PWA** | Web App Manifest, Service Worker | [`static/manifest.json`](file:///D:/Daily-brain/static/manifest.json), [`static/sw.js`](file:///D:/Daily-brain/static/sw.js) | • PWA manifest with `id`, `scope`, standalone display<br>• Shell caching service worker<br>• Injected directly into parent window head | • Browser caching needs tuning for real-time websocket connections |

---

## B. Architecture Map

```
                                  ┌───────────────────────────────┐
                                  │   User Natural Language &     │
                                  │      Voice Task Inputs        │
                                  └──────────────┬────────────────┘
                                                 │
                   ┌─────────────────────────────┼─────────────────────────────┐
                   ▼                             ▼                             ▼
       ┌───────────────────────┐   ┌───────────────────────────┐   ┌───────────────────────┐
       │   Web & PWA Client    │   │      Desktop Client       │   │  Mobile Native Apps   │
       │ (Chrome / Safari PWA) │   │ (pywebview Desktop Window)│   │ (Android KT / iOS SW) │
       └───────────┬───────────┘   └─────────────┬─────────────┘   └───────────┬───────────┘
                   │                             │                             │
                   └─────────────────────────────┼─────────────────────────────┘
                                                 ▼
                                ┌─────────────────────────────────┐
                                │     Streamlit / Python Engine   │
                                │   (`app.py` UI + Session State) │
                                └────────────────┬────────────────┘
                                                 │
                                                 ▼
                                ┌─────────────────────────────────┐
                                │     Daily Brain Core Agent      │
                                │  (`main.py` - Gemini 3.6 Flash) │
                                └────────────────┬────────────────┘
                                                 │
                   ┌─────────────────────────────┼─────────────────────────────┐
                   ▼                             ▼                             ▼
       ┌───────────────────────┐   ┌───────────────────────────┐   ┌───────────────────────┐
       │  Multimodal Audio STT │   │     8 Tool Call Engine    │   │  Urgency/Date Engine  │
       │  (Gemini Audio WAV)   │   │(save/list/cat/due/subs...)│   │ (Deterministic Math)  │
       └───────────────────────┘   └─────────────┬─────────────┘   └───────────────────────┘
                                                 │
                                                 ▼
                                  ┌───────────────────────────────┐
                                  │     Local `tasks.json`        │
                                  │     (Persistent File)         │
                                  └───────────────────────────────┘
```

---

## C. Packaging Status

* **Web**: Packaged via standard `requirements.txt` and `.streamlit/config.toml`, hosted on Streamlit Cloud.
* **Desktop**: Currently launched via batch script `DailyBrain.bat` calling `python desktop_app.py`. A standalone bundled installer (`.exe` with bundled runtime) is not yet compiled.
* **Android**: Scaffolding exists in `D:\Daily-brain\android` (Gradle project with Kotlin WebView, `AndroidManifest.xml`). Build scripts are ready for `gradle assembleRelease` / `gradle bundleRelease`.
* **iOS**: Native SwiftUI source and `Info.plist` exist in `D:\Daily-brain\ios\DailyBrain`. Needs `.xcodeproj` envelope for automated command-line builds.
* **PWA**: Fully configured in `static/manifest.json` and injected into the parent DOM.

---

## D. Distribution & Productionization Gaps

1. **Standalone Windows Installer**: End users currently need Python installed. A standalone single-file installer (`DailyBrainSetup.exe`) or MSI with embedded Python and desktop shortcuts is needed.
2. **Android Release Pipeline**: The Android project needs Gradle wrapper scripts (`gradlew.bat` / `gradlew`), release keystore generation guidelines, and an automated build script to output `DailyBrain-release.apk` and `DailyBrain-release.aab`.
3. **Branding Assets**: Existing icons are basic generated placeholders. A unified, high-resolution vector branding system (Adaptive Android icon, iOS asset catalog, Windows `.ico`, PWA maskable icons) is needed.
4. **Data Isolation**: `tasks.json` is stored in the application directory. On desktop installations (Program Files), this needs to resolve to `%APPDATA%\DailyBrain\tasks.json` so user permissions and updates never overwrite data.
5. **Cross-Device Sync Layer**: Currently, each instance reads its own local `tasks.json` (or the cloud instance on Streamlit Cloud). To synchronize tasks seamlessly between a user's phone, laptop, and web browser, a lightweight cloud synchronization mechanism will be introduced in Milestone 8.

---

## E. Branding & Asset Status

* **Current Assets in `static/`**:
  * `icon-192.png` (192x192 PNG)
  * `icon-512.png` (512x512 PNG)
  * `apple-touch-icon.png` (180x180 PNG)
  * `favicon.png` (32x32 PNG)
* **Status**: Functional placeholders. Needs a cohesive Master Vector Icon (SVG) and proper density generation for Android (`mdpi`, `hdpi`, `xhdpi`, `xxhdpi`, `xxxhdpi`, `anydpi-v26` adaptive XML), iOS (`AppIcon.appiconset`), and Windows (`app.ico`).

---

## F. Data & State Storage Status

* **Store**: `tasks.json` (JSON flat file).
* **Schema**:
  ```json
  {
    "task": "Task description string",
    "priority": "high / medium / low",
    "due_date": "Resolved calendar string or 'Not specified'",
    "category": "Academics / Project / Exam / Personal / Work / General",
    "status": "pending / completed",
    "saved_at": "YYYY-MM-DD HH:MM",
    "subtasks": [
      {
        "title": "Subtask title",
        "done": false
      }
    ]
  }
  ```
* **Normalizer**: `get_saved_tasks()` in `main.py` guarantees 100% backward-compatibility for legacy tasks missing subtasks, due dates, or categories.

---

## G. AI & Tool Engine Status

* **Model**: `gemini-3.6-flash` (via official `google-genai` SDK).
* **Connection Architecture**: Persistent singleton client (`get_client()`) with strong reference anchor (`chat._client_ref = client`) and auto-recovery retry mechanism.
* **Tools Active**: 8 tools covering creation, date calculation, category updates, checklist management, deletion, completion, and urgency querying.
* **Speech-to-Text**: Native 16kHz WAV audio capture passing to Gemini multimodal vision/audio input (`Part.from_bytes(audio_bytes, mime_type="audio/wav")`), completely free and zero third-party dependencies.

---

## H. Recommended Target Architecture

To satisfy the principle of **"ONE PRODUCT across platforms"**:

```
                              ┌───────────────────────────────────┐
                              │            DAILY BRAIN            │
                              │       Unified Product Layer       │
                              └─────────────────┬─────────────────┘
                                                │
                 ┌──────────────────────────────┼──────────────────────────────┐
                 ▼                              ▼                              ▼
    ┌─────────────────────────┐   ┌───────────────────────────┐   ┌───────────────────────────┐
    │     Web / PWA Client    │   │   Native Desktop Client   │   │   Native Mobile Clients   │
    │  (Responsive Browser &  │   │  (Windows Installer .exe  │   │  (Android Release APK/AAB │
    │   Installable PWA App)  │   │   & WebView2 Desktop App) │   │   & iOS SwiftUI Project)  │
    └────────────┬────────────┘   └─────────────┬─────────────┘   └─────────────┬─────────────┘
                 │                              │                               │
                 └──────────────────────────────┼───────────────────────────────┘
                                                ▼
                               ┌─────────────────────────────────┐
                               │     Shared Business Logic &     │
                               │        Task Schema Core         │
                               └────────────────┬────────────────┘
                                                │
                 ┌──────────────────────────────┴──────────────────────────────┐
                 ▼                                                             ▼
  ┌───────────────────────────────┐                             ┌───────────────────────────────┐
  │     Gemini 3.6 Flash Agent    │                             │      Sync & Storage Layer     │
  │   (8 Tools + Multimodal STT)  │                             │  (Local AppData / Cloud Sync) │
  └───────────────────────────────┘                             └───────────────────────────────┘
```

1. **Preserve Current Working Engine**: Keep `main.py`, `app.py`, and the 8 Gemini tools as the validated core.
2. **Productionize Android (`android/`)**: Add Gradle wrapper, build scripts for Debug/Release APK and AAB, adaptive icon drawables, and clean release signing configs.
3. **Productionize Windows Desktop**: Build a PyInstaller specification that bundles the runtime and creates an Inno Setup installer script for a true `DailyBrainSetup.exe` with desktop shortcut and uninstaller.
4. **Productionize iOS (`ios/`)**: Package with proper Xcode asset catalogs and build documentation.
5. **Unified Branding**: Create a master vector asset in `assets/branding/` and generate all platform-specific icon densities.

---

## I. Master Release Plan (12 Milestones)

* **Milestone 1**: Comprehensive Ecosystem Audit & Technical Architecture Baseline *(Completed here)*.
* **Milestone 2**: Master Branding & Professional Icon System across all platforms.
* **Milestone 3**: Desktop Productionization — PyInstaller bundling + Windows Installer (`.exe` setup).
* **Milestone 4**: Android Productionization — Gradle Wrapper, Adaptive Icons, Debug & Release APK/AAB builds.
* **Milestone 5**: iOS Productionization — Xcode structure, Asset Catalogs, and TestFlight preparation.
* **Milestone 6**: PWA Production Verification & Offline Polish.
* **Milestone 7**: User Data & System Storage Isolation (`%APPDATA%` / Sandboxing).
* **Milestone 8**: Cross-Device Synchronization Architecture.
* **Milestone 9**: Daily Brief & Smart Scheduling Engine.
* **Milestone 10**: Recurring Tasks & Task Dependencies.
* **Milestone 11**: Focus Mode (Pomodoro) & Productivity Insights.
* **Milestone 12**: Advanced Voice Agent Capabilities & Final Release QA.

---

## J. Immediate Next Step

**Milestone 2: Master Branding & Professional Icon System**.

We will create a dedicated `assets/branding/` directory with a master vector logo (Modern AI Brain / Circuit Motif in Indigo & Electric Violet) and generate:
1. Android Adaptive XML (`ic_launcher.xml`, foreground SVG/PNG, background color, round icon).
2. Windows Application Icon (`app.ico` with 16x16, 32x32, 48x48, 64x64, 128x128, 256x256 mipmaps).
3. iOS Asset Catalog (`AppIcon.appiconset` with 20pt, 29pt, 40pt, 60pt, 76pt, 83.5pt, 1024pt sizes).
4. Web/PWA High-Res Icons & Maskable PNGs.
