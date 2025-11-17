import sqlite3


def create_database(db_file="todo.db"):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                status TEXT NOT NULL,
                description TEXT
            )
        ''')
        conn.commit()
        print(f"✓ Database ready: {db_file}")
    except sqlite3.Error as e:
        print(f"Error creating database: {e}")
    finally:
        conn.close()


def add_task(title, description="", status="todo", db_file="todo.db"):
    valid_statuses = ['todo', 'inprogress', 'done']
    status = status.lower()
    if status not in valid_statuses:
        print("Invalid status! Use: todo, inprogress, or done")
        return
    if not title.strip():
        print("Title cannot be empty!")
        return

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tasks (title, status, description) VALUES (?, ?, ?)',
                       (title, status, description))
        conn.commit()
        print(f"Task added! ID: {cursor.lastrowid}")
    except sqlite3.Error as e:
        print(f"Error adding task: {e}")
    finally:
        conn.close()

def remove_task(task_id, db_file="todo.db"):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Task {task_id} deleted successfully.")
        else:
            print(f"Task with ID {task_id} not found.")
    except sqlite3.Error as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def update_task_status(task_id, new_status, db_file="todo.db"):
    valid = ['todo', 'inprogress', 'done']
    new_status = new_status.lower()
    if new_status not in valid:
        print("Invalid status! Choose: todo, inprogress, done")
        return False

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', (new_status, task_id))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Task {task_id} → Now: {new_status.upper()}")
            return True
        else:
            print(f"Task {task_id} not found!")
            return False
    except sqlite3.Error as e:
        print(f"Error updating: {e}")
        return False
    finally:
        conn.close()

def get_tasks_by_status(status, db_file="todo.db"):
    status = status.lower()
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, status, description FROM tasks WHERE LOWER(status) = ?', (status,))
        rows = cursor.fetchall()
        return [{'id': r[0], 'title': r[1], 'status': r[2], 'description': r[3]} for r in rows]
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return []
    finally:
        conn.close()

def get_all_tasks(db_file="todo.db"):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, status, description FROM tasks ORDER BY id')
        rows = cursor.fetchall()
        return [{'id': r[0], 'title': r[1], 'status': r[2], 'description': r[3]} for r in rows]
    except:
        return []
    finally:
        conn.close()

def search_task(db_file="todo.db"):
    print("\nSearch by: (1) ID  |  (2) Title")
    choice = input("→ ").strip()
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        if choice == "1":
            tid = input("Enter ID: ").strip()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (tid,))
        elif choice == "2":
            title = input("Enter title: ").strip()
            cursor.execute("SELECT * FROM tasks WHERE LOWER(title) LIKE ?", (f"%{title.lower()}%",))
        else:
            print("Invalid choice!")
            return

        row = cursor.fetchone()
        if row:
            print("\n" + "═" * 50)
            print(f"ID: {row[0]}")
            print(f"Title: {row[1]}")
            print(f"Status: {row[2].upper()}")
            print(f"Description: {row[3] or '—'}")
            print("═" * 50)
        else:
            print("No task found.")
    except:
        print("Error during search.")
    finally:
        conn.close()


def print_tasks(tasks, category):
    if not tasks:
        print(f"\n→ No tasks in '{category.upper()}'\n")
        return
    print(f"\n{category.upper()} TASKS")
    print("-" * 50)
    for t in tasks:
        desc = t['description'] or "No description"
        print(f"[{t['id']}] {t['title']}")
        print(f"    ↳ {desc}\n")


def main():
    create_database()  

    while True:
        print("\n" + "═" * 45)
        print("         MY TO-DO LIST APP")
        print("═" * 45)
        print("1. View To Do")
        print("2. View In Progress")
        print("3. View Done")
        print("4. View All Tasks")
        print("5. Add New Task")
        print("6. Update Task Status")
        print("7. Delete Task")
        print("8. Search Task")
        print("9. Exit")
        print("-" * 45)

        choice = input("Choose (1-9): ").strip()

        if choice == "1":
            print_tasks(get_tasks_by_status("todo"), "todo")
        elif choice == "2":
            print_tasks(get_tasks_by_status("inprogress"), "inprogress")
        elif choice == "3":
            print_tasks(get_tasks_by_status("done"), "done")
        elif choice == "4":
            tasks = get_all_tasks()
            if tasks:
                print("\nALL TASKS")
                print("-" * 50)
                for t in tasks:
                    print(f"[{t['id']}] {t['title']} → {t['status'].upper()}")
            else:
                print("\nNo tasks yet! Add one :)")
        elif choice == "5":
            title = input("\nTask title: ").strip()
            if not title:
                print("Title required!")
                continue
            desc = input("Description (optional): ").strip()
            add_task(title, desc)
        elif choice == "6":
            try:
                tid = int(input("Task ID: ").strip())
                print("New status → 1.Todo  2.In Progress  3.Done")
                s = input("→ ").strip()
                status_map = {"1": "todo", "2": "inprogress", "3": "done"}
                new_st = status_map.get(s)
                if new_st:
                    update_task_status(tid, new_st)
                else:
                    print("Invalid choice!")
            except ValueError:
                print("ID must be a number!")
        elif choice == "7":
            try:
                tid = int(input("Delete task ID: ").strip())
                remove_task(tid)
            except ValueError:
                print("Invalid ID!")
        elif choice == "8":
            search_task()
        elif choice == "9":
            print("Goodbye! Have a productive day!")
            break
        else:
            print("Please choose 1–9")


if __name__ == "__main__":
    main()