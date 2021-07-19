import os
from threading import Thread
from todo_app.data.trello_request_handler import real_trello_request_handler
import pytest
from dotenv import load_dotenv, find_dotenv
from todo_app import app

@pytest.fixture(scope='module')
def app_with_temp_board():
    
    os.environ['TRELLO_board_name'] = 'TEST_BOARD'
    application = app.create_app()

    #load_dotenv()    
    key = os.getenv('TRELLO_KEY')
    token = os.getenv('TRELLO_TOKEN')
    board_name = 'TEST_BOARD'
    request_handler = real_trello_request_handler(key, token, application.logger) # don't know how to get logger until app created

    try:
         # if the board already exists, delete it
        board_id = request_handler.get_board(board_name)["id"]
        request_handler.delete_board(board_id)
        request_handler.create_board("TEST_BOARD")
    except:
        request_handler.create_board("TEST_BOARD")
    finally:
        board_id = request_handler.get_board(board_name)["id"]
    
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application

    thread.join(1)
    request_handler.delete_board(board_id) # cleanup

def test_index_page(app_with_temp_board):
    # this is not thread safe, when the other tests run at the same time they mess about with the config!
    # if it runs with FAKE_KEY then it will fail
    client = app_with_temp_board.test_client()
    response = client.get('/')
    assert "Do Me" in str(response.data)