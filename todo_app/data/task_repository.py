from abc import ABC, abstractmethod
from todo_app.data.task import Task

class task_repository(ABC):

    @abstractmethod 
    def get_tasks(self):
        pass

    @abstractmethod 
    def add_task(self, taskName, status):
        pass

    @abstractmethod 
    def update_task_status(self, id, status):
        pass    

    @abstractmethod 
    def delete_task(self, id):
        pass