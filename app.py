from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('users/login.html')


from Users.views import users_blueprint

app.register_blueprint(users_blueprint)

if __name__ == '__main__':
    app.run()
