from flask import Flask, render_template, redirect, request
from todo_app.data.mongodb_repository import mongodb_repository
import os
from dotenv import load_dotenv
from todo_app.viewmodel import ViewModel
import logging
from flask_login import LoginManager, login_required, login_user
from oauthlib.oauth2 import WebApplicationClient
import requests
import json
from todo_app.data.user import User

def init_repository(logger):        
    connectionstring = os.getenv('MONGODB_CONNECTIONSTRING')
    dbname = os.getenv('MONGODB_DATABASE')
    return mongodb_repository(connectionstring, dbname)

def create_app(): 

    app = Flask(__name__)
    logging.basicConfig(filename='todo_app\\app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    app.config.from_object('todo_app.flask_config.Config')
    repository = init_repository(app.logger)    

    login_manager = LoginManager() 
    login_manager.init_app(app) 

    @login_manager.unauthorized_handler 
    def unauthenticated():  
        client = WebApplicationClient('Iv1.17399bdf0f013e8c')
        uri = client.prepare_request_uri('https://github.com/login/oauth/authorize', redirect_uri='http://localhost:5000/login/callback')
        app.logger.info(f"unauthenticated... redirecting to: {uri}")
        return redirect(uri)
    
    @login_manager.user_loader 
    def load_user(user_id): 
        return User(user_id)         

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

    @app.route('/login/callback', methods=['GET'])
    def login_callback():
        try:
            app.logger.info("login_callback()")
            auth_code = request.args["code"]
            app.logger.info(f"login_callback() => {auth_code}")

            # # exchange the authorization code for an access token
            # payload = {"client_id": "Iv1.17399bdf0f013e8c", "client_secret":"f8fc05f9b7a476023c4b6552acea00b6139f4c6e", "code": auth_code}
            # headers = {"Accept": "application/json"} #this is not working!
            # r = requests.post("https://github.com/login/oauth/access_token", payload, headers)
            # app.logger.info(f"access_token reponse: {r.text}")    
            # access_token = r.json()["access_token"]

            # # get the user information
            # headers = {"Authorization": f"Bearer {access_token}"}
            # r = requests.get("https://api.github.com/user", headers)
            # app.logger.info(f"user info reponse: {r.raw}")
            # user_id = r.json()["login"]
            
            user_id = "JackieMaw"
            
            app.logger.info(f"login_user: {user_id}")
            user = User(user_id)
            logged_in = login_user(user)          
            app.logger.info(f"logged_in: {logged_in}")  

            return redirect('/')

        except Exception as e:
            app.logger.error("Error: %s", e)
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
    
    logging.info('create_app() completed')
    return app

if __name__ == '__main__':

    app = create_app()
    app.run()
