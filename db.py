import sqlite3


class Database:
    def __init__(self, db_file="todo.db") :
        self.db_file= db_file
        self.conn= sqlite3.connect(self.db_file)
        self.create_table()
        
        
        
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute(''' 
                       CREATE TABLE IF NOT EXISTS tasks (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           title TEXT NOT NULL,
                           status TEXT NOT NULL,
                           description TEXT
                       )
                       ''') 
        self.conn.commit()
        
    def add_task(self , title , status='todo' , description='') :
        valid_status= ['todo', 'inprogress', 'done']
        if status not in valid_status :
            raise ValueError(f"Invalid status, must be one of {valid_status}")
        if not title:
            raise ValueError("Title is reqiured to continue")
        
        try:
            cursor = self.conn.cursor()
            cursor.execute(''' 
                           INSERT INTO tasks (title, status, description)
                           VALUES(?, ? , ?)
                           ''' , (title, status, description))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"error adding task : {e}")
            raise 
        
    def remove_task(self, task_id ):
        try:
            cursor= self.conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE id = ?' , (task_id,))
            self.conn.commit()
            return cursor.rowcount> 0    
        except sqlite3.Error as e:
            print(f"Error {e}")
            raise
    
    def get_tasks_by_status(self, status):
        valid_status=    ['todo', 'inprogress', 'done']
        if status not in valid_status:
            raise ValueError(f"Invalid status. Must be one of: {valid_status}")
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT id, title, status, description FROM tasks WHERE LOWER(status) = LOWER(?)', (status,))
            rows = cursor.fetchall()
            return [{'id': row[0], 'title': row[1], 'status': row[2], 'description': row[3]} for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching tasks by status: {e}")
            raise
    def get_all_tasks(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT id, title, status, description FROM tasks')
            rows = cursor.fetchall()
            return [{'id': row[0], 'title': row[1], 'status': row[2], 'description': row[3]} for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching all tasks: {e}")
            raise

    def close(self):
        
        self.conn.close()    
        
     
if __name__ == '__main__':
    db = Database()
    try:
        new_id = db.add_task("Sample Task", "todo", "This is a test")
        print(f"Added task with ID: {new_id}")
        print("All tasks:", db.get_all_tasks())
        print("Todo tasks:", db.get_tasks_by_status("todo"))
        removed = db.remove_task(new_id)
        print(f"Removed: {removed}")
    finally:
        db.close()       