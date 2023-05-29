"""
File: app.py
Authors: Alexander MacMillan, Sreejith Sudhir Kalathil, Broden Bates
Description: Initialises several components of the app including: The connection to the database, the Flask login
manager, the html blueprints, and returning in case of an error, returning error pages.
"""
from flask import Flask, render_template
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
import pymysql
from flask_login import current_user
import os
from dotenv import load_dotenv

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Get and validate password from secure environment variable
load_dotenv()
db_password = os.environ.get('DB_PASSWORD')
if not db_password:
    raise ValueError('Database password not found')

# Connect to database
db_uri = f'mariadb://csc2033_team37:{db_password}@cs-db.ncl.ac.uk/csc2033_team37'
engine = create_engine(db_uri)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

# imports LoginManager
from flask_login import LoginManager, current_user
from models import Consumer, Producer

login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.init_app(app)

@app.route('/')
def index():
    return render_template('main/index.html',  current_user=current_user)


# BLUEPRINTS
# import blueprints
from user.views import users_blueprint
from producer.view import producer_blueprint
from consumer.view import consumer_blueprint


# # register blueprints with app
app.register_blueprint(users_blueprint)
app.register_blueprint(producer_blueprint)
app.register_blueprint(consumer_blueprint)


@login_manager.user_loader
def load_user(user_id):
    # producer IDs increment from 1000 onward, consumer IDs increment from 0
    if int(user_id) < 1000:
        return Consumer.query.get(int(user_id))
    else:
        return Producer.query.get(int(user_id))


@app.route('/about_us')
def about_us():
    return render_template('main/about_us.html')


@app.route('/contact')
def contact_us():
    return render_template('main/contact.html')

"""
@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/error404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/error500.html"), 500


@app.errorhandler(403)
def forbidden_action(error):
    return render_template("errors/error403.html"), 403
"""

if __name__ == '__main__':
    app.run()
