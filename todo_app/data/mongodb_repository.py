from todo_app.data.task_repository import task_repository
from todo_app.data.task import Task, TaskStatus
import pymongo
from bson.objectid import ObjectId

class mongodb_repository(task_repository):

    def __init__(self, connectionstring, dbname):
        self.connectionstring = connectionstring
        self.dbname = dbname
        self.client = pymongo.MongoClient(self.connectionstring)
        self.tasks_collection = self.client[self.dbname].tasks

    def get_tasks(self):
        alltasks = [Task(str(task["_id"]), task["Name"], TaskStatus(task["Status"])) for task in self.tasks_collection.find()]
        return alltasks

    def add_task(self, name, status):
        self.tasks_collection.insert_one({"Name" : name, "Status" : status})

    def update_task_status(self, id, status):
        filter = { "_id" : ObjectId(id) }
        updater = { "$set": {"Status" : status} } 
        self.tasks_collection.update_one(filter, updater)  

    def delete_task(self, id):
        filter = { "_id" : ObjectId(id) }
        self.tasks_collection.delete_one(filter)  