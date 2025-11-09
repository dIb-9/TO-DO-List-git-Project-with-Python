import sqlite3

def get_task_status():
    
    choice = input("Search task by (1) ID or (2) Name? ")

    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()

    if choice == "1":
        task_id = input("Enter the task ID: ")
        cursor.execute("SELECT id, title, status, description FROM tasks WHERE id = ?", (task_id,))
    elif choice == "2":
        task_name = input("Enter the task name (title): ")
        cursor.execute("SELECT id, title, status, description FROM tasks WHERE title = ?", (task_name,))
    else:
        print("Invalid choice. Please select 1 or 2.")
        conn.close()
        return

    row = cursor.fetchone()
    conn.close()

    if row:
        print("\nTask found:")
        print("-" * 50)
        print(f"ID: {row[0]}")
        print(f"Title: {row[1]}")
        print(f"Status: {row[2]}")
        print(f"Description: {row[3]}")
        print("-" * 50)
    else:
        print("No task found with that ID or name.")