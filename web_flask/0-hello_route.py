#!/usr/bin/python3
"""
This is 0-hello_route Module Documentation

"""
from flask import Flask

app = Flask(__name__)


# Route to display "Hello HBNB!"
@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    This is hello_hbnb Function Documentation
    """
    return 'Hello HBNB!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
