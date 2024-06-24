id_list = {
    1: "to_do",
    2: "in_progress",
    3: "in_testing",
    4: "finished"
}


class Task:
    task_id: str
    assigned_to: int
    description: str

    def __init__(self, task_id, assigned_to, description):
        self.task_id = task_id
        self.assigned_to = assigned_to
        self.description = description

    def move_to_right(self):
        self.assigned_to += 1