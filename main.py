import sqlite3

def create_database(db_file="todo.db"):
    """
    Create a SQLite database and a tasks table if they don't exist.
    
    :param db_file: Path to the SQLite database file (default: 'todo.db')
    :return: None
    """
    try:
        # Connect to the database (creates the file if it doesn't exist)
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Create the tasks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                status TEXT NOT NULL,
                description TEXT
            )
        ''')
        
        # Commit the changes and close the connection
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