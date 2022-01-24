import pytest
from dotenv import load_dotenv, find_dotenv
from unittest.mock import Mock, patch
from todo_app.data import mongodb_repository
from todo_app.data.mongodb_repository import mongodb_repository
import random
import string
import logging
import pymongo
from threading import Thread
from todo_app.data.task import TaskStatus
import mongomock 

connection_string = "mongodb://fakemongo.com"

@pytest.fixture(scope='module')
def testdbname():
    with mongomock.patch(servers=(('fakemongo.com', 27017),)): 
        dbname = 'doMeTest'
        logging.info(f"Creating Test Database using mongomock: {dbname}")

        client = pymongo.MongoClient(connection_string)
        collection = client[dbname]
        tasks = collection.tasks

        tasks.insert_one({"Name" : "1. Setup Database", "Status" : "Done"})
        tasks.insert_one({"Name" : "2. Test Connectivity", "Status" : "Done"})
        tasks.insert_one({"Name" : "3. Write Integration Tests", "Status" : "Doing"})
        tasks.insert_one({"Name" : "4. Write Unit Tests with Mocking", "Status" : "ToDo"})
        tasks.insert_one({"Name" : "5. Switch Over", "Status" : "ToDo"})
    
        logging.info(f"Performing Tests On Test Database using mongomock: {dbname}")
        yield dbname

def test_get_tasks(testdbname):
    repo = mongodb_repository(connection_string, testdbname)
    tasks = repo.get_tasks()
    
    assert len(tasks) == 5
    task3 = next(task for task in tasks if task.name == "3. Write Integration Tests") 
    assert task3.status == TaskStatus.Doing


def test_update_task(testdbname):
    repo = mongodb_repository(connection_string, testdbname)
    tasks = repo.get_tasks()
    task3 = next(task for task in tasks if task.name == "3. Write Integration Tests") 

    repo.update_task_status(task3.id, "Done")
    
    tasks = repo.get_tasks()
    task3 = next(task for task in tasks if task.name == "3. Write Integration Tests") 
    assert task3.status == TaskStatus.Done

def test_delete_task(testdbname):
    repo = mongodb_repository(connection_string, testdbname)
    tasks = repo.get_tasks()
    task3 = next(task for task in tasks if task.name == "3. Write Integration Tests") 

    repo.delete_task(task3.id)
    
    tasks = repo.get_tasks()
    task3 = next((task for task in tasks if task.name == "3. Write Integration Tests"), None) 
    assert task3 ==None