class TodoList:
    def __init__(self):
        self.tasks = []  # A list to hold all tasks
        self.next_id = 1  # To give each task a unique ID

    def add_task(self, title, description, status="Todo"):
        # Create a new task dictionary
        task = {
            "id": self.next_id,
            "title": title,
            "description": description,
            "status": status
        }
        # Add it to the list
        self.tasks.append(task)
        # Increase the ID for the next task
        self.next_id += 1

    def remove_task(self, task_id):
        # Loop through tasks to find the one with matching ID
        for task in self.tasks:
            if task["id"] == task_id:
                self.tasks.remove(task)
                return True  # Found and removed
        return False  # Not found

    def get_all_tasks(self):
        # Return a copy of the tasks list
        return self.tasks[:]