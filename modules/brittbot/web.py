import threading

from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit, send
app = Flask(__name__)
socketio = SocketIO(app)

gjenni = None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/test")
def test_message():
    gjenni.msg(
        "##brittslittlesliceofheaven",
        "This is a web posted message"
    )
    return str(gjenni.brain)


@socketio.on('my event')
def ws_logger(jenni, msg):
    send({
        'room': str(msg.sender),
        'msg': str(msg),
        'nick': str(msg.nick),
    }, json=True, broadcast=True)
ws_logger.rule = r".*"


def setup(jenni):
    global gjenni
    gjenni = jenni
    jenni.flask = threading.Thread(target=socketio.run, args=(app, ), kwargs={
        'host': '0.0.0.0',
    })
    jenni.flask.start()
