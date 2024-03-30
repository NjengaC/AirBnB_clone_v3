#!/usr/bin/python3
"""
This is Module Documentation- starts a Flask web application

"""
from flask import Flask, render_template
from models import storage
from models.state import State
app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """Remove the current SQLAlchemy Session"""
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """Displays a HTML page with a list of all State objects and their cities"""

    states = storage.all('State').values()
    states_list_dicts = [state.to_dict() for state in states]
    sorted_states = sorted(states_list_dicts, key=lambda state: state['name'])
    return render_template("8-cities_by_states.html", states=sorted_states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
