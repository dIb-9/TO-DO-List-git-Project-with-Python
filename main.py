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
        print(f"Database and tasks table created successfully at {db_file}")
        
    except sqlite3.Error as e:
        print(f"Error creating database or table: {e}")
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    # Test the function
    create_database()