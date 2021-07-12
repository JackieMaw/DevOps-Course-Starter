from enum import Enum

class TaskStatus(Enum):
    ToDo = "To Do"
    Doing = "Doing"
    Done = "Done"

class Task():

    def __init__(self, id, name, status : TaskStatus):
        self.id = id
        self.name = name
        self.status = status