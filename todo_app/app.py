from werkzeug.utils import redirect
from todo_app.data.session_items import get_items
from todo_app.data.session_items import add_item
from flask import Flask
from flask import render_template
from flask import request

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    print("index()")
    items = get_items()
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
    items = get_items()
    for i in get_items():
        print(i)
    return render_template('index.html', items=items) 

if __name__ == '__main__':
    app.run()
