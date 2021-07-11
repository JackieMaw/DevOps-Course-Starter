from abc import ABC, abstractmethod
import json
import requests

class trello_request_handler(ABC):        
    @abstractmethod 
    def get_board(self):
        pass
       
    @abstractmethod 
    def get_all_cards(self):
        pass
       
    @abstractmethod 
    def get_all_lists(self):
        pass

    @abstractmethod 
    def update_list_on_card(self, cardId, listId):
        pass

    @abstractmethod 
    def add_new_card(self, cardName, listId):
        pass

    @abstractmethod
    def delete_card(self, cardId):
        pass

class fake_trelllo_request_handler(trello_request_handler):   
    def get_board(self):
        return json.loads("""
    {
        "name": "ToDoApp",
        "id": "60cc9c9354703a81f8f3ecbe",
        "url": "https://trello.com/b/NLvhLBOS/todoapp"
    }""")
       
    def get_all_cards(self, boardId):
        return json.loads("""
[
    {
        "id": "60cc9cb34f33b07ed4e7563b",
        "name": "Task3",
        "idList": "60cc9c9354703a81f8f3ecbf"
    },
    {
        "id": "60cc9cb60118297472d2733c",
        "name": "Task4",
        "idList": "60cc9c9354703a81f8f3ecbf"
    },
    {
        "id": "60cc9ca59593fc703c332a1a",
        "name": "Task1",
        "idList": "60cc9c9354703a81f8f3ecc0"
    },
    {
        "id": "60cc9cad6e2a3b11cb093ba1",
        "name": "Task2",
        "idList": "60cc9c9354703a81f8f3ecc1"
    }
]""")
       
    def get_all_lists(self, boardId):
        return json.loads("""
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

    def update_list_on_card(self, cardId, listId):
        pass

    def add_new_card(self, cardName, listId):
        pass

    def delete_card(self, cardId):
        pass

class real_trello_request_handler(trello_request_handler):

    def __init__(self, key, token, workspace_name, logger) -> None:
        self.key = key
        self.token = token
        self.workspace_name = workspace_name
        self.logger = logger
        super().__init__()

    def get_board(self):
        payload = {'fields': "name,url", 'key': self.key, 'token' : self.token}
        r = requests.get(f"https://api.trello.com/1/members/me/boards", payload)
        self.logger.info(f'get_board: {r.url} => {r.status_code}')
        allBoards = r.json()
        return next ((board for board in allBoards if board["name"] == self.workspace_name), None)
       
    def get_all_cards(self, boardId):
        payload = {'fields': "name,idList", 'key': self.key, 'token' : self.token}
        r = requests.get(f"https://api.trello.com/1/boards/{boardId}/cards", payload)
        self.logger.info(f'get_all_cards: {r.url} => {r.status_code}')
        return r.json()
       
    def get_all_lists(self, boardId):
        payload = {'fields': "name", 'key': self.key, 'token' : self.token}
        r = requests.get(f"https://api.trello.com/1/boards/{boardId}/lists", payload)
        self.logger.info(f'get_all_lists: {r.url} => {r.status_code}')
        return r.json()

    def update_list_on_card(self, cardId, listId):
        payload = {'idList': listId, 'key': self.key, 'token' : self.token}
        r = requests.put(f"https://api.trello.com/1/cards/{cardId}", payload)
        self.logger.info(f'update_list_on_card: {r.url} => {r.status_code}')

    def add_new_card(self, cardName, listId):
        payload = {'name': cardName, 'idList': listId, 'key': self.key, 'token' : self.token}
        r = requests.post(f"https://api.trello.com/1/cards", payload)
        self.logger.info(f'add_new_card: {r.url} => {r.status_code}')

    def delete_card(self, cardId):
        r = requests.delete(f"https://api.trello.com/1/cards/{cardId}?key={self.key}&token={self.token}")
        self.logger.info(f'delete_card: {r.url} => {r.status_code}')