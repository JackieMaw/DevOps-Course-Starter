from flask import Flask, render_template, request, redirect
from todo_app.data.trello_repository import trello_repository
from todo_app.flask_config import Config
import os
from dotenv import load_dotenv
from todo_app.viewmodel import ViewModel

def init_repository(logger):        
    load_dotenv()    
    key = os.getenv('TRELLO_KEY')
    token = os.getenv('TRELLO_TOKEN')
    workspace_name = os.getenv('TRELLO_WORKSPACE_NAME')
    return trello_repository(key, token, workspace_name, logger)

def create_app(): 
    app = Flask(__name__)
    app.config.from_object('todo_app.flask_config.Config')
    repository = init_repository(app.logger)
    return (app, repository)

(app, repository) = create_app()

@app.route('/')
def index():
    try:
        app.logger.info("index()")
        tasks = repository.get_tasks()
        app.logger.info(f"index() => {len(tasks)} tasks retrieved from repository")
        view_model = ViewModel(tasks, repository.description)
        return render_template('index.html', view_model=view_model) 
    except Exception as e:
        app.logger.error("Error", e)
        raise e

@app.route('/tasks', methods=['POST'])
def add_new_task():
    try:
        app.logger.info("add_new_task()")
        task_name = request.form["task_name"]
        app.logger.info(f"add_new_task() => {task_name}")
        repository.add_task(task_name, "To Do")
        return redirect('/')
    except Exception as e:
        app.logger.error("Error", e)
        raise e

@app.route('/change_status/<id>', methods=['POST']) 
def change_status(id): 
    try:
        status = request.args["status"]
        app.logger.info(f"mark_as_done: id = {id}, status = {status}")
        repository.update_task_status(id, status)
        return redirect('/')
    except Exception as e:
        app.logger.error("Error", e)
        raise e

@app.route('/delete/<id>', methods=['POST']) 
def delete(id): 
    try:
        app.logger.info(f"delete: id = {id}")
        repository.delete_task(id)  
        return redirect('/')
    except Exception as e:
        app.logger.error("Error", e)
        raise e

if __name__ == '__main__':
    app.run()
