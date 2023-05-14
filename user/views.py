from flask import Blueprint, render_template, flash, redirect, url_for,session,Markup,request
from user.forms import RegisterForm, LoginForm
import bcrypt
from flask_login import login_user,current_user
from datetime import datetime
import logging


users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/index')
def home():
    return render_template('main/index.html')


@users_blueprint.route('/feed')
def feed():
    return render_template('consumer/feed.html')

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    # create signup form object
    form = RegisterForm()

    return render_template('users/register.html', form=form)
    # if request method is GET or form not valid re-render signup page
    # return render_template('users/register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        # session implemented to limit the number of logins if user failsto login
        if not session.get('authentication_attempts'):
            session['authentication_attempts'] = 0

        # checks if the user already exists in the database

        # if condition checking if the encrypted password is similar to database, if the user exists and the verification key entered is false

    return render_template('users/login.html', form=form)

