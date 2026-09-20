# Daily Brain System Architecture

This document provides a technical overview of the **Daily Brain** multi-platform system architecture, AI agent engine, tool coordination, and storage layers.

---

## 🏗️ High-Level System Architecture

```
                                +---------------------------+
                                |  Natural Language Prompt  |
                                |  or 🎙️ Voice Audio Stream  |
                                +-------------+-------------+
                                              |
                                              v
                              +---------------+---------------+
                              |    Gemini 3.6 Flash Engine    |
                              |   (Autonomous Agent Runtime)  |
                              +---------------+---------------+
                                              |
                          Function Calling / Tool Dispatching
                                              |
               +------------------------------+------------------------------+
               |              |               |               |              |
               v              v               v               v              v
         +------------+ +------------+ +------------+ +------------+ +------------+
         | save_task  | | list_tasks | | comp_task  | | del_task   | | add_subtask|
         +-----+------+ +-----+------+ +-----+------+ +-----+------+ +-----+------+
               |              |               |               |              |
               +--------------+---------------+---------------+--------------+
                                              |
                                              v
                               +--------------+--------------+
                               | Storage Isolation Engine    |
                               | (Local or %APPDATA%/DailyB) |
                               +--------------+--------------+
                                              |
                                              v
                               +--------------+--------------+
                               |     tasks.json Persistence  |
                               +-----------------------------+
```

---

## 🧠 AI Agent & Tool Coordination Layer

Daily Brain utilizes **Google GenAI SDK** with **Gemini 3.6 Flash** to create an autonomous task management agent. 

### Core Agent Characteristics:
1. **Dynamic Temporal Resolution**: Computes real-world dates dynamically using `get_current_date` to resolve terms like *"tomorrow"*, *"this Friday"*, or *"next month"*.
2. **Deterministic Tool Schema**: Strict parameter typings (`priority`: `"high" | "medium" | "low"`, `subtasks`: `list[str]`, `category`: `str`).
3. **Conversational Resilience**: Automatically handles session recreation upon network timeouts.

---

## 💾 Storage & Data Isolation

Daily Brain guarantees data isolation across operating environments via `get_storage_path()` in `main.py`:

- **Windows Standalone App**: `%APPDATA%\DailyBrain\tasks.json`
- **Cloud / Streamlit Hosting**: Local working directory `./tasks.json`
- **Automated Migration**: Copies local `tasks.json` to `%APPDATA%` on first desktop execution.

---

## 📱 Multi-Platform Client Targets

1. **Web / PWA**: Streamlit Cloud + Service Worker v2 + Web App Manifest.
2. **Desktop**: Python 3.11/3.14 + `pywebview` (Microsoft Edge WebView2) + PyInstaller.
3. **Android**: Native Android Kotlin Application + WebChromeClient Media Bridge + SwipeRefresh.
4. **iOS**: Native SwiftUI App + WKWebView Coordinator + Network.framework connection observer.
