# IMPORTS
from flask import Flask, render_template

# from flask_sqlalchemy import SQLAlchemy

# CONFIG
app = Flask(__name__)

app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'


@app.route('/')
def index():
    return render_template('main/index.html')


from Users.views import users_blueprint

app.register_blueprint(users_blueprint)

if __name__ == "__main__":
    app.run()
