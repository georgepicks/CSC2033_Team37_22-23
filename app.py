
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

app = Flask(__name__)
# initialise database
engine = create_engine('mariadb:///csc2033_team37:BikeRode4out@cs-db.ncl.ac.uk:3306/csc2033_team37')
# engine = create_engine("jdbc:mariadb://cs-db.ncl.ac.uk:3306/csc2033_team37")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb://csc2033_team37:BikeRode4out@cs-db.ncl.ac.uk/csc2033_team37'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
=======
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask import flash, render_template, request, redirect
from models import Inventory
from consumer import view


app = Flask(__name__)
# initialise database
engine = create_engine('mariadb:///csc2033_team37:BikeRode4out@cs-db.ncl.ac.uk:3306/csc2033_team37')
# engine = create_engine("jdbc:mariadb://cs-db.ncl.ac.uk:3306/csc2033_team37")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb://csc2033_team37:BikeRode4out@cs-db.ncl.ac.uk/csc2033_team37'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/', methods=['GET', 'POST'])
def index():
    search = view.Search_Item(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('', form=search)

@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']
    if search.data['search'] == '':
        qry = db.session.query(Inventory.item)
        results = qry.all()
    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        return render_template('', results=results)



if __name__ == '__main__':
    app.run()

=======
from flask import Flask, redirect, url_for
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'


# initialise database
engine = create_engine('mariadb:///csc2033_team37:BikeRode4out@cs-db.ncl.ac.uk:3306/csc2033_team37')
# engine = create_engine("jdbc:mariadb://cs-db.ncl.ac.uk:3306/csc2033_team37")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb://csc2033_team37:BikeRode4out@cs-db.ncl.ac.uk/csc2033_team37'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from flask import  redirect

# BLUEPRINTS
# import blueprints
from user.views import users_blueprint
from producer.view import producer_blueprint
from consumer.view import consumer_blueprint

# imports LoginManageer
from flask_login import LoginManager, current_user
from models import User

# # register blueprints with app
app.register_blueprint(users_blueprint)
app.register_blueprint(producer_blueprint)
app.register_blueprint(consumer_blueprint)

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

@app.route('/dashboard')
def dashboard():
    return 'Welcome to the dashboard!'

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()


