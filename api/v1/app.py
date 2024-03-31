#!/usr/bin/python3
"""
Main docs for app module
"""

from os import getenv
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    """
    Closes current session
    """
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """
    Handles custorm json(404)
    """
    return jsonify({'error': 'Not found'}), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST")
    port = int(getenv("HBNB_API_PORT"))
    app.run(host=host, port=port, threaded=True, debug=True)
