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

    
    

