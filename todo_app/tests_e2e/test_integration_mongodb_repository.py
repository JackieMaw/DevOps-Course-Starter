import pytest
from todo_app.data.mongodb_repository import mongodb_repository
import random
import string
import logging
import pymongo
from dotenv import load_dotenv

from todo_app.data.task import TaskStatus

@pytest.fixture(scope='module')
def testdbname():
    dbname = 'doMeTest_' + ''.join(random.choice(string.ascii_letters) for i in range(10))
    logging.info(f"Creating Test Database: {dbname}")

    load_dotenv(override=True)
    os.environ['MONGODB_DATABASE'] = dbname
    application = app.create_app()
    connection_string = os.getenv('MONGODB_CONNECTIONSTRING')
    dbname = os.getenv('MONGODB_DATABASE')

    logging.info(f"Connecting to MongoDB...")
    client = pymongo.MongoClient(connection_string)
    logging.info(f"Connection Successful.")
    
    collection = client[dbname]
    tasks = collection.tasks

    tasks.insert_one({"Name" : "1. Setup Database", "Status" : "Done"})
    tasks.insert_one({"Name" : "2. Test Connectivity", "Status" : "Done"})
    tasks.insert_one({"Name" : "3. Write Integration Tests", "Status" : "Doing"})
    tasks.insert_one({"Name" : "4. Write Unit Tests with Mocking", "Status" : "ToDo"})
    tasks.insert_one({"Name" : "5. Switch Over", "Status" : "ToDo"})
   
    logging.info(f"Performing Tests On Test Database: {dbname}")
    yield dbname

    # cleanup
    logging.info(f"Deleting Test Database: {dbname}")
    # pymongo.errors.OperationFailure: user is not allowed to do action [dropDatabase] on [doMeTest_YmFytQPMhe.]
    # Solution: Give User atlasAdmin Role
    client.drop_database(dbname)

    for old_dbname in client.list_database_names():
        if old_dbname.startswith("doMeTest_"):            
            logging.info(f"Deleting OLDER Test Database: {old_dbname}")
            client.drop_database(old_dbname)


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

     repo = mongodb_repository(connection_string, testdbname)
    tasks = repo.get_tasks()
    task3 = next(task for task in tasks if task.name == "3. Write Integration Tests") 

    repo.delete_task(task3.id)
    
    tasks = repo.get_tasks()
    task3 = next((task for task in tasks if task.name == "3. Write Integration Tests"), None) 
    assert task3 ==None