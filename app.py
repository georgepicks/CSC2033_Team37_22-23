from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# initialise database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leftovers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
