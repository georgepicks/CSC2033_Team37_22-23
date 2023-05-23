from flask import Flask, redirect, url_for, render_template
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()


app = Flask(__name__)
app.secret_key = 'your_secret_key'


# initialise database
engine = create_engine('mariadb:///csc2033_team37:BikeRode4out@cs-db.ncl.ac.uk:3306/csc2033_team37')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb://csc2033_team37:BikeRode4out@cs-db.ncl.ac.uk/csc2033_team37'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# imports LoginManageer
from flask_login import LoginManager, current_user
from models import Consumer, Producer


@app.route('/')
def index():
    return render_template('main/index.html')


# define login manager
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.init_app(app)

# BLUEPRINTS
# import blueprints
from user.views import users_blueprint
from producer.view import producer_blueprint
from consumer.view import consumer_blueprint
from pages.view import pages_blueprint

# # register blueprints with app
app.register_blueprint(users_blueprint)
app.register_blueprint(producer_blueprint)
app.register_blueprint(consumer_blueprint)
app.register_blueprint(pages_blueprint)


@login_manager.user_loader
def load_user(email):
    # if user exists in consumer table, return it's ID
    if Consumer.query.filter_by(email=email).first():
        user = Consumer.query.filter_by(email=email).first()
        return user.id
    # if the user's email doesn't exist in the consumer table, check the producer table too
    else:
        user = Producer.query.filter_by(email=email).first()
        return user.id


with app.app_context():
    load_user('jd@jdwetherspoons.com')


@app.route('/about_us')
def about_us():
    return render_template('main/about_us.html')


@app.route('/contact')
def contact_us():
    return render_template('main/contact.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/error404.html"), 404


@app.errorhandler(500)
def server_error(error):
    return render_template("errors/error500.html"), 500


@app.errorhandler(403)
def forbidden_action(error):
    return render_template("errors/error403.html"), 403


if __name__ == '__main__':
    app.run()
