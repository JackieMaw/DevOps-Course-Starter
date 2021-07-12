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