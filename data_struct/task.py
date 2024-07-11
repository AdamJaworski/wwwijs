id_list = {
    1: "To Do",
    2: "In Progress",
    3: "In Testing",
    4: "Finished"
}

table_list = {
    "to_do": 1,
    "in_progress": 2,
    "in_testing": 3,
    "finished": 4
}


class Task:
    task_id: str
    assigned_to: int
    description: str
    title: str
    priority: int

    def __init__(self, task_id, assigned_to, description, title, priority):
        self.task_id = task_id
        self.assigned_to = assigned_to
        self.description = description
        self.title = title
        self.priority = priority

    def __str__(self):
        return f"Task: id: {self.task_id}, title: {self.title}, table: {id_list[self.assigned_to]}"
