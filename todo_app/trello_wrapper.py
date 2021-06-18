from abc import abstractmethod
import json

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
    @abstractmethod 
    def getAllBoards(self):
        return json.loads("""
[
    {
        "name": "ToDoApp",
        "id": "60cc9c9354703a81f8f3ecbe",
        "url": "https://trello.com/b/NLvhLBOS/todoapp"
    }
]""")
       
    @abstractmethod 
    def getAllCards(self):
        #https://api.trello.com/1/members/me/boards?fields=name,url&key=b4b0f437afe756ad8944b7aedfbe3cf4&token=946719d7da9b126dd37539a72e97f92c1298f73cbb70a0eb365c7f4fdd732829
        return json.loads()
       
    @abstractmethod 
    def getAllLists(self):
        #https://api.trello.com/1/boards/60cc9c9354703a81f8f3ecbe/cards?fields=name,idList&key=b4b0f437afe756ad8944b7aedfbe3cf4&token=946719d7da9b126dd37539a72e97f92c1298f73cbb70a0eb365c7f4fdd732829
        return json.loads()
       
    @abstractmethod 
    def getAllLists(self):
        #https://api.trello.com/1/boards/60cc9c9354703a81f8f3ecbe/lists?fields=name&key=b4b0f437afe756ad8944b7aedfbe3cf4&token=946719d7da9b126dd37539a72e97f92c1298f73cbb70a0eb365c7f4fdd732829
        return json.loads()