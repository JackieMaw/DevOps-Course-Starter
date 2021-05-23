from werkzeug.utils import redirect
from todo_app.data.session_items import delete_item, get_items
from todo_app.data.session_items import add_item
from todo_app.data.session_items import get_item
from todo_app.data.session_items import save_item
from flask import Flask
from flask import render_template
from flask import request

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    print("index()")
    items = sorted(get_items(), key=lambda item: item["status"], reverse=True)
    for i in get_items():
        print(i)
    return render_template('index.html', items=items) 

@app.route('/items', methods=['POST'])
def add_new_item():
    print("add_new_item")
    title = request.form['title']
    print(title)
    add_item(title)
    # HELP: how to redirect back to index
    return index()

@app.route('/mark_as_done/<itemId>') 
def mark_as_done(itemId): 
    print(f"mark_as_done: itemId = {itemId}")
    item = get_item(itemId)
    item["status"] = "Done"
    save_item(item)
    # HELP: how to redirect back to index
    return index()

@app.route('/delete/<itemId>') 
def delete(itemId): 
    try:
        print(f"delete: itemId = {itemId}")
        delete_item(itemId)        
    except Exception as error:
        print(f"Exception: {error}")
    finally:
        # HELP: how to redirect back to index
        return index()

if __name__ == '__main__':
    app.run()
