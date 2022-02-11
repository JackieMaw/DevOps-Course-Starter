from enum import Enum

class TaskStatus(Enum):
    ToDo = "ToDo"
    Doing = "Doing"
    Done = "Done"

class Task():

    def __init__(self, id, name, status : TaskStatus):
        self.id = id
        self.name = name
        self.status = status