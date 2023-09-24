#!/usr/bin/python3
"""This script starts a flask web application
"""

from flask import Flask, render_template

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


@app.route('/python/')
@app.route('/python/<text>', strict_slashes=False)
def python(text="is cool"):
    """ custom python route"""
    if '_' in text:
        text = text.split("_")
        text = " ".join(text)

    return (f"Python {text}")


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """ displays only integer numbers """
    if isinstance(n, int):
        return (f"{n} is a number")


@app.route('/number_template/<int:n>', strict_slashes=False)
def template(n):
    """ displays html page if n is int """
    if isinstance(n, int):
        return render_template("5-number.html", n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=None)
