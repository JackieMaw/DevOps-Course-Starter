import pytest
from dotenv import load_dotenv, find_dotenv
from todo_app import app
from unittest.mock import Mock, patch
import json

ALL_LISTS = json.loads("""
[
    {
        "id": "LIST_ID_TODO",
        "name": "To Do"
    },
    {
        "id": "LIST_ID_DOING",
        "name": "Doing"
    },
    {
        "id": "LIST_ID_DONE",
        "name": "Done"
    }
]""")

ALL_BOARDS = json.loads("""
[
    {
        "name": "ToDoApp",
        "id": "BOARD_ID",
        "url": "https://trello.com/b/NLvhLBOS/todoapp"
    }
]""")

ALL_CARDS = json.loads("""
[
    {
        "id": "CARD_ID_3",
        "name": "Task3",
        "idList": "LIST_ID_TODO"
    },
    {
        "id": "CARD_ID_4",
        "name": "Task4",
        "idList": "LIST_ID_TODO"
    },
    {
        "id": "CARD_ID_1",
        "name": "Task1",
        "idList": "LIST_ID_DOING"
    },
    {
        "id": "CARD_ID_2",
        "name": "Task2",
        "idList": "LIST_ID_DONE"
    }
]""")

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    test_app = app.create_app()
    with test_app.test_client() as client:
        yield client

@patch('requests.get')
def test_index_page(requests_get, client):
    requests_get.side_effect = get_mock_requests_get
    response = client.get('/')

    assert "CARD_ID_1" in str(response.data)
    assert "CARD_ID_2" in str(response.data)
    assert "CARD_ID_3" in str(response.data)
    assert "CARD_ID_4" in str(response.data)

@patch('requests.delete')
@patch('requests.get')
def test_delete_page(requests_get, requests_delete, client):
    requests_get.side_effect = get_mock_requests_get
    requests_delete.side_effect = get_mock_requests_delete
    response = client.post('/delete/CARD_ID_1')
    
    requests_delete.assert_called_with('https://api.trello.com/1/cards/CARD_ID_1?key=FAKE_KEY&token=FAKE_TOKEN')

def get_mock_requests_get(url, params):    
    print(f'MOCK requests.get: {url}')
    if url == 'https://api.trello.com/1/members/me/boards':
        response = Mock()
        response.json.return_value = ALL_BOARDS
        response.url = 'https://api.trello.com/1/members/me/boards'
        response.status_code = 200
        return response
    elif url == 'https://api.trello.com/1/boards/BOARD_ID/lists':
        response = Mock()
        response.json.return_value = ALL_LISTS
        response.url = 'https://api.trello.com/1/boards/BOARD_ID/lists'
        response.status_code = 200
        return response
    elif url == 'https://api.trello.com/1/boards/BOARD_ID/cards':
        response = Mock()
        response.json.return_value = ALL_CARDS
        response.url = 'https://api.trello.com/1/boards/BOARD_ID/cards'
        response.status_code = 200
        return response    
    else:
        print(f'url not supported by Mock: {url}')
        raise ValueError (f'url not supported by Mock: {url}')


def get_mock_requests_delete(url):    
    print(f'MOCK requests.delete: {url}')
    if url == 'https://api.trello.com/1/cards/CARD_ID_1?key=FAKE_KEY&token=FAKE_TOKEN':
        response = Mock()
        response.json.return_value = ALL_CARDS
        response.url = 'https://api.trello.com/1/cards/CARD_ID_1?key=FAKE_KEY&token=FAKE_TOKEN'
        response.status_code = 200
        return response        
    else:
        print(f'url not supported by Mock: {url}')
        raise ValueError (f'url not supported by Mock: {url}')