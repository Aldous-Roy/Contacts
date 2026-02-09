from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS

#initaliza the name to the app 
app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)