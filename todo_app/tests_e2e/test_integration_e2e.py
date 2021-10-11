import os
from threading import Thread
from todo_app.data.trello_request_handler import real_trello_request_handler
import pytest
from dotenv import load_dotenv, find_dotenv
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
