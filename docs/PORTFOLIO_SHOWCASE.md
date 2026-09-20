# 🧠 Daily Brain — Portfolio & Engineering Showcase

> **Autonomous AI-Powered Task Management Agent with Multi-Platform Ecosystem (Web, Windows Desktop, Android & iOS)**

---

## 💼 Resume-Ready Project Descriptions

### 🌟 Concise Bullet Points (for Resume Projects Section)
- **Daily Brain — Autonomous AI Task Management Agent & Multi-Platform Ecosystem** *(Python, Streamlit, Gemini 3.6 Flash, Kotlin, Swift, WebKit, GitHub Actions)*
  - Engineered an autonomous AI task management agent leveraging **Google Gemini 3.6 Flash** and Function Calling to parse conversational natural language, calculate dynamic calendar dates, and automate task scheduling.
  - Architected a **multi-platform ecosystem** supporting Web/PWA, standalone Windows Desktop (`pywebview`, Inno Setup), Android (Kotlin, Android SDK 34), and iOS (SwiftUI, Xcode 15).
  - Built a **multimodal voice transcription engine** enabling hands-free spoken task entry via Gemini audio understanding.
  - Implemented **hierarchical subtask checklists**, category tagging (`#Academics`, `#Exam`, `#Project`), and a real-time **deadline urgency engine** classifying overdue and due-today tasks.
  - Implemented **local-first storage isolation** (`%APPDATA%\DailyBrain\tasks.json`) guaranteeing 100% privacy and zero third-party cloud data exposure.
  - Configured end-to-end **CI/CD pipelines via GitHub Actions** for automated quality testing, desktop artifact compilation, and release publishing.

---

## 🏛️ System Architecture Summary

```
                                 DAILY BRAIN ECOSYSTEM
                                 
      [ Web / PWA ]       [ Windows Desktop ]      [ Android Native ]     [ iOS Native ]
  Streamlit + ServiceWorker  PyWebView (Edge)        Kotlin + WebView      SwiftUI + WKWebView
            \                    |                    |                   /
             \                   |                    |                  /
              v                  v                    v                 v
           +-------------------------------------------------------------+
           |               Daily Brain Application Core (app.py)         |
           |             - Theme-Adaptive Dark UI (Streamlit)            |
           |             - Real-Time Search & Priority Filters           |
           |             - Multimodal Voice Audio Capture Bridge         |
           +------------------------------+------------------------------+
                                          |
                                          v
           +-------------------------------------------------------------+
           |                 Agent Reasoning Engine (main.py)            |
           |               - Gemini 3.6 Flash + Function Calling         |
           |               - Dynamic Temporal Date Parsing               |
           |               - Category & Urgency Classification Engine    |
           +------------------------------+------------------------------+
                                          |
                                          v
           +-------------------------------------------------------------+
           |             Isolated Local Storage Layer (tasks.json)       |
           |               - Windows: %APPDATA%\DailyBrain\tasks.json    |
           |               - Web / Portable: ./tasks.json                |
           +-------------------------------------------------------------+
```

---

## 🚀 Live Demo & Distribution Links

- **Live Web Application**: [https://daily-brain-agent.streamlit.app](https://daily-brain-agent.streamlit.app)
- **GitHub Repository**: [https://github.com/Aabhipsa12/daily-brain-ai-agent](https://github.com/Aabhipsa12/daily-brain-ai-agent)
- **Supported Targets**:
  - **Web**: Progressive Web App with offline service worker.
  - **Desktop**: Standalone `.exe` with Start Menu & Desktop shortcut installers.
  - **Android**: Native Kotlin project with microphone bridge and Gradle wrapper.
  - **iOS**: Native SwiftUI Xcode project with media capture permissions and network monitor.

---

## 🎓 Key Engineering Competencies Demonstrated

1. **Applied Generative AI**: Function calling, autonomous tool loops, multimodal audio processing, prompt engineering.
2. **Full-Stack & Systems Architecture**: Python, Web Technologies, Modern Responsive UI, Local Storage Isolation.
3. **Cross-Platform Engineering**: Windows Desktop (PyInstaller, Inno Setup), Android (Kotlin, Android SDK), iOS (SwiftUI, Xcode).
4. **DevOps & Quality Assurance**: GitHub Actions CI/CD matrix builds, automated unit testing with sandboxed mock fixtures.
