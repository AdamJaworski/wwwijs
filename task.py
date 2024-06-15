from uuid import uuid4


id_list = {
    1: "to_do",
    2: "in_progress",
    3: "in_testing",
    4: "finished"
}


class Task:
    id: str
    assigned_to: int
    title: str
    task: str

    def __init__(self):
        self.id = str(uuid4())

    def move_to_right(self):
        self.assigned_to += 1