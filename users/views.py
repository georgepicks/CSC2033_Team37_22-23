from flask import Blueprint, render_template, flash, redirect, url_for

from Users.forms import RegisterForm, LoginForm

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

