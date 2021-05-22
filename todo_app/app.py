from todo_app.data.session_items import get_items
from flask import Flask
from flask import render_template

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    items = get_items()
    for i in get_items():
        print(i)
    return render_template('index.html', items=items) 


if __name__ == '__main__':
    app.run()
