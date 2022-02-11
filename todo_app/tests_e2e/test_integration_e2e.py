import os
from threading import Thread
import pytest
from dotenv import load_dotenv
from todo_app import app
import random
import string
import logging
import pymongo

@pytest.fixture(scope='module')
def app_with_temp_board():
   
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

    # tasks.insert_one({"Name" : "1. Setup Database", "Status" : "Done"})
    # tasks.insert_one({"Name" : "2. Test Connectivity", "Status" : "Done"})
    # tasks.insert_one({"Name" : "3. Write Integration Tests", "Status" : "Doing"})
    # tasks.insert_one({"Name" : "4. Write Unit Tests with Mocking", "Status" : "ToDo"})
    # tasks.insert_one({"Name" : "5. Switch Over", "Status" : "ToDo"})
   
    logging.info(f"Performing Tests On Test Database: {dbname}")
    
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application

    thread.join(1)
    
    # cleanup
    logging.info(f"Deleting Test Database: {dbname}")
    # Error: pymongo.errors.OperationFailure: user is not allowed to do action [dropDatabase] on [doMeTest_YmFytQPMhe.]
    # Solution: Give User atlasAdmin Role
    client.drop_database(dbname)

    for old_dbname in client.list_database_names():
        if old_dbname.startswith("doMeTest_"):            
            logging.info(f"Deleting OLDER Test Database: {old_dbname}")
            client.drop_database(old_dbname)


def test_index_page(app_with_temp_board):
    client = app_with_temp_board.test_client()
    response = client.get('/')
    assert "Do Me" in str(response.data)
    assert "card_title" not in str(response.data) # there should be no tasks

def test_add_task(app_with_temp_board):
    client = app_with_temp_board.test_client()
    response = client.get('/')
    assert "Do Me" in str(response.data)
    assert "card-title" not in str(response.data) # there should be no tasks

    response = client.post('/tasks', data=dict(task_name="AddedByIntegrationTest"))
    assert "Redirecting..." in str(response.data)

    response = client.get('/')
    assert "Do Me" in str(response.data)
    assert "card-title" in str(response.data) # there should be at least 1 task
    assert "AddedByIntegrationTest" in str(response.data) # there should be at least 1 task
