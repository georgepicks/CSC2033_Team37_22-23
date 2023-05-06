from flask import Blueprint, render_template, flash, redirect, url_for

from Users.forms import LoginForm, RegisterForm

users_blueprint = Blueprint('users_templates', __name__, template_folder='templates')

@users_blueprint.route('/register', methods=['Get', 'Post'])
def register():
    form = RegisterForm()

    return render_template('../users/register.html', form=form)


def login():
    pass



def account():
    pass