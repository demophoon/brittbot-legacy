import threading

from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit, send
app = Flask(__name__)
socketio = SocketIO(app)

gjenni = None


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<room>/<x>ofthe<y>")
def karma_list(room, x, y):
    brain = gjenni.brain['ofthe']
    room = room.replace("_", "#")
    xes = brain[x][y][room]
    xes.reverse()
    l = []
    fstr = '<br>'.join(["%s. %s" % (x, y) for x, y in enumerate(xes)])
    print "Web called."
    return fstr


def setup(jenni):
    global gjenni
    gjenni = jenni
    jenni.flask = threading.Thread(target=socketio.run, args=(app, ), kwargs={
        'host': '0.0.0.0',
    })
    jenni.flask.start()
