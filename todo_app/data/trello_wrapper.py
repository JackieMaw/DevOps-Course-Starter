from abc import abstractmethod
import json
import requests
from requests.api import request

class trelllo_request_handler:        
    @abstractmethod 
    def get_all_boards(self):
        pass
       
    @abstractmethod 
    def get_all_cards(self):
        pass
       
    @abstractmethod 
    def get_all_lists(self):
        pass

class fake_trelllo_request_handler(trelllo_request_handler):   
    def get_all_boards(self):
        #https://api.trello.com/1/members/me/boards?fields=name,url&key=b4b0f437afe756ad8944b7aedfbe3cf4&token=946719d7da9b126dd37539a72e97f92c1298f73cbb70a0eb365c7f4fdd732829
        return json.loads("""
[
    {
        "name": "ToDoApp",
        "id": "60cc9c9354703a81f8f3ecbe",
        "url": "https://trello.com/b/NLvhLBOS/todoapp"
    }
]""")
       
    def get_all_cards(self, boardId):
        #https://api.trello.com/1/boards/60cc9c9354703a81f8f3ecbe/cards?fields=name,idList&key=b4b0f437afe756ad8944b7aedfbe3cf4&token=946719d7da9b126dd37539a72e97f92c1298f73cbb70a0eb365c7f4fdd732829
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
        #https://api.trello.com/1/boards/60cc9c9354703a81f8f3ecbe/lists?fields=name&key=b4b0f437afe756ad8944b7aedfbe3cf4&token=946719d7da9b126dd37539a72e97f92c1298f73cbb70a0eb365c7f4fdd732829
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

class real_trelllo_request_handler(trelllo_request_handler):          
    key = "b4b0f437afe756ad8944b7aedfbe3cf4"
    token = "946719d7da9b126dd37539a72e97f92c1298f73cbb70a0eb365c7f4fdd732829"

    def get_all_boards(self):
        #https://api.trello.com/1/members/me/boards?fields=name,url&key=b4b0f437afe756ad8944b7aedfbe3cf4&token=946719d7da9b126dd37539a72e97f92c1298f73cbb70a0eb365c7f4fdd732829
        payload = {'fields': "name,url", 'key': self.key, 'token' : self.token}
        r = requests.get(f"https://api.trello.com/1/members/me/boards", payload)
        print(r.url)
        print(r.status_code)
        return r.json()
       
    def get_all_cards(self, boardId):
        #https://api.trello.com/1/boards/60cc9c9354703a81f8f3ecbe/cards?fields=name,idList&key=b4b0f437afe756ad8944b7aedfbe3cf4&token=946719d7da9b126dd37539a72e97f92c1298f73cbb70a0eb365c7f4fdd732829
        payload = {'fields': "name,idList", 'key': self.key, 'token' : self.token}
        r = requests.get(f"https://api.trello.com/1/boards/{boardId}/cards", payload)
        print(r.url)
        print(r.status_code)
        return r.json()
       
    def get_all_lists(self, boardId):
        #https://api.trello.com/1/boards/60cc9c9354703a81f8f3ecbe/lists?fields=name&key=b4b0f437afe756ad8944b7aedfbe3cf4&token=946719d7da9b126dd37539a72e97f92c1298f73cbb70a0eb365c7f4fdd732829
        payload = {'fields': "name", 'key': self.key, 'token' : self.token}
        r = requests.get(f"https://api.trello.com/1/boards/{boardId}/lists", payload)
        print(r.url)
        print(r.status_code)
        return r.json()

    def update_list_on_card(self, cardId, listId):
        #PUT /1/cards/{cardID}?idList={listID}
        payload = {'idList': listId, 'key': self.key, 'token' : self.token}
        r = requests.put(f"https://api.trello.com/1/cards/{cardId}", payload)
        print(r.url)
        print(r.status_code)

    def add_new_card(self, cardName, listId):
        #POST /1/cards?name={name}&idList={listID}
        payload = {'name': cardName, 'idList': listId, 'key': self.key, 'token' : self.token}
        r = requests.post(f"https://api.trello.com/1/cards", payload)
        print(r.url)
        print(r.status_code)

    def delete_card(self, cardId):
        #DELETE /1/cards/{cardID}
        #payload = {'key': self.key, 'token' : self.token}
        #r = requests.delete(f"https://api.trello.com/1/cards/{cardId}", payload)
        #r = requests.request("DELETE", f"https://api.trello.com/1/cards/{cardId}", payload)
        r = requests.delete(f"https://api.trello.com/1/cards/{cardId}?key={self.key}&token={self.token}")
        print(r.url)
        print(r.status_code)