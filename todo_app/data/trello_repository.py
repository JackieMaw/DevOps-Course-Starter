from todo_app.data.trello_request_handler import real_trello_request_handler

class trello_repository:

    def __init__(self, key, token, workspace_name):
        self.boardId = None
        self.lists = None
        self.request_handler = real_trello_request_handler(key, token, workspace_name)

    def get_boardId(self):
        if (self.boardId is None):
            allBoards = self.request_handler.get_all_boards()
            self.boardId = allBoards[0]["id"]
        return self.boardId

    def get_lists(self):
        if (self.lists is None):
            allLists = self.request_handler.get_all_lists(self.get_boardId())
            self.lists = dict([(list["id"], list["name"]) for list in allLists])
        return self.lists

    def get_items(self):

        self.get_boardId()
        self.get_lists()

        allCards = self.request_handler.get_all_cards(self.get_boardId())
        allItems = [self.__transform_card_to_item(card) for card in allCards]

        return allItems

    def __transform_card_to_item(self, card):
        return { "id": card["id"], "title": card["name"], "status": self.__get_status(card["idList"])}

    def __get_status(self, idList):
        return self.lists[idList]

    def get_item(self, id):
        items = self.get_items()
        return next((item for item in items if item['id'] == int(id)), None)

    def get_listId_for_status(self, status):
        for listId, listName in self.get_lists().items():
            if listName == status:
                return listId
        return None

    def update_item_status(self, id, newStatus):
        listId = self.get_listId_for_status(newStatus)
        self.request_handler.update_list_on_card(id, listId)        

    def add_item(self, itemName, status):
        listId = self.get_listId_for_status(status)
        self.request_handler.add_new_card(itemName, listId)

    def delete_item(self, id):
        self.request_handler.delete_card(id)