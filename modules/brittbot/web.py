import threading
from flask import Flask
app = Flask(__name__)


@app.route("/")
def index():
    return "Hello world"


def setup(jenni):
    jenni.flask = threading.Thread(target=app.run, kwargs={
        'host': '0.0.0.0',
    })
    jenni.flask.start()
