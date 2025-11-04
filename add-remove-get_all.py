import json
import os
from enum import Enum

class Status(Enum):
    TODO = 'Todo'
    IN_PROGRESS = 'In progress'
    DONE = 'Done'

class TodoList:
    def __init__(self):
        self.tasks = {}  # Use dict for O(1) lookups/removals (key: id, value: task dict)
        self.next_id = 1
        # Optionally load from file on init, but leaving it manual for flexibility

    def add_task(self, title, description, status=Status.TODO.value):
        """
        Adds a new task to the TODO list.
        
        :param title: The title of the task (str)
        :param description: The description of the task (str)
        :param status: The initial status of the task (default: 'Todo') (str)
        """
        if not isinstance(title, str) or not isinstance(description, str) or not isinstance(status, str):
            raise ValueError("Title, description, and status must be strings.")
        if not title.strip() or not description.strip():
            raise ValueError("Title and description cannot be empty.")
        if any(task['title'] == title for task in self.tasks.values()):
            raise ValueError("Task with this title already exists.")
        if status not in [s.value for s in Status]:
            raise ValueError("Status must be one of: 'Todo', 'In progress', 'Done'.")
        
        task = {
            'id': self.next_id,
            'title': title,
            'description': description,
            'status': status
        }
        self.tasks[self.next_id] = task
        self.next_id += 1

    def remove_task(self, task_id):
        """
        Removes a task from the TODO list by its ID.
        
        :param task_id: The ID of the task to remove (int)
        :return: True if task was removed, False if not found
        """
        try:
            task_id = int(task_id)  # Ensure it's an int, convert if needed
        except ValueError:
            raise ValueError("Task ID must be an integer.")
        
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def get_all_tasks(self):
        """
        Returns a list of all tasks in the TODO list, sorted by ID.
        
        :return: List of task dictionaries
        """
        # Sort by ID and return copies to prevent external modification
        sorted_tasks = sorted(self.tasks.values(), key=lambda t: t['id'])
        return [task.copy() for task in sorted_tasks]

    def get_task_by_id(self, task_id):
        """
        Retrieves a task by its ID.
        
        :param task_id: The ID of the task (int)
        :return: Task dictionary if found, None otherwise
        """
        try:
            task_id = int(task_id)
        except ValueError:
            raise ValueError("Task ID must be an integer.")
        
        task = self.tasks.get(task_id)
        return task.copy() if task else None

    def save_to_file(self, filename='tasks.json'):
        """
        Saves the current tasks to a JSON file.
        
        :param filename: The file to save to (default: 'tasks.json')
        """
        data = {
            'next_id': self.next_id,
            'tasks': list(self.tasks.values())  # Convert dict to list for JSON
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def load_from_file(self, filename='tasks.json'):
        """
        Loads tasks from a JSON file if it exists.
        
        :param filename: The file to load from (default: 'tasks.json')
        """
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
                self.next_id = data.get('next_id', 1)
                self.tasks = {task['id']: task for task in data.get('tasks', [])}
        else:
            print(f"File '{filename}' not found. Starting with empty list.")