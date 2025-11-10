import sqlite3
from db import Database
db = Database()
todo_tasks = db.get_tasks_by_status("todo")
inprogress_tasks = db.get_tasks_by_status("inprogress")
done_tasks = db.get_tasks_by_status("done")
while True:
    choice_input = input(" please choose task_status that you want:\n"
        "1) todo \n"
        "2) inprogress \n"
        "3) done \n"
        "4) exit \n""your choice is : ")
    choice = int(choice_input)
    if choice == 1 :
        print (todo_tasks)
    elif choice == 2 :
        print(inprogress_tasks)
    elif choice == 3 :
        print(done_tasks)
    elif choice == 4 :
        break
    else:
        print ("please enter valid choice\n"
               "Please enter a number from 1 to 4.")

    
    

