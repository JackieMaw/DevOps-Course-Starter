from todo_app.trello_wrapper import fake_trello_wrapper, real_trello_wrapper
from flask import Flask, render_template, request, redirect
from todo_app.data.session_items import delete_item, get_items, save_item, add_item, get_item

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    print("index()")
    items = sorted(get_items(), key=lambda item: item["status"], reverse=True)
    for i in get_items():
        print(i)

    trello = fake_trello_wrapper()
    print(trello.getAllBoards())
    print(trello.getAllCards())
    print(trello.getAllLists())

    return render_template('index.html', items=items) 

@app.route('/items', methods=['POST'])
def add_new_item():
    print("add_new_item")
    title = request.form['title']
    print(title)
    add_item(title)
    return redirect('/')

@app.route('/mark_as_done/<itemId>', methods=['POST']) 
def mark_as_done(itemId): 
    print(f"mark_as_done: itemId = {itemId}")
    item = get_item(itemId)
    item["status"] = "Done"
    save_item(item)
    return redirect('/')

@app.route('/delete/<itemId>', methods=['POST']) 
def delete(itemId): 
    try:
        print(f"delete: itemId = {itemId}")
        delete_item(itemId)        
    except Exception as error:
        print(f"Exception: {error}")
    finally:
        return redirect('/')

if __name__ == '__main__':
    app.run()
