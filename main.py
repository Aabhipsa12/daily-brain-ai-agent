import os
import json
from datetime import datetime
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# --- Tool 1: Save a task ---
def save_task(task: str, priority: str) -> str:
    """Saves a task to a local file called tasks.json, with a priority level.

    Args:
        task: A short description of the task to save.
        priority: How urgent the task is — 'high', 'medium', or 'low'.
    """
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as f:
            tasks = json.load(f)
    else:
        tasks = []

    tasks.append({
        "task": task,
        "priority": priority,
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=2)

    return f"Saved task: '{task}' with priority '{priority}'."

# --- Tool 2: Read back saved tasks ---
def list_tasks() -> str:
    """Returns all previously saved tasks, so the assistant can review or summarize them."""
    if not os.path.exists("tasks.json"):
        return "No tasks have been saved yet."

    with open("tasks.json", "r") as f:
        tasks = json.load(f)

    if not tasks:
        return "No tasks have been saved yet."

    return json.dumps(tasks, indent=2)

# --- Chat session with both tools available ---
chat = client.chats.create(
    model="gemini-3.6-flash",
    config={
        "tools": [save_task, list_tasks],
        "system_instruction": (
            "You are a productivity assistant. When the user tells you about tasks, "
            "organize them into a clear plan. If a task seems worth remembering long-term, "
            "call save_task to actually save it. If the user asks what's on their list, "
            "their tasks, or similar, call list_tasks and summarize the result clearly."
        )
    }
)

print("=== Daily Brain ===")
print("Type your tasks/thoughts and I'll organize them. Type 'quit' to exit.\n")

while True:
    task_input = input("What's on your mind? ")

    if task_input.lower() == "quit":
        print("See you tomorrow!")
        break

    response = chat.send_message(task_input)

    print("\n--- Your Plan ---")
    print(response.text)
    print()