#!/usr/bin/python3
"""This script starts a flask web application
"""

from flask import Flask

app = Flask("__name__")


@app.route('/', strict_slashes=False)
def hello():
    """Return HBNB"""
    return ("Hello HBNB!")


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ hbnb route """
    return ("HBNB")


@app.route('/c/<text>')
def custom(text):
    """ custom c page """
    if '_' in text:
        text = text.split("_")
        text = " ".join(text)

    return (f"C {text}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=None)
