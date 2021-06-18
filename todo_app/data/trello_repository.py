from todo_app.data.trello_wrapper import fake_trello_wrapper, real_trello_wrapper, trello_wrapper

class trello_repository:
    wrapper = fake_trello_wrapper()

    def __init__(self):
        self.boardId = None
        self.lists = None

    def get_items(self):

        if (self.boardId is None):
            allBoards = trello_repository.wrapper.getAllBoards()
            self.boardId = allBoards[0]["id"]

        if (self.lists is None):
            allLists = trello_repository.wrapper.getAllLists(self.boardId)
            keyValuePairs = [(list["id"], list["name"]) for list in allLists]
            self.lists = {key: value for (key, value) in keyValuePairs}

        allCards = trello_repository.wrapper.getAllCards(self.boardId)
        allItems = [self.__transform_card_to_item(card) for card in allCards]

        return allItems

    def __transform_card_to_item(self, card):
        return { "id": card["id"], "title": card["name"], "status": self.__get_status(card["idList"])}

    def __get_status(self, idList):
        return self.lists[idList]

    def get_item(self, id):
        items = self.get_items()
        return next((item for item in items if item['id'] == int(id)), None)

    def add_item(self, title):
        items = self.get_items()

        # Determine the ID for the item based on that of the previously added item
        id = items[-1]['id'] + 1 if items else 0

        item = { 'id': id, 'title': title, 'status': 'Not Started' }
        items.append(item)
        session['items'] = items

        return item

    def save_item(self, item):
        existing_items = self.get_items()
        updated_items = [item if item['id'] == existing_item['id'] else existing_item for existing_item in existing_items]
        session['items'] = updated_items
        return item

    def delete_item(self, id):
        items = self.get_items()
        item = self.get_item(id)
        items.remove(item)
        session['items'] = items