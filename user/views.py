"""
File: views.py
Authors: Sreejith Sudhir Kalathil, Alexander MacMillan
Description: This file provides features which are shared among both Consumer and Producer users, including login/logout
functionality, and automated e-mails.
"""
from flask import Blueprint, render_template, flash, redirect, url_for, session
from models import Orders, Producer, Consumer
from app import db
from user.forms import LoginForm
import bcrypt
from flask_login import login_user, current_user, logout_user, login_required
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
                return redirect(url_for('consumer.feed', suppliers=feed))
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


def send_email(subject, recipients, body):
    """
    send_email(subject, recipients, body) is a functions that records the message for a mail ans sends it
    """
    msg = Message(subject=subject, recipients=recipients)
    msg.body = body
    Mail.send(msg)


def send_mail_notification_producer(order_id):
    """
    send_mail_notification_producer(order_id) is a function that is invoked when an order is placed, which further sends
    a notification mail to the producer about the order. The function calls send_mail(subject, recipients, body) whcih does
    the operation of sending message via the server. The order_id constraint is used as a reference tp retrieve the producer mail
    from the database through get_producer_mail(order_id).
    """
    subject = 'New Order Notification'
    recipients = get_producer_email(order_id)
    body = f"You have received a new order from a consumer. Order ID: {order_id}"
    send_email(subject, recipients, body)
    return 'Email sent successfully!'


"""
get_producer_email(order_id) is a function that retrieves the producer mail ID, to send the notification mails
at relevant events.
"""
def get_producer_email(order_id):
    order = Orders.query.filter_by(Orders.producer_id, id=order_id)
    if order :
        producer = Producer.query.get(Producer.email).filter_by(Orders.producer_id)
        return  producer
    return None


"""
send_mail_notification_consumer(order_id) is used to send notification mail about the confirmation of an order
to the user, the function formats the structure of the mail with subject, body and recipient, which is retrieved 
through another function invoked get_consumer_mail(order_id) gets the relevant mail through filtering in reference to
the order_id from the database.
"""
def send_mail_notification_consumer(order_id):
    """
    send_mail_notification_consumer(order_id) is used to send notification mail about the confirmation of an order
    to the user, the function formats the structure of the mail with subject, body and recipient, which is retrieved
    through another function invoked get_consumer_mail(order_id) gets the relevant mail through filtering in reference to
    the order_id from the database.
    """
    subject = 'New Order Notification'
    recipients = get_consumer_mail(order_id)
    body = f"Your order have been received, Order ID: {order_id}"
    send_email(subject, recipients, body)
    return 'Email sent successfully!'


def get_consumer_mail(order_id):
    """
    get_consumer_mail(order_id) is a function that retrieves the consumer mail ID, to send the notification mails
    at relevant events.
    """
    order = Orders.query.filter_by(order_id=order_id).first()
    if order:
        consumer = Consumer.query.get(Consumer.email).filter_by(Orders.producer_id)
        return consumer
    return None


'''
cancel_mail(order_id) is a formatted  mail function that has the content for notification once an order is 
cancelled by a consumer within a timeframe.
'''
def cancel_mail(order_id):
    '''
    cancel_mail(order_id) is a formatted  mail function that has the content for notification once an order is
    cancelled by a consumer within a timeframe.
    '''
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
