# Daily Brain API & Agent Tool Reference

This document outlines the callable tool functions provided to the Gemini 3.6 Flash agent in `main.py`.

---

## 🛠️ Tool Definitions

### 1. `save_task`
Saves a new structured task to persistent storage.

```python
def save_task(
    task: str,
    priority: str = "medium",
    due_date: str = "Not specified",
    category: str = "General",
    subtasks: list[str] = None
) -> str
```
- **`task`** *(required)*: Descriptive name/summary of the task.
- **`priority`**: `"high"`, `"medium"`, or `"low"`.
- **`due_date`**: Calendar date (e.g. `YYYY-MM-DD`) or status.
- **`category`**: Classification tag (`Academics`, `Project`, `Exam`, `Work`, `Personal`, etc.).
- **`subtasks`**: Optional list of subtask checklist strings.

---

### 2. `list_tasks`
Retrieves currently stored tasks.

```python
def list_tasks(status: str = "all") -> str
```
- **`status`**: `"all"`, `"pending"`, or `"completed"`.

---

### 3. `get_current_date`
Returns current date and day of the week for dynamic calculation.

```python
def get_current_date() -> str
```

---

### 4. `complete_task`
Marks an existing task as completed.

```python
def complete_task(task_name: str) -> str
```

---

### 5. `delete_task`
Deletes a task matching the given search query.

```python
def delete_task(task_name: str) -> str
```

---

### 6. `add_checklist_item`
Adds a subtask item to an existing task.

```python
def add_checklist_item(task_name: str, subtask_title: str) -> str
```

---

### 7. `update_task_category`
Updates the category classification of a task.

```python
def update_task_category(task_name: str, new_category: str) -> str
```

---

### 8. `get_urgent_tasks`
Analyzes stored tasks and returns overdue tasks or tasks due within 24 hours.

```python
def get_urgent_tasks() -> str
```

---

### 9. `transcribe_audio`
Transcribes audio byte recordings into plain English using Gemini multimodal audio.

```python
def transcribe_audio(audio_bytes: bytes, api_key: str = None) -> str
```
