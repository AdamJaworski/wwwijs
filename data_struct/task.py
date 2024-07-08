id_list = {
    1: "to_do",
    2: "in_progress",
    3: "in_testing",
    4: "finished"
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

    def __init__(self, task_id, assigned_to, description, title):
        self.task_id = task_id
        self.assigned_to = assigned_to
        self.description = description
        self.title = title

    def move_to_right(self):
        self.assigned_to += 1

    def __str__(self):
        return f"Task: id: {self.task_id}, title: {self.title}, table: {id_list[self.assigned_to]}"
