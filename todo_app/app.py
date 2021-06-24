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
    print("index()")
    items = sorted(repository.get_items(), key=lambda item: item["status"], reverse=True)
    for i in items:
        print(i)        
    return render_template('index.html', items=items) 

@app.route('/items', methods=['POST'])
def add_new_item():
    print("add_new_item")
    title = request.form['title']
    print(title)
    repository.add_item(title, "To Do")
    return redirect('/')

@app.route('/change_status/<id>', methods=['POST']) 
def change_status(id): 
    status = request.args["status"]
    print(f"mark_as_done: id = {id}, status = {status}")
    repository.update_item_status(int(id), status)
    return redirect('/')

@app.route('/delete/<id>', methods=['POST']) 
def delete(id): 
    print(f"delete: id = {id}")
    repository.delete_item(id)  
    return redirect('/')

if __name__ == '__main__':
    app.run()
