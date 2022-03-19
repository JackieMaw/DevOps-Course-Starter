from flask import Flask, render_template, redirect, request
from todo_app.data.mongodb_repository import mongodb_repository
import os
from dotenv import load_dotenv
from todo_app.viewmodel import ViewModel
import logging
from flask_login import LoginManager, current_user, login_required, login_user
from oauthlib.oauth2 import WebApplicationClient
import requests
import json
from todo_app.data.user import AnonymousUser, User, UserRole

def init_repository(logger):        
    connectionstring = os.getenv('MONGODB_CONNECTIONSTRING')
    dbname = os.getenv('MONGODB_DATABASE')
    return mongodb_repository(connectionstring, dbname)

def create_app(): 

    app = Flask(__name__)
    logging.basicConfig(filename='todo_app\\app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    app.config.from_object('todo_app.flask_config.Config')
    repository = init_repository(app.logger)    

    login_disabled = os.getenv('LOGIN_DISABLED') == 'True'
    app.config['LOGIN_DISABLED'] = login_disabled

    login_manager = LoginManager() 
    login_manager.init_app(app) 
    if login_disabled:
        app.logger.info(f"LOGIN DISABLED: Setting Anonymous User")
        login_manager.anonymous_user = AnonymousUser

    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')

    @login_manager.unauthorized_handler 
    def unauthenticated():  
        app.logger.info(f"Session is Unauthenticated!")
        client = WebApplicationClient(client_id)
        redirect_uri=f'{request.url}login/callback'
        uri = client.prepare_request_uri('https://github.com/login/oauth/authorize', redirect_uri=redirect_uri)
        app.logger.info(f"Authentication Step 1) Ask GitHub for Authorization Code")
        app.logger.info(f"Ask GitHub to Redirect to: {redirect_uri}")
        app.logger.info(f"Redirecting to: {uri}")
        return redirect(uri)
    
    @login_manager.user_loader 
    def load_user(user_id): 
        return User(user_id)         

    @app.route('/')
    @login_required
    def index():
        try:
            username = current_user.get_id()
            app.logger.info(f"[{username}] index() => loading tasks from repository")
            tasks = repository.get_tasks()
            app.logger.info(f"[{username}] index() => {len(tasks)} tasks retrieved from repository")
            view_model = ViewModel(tasks, username, current_user.get_role())
            response = render_template('index.html', view_model=view_model) 
            return response
        except Exception as e:
            app.logger.error(f"Error : {e}")
            raise e

    @app.route('/login/callback', methods=['GET'])
    def login_callback():
        try:            
            app.logger.info(f"Authentication Step 1) Completed.")
            auth_code = request.args["code"]            
            app.logger.info(f"GitHub Authorization Code: {auth_code}")

            # exchange the authorization code for an access token
            payload = {"client_id": client_id, "client_secret": client_secret, "code": auth_code}
            headers = {"Accept": "application/json"}
            app.logger.info(f"Authentication Step 2) Exchange GitHub Authorization Code for Access Token")
            app.logger.info(f"POST: https://github.com/login/oauth/access_token")
            r = requests.post("https://github.com/login/oauth/access_token", data = payload, headers = headers)
            app.logger.info(f"Authentication Step 2) Complete. Response: {r.text}")

            if "access_token" not in r.json():
                return "Authentication Failed at Step 2. See application logs.", 401
            access_token = r.json()["access_token"]

            # get the user information
            app.logger.info(f"Authentication Step 3) Use GitHub Access Token to retrieve User Details.")
            app.logger.info(f"GET: https://api.github.com/user")
            headers = {"Accept": "application/json", "Authorization": f"Bearer {access_token}"}
            r = requests.get("https://api.github.com/user", headers = headers)
            app.logger.info(f"Authentication Step 3) Complete. Response: {r.text}")
            
            if "login" not in r.json():
                # HELP - is there a better way to handle this? how to return 401 - Unauthorized?
                raise Exception("Authentication Failed at Step3. See application logs.")
            user_id = r.json()["login"]
                        
            app.logger.info(f"Logging in User: {user_id}")
            user = User(user_id)
            logged_in = login_user(user)          

            return redirect('/')

        except Exception as e:
            # HELP - is there a better way to handle this? how to return 401 - Unauthorized?
            app.logger.error("Error: %s", e)
            raise e

    @app.route('/tasks', methods=['POST'])
    @login_required
    def add_new_task():
        if (current_user.get_role() == UserRole.writer):
            try:
                app.logger.info("add_new_task()")
                task_name = request.form["task_name"]
                app.logger.info(f"add_new_task() => {task_name}")
                repository.add_task(task_name, "ToDo")
                return redirect('/')
            except Exception as e:
                app.logger.error("Error: %s", e)
                raise e
        else:
            # HELP - is there a better way to handle this? how to return 401 - Unauthorized?
            raise Exception("Unauthorized. To Add a New Task, the User must have the 'writer' role.")

    @app.route('/change_status/<id>', methods=['POST']) 
    @login_required
    def change_status(id): 
        if (current_user.get_role() == UserRole.writer):
            try:
                status = request.args["status"]
                app.logger.info(f"mark_as_done: id = {id}, status = {status}")
                repository.update_task_status(id, status)
                return redirect('/')
            except Exception as e:
                app.logger.error(f"Error : {e}")
                raise e
        else:
            # HELP - is there a better way to handle this? how to return 401 - Unauthorized?
            raise Exception("Unauthorized. To Change a Task Status, the User must have the 'writer' role.")

    @app.route('/delete/<id>', methods=['POST']) 
    @login_required
    def delete(id):         
        if (current_user.get_role() == UserRole.writer):
            try:
                app.logger.info(f"delete: id = {id}")
                repository.delete_task(id)  
                return redirect('/')
            except Exception as e:
                app.logger.error(f"Error : {e}")
                raise e
        else:
            # HELP - is there a better way to handle this? how to return 401 - Unauthorized?
            raise Exception("Unauthorized. To Delete a Task, the User must have the 'writer' role.")
    
    logging.info('create_app() completed')
    return app

if __name__ == '__main__':

    app = create_app()
    app.run()
