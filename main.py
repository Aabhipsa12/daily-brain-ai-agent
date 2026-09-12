import os
import json
from datetime import datetime
from dotenv import load_dotenv
from google import genai

load_dotenv()

# --- Storage Helpers & Normalization ---
def get_saved_tasks() -> list:
    """Helper to return normalized list of saved task dictionaries for display and manipulation."""
    if not os.path.exists("tasks.json"):
        return []
    with open("tasks.json", "r", encoding="utf-8") as f:
        try:
            tasks = json.load(f)
        except json.JSONDecodeError:
            return []

    normalized = []
    for t in tasks:
        if not isinstance(t, dict):
            continue
        item = dict(t)
        if "status" not in item:
            item["status"] = "pending"
        if "due_date" not in item:
            item["due_date"] = "Not specified"
        normalized.append(item)
    return normalized

def toggle_task_status(task_idx: int) -> bool:
    """Toggles task status between pending and completed."""
    tasks = get_saved_tasks()
    if 0 <= task_idx < len(tasks):
        current = tasks[task_idx].get("status", "pending")
        tasks[task_idx]["status"] = "completed" if current == "pending" else "pending"
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)
        return True
    return False

def delete_task_by_index(task_idx: int) -> bool:
    """Deletes a task by index from storage."""
    tasks = get_saved_tasks()
    if 0 <= task_idx < len(tasks):
        tasks.pop(task_idx)
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)
        return True
    return False

# --- Tool 1: Save a task with due date ---
def save_task(task: str, priority: str, due_date: str = "Not specified") -> str:
    """Saves a task to a local file called tasks.json, with a priority level and due date.

    Args:
        task: A short description of the task to save.
        priority: How urgent the task is — 'high', 'medium', or 'low'.
        due_date: The resolved calendar deadline (e.g. 'Friday, September 18, 2026' or 'Today'). Use get_current_date to calculate exact dates for relative references.
    """
    tasks = get_saved_tasks()
    tasks.append({
        "task": task,
        "priority": priority.lower(),
        "due_date": due_date,
        "status": "pending",
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    with open("tasks.json", "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)

    return f"Saved task: '{task}' with priority '{priority}' and due date '{due_date}'."

# --- Tool 2: Read back saved tasks ---
def list_tasks(filter_status: str = "all") -> str:
    """Returns saved tasks, optionally filtered by status ('pending', 'completed', or 'all').

    Args:
        filter_status: Filter tasks by 'all', 'pending', or 'completed'.
    """
    tasks = get_saved_tasks()
    if not tasks:
        return "No tasks have been saved yet."

    status = filter_status.lower()
    if status == "pending":
        filtered = [t for t in tasks if t.get("status") == "pending"]
    elif status == "completed":
        filtered = [t for t in tasks if t.get("status") == "completed"]
    else:
        filtered = tasks

    if not filtered:
        return f"No {filter_status} tasks found."

    return json.dumps(filtered, indent=2)

# --- Tool 3: Complete a task ---
def complete_task(task_name: str) -> str:
    """Marks an existing task as completed in tasks.json.

    Args:
        task_name: The name or keyword of the task to mark as completed.
    """
    tasks = get_saved_tasks()
    if not tasks:
        return "You have no saved tasks to complete."

    query = task_name.lower().strip()
    matched_idx = None
    for idx, t in enumerate(tasks):
        if query in t.get("task", "").lower():
            matched_idx = idx
            break

    if matched_idx is not None:
        tasks[matched_idx]["status"] = "completed"
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)
        return f"Marked task '{tasks[matched_idx]['task']}' as completed! 🎉"
    return f"Could not find an active task matching '{task_name}' in your list."

# --- Tool 4: Delete a task ---
def delete_task(task_name: str) -> str:
    """Deletes an existing task from tasks.json.

    Args:
        task_name: The name or keyword of the task to delete.
    """
    tasks = get_saved_tasks()
    if not tasks:
        return "You have no saved tasks to delete."

    query = task_name.lower().strip()
    matched_idx = None
    for idx, t in enumerate(tasks):
        if query in t.get("task", "").lower():
            matched_idx = idx
            break

    if matched_idx is not None:
        removed = tasks.pop(matched_idx)
        with open("tasks.json", "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)
        return f"Deleted task: '{removed.get('task')}' from your list."
    return f"Could not find a task matching '{task_name}' to delete."

# --- Tool 5: Get today's real date ---
def get_current_date() -> str:
    """Returns today's actual date and day of the week, so the assistant can calculate real deadlines."""
    return datetime.now().strftime("%A, %B %d, %Y")

# --- Agent factory ---
_client = None

def get_client(api_key: str = None):
    """Returns a persistent GenAI client instance to prevent garbage collection closure."""
    global _client
    key = api_key or os.getenv("GEMINI_API_KEY")
    if _client is None or getattr(_client, "_current_key", None) != key:
        _client = genai.Client(api_key=key)
        _client._current_key = key
    return _client

def create_agent(api_key: str = None):
    """Creates and returns an active Gemini chat session with all 5 tools."""
    client = get_client(api_key)
    chat = client.chats.create(
        model="gemini-3.6-flash",
        config={
            "tools": [save_task, list_tasks, get_current_date, complete_task, delete_task],
            "system_instruction": (
                "You are Daily Brain, an intelligent productivity and task management assistant. "
                "When the user mentions tasks or todos, organize them into a clear, structured plan with actionable steps. "
                "- If a relative day is mentioned (e.g. 'today', 'tomorrow', 'Friday', 'next week'), call get_current_date first to accurately determine the real calendar date. "
                "- When adding/saving a task, call save_task with a clear task summary, priority ('high', 'medium', or 'low'), and the calculated due_date. "
                "- When the user asks what tasks they have or requests a summary, call list_tasks. "
                "- When the user mentions completing, finishing, or checking off a task, call complete_task with the task name. "
                "- When the user asks to delete or remove a task, call delete_task with the task name."
            )
        }
    )
    # Store strong reference to client on the chat object
    chat._client_ref = client
    return chat

if __name__ == "__main__":
    chat = create_agent()
    print("=== Daily Brain ===")
    print("Type your tasks/thoughts and I'll organize them. Type 'quit' to exit.\n")

    while True:
        task_input = input("What's on your mind? ")

        if task_input.lower() == "quit":
            print("See you tomorrow!")
            break

        try:
            response = chat.send_message(task_input)
            print("\n--- Your Plan ---")
            print(response.text)
            print()
        except Exception as e:
            print(f"Error: {e}\n")
