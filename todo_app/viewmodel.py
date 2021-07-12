from todo_app.data.task import TaskStatus


class ViewModel:

    def __init__(self, tasks, repository_description):
        self._tasks = tasks
        self._repository_description = repository_description
 
    @property
    def tasks(self):
        return self._tasks

    @property
    def repository_description(self):
        return self._repository_description

    @property
    def task_count(self):
        return len(self._tasks) 

    @property
    def ToDo(self):
        return [x for x in self._tasks if x.status == TaskStatus.ToDo]

    @property
    def Doing(self):
        return [x for x in self._tasks if x.status == TaskStatus.Doing]

    @property
    def Done(self):
        return [x for x in self._tasks if x.status == TaskStatus.Done]