def add_task(title, description, status="todo", db_file="todo.db"):
    """
    Add a new task to the database.
    """
    valid_status = ['todo', 'inprogress', 'done']
    if status not in valid_status:
        raise ValueError(f"Invalid status. Must be one of: {valid_status}")
    if not title:
        raise ValueError("Title is required.")

    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (title, status, description)
            VALUES (?, ?, ?)
        ''', (title, status, description))
        conn.commit()
        new_id = cursor.lastrowid
        print(f"Task added with ID: {new_id}")
        return new_id
    except sqlite3.Error as e:
        print(f"Error adding task: {e}")
        raise
    finally:
        conn.close()

def remove_task(task_id, db_file="todo.db"):
    """
    Remove a task from the database by ID.
    """
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        removed = cursor.rowcount > 0
        if removed:
            print(f"Task with ID {task_id} removed.")
        else:
            print(f"Task with ID {task_id} not found.")
        return removed
    except sqlite3.Error as e:
        print(f"Error removing task: {e}")
        raise
    finally:
        conn.close()

def get_all_tasks(db_file="todo.db"):
    """
    Get all tasks from the database.
    """
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, status, description FROM tasks')
        rows = cursor.fetchall()
        tasks = [{'id': row[0], 'title': row[1], 'status': row[2], 'description': row[3]} for row in rows]
        return tasks
    except sqlite3.Error as e:
        print(f"Error fetching tasks: {e}")
        raise
    finally:
        conn.close()