from abc import abstractmethod
import json
import requests

class trello_wrapper:        
    @abstractmethod 
    def getAllBoards(self):
        pass
       
    @abstractmethod 
    def getAllCards(self):
        pass
       
    @abstractmethod 
    def getAllLists(self):
        pass

class fake_trello_wrapper(trello_wrapper):   
    def getAllBoards(self):
        #https://api.trello.com/1/members/me/boards?fields=name,url&key=b4b0f437afe756ad8944b7aedfbe3cf4&token=946719d7da9b126dd37539a72e97f92c1298f73cbb70a0eb365c7f4fdd732829
        return json.loads("""
[
    {
        "name": "ToDoApp",
        "id": "60cc9c9354703a81f8f3ecbe",
        "url": "https://trello.com/b/NLvhLBOS/todoapp"
    }
]""")
       
    def getAllCards(self):
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
       
    def getAllLists(self):
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

class real_trello_wrapper(trello_wrapper):          
    key = "b4b0f437afe756ad8944b7aedfbe3cf4"
    token = "946719d7da9b126dd37539a72e97f92c1298f73cbb70a0eb365c7f4fdd732829"

    def getAllBoards(self):
        #https://api.trello.com/1/members/me/boards?fields=name,url&key=b4b0f437afe756ad8944b7aedfbe3cf4&token=946719d7da9b126dd37539a72e97f92c1298f73cbb70a0eb365c7f4fdd732829
        payload = {'fields': "name,url", 'key': self.key, 'token' : self.token}
        r = requests.get(f"https://api.trello.com/1/members/me/boards", payload)
        print(r.url)
        print(r.status_code)
        return r.json()
       
    def getAllCards(self, boardId = "60cc9c9354703a81f8f3ecbe"):
        #https://api.trello.com/1/boards/60cc9c9354703a81f8f3ecbe/cards?fields=name,idList&key=b4b0f437afe756ad8944b7aedfbe3cf4&token=946719d7da9b126dd37539a72e97f92c1298f73cbb70a0eb365c7f4fdd732829
        payload = {'boardId' : boardId, 'fields': "name,idList", 'key': self.key, 'token' : self.token}
        r = requests.get("https://api.trello.com/1/boards/{boardId}/cards", payload)
        print(r.url)
        print(r.status_code)
        return r.json()
       
    def getAllLists(self, boardId = "60cc9c9354703a81f8f3ecbe"):
        #https://api.trello.com/1/boards/60cc9c9354703a81f8f3ecbe/lists?fields=name&key=b4b0f437afe756ad8944b7aedfbe3cf4&token=946719d7da9b126dd37539a72e97f92c1298f73cbb70a0eb365c7f4fdd732829
        payload = {'boardId' : boardId, 'fields': "name", 'key': self.key, 'token' : self.token}
        r = requests.get("https://api.trello.com/1/boards/{boardId}/lists", payload)
        print(r.url)
        print(r.status_code)
        return r.json()