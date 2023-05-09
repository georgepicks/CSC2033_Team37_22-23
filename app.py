from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import create_engine

app = Flask(__name__)
# initialise database
engine = create_engine('mariadb:///csc2033_team37:BikeRode4out@cs-db.ncl.ac.uk:3306/csc2033_team37')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+mariadbconnector://csc2033_team37:BikeRode4out@cs-db.ncl.ac.uk:3306/csc2033_team37'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


# allows user to log in and have server remember who they are during session
login_manager = LoginManager()
login_manager.login_view = 'user.login'
login_manager.init_app(app)

from models import User
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


if __name__ == '__main__':
    app.run()
