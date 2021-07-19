from todo_app.data.task_repository import task_repository
from todo_app.data.trello_request_handler import real_trello_request_handler
from todo_app.data.task import Task, TaskStatus
from pickle import dumps, loads
import os

class trello_repository(task_repository):

    def __init__(self, key, token, logger):
        self.boardid = None
        self.status_to_listid = None
        self.listid_to_status = None
        self.request_handler = real_trello_request_handler(key, token, logger)
        self.description = "Using Trello Repository with Real Request Handler"
        self.loaded = False

    def __load(self):        
        workspace_name = os.getenv('TRELLO_WORKSPACE_NAME') #TODO - i don't like this from here...
        board = self.request_handler.get_board(workspace_name)
        self.boardid = board["id"]
        allLists = self.request_handler.get_all_lists(self.boardid)
        self.status_to_listid = dict([(list["name"], list["id"]) for list in allLists])
        self.listid_to_status = dict([(list["id"], list["name"]) for list in allLists])
        self.loaded = True

    def get_tasks(self):
        if not self.loaded:
            self.__load()
        allCards = self.request_handler.get_all_cards(self.boardid)
        alltasks = [self.__transform_card_to_task(card) for card in allCards]
        return alltasks

    def __transform_card_to_task(self, card):
        if not self.loaded:
            self.__load()
        status = self.__get_status(card["idList"])
        return Task(card["id"], card["name"], status)

    def __get_status(self, idList):
        if not self.loaded:
            self.__load()
        status_string = self.listid_to_status[idList]
        # this doesn't work for To Do
        #status = TaskStatus[status_string]
        if status_string == "To Do":
            return TaskStatus.ToDo
        elif status_string == "Doing":
            return TaskStatus.Doing
        elif status_string == "Done":
            return TaskStatus.Done
        else:
            raise TypeError("TaskStatus must be 'To Do', 'Doing', or 'Done'")

    def add_task(self, taskName, status):
        if not self.loaded:
            self.__load()
        self.request_handler.add_new_card(taskName, self.status_to_listid[status])

    def update_task_status(self, id, status):
        if not self.loaded:
            self.__load()
        self.request_handler.update_list_on_card(id, self.status_to_listid[status])     

    def delete_task(self, id):
        if not self.loaded:
            self.__load()
        self.request_handler.delete_card(id)