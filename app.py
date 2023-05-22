from flask import Flask, redirect, url_for, render_template
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# initialise database
engine = create_engine('mariadb:///csc2033_team37:BikeRode4out@cs-db.ncl.ac.uk:3306/csc2033_team37')
# engine = create_engine("jdbc:mariadb://cs-db.ncl.ac.uk:3306/csc2033_team37")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb://csc2033_team37:BikeRode4out@cs-db.ncl.ac.uk/csc2033_team37'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from flask import redirect
# BLUEPRINTS
# import blueprints
from user.views import users_blueprint
from producer.view import producer_blueprint
from consumer.view import consumer_blueprint
from pages.view import pages_blueprint

# imports LoginManageer
from flask_login import LoginManager, current_user
from models import User

# # register blueprints with app
app.register_blueprint(users_blueprint)
app.register_blueprint(producer_blueprint)
app.register_blueprint(consumer_blueprint)
app.register_blueprint(pages_blueprint)

# define login manager
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(email):
    return User.query.get(int(email))


@app.route('/')
def index():
    redirect_url = url_for('dashboard')
    return redirect(redirect_url)


@app.errorhandler(400)
def internal_error(error):
    return render_template('errors/400.html'), 400


@app.errorhandler(403)
def internal_error(error):
    return render_template('errors/403.html'), 403


@app.errorhandler(404)
def internal_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


if __name__ == '__main__':
    app.run()
