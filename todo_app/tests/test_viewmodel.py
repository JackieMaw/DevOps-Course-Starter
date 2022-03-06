from todo_app.viewmodel import ViewModel
from todo_app.data.task import Task, TaskStatus
import pytest

@pytest.fixture
def tasks():
    task1_ToDo = Task(1, "Task1", TaskStatus.ToDo)
    task2_Doing = Task(2, "Task2", TaskStatus.Doing)
    task3_Done = Task(2, "Task2", TaskStatus.Done)
    return [task1_ToDo, task2_Doing, task3_Done]

def test_viewmodel_returns_ToDo(tasks):

    # Arrange    
    view_model = ViewModel(tasks, "username", "UserRole.writer")

    # Act
    todo_list = view_model.ToDo

    # Assert
    assert len(todo_list) == 1
    assert todo_list[0] == tasks[0] #this is horrible!

def test_viewmodel_returns_Doing(tasks):

    # Arrange    
    view_model = ViewModel(tasks, "username", "UserRole.writer")

    # Act
    todo_list = view_model.Doing

    # Assert
    assert len(todo_list) == 1
    assert todo_list[0] == tasks[1] #this is horrible!

def test_viewmodel_returns_Done(tasks):

    # Arrange    
    view_model = ViewModel(tasks, "username", "UserRole.writer")

    # Act
    todo_list = view_model.Done

    # Assert
    assert len(todo_list) == 1
    assert todo_list[0] == tasks[2] #this is horrible!