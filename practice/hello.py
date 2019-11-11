"""Minimal flask app"""

from flask import Flask, render_template

# Make the application
app = Flask(__name__)

# Make the route
@app.route("/")

# Now we define a function
def hello():
    return render_template('home.html')

# Creating another route
@app.route("/about")

def preds():
    return render_template("about.html")