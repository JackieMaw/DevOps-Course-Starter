from todo_app.data.task import TaskStatus

class ViewModel:

    def __init__(self, tasks, username, user_role):
        self._tasks = tasks
        self._username = username
        self._user_role = str(user_role)
 
    @property
    def tasks(self):
        return self._tasks

    @property
    def task_count(self):
        return len(self._tasks) 

    @property
    def username(self):
        return self._username

    @property
    def user_role(self):
        return self._user_role

    @property
    def ToDo(self):
        return [x for x in self._tasks if x.status == TaskStatus.ToDo]

    @property
    def Doing(self):
        return [x for x in self._tasks if x.status == TaskStatus.Doing]

    @property
    def Done(self):
        return [x for x in self._tasks if x.status == TaskStatus.Done]