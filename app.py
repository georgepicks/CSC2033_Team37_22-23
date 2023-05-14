from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from user.views import users_blueprint

app = Flask(__name__)
app.register_blueprint(users_blueprint)
# initialise database
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb://csc2033_team37:BikeRode4out@cs-db.ncl.ac.uk/csc2033_team37'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/')
def index():  # put application's code here
    return render_template('main/index.html')

if __name__ == '__main__':
    app.run()