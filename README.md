# 🧠 Daily Brain — Autonomous AI Task Management Agent

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-3.6%20Flash-orange?logo=google&logoColor=white)](https://aistudio.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**Daily Brain** is an intelligent, context-aware productivity assistant that converts everyday natural language into structured, scheduled, and actionable plans. Powered by Google Gemini's native function/tool calling, it dynamically reasons about deadlines, computes real calendar dates, and manages your personal tasks through an interactive Streamlit web dashboard and command-line interface.

---

## 🌟 Key Features

- **Natural Language Task Capture**: Express thoughts naturally (e.g., *"Finish my CN assignment by Friday"*, *"Prepare for DAA exam next Wednesday with high priority"*).
- **Autonomous Tool/Function Calling**: The agent dynamically selects and coordinates 5 Python tools based on conversational intent:
  - `get_current_date`: Resolves relative dates (*"today"*, *"tomorrow"*, *"this Friday"*, *"next week"*) against the live calendar.
  - `save_task`: Extracts task descriptions, infers priority, and records exact deadlines.
  - `list_tasks`: Retrieves active and completed tasks for summarization and status reviews.
  - `complete_task`: Autonomously identifies and marks tasks as completed through natural language.
  - `delete_task`: Removes obsolete tasks based on intent.
- **Intelligent Action Plans**: In addition to saving tasks, Daily Brain synthesizes realistic, step-by-step execution strategies (e.g., Pomodoro time blocks, requirement checks, submission verification).
- **Interactive Web Dashboard**:
  - **Live AI Assistant**: Multi-turn conversational chat with session memory and quick-action prompt buttons.
  - **Task Board**: Real-time cards displaying priority badges (High 🔴, Medium 🟡, Low 🟢), status pills (Pending/Done), and calendar deadlines.
  - **Search & Filter**: Filter by status (*Active / Pending*, *Completed*), filter by priority, or search by keyword.
  - **One-Click Actions**: Toggle completion or delete tasks directly with UI controls.
- **Dual Interface Architecture**: Seamlessly switch between the **Streamlit Web UI** (`app.py`) and a lightweight **Terminal CLI** (`main.py`).
- **Free & Lightweight**: Designed to run entirely on free-tier services (Google AI Studio Gemini API + Streamlit Community Cloud) with zero paid database dependencies.

---

## 🏗️ System Architecture

```
                       ┌─────────────────────────┐
                       │   User Natural Input    │
                       └────────────┬────────────┘
                                    │
               ┌────────────────────┴────────────────────┐
               ▼                                         ▼
     ┌──────────────────┐                      ┌──────────────────┐
     │  Streamlit App   │                      │   Terminal CLI   │
     │     (app.py)     │                      │    (main.py)     │
     └─────────┬────────┘                      └─────────┬────────┘
               │                                         │
               └────────────────────┬────────────────────┘
                                    ▼
                     ┌─────────────────────────────┐
                     │    Gemini 3.6 Flash Agent   │
                     │  (Autonomous Tool Selector) │
                     └──────────────┬──────────────┘
                                    │
       ┌────────────────────────────┼────────────────────────────┐
       ▼                            ▼                            ▼
┌───────────────┐          ┌─────────────────┐          ┌─────────────────┐
│get_current_date│          │    save_task    │          │  complete_task  │
│  (Date Math)  │          │(Priority & Due) │          │  & delete_task  │
└───────┬───────┘          └────────┬────────┘          └────────┬────────┘
        │                           │                            │
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
├── app.py              # Streamlit web application & interactive task board
├── main.py             # Agent engine, tool definitions & CLI runner
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

## 💬 Example Interactions

| User Prompt | Agent Action & Tool Called | Resulting State |
| :--- | :--- | :--- |
| *"Finish my CN assignment by Friday"* | `get_current_date` ➡️ `save_task(..., priority="high", due_date="Friday, Sep 18, 2026")` | Task saved with calculated calendar date & high priority. |
| *"Prepare for DAA exam next Wednesday"* | `get_current_date` ➡️ `save_task(..., priority="high", due_date="Wednesday, Sep 23, 2026")` | Saved with exam date breakdown. |
| *"Mark DAA assignment as done"* | `complete_task("DAA assignment")` | Status toggled to `completed` in `tasks.json`. |
| *"What tasks are currently pending?"* | `list_tasks(filter_status="pending")` | Generates a clean bulleted summary of active deadlines. |
| *"Delete the Google Form task"* | `delete_task("Google Form")` | Task permanently removed from storage. |

---

## ☁️ Deployment (Streamlit Community Cloud)

This project is configured for one-click free deployment on [Streamlit Community Cloud](https://streamlit.io/cloud):

1. Push your repository to GitHub.
2. Sign in to Streamlit Cloud and click **"New app"**.
3. Select this repository, branch `main`, and main file path `app.py`.
4. Under **Advanced Settings > Secrets**, add your API key:
   ```toml
   GEMINI_API_KEY = "your_actual_api_key_here"
   ```
5. Click **Deploy**!

---

## 🛠️ Tech Stack & Skills Demonstrated

- **Core AI**: Google GenAI SDK (`google-genai`), Gemini 3.6 Flash
- **Agent Architecture**: Autonomous Function/Tool Calling, Multi-turn Chat Session State
- **Frontend**: Streamlit, Custom Responsive CSS (Dark/Light Mode)
- **Backend & Logic**: Python 3.10+, JSON Persistence, Deterministic Date Reasoning
- **DevOps & Security**: Environment isolation (`python-dotenv`), Git hygiene, Secret management

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
