from database import Database  # Import from your teammate's file

class TodoList:
    def __init__(self):
        self.db = Database()  # Use the database for storage

    def add_task(self, title, description, status="Todo"):
        # Map your status to DB format (lowercase, no space)
        db_status = status.lower().replace(" ", "")
        # Call DB add_task
        new_id = self.db.add_task(title, db_status, description)
        return new_id  # Return the new ID for convenience

    def remove_task(self, task_id):
        # Call DB remove_task
        return self.db.remove_task(task_id)

    def get_all_tasks(self):
        # Call DB get_all_tasks
        tasks = self.db.get_all_tasks()
        # Map DB status back to your format (optional, for consistency)
        for task in tasks:
            if task["status"] == "todo":
                task["status"] = "Todo"
            elif task["status"] == "inprogress":
                task["status"] = "In progress"
            elif task["status"] == "done":
                task["status"] = "Done"
        return tasks

    def close(self):
        # Close the DB when done
        self.db.close()