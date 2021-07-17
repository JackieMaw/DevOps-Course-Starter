from todo_app.data.trello_request_handler import trello_request_handler
import json

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