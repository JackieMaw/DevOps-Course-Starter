from todo_app.data.trello_request_handler import fake_trelllo_request_handler, real_trello_request_handler
from todo_app.data.task import task

class trello_repository:

    def __init__(self, key, token, workspace_name):
        self.boardid = None
        self.status_to_listid = None
        self.listid_to_status = None
        self.request_handler = real_trello_request_handler(key, token, workspace_name)
        self.description = "Using Trello Repository with Real Request Handler"
        #self.request_handler = fake_trelllo_request_handler()
        #self.description = "Using Trello Repository with Fake Request Handler"
        self.__init_data()

    def __init_data(self):
        self.__get_boardid()
        self.__get_status_lists()

    def __get_boardid(self):
        board = self.request_handler.get_board()
        self.boardid = board["id"]

    def __get_status_lists(self):
        allLists = self.request_handler.get_all_lists(self.boardid)
        self.status_to_listid = dict([(list["name"], list["id"]) for list in allLists])
        self.listid_to_status = dict([(list["id"], list["name"]) for list in allLists])

    def get_tasks(self):
        allCards = self.request_handler.get_all_cards(self.boardid)
        alltasks = [self.__transform_card_to_task(card) for card in allCards]
        return alltasks

    def __transform_card_to_task(self, card):
        return task(card["id"], card["name"], self.listid_to_status[(card["idList"])])

    def add_task(self, taskName, status):
        self.request_handler.add_new_card(taskName, self.status_to_listid[status])

    def update_task_status(self, id, status):
        self.request_handler.update_list_on_card(id, self.status_to_listid[status])     

    def delete_task(self, id):
        self.request_handler.delete_card(id)