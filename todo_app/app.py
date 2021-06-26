from flask import Flask, render_template, request, redirect
from todo_app.data.session_repository import session_repository
from todo_app.data.trello_repository import trello_repository
from todo_app.flask_config import Config
import os
from dotenv import load_dotenv

def init_repository():        
    load_dotenv()    
    repository = os.getenv('REPOSITORY')
    if repository == 'trello':
        key = os.getenv('TRELLO_KEY')
        token = os.getenv('TRELLO_TOKEN')
        workspace_name = os.getenv('TRELLO_WORKSPACE_NAME')
        return trello_repository(key, token, workspace_name)
    else:
        return session_repository()

app = Flask(__name__)
app.config.from_object(Config)
repository = init_repository()

@app.route('/')
def index():
    try:
        app.logger.info("index()")
        tasks = sorted(repository.get_tasks(), key=lambda task: task.status, reverse=True) 
        app.logger.info(f"index() => {len(tasks)} tasks retrieved from repository")
        return render_template('index.html', tasks=tasks, repository_description=repository.description, task_count=len(tasks)) 
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
