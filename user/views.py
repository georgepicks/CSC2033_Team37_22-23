"""
File: views.py
Authors: Sreejith Sudhir Kalathil, Alexander MacMillan
Description: This file provides features which are shared among both Consumer and Producer users, including login/logout
functionality, and automated e-mails.
"""

from flask import Blueprint, render_template, flash, redirect, url_for, session, Markup, request
from models import Orders, Producer, Consumer
from app import db
from user.forms import LoginForm
import bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
import logging
from flask_mail import Message, Mail
from consumer.view import find_producers

users_blueprint = Blueprint('users', __name__, template_folder='templates')

@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login() is called when the user is redirected to the login page. It calls on the form in forms.py, then when the user
    submits their email and password combination, checks if this is a valid combination, if so the user is signed in using
    flask's loginManager features in app.py. If the user inputs a non-existent email/password combination 5 times they're
    redirected to their register page.
    """
    # create login form object
    form = LoginForm()
    # if request method is POST or form is valid
    if form.validate_on_submit():
        # session implemented to limit the number of logins if user fails to login
        if not session.get('authentication_attempts'):
            session['authentication_attempts'] = 0
        # checks if the user mail logged in is a producer mail
        if Producer.query.filter_by(email=form.email.data).first() is not None:
            user = Producer.query.filter_by(email=form.email.data).first()
            # if condition checking if the encrypted password is similar to database, if the user exists and the
            # verification key entered is false
            if user and bcrypt.checkpw(form.password.data.encode('utf-8'), user.password.encode('utf-8')):
                login_user(user)
                session['user_id'] = current_user.id
                db.session.add(user)
                db.session.commit()
                # Data is recorded in lottery.log each time login action takes place
                logging.warning('SECURITY - Log in [%s, %s]', current_user.id, current_user.email)
                return render_template('consumer/feed.html', form=form)
                # current login user is matched to the last login user
                db.session.add(user)
                db.session.commit()
                return render_template('producer/supplier_dash.html', id=current_user.id)

            session['authentication_attempts'] = session.get('authentication_attempts', 0) + 1

            # Check the number of authentication attempts
            if session['authentication_attempts'] >= 5:
                flash('Number of incorrect login attempts exceeded.')
                # Clear the authentication_attempts session counter
                session.pop('authentication_attempts', None)
                return redirect(url_for('producer.register'))

            flash('Please check your login details and try again, {} login attempts remaining'.format(
                5 - session['authentication_attempts']))

        # checks if the user mail logged in is a consumer mail
        elif Consumer.query.filter_by(email=form.email.data).first() is not None:
            user = Consumer.query.filter_by(email=form.email.data).first()
            # if condition checking if the encrypted password is similar to database, if the user exists and the
            # verification key entered is false

            if user and bcrypt.checkpw(form.password.data.encode('utf-8'), user.password.encode('utf-8')):
                # user login is initiated
                login_user(user)
                session['user_id'] = current_user.id
                db.session.add(user)
                db.session.commit()
                feed = find_producers(0)
                return render_template('consumer/feed.html', suppliers=feed)
            session['authentication_attempts'] = session.get('authentication_attempts', 0) + 1

            # Check the number of authentication attempts
            if session['authentication_attempts'] >= 5:
                flash('Number of incorrect login attempts exceeded.')
                # Clear the authentication_attempts session counter
                session.pop('authentication_attempts', None)
                return redirect(url_for('consumer.register'))

            flash('Please check your login details and try again, {} login attempts remaining'.format(
                5 - session['authentication_attempts']))

        else:
            return 'invalid User'
    # returns login if all the functions fail
    return render_template('users/login.html', form=form)


@users_blueprint.route('/logout')
@login_required
def logout():
    # Data is recorded in lottery.log each time a user logs out of the program
    logging.warning('SECURITY - Log out [%s, %s, %s]', current_user.id, current_user.email, request.remote_addr)
    #Function for the user to log out
    session.clear()
    # Function for the user to log out
    logout_user()
    # the user is redirected to index page after logout
    return redirect(url_for('index'))


# Function to send mails to producers while an order is made
def send_email(subject, recipients, body):
    msg = Message(subject=subject, recipients=recipients)
    msg.body = body
    Mail.send(msg)


# Message for the producer that is sent through email
def send_mail_notification_producer(order_id):
    subject = 'New Order Notification'
    recipients = get_producer_email(order_id)
    body = f"You have received a new order from a consumer. Order ID: {order_id}"
    send_email(subject, recipients, body)
    return 'Email sent successfully!'


# Function to retrieve relevant producer mail for the message to be sent
def get_producer_email(order_id):
    # order is retrieved in reference to the customer_id
    order = Orders.query.filter_by(id=order_id).first()
    if order:
        producer = Producer.query.get(order.producer_id)
        return [producer.email]
    return []


# Message for the consumer that is sent through email
def send_mail_notification_consumer(order_id):
    subject = 'New Order Notification'
    recipients = get_consumer_mail(order_id)
    body = f"Your order have been received, Order ID: {order_id}"
    send_email(subject, recipients, body)
    return 'Email sent successfully!'


# Function to retrieve relevant consumer mail for the message to be sent
def get_consumer_mail(order_id):
    order = Orders.query.filter_by(order_id=order_id).first()
    if order:
        consumer = Consumer.query.get(order.consumer_id)
        return [consumer.email]
    return []


def cancel_mail(order_id):
    subject = 'New Order Notification'
    recipients = get_producer_email(order_id)
    body = f"The order,  Order ID: {order_id} is cancelled"
    send_email(subject, recipients, body)
    return 'Email sent successfully!'


@users_blueprint.route('/account')
@login_required
def account():
    """
    Checks whether the user is a consumer or producer, then renders a page which shows them their details.
    """
    if isinstance(current_user, Producer):
        return render_template('users/account.html',
                               id=current_user.id,
                               email=current_user.email,
                               producer_name=current_user.producer_name,
                               phone=current_user.phone,
                               postcode=current_user.postcode,
                               address_1=current_user.address_1,
                               address_2=current_user.address_2,
                               address_3=current_user.address_3)
    else:
        return render_template('users/account.html',
                               id=current_user.id,
                               email=current_user.email,
                               firstname=current_user.firstname,
                               lastname=current_user.lastname,
                               postcode=current_user.postcode,
                               phone=current_user.phone)
