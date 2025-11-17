import sqlite3

def enter_int ():
           print ("please enter valid choice\n"
               "Please enter a number from 1 to 4.")
def get_tasks_by_status(status):
        valid_status=    ['todo', 'inprogress', 'done']
        if status not in valid_status:
            raise ValueError(f"Invalid status. Must be one of: {valid_status}")
        try:
            db_file= "todo.db"
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute('SELECT id, title, status, description FROM tasks WHERE LOWER(status) = LOWER(?)', (status,))
            rows = cursor.fetchall()
            return [{'id': row[0], 'title': row[1], 'status': row[2], 'description': row[3]} for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching tasks by status: {e}")
            raise
todo_tasks = get_tasks_by_status("todo")
inprogress_tasks = get_tasks_by_status("inprogress")
done_tasks = get_tasks_by_status("done")
while True:
    choice_input = input(" please choose task_status that you want:\n"
        "1) todo \n"
        "2) inprogress \n"
        "3) done \n"
        "4) exit \n""your choice is : ")
    try:
        
        choice = int(choice_input)

    except ValueError:
        
        enter_int()
        continue 
   

    if choice == 1 :
        print (todo_tasks)
    elif choice == 2 :
        print(inprogress_tasks)
    elif choice == 3 :
        print(done_tasks)
    elif choice == 4 :

         exit()
    else :
         enter_int()
    
if __name__ == '__main__':
    
    get_tasks_by_status()
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
        print(f"Database and tasks table created successfully at {db_file}")
        
    except sqlite3.Error as e:
        print(f"Error creating database or table: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    # Test the function
    create_database()
     
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