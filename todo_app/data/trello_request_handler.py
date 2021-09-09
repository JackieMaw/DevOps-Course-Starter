from abc import ABC, abstractmethod
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

class real_trello_request_handler(trello_request_handler):

    def __init__(self, key, token, logger) -> None:
        self.key = key
        self.token = token
        self.logger = logger
        self.trello_url = "https://api.trello.com"
        super().__init__()

    def get_board(self, board_name):
        payload = {'fields': "name,url", 'key': self.key, 'token' : self.token}
        r = requests.get(f"{self.trello_url}/1/members/me/boards", payload)
        self.logger.info(f'get_board: {board_name} {r.url} => {r.status_code}')
        if (r.status_code == 200):
            allBoards = r.json()
            board = next ((board for board in allBoards if board["name"] == board_name), None)
            if (board == None):
                raise RuntimeError(f'get_board: Board does not exist: {board_name}')
            return board
        else:
            raise RuntimeError(f'get_board: Web Request Failed with status_code {r.status_code}: {r.url}')
       
    def get_all_cards(self, boardId):
        payload = {'fields': "name,idList", 'key': self.key, 'token' : self.token}
        r = requests.get(f"{self.trello_url}/1/boards/{boardId}/cards", payload)
        self.logger.info(f'get_all_cards [{boardId}]: {r.url} => {r.status_code}')
        return r.json()
       
    def get_all_lists(self, boardId):
        payload = {'fields': "name", 'key': self.key, 'token' : self.token}
        r = requests.get(f"{self.trello_url}/1/boards/{boardId}/lists", payload)
        self.logger.info(f'get_all_lists: {r.url} => {r.status_code}')
        return r.json()

    def update_list_on_card(self, cardId, listId):
        payload = {'idList': listId, 'key': self.key, 'token' : self.token}
        r = requests.put(f"{self.trello_url}/1/cards/{cardId}", payload)
        self.logger.info(f'update_list_on_card: {r.url} => {r.status_code}')

    def add_new_card(self, cardName, listId):
        payload = {'name': cardName, 'idList': listId, 'key': self.key, 'token' : self.token}
        r = requests.post(f"{self.trello_url}/1/cards", payload)
        self.logger.info(f'add_new_card: {cardName} {r.url} => {r.status_code}')

    def delete_card(self, cardId):
        r = requests.delete(f"{self.trello_url}/1/cards/{cardId}?key={self.key}&token={self.token}")
        self.logger.info(f'delete_card: {r.url} => {r.status_code}')

    def create_board(self, boardName):
        payload = {'name': boardName, 'key': self.key, 'token' : self.token}
        r = requests.post(f"{self.trello_url}/1/boards", payload)
        self.logger.info(f'create_board: {boardName} {r.url} => {r.status_code}')

    def delete_board(self, boardId):
        r = requests.delete(f"{self.trello_url}/1/boards/{boardId}?key={self.key}&token={self.token}")
        self.logger.info(f'delete_board: {r.url} => {r.status_code}')
