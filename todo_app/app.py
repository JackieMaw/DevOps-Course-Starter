from flask import Flask, render_template, request, redirect
from todo_app.data.session_repository import session_repository
from todo_app.data.trello_repository import trello_repository

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)
repository = trello_repository()


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
    repository.add_item(title)
    return redirect('/')

@app.route('/mark_as_done/<itemId>', methods=['POST']) 
def mark_as_done(itemId): 
    print(f"mark_as_done: itemId = {itemId}")
    item = repository.get_item(itemId)
    item["status"] = "Done"
    repository.save_item(item)
    return redirect('/')

@app.route('/delete/<itemId>', methods=['POST']) 
def delete(itemId): 
    try:
        print(f"delete: itemId = {itemId}")
        repository.delete_item(itemId)        
    except Exception as error:
        print(f"Exception: {error}")
    finally:
        return redirect('/')

if __name__ == '__main__':
    app.run()
