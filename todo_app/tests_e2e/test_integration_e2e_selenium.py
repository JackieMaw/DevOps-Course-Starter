import time
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

    os.environ['LOGIN_DISABLED'] = 'True'
    
    dbname = 'doMeTest_' + ''.join(random.choice(string.ascii_letters) for i in range(10))
    logging.info(f"Creating Test Database: {dbname}")

    load_dotenv(override=True)
    os.environ['MONGODB_DATABASE'] = dbname
    application = app.create_app()
    connection_string = os.getenv('MONGODB_CONNECTIONSTRING')
    dbname = os.getenv('MONGODB_DATABASE')

    client = pymongo.MongoClient(connection_string)
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


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.firefox.options import Options

@pytest.fixture(scope='module')
def driver():
    opts = Options()
    opts.headless = True
    with webdriver.Firefox(options=opts) as driver:
        yield driver

def test_task_journey(driver : webdriver.Firefox, app_with_temp_board):

    #load the index
    driver.get('http://localhost:5000/')
    assert driver.title == 'Do Me'

    #check that there are no tasks
    tasks = driver.find_elements_by_class_name("card-title")
    assert len(tasks) == 0

    #add a new task
    elem = driver.find_element_by_name("task_name")
    elem.clear()
    elem.send_keys("AddedByIntegrationTest_Selenium")
    elem.send_keys(Keys.RETURN)

    #check that the task has been added
    element = WebDriverWait(driver, 5).until(lambda d: d.find_element_by_xpath("//h5[@class='card-title' and contains(text(), 'AddedByIntegrationTest_Selenium')]"))

    #delete the task
    elem = driver.find_element_by_class_name("btn-danger")
    elem.click()

    #check that there are no tasks
    time.sleep(2)
    tasks = driver.find_elements_by_class_name("card-title")
    assert len(tasks) == 0

    driver.close()
