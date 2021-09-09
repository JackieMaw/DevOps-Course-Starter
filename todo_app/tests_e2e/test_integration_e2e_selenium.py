import time
import os
from threading import Thread
from todo_app.data.trello_request_handler import real_trello_request_handler
import pytest
from dotenv import load_dotenv
from todo_app import app
import random
import string
import logging

@pytest.fixture(scope='module')
def app_with_temp_board():
    # pytest runs tests in parallel, so each test must have it's own board
    board_name = 'TEST_BOARD_' + ''.join(random.choice(string.ascii_letters) for i in range(10))
    logging.info(f"NEW BOARD NAME FOR TEST => {board_name}")
    load_dotenv(override=True)
    os.environ['TRELLO_BOARD_NAME'] = board_name
    application = app.create_app()
    key = os.getenv('TRELLO_KEY')
    token = os.getenv('TRELLO_TOKEN')
    request_handler = real_trello_request_handler(key, token, application.logger) # don't know how to get logger until app created

    try:
         # if the board already exists, delete it
        board_id = request_handler.get_board(board_name)["id"]
        request_handler.delete_board(board_id)
        request_handler.create_board(board_name)
    except:
        request_handler.create_board(board_name)
    finally:
        board_id = request_handler.get_board(board_name)["id"]
    
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application

    thread.join(1)
    request_handler.delete_board(board_id) # cleanup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

@pytest.fixture
def driver():
    with webdriver.Firefox() as driver:
        yield driver

def test_task_journey(driver : webdriver.Firefox, app_with_temp_board):
    driver.get('http://localhost:5000/')
    assert driver.title == 'Do Me'

    elem = driver.find_element_by_name("task_name")
    elem.clear()
    elem.send_keys("AddedByIntegrationTest_Selenium")
    elem.send_keys(Keys.RETURN)

    #check that the task has been added
    element = WebDriverWait(driver, 5).until(lambda d: d.find_element_by_xpath("//h5[@class='card-title' and contains(text(), 'AddedByIntegrationTest_Selenium')]"))

    elem = driver.find_element_by_class_name("btn-danger")
    elem.click()

    time.sleep(2)

    #check that there are no tasks
    elemements = driver.find_elements_by_class_name("card-title")
    assert len(elemements) == 0

    driver.close()
