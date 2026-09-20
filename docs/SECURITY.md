# Daily Brain — Security & Privacy Architecture

This document outlines the security, privacy guarantees, data isolation practices, and credential management standards implemented across **Daily Brain**.

---

## 🔒 1. Zero Cloud Data Leakage & Local-First Storage

- **Local Storage**: All user tasks, checklists, notes, categories, and deadlines are stored strictly in local flat JSON storage.
  - **Windows Desktop App**: `%APPDATA%\DailyBrain\tasks.json`
  - **Cloud/Web Session**: Isolated server session / local storage.
- **Zero Remote Task Databases**: Tasks are never synced, sold, or sent to unauthorized third-party databases.
- **Microphone Audio Transience**: Voice recordings are processed in-memory as ephemeral binary bytes solely to generate text transcripts via Gemini multimodal API and are never persisted to disk or external audio archives.

---

## 🔑 2. Secure Credential & API Key Management

- **No Hardcoded Keys**: The repository contains zero hardcoded API keys, secrets, or access tokens.
- **Environment & Secret Resolution**: Keys are resolved strictly at runtime via:
  1. Operating system environment variable `GEMINI_API_KEY`
  2. Streamlit Cloud secrets management (`st.secrets["GEMINI_API_KEY"]`)
  3. Interactive session input via password-masked fields (`type="password"`).
- **Git Protection**: `.env`, `.keystore`, `.jks`, and credential files are strictly excluded via `.gitignore`.

---

## 🛡️ 3. Safe AI Execution & Function Calling Sandbox

- The AI Agent runtime uses deterministic tool schemas with strict parameter typing.
- Only registered and verified Python functions (`save_task`, `list_tasks`, `complete_task`, `delete_task`, `add_checklist_item`, `update_task_category`, `get_urgent_tasks`, `get_current_date`) can be triggered.
- No dynamic `eval()`, `exec()`, or arbitrary shell execution capabilities are exposed to the AI model.

---

## 📜 4. Privacy Policy Summary

Daily Brain operates under a strict privacy-first model:
1. **User Ownership**: You retain 100% ownership of your tasks and data.
2. **Data Deletion**: Deleting a task immediately and permanently purges it from `tasks.json`.
3. **No Tracking / Analytics Telemetry**: Zero tracking scripts, ads, cookies, or third-party behavioral analytics.
