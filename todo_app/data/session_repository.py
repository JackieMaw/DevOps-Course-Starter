from flask import session
from todo_app.data.task import task

_DEFAULT_taskS = [ task(1, 'Fake Task 1', 'To Do'), task(2, 'Fake Task 2', 'To Do') ]

class session_repository:

    def get_tasks(self):
        return session.get('tasks', _DEFAULT_taskS.copy())

    def __get_task(self, id):
        tasks = self.get_tasks()
        return next((t for t in tasks if t.id == int(id)), None)

    def add_task(self, title, status):
        tasks = self.get_tasks()

        # Determine the ID for the task based on that of the previously added task
        id = tasks[-1].id + 1 if tasks else 0

        new_task = task(id, title, status)
        tasks.append(new_task)
        session['tasks'] = tasks

    def update_task_status(self, id, status):
        task_to_update = self.__get_task(id)
        task_to_update.status = status

    def delete_task(self, id):
        tasks = self.get_tasks()
        task_to_delete = next((t for t in tasks if t.id == int(id)), None)
        tasks.remove(task_to_delete)
        session['tasks'] = tasks