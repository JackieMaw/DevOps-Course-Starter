import pytest
from dotenv import load_dotenv, find_dotenv
from todo_app import app
from unittest.mock import Mock, patch
import json

TEST_BOARD_ID = 1

ALL_LISTS = json.loads("""
[
    {
        "id": "60cc9c9354703a81f8f3ecbf",
        "name": "To Do"
    },
    {
        "id": "60cc9c9354703a81f8f3ecc0",
        "name": "Doing"
    },
    {
        "id": "60cc9c9354703a81f8f3ecc1",
        "name": "Done"
    }
]""")

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    (test_app, repository) = app.create_app()
    with test_app.test_client() as client:
        yield client

@patch('requests.get')
def test_index_page(mock_get_requests, client):
    mock_get_requests.side_effect = mock_get_lists
    response = client.get('/')
    print(f'test_index_page: {response}')

def mock_get_lists(url, params):    
    print(f'MOCK: {url}')
    if url == f'https://api.trello.com/1/boards/{TEST_BOARD_ID}/lists':
        response = Mock()
        response.json.return_value = ALL_LISTS
        return response
    return None