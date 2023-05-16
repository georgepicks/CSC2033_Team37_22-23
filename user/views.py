from flask import Blueprint, render_template, flash, redirect, url_for, session, Markup, request
from user.forms import RegisterForm, LoginForm
import bcrypt
from flask_login import login_user, current_user
from datetime import datetime
import logging

users_blueprint = Blueprint('users', __name__, template_folder='templates')

@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    return render_template('users/register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        # session implemented to limit the number of logins if user failsto login
        if not session.get('authentication_attempts'):
            session['authentication_attempts'] = 0

    return render_template('users/login.html', form=form)
