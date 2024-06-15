
id_list = {
    1: "to_do",
    2: "in_progress"
}


class Task:
    id: str
    assigned_to: int

    def move_to_right(self):
        self.assigned_to += 1