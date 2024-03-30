#!/usr/bin/python3
"""
Starts a Flask web application.
"""
from flask import Flask, render_template, abort
from models import storage
from models.state import State
app = Flask(__name__)


@app.teardown_appcontext
def app_teardown(error):
    """close the current session"""
    storage.close()


@app.route("/states", strict_slashes=False)
def states():
    """Displays page with a list of all States """
    states = storage.all(State)
    return render_template("9-states.html", state=states)


@app.route("/states/<id>", strict_slashes=False)
def states_id(id):
    """Display page with state and its cities if id is passes """
    for state in storage.all(State).values():
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
