from flask import Flask
from applib import *
import flask_restful



app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Bloga Bot</h1>"


if __name__ == "__main__":
    app.run(debug=True)