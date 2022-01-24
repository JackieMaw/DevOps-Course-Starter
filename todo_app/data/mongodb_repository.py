from todo_app.data.task_repository import task_repository
from todo_app.data.trello_request_handler import real_trello_request_handler
from todo_app.data.task import Task, TaskStatus
import os
import pymongo

class mongodb_repository(task_repository):

    def __init__(self, connectionstring, dbname):
        self.connectionstring = connectionstring
        self.dbname = dbname
        self.client = pymongo.MongoClient(self.connectionstring)
        self.tasks_collection = self.client[self.dbname].tasks

    def get_tasks(self):
        # {'_id': ObjectId('61eeb34d8ebddad2827fca27'), 'Name': 'Write Integration Tests', 'Status': 'ToDo'}
        alltasks = [Task(task["_id"], task["Name"], TaskStatus(task["Status"])) for task in self.tasks_collection.find()]
        return alltasks

    def add_task(self, name, status):
        self.tasks_collection.insert_one({"Name" : name, "Status" : status})

    def update_task_status(self, id, status):
        filter = { "_id" : id }
        updater = { "$set": {"Status" : status} } 
        self.tasks_collection.update_one(filter, updater)  

    def delete_task(self, id):
        filter = { "_id" : id }
        self.tasks_collection.delete_one(filter)  