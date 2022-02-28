from flask import Flask, render_template, redirect, request
from todo_app.data.mongodb_repository import mongodb_repository
import os
from dotenv import load_dotenv
from todo_app.viewmodel import ViewModel

import logging

from flask_login import LoginManager, login_required

def init_repository(logger):        
    connectionstring = os.getenv('MONGODB_CONNECTIONSTRING')
    dbname = os.getenv('MONGODB_DATABASE')
    return mongodb_repository(connectionstring, dbname)

def create_app(): 
    app = Flask(__name__)
    logging.basicConfig(filename='todo_app\\app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    app.config.from_object('todo_app.flask_config.Config')
    repository = init_repository(app.logger)    
    logging.info('create_app() completed')

    @app.route('/')
    @login_required
    def index():
        try:
            app.logger.info("index()")
            tasks = repository.get_tasks()
            app.logger.info(f"index() => {len(tasks)} tasks retrieved from repository")
            view_model = ViewModel(tasks)
            response = render_template('index.html', view_model=view_model) 
            return response
        except Exception as e:
            app.logger.error(f"Error : {e}")
            raise e

    @app.route('/tasks', methods=['POST'])
    def add_new_task():
        try:
            app.logger.info("add_new_task()")
            task_name = request.form["task_name"]
            app.logger.info(f"add_new_task() => {task_name}")
            repository.add_task(task_name, "ToDo")
            return redirect('/')
        except Exception as e:
            app.logger.error("Error: %s", e)
            raise e

    @app.route('/change_status/<id>', methods=['POST']) 
    def change_status(id): 
        try:
            status = request.args["status"]
            app.logger.info(f"mark_as_done: id = {id}, status = {status}")
            repository.update_task_status(id, status)
            return redirect('/')
        except Exception as e:
            app.logger.error(f"Error : {e}")
            raise e

    @app.route('/delete/<id>', methods=['POST']) 
    def delete(id): 
        try:
            app.logger.info(f"delete: id = {id}")
            repository.delete_task(id)  
            return redirect('/')
        except Exception as e:
            app.logger.error(f"Error : {e}")
            raise e
    
    return app

if __name__ == '__main__':

    login_manager = LoginManager() 

    @login_manager.unauthorized_handler 
    def unauthenticated(): 
        app.logger.info(f"unauthenticated... redirecting")
        return redirect('https://github.com/login/oauth/authorize')
        pass # Add logic to redirect to the Github OAuth flow when unauthenticated 
    
    @login_manager.user_loader 
    def load_user(user_id): 
        return None 

    app = create_app()
    login_manager.init_app(app) 
    app.run()
