# 🧠 Daily Brain — Autonomous AI Task Management Agent

[![Live Demo](https://img.shields.io/badge/Live_Demo-daily--brain--agent.streamlit.app-brightgreen?logo=streamlit&logoColor=white)](https://daily-brain-agent.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.40%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-3.6%20Flash-orange?logo=google&logoColor=white)](https://aistudio.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**Daily Brain** is an intelligent, context-aware productivity assistant that converts everyday natural language (spoken or typed) into structured, scheduled, and actionable plans. Powered by Google Gemini's native function/tool calling and multimodal audio understanding, it dynamically reasons about deadlines, computes real calendar dates, tracks sub-step checklists, manages category tags, and provides visual urgency alerts through an interactive Streamlit web dashboard and command-line interface.

---

## 🌟 Key Features

- **🎙️ Voice Input (Speech-to-Text)**: Speak tasks, deadlines, and notes aloud directly from any desktop or mobile browser. Gemini 3.6 Flash multimodal AI transcribes voice input with high precision and immediately executes task scheduling.
- **📝 Sub-tasks & Actionable Checklists**: Tasks are automatically broken down into 2–5 structured sub-steps with interactive checkboxes and real-time progress bars.
- **🏷️ Category & Domain Tags**: Automatically categorizes items into `#Academics`, `#Project`, `#Exam`, `#Personal`, and `#Work` with custom-styled color pills.
- **🚨 Deadlines & Urgency Engine**: Dynamic deadline reasoning with visual urgency badges (`🚨 Overdue`, `⚠️ Due Today`, `⏰ Due Tomorrow`, `⏳ Upcoming`), an automated **Attention Required** banner, and urgency-based sorting.
- **Autonomous Tool Calling (8 Native Python Tools)**:
  - `get_current_date`: Resolves relative dates against the live calendar.
  - `save_task`: Saves tasks with priority, due date, category, and subtasks.
  - `list_tasks`: Retrieves active or completed tasks for summarization.
  - `complete_task`: Autonomously identifies and marks tasks as completed.
  - `delete_task`: Removes obsolete tasks based on user intent.
  - `add_checklist_item`: Adds actionable steps to existing checklists.
  - `update_task_category`: Reassigns domain tags.
  - `get_urgent_tasks`: Surfaces overdue and upcoming deadlines.
- **Interactive Web Dashboard**:
  - **Live AI Assistant**: Multi-turn conversational chat with session memory, quick prompts, and voice dictation.
  - **Task Board**: Real-time cards displaying priority badges, category pills, checklist progress, and urgency statuses.
  - **Search & Multi-Faceted Filters**: Filter by Status, Category, Priority, or search by keyword.
  - **One-Click Actions**: Toggle completion, add steps, or delete tasks directly from UI cards.
- **Dual Interface Architecture**: Seamlessly switch between the **Streamlit Web UI** (`app.py`) and a lightweight **Terminal CLI** (`main.py`).
- **100% Free & Lightweight**: Operates entirely on free-tier services (Google AI Studio Gemini API + Streamlit Community Cloud) with zero paid database dependencies.

---

## 🏗️ System Architecture

```
                       ┌─────────────────────────┐
                       │   User Natural Input    │
                       │     (Text / Voice)      │
                       └────────────┬────────────┘
                                    │
               ┌────────────────────┴────────────────────┐
               ▼                                         ▼
     ┌──────────────────┐                      ┌──────────────────┐
     │  Streamlit App   │                      │   Terminal CLI   │
     │  (Voice + UI)    │                      │    (main.py)     │
     └─────────┬────────┘                      └─────────┬────────┘
               │                                         │
               └────────────────────┬────────────────────┘
                                    ▼
                     ┌─────────────────────────────┐
                     │    Gemini 3.6 Flash Agent   │
                     │  (Multimodal Audio + Tools) │
                     └──────────────┬──────────────┘
                                    │
       ┌────────────────────────────┼────────────────────────────┐
       ▼                            ▼                            ▼
┌───────────────┐          ┌─────────────────┐          ┌─────────────────┐
│get_current_date│         │    save_task    │          │  complete_task  │
│(Date Math)    │          │(Cat/Due/Subtasks│          │  & delete_task  │
└───────┬───────┘          └────────┬────────┘          └────────┬────────┘
        │                           │                            │
        │                  ┌────────┴────────┐                   │
        │                  │add_checklist_item│                   │
        │                  │get_urgent_tasks │                   │
        │                  └────────┬────────┘                   │
        └───────────────────────────┼────────────────────────────┘
                                    ▼
                         ┌──────────────────────┐
                         │      tasks.json      │
                         │ (Persistent Storage) │
                         └──────────────────────┘
```

---

## 📁 Project Structure

```
Daily-brain/
├── app.py              # Streamlit web application, voice input & interactive task board
├── main.py             # Agent engine, 8 tool definitions, audio transcription & CLI
├── tasks.json          # Persistent JSON storage for task data
├── requirements.txt    # Minimal, pinned Python dependencies
├── .env.example        # Environment variable template
├── .gitignore          # Security rules for credentials and cache
└── README.md           # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- A free Gemini API Key from [Google AI Studio](https://aistudio.google.com/)

### 1. Clone the Repository

```bash
git clone https://github.com/Aabhipsa12/daily-brain-ai-agent.git
cd daily-brain-ai-agent
```

### 2. Set Up a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Your API Key

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Add your Gemini API Key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

---

## 💻 Usage

### Web Interface (Streamlit)

Launch the interactive web application:

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

### Terminal Interface (CLI)

Run the agent in your terminal:

```bash
python main.py
```

Type `quit` to exit.

---

## 💬 Example Voice & Text Interactions

| User Input (Spoken or Typed) | Agent Action & Tool Called | Resulting State |
| :--- | :--- | :--- |
| *"Finish my CN assignment by Friday #Academics"* | `get_current_date` ➡️ `save_task(..., category="Academics", priority="high", due_date="Friday, Sep 18, 2026", subtasks=[...])` | Task saved with #Academics tag, calculated calendar date & checklist steps. |
| *"Prepare for DAA exam next Wednesday #Exam"* | `get_current_date` ➡️ `save_task(..., category="Exam", priority="high", due_date="Wednesday, Sep 23, 2026")` | Saved under #Exam with study milestones. |
| *"What tasks are overdue or due soon?"* | `get_urgent_tasks()` | Highlights urgent deadlines and displays overdue items. |
| *"Add subtask test client to CN assignment"* | `add_checklist_item("CN assignment", "test client")` | Checklist dynamically updated with new sub-step. |
| *"Mark DAA assignment as done"* | `complete_task("DAA assignment")` | Status toggled to `completed` in `tasks.json`. |
| *"Delete the Google Form task"* | `delete_task("Google Form")` | Task permanently removed from storage. |

---

---

## 📱 Mobile Applications (PWA, Android & iOS)

Daily Brain is designed to run seamlessly on smartphones and tablets across three deployment modes:

### 1. Progressive Web App (PWA — iPhone & Android)
The quickest, zero-cost way to install Daily Brain directly on any mobile device:
- **iPhone (iOS Safari)**:
  1. Open [daily-brain-agent.streamlit.app](https://daily-brain-agent.streamlit.app) in Safari.
  2. Tap the **Share** button (box with upward arrow).
  3. Scroll down and tap **"Add to Home Screen"**.
  4. Tap **Add** — Daily Brain will now launch from your home screen as a full-screen, standalone app with its custom app icon.
- **Android (Google Chrome)**:
  1. Open [daily-brain-agent.streamlit.app](https://daily-brain-agent.streamlit.app) in Chrome.
  2. Tap the **"Install Daily Brain"** banner (or tap the 3 dots menu ➡️ **"Install app"**).
  3. Daily Brain is added directly into your Android launcher and app drawer.

### 2. Native Android Application (`android/`)
A dedicated native Android Kotlin application with full-screen hardware acceleration, HTML5 microphone permission handling, and pull-to-refresh:
1. Open the `android/` folder in **Android Studio**.
2. Sync Gradle dependencies.
3. Select your connected Android phone or Android Virtual Device (AVD).
4. Click **Run** (`Shift + F10`) or go to **Build > Build Bundle(s) / APK(s) > Build APK(s)** to produce an installable `.apk`.

### 3. Native iOS Application (`ios/`)
A native SwiftUI `WKWebView` wrapper project configured with microphone permissions (`NSMicrophoneUsageDescription`) for voice task dictation:
1. Open the `ios/` folder in **Xcode** on macOS.
2. Select your target device (iPhone or iOS Simulator).
3. Click **Run** (`Cmd + R`) to compile and launch.

---

## 🛠️ Tech Stack & Skills Demonstrated

- **Core AI & Multimodal**: Google GenAI SDK (`google-genai`), Gemini 3.6 Flash (Text & Audio Understanding)
- **Agent Architecture**: Autonomous Function/Tool Calling (8 tools), Multi-turn Chat Session State
- **Speech Processing**: Native In-Browser Audio Capture (16kHz WAV), Multimodal STT Transcription
- **Frontend**: Streamlit, Custom Responsive CSS (Dark/Light Mode), Interactive Checklists & Badges
- **Backend & Logic**: Python 3.10+, JSON Persistence, Urgency Engine & Deterministic Date Math
- **DevOps & Security**: Environment isolation (`python-dotenv`), Git hygiene, Secret management

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
