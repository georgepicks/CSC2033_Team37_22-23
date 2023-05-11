
from flask import Blueprint, render_template, flash, redirect, url_for

from Users.forms import RegisterForm, LoginForm
=======
from flask import Blueprint, render_template, flash, redirect, url_for,session,Markup,request
from models import User
from app import db
from user.form import RegisterForm, LoginForm
import bcrypt
from flask_login import login_user,current_user
from datetime import datetime
import logging


users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/index')
def home():
    return render_template('main/index.html')


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    return render_template('users/register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    return render_template('users/login.html', form=form)


    # if request method is POST or form is valid
    if form.validate_on_submit():
        # session implemented to limit the number of logins if user failsto login
        if not session.get('authentication_attempts'):
            session['authentication_attempts'] = 0

        # checks if the user already exists in the database
        user = User.query.filter_by(email=form.email.data).first()

        # if condition checking if the encrypted password is similar to database, if the user exists and the verification key entered is false
        if not user or not bcrypt.checkpw(form.password.data.encode('utf-8'), user.password) :
            logging.warning('SECURITY - Failed login attempt [%s, %s]', form.email.data, request.remote_addr)
            # logging warning returns the login is failed and to try again

            # Session incremented after each invalid login
            session['authentication_attempts'] += 1

            # checks if the user has invalid logins for five consecutive times
            if session.get('authentication_attempts') == 5:
                flash(Markup('Number of incorrect login attempts exceeded.'))
                # reinitialises sessions to 0
                session['authentication_attempts'] = 0

                # invalid user is redirected to register page since user login is invalid
                return redirect(url_for('users.register'))

            flash('Please check your login details and try again,{} login attempts remaining'.format(
                5 - session.get('authentication_attempts')))
        else:
            # user login is initiated
            login_user(user)
            # current login user is matched to the last login user
            user.last_login = user.current_login
            user.current_login = datetime.now()
            db.session.add(user)
            db.session.commit()
            # Data is recorded in lottery.log each time login action takes place
            logging.warning('SECURITY - Log in [%s, %s]', current_user.id, current_user.email)
            if current_user.role == "admin":
                # returns to admin page if the logged in user is an "admin"
                return render_template('')
            # returns to profile page if the logged in user is a normal user
            return render_template('')
    # returns login if all the functions fail
    return render_template('login.html', form=form)

