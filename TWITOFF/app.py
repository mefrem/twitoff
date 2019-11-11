""" """
from flask import Flask
# Now we want to make an app factory

def create_app():
    app = Flask(__name__)
    @app.route('/')
    def root():
        return 'Welcome to Twitoff'
    return app