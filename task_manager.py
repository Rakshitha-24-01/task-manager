import json
import os
import sys

TASK_FILE = 'tasks.json'

# Load tasks from file
def load_tasks():
    if os.path.exists(TASK_FILE):
        with open(TASK_FILE, 'r') as f:
            try:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                else:
                    return []
            except json.JSONDecodeError:
                return []
    return []

# Save tasks to file
def save_tasks(tasks):
    with open(TASK_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

# Add a new task
def add_task(description):
    tasks = load_tasks()
    tasks.append({'description': description, 'done': False})
    save_tasks(tasks)
    print(f"✅ Task added: {description}")

# List tasks
def list_tasks(show_all=True):
    tasks = load_tasks()
    if not tasks:
        print("📭 No tasks found.")
        return
    for i, task in enumerate(tasks):
        status = "✅" if task['done'] else "⏳"
        if show_all or not task['done']:
            print(f"{i + 1}. {status} {task['description']}")

# Mark a task as done
def mark_done(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]['done'] = True
        save_tasks(tasks)
        print(f"🎉 Task marked as done: {tasks[index]['description']}")
    else:
        print("❌ Invalid task number.")

# Delete a task
def delete_task(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        removed = tasks.pop(index)
        save_tasks(tasks)
        print(f"🗑️ Deleted task: {removed['description']}")
    else:
        print("❌ Invalid task number.")

# Show help message
def print_help():
    print("""
📌 Task Manager CLI

Usage:
  python task_manager.py add "Task description"    → Add new task
  python task_manager.py list                      → List all tasks
  python task_manager.py pending                   → List only pending tasks
  python task_manager.py done <task_number>        → Mark task as done
  python task_manager.py delete <task_number>      → Delete a task
  python task_manager.py help                      → Show help
""")

# Main command-line interface
if __name__ == "__main__":
    args = sys.argv[1:]

    if not args or args[0] == "help":
        print_help()
    elif args[0] == "add":
        if len(args) < 2:
            print("❌ Please provide a task description.")
        else:
            add_task(' '.join(args[1:]))
    elif args[0] == "list":
        list_tasks(show_all=True)
    elif args[0] == "pending":
        list_tasks(show_all=False)
    elif args[0] == "done":
        if len(args) < 2 or not args[1].isdigit():
            print("❌ Please provide a valid task number.")
        else:
            mark_done(int(args[1]) - 1)
    elif args[0] == "delete":
        if len(args) < 2 or not args[1].isdigit():
            print("❌ Please provide a valid task number.")
        else:
            delete_task(int(args[1]) - 1)
    else:
        print("❌ Unknown command.")
        print_help()
