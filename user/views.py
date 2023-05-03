from flask import Blueprint, render_template, flash, redirect, url_for,session,Markup,request
from sqlalchemy.testing.pickleable import User

from app import db
from user.form import RegisterForm, LoginForm
import bcrypt
import pyotp
import logging

# @user_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    # create signup form object
    form = RegisterForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # if this returns a user, then the email already exists in database

        # if email already exists redirect user back to signup page with error message so user can try again
        if user:
            flash('Email address already exists')
            return render_template('users/register.html', form=form)

        # create a new user with the form data
        new_user = User(email=form.email.data,
                        firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        phone=form.phone.data,
                        password=form.password.data,
                        postcode=form.postcode.data,
                        role=form.role.data)

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # sends user to login page
        logging.warning('SECURITY - User registration [%s, %s]',form.email.data,request.remote_addr)
        return redirect(url_for('user.login'))
    # if request method is GET or form not valid re-render signup page
    return render_template('users/register.html', form=form)
