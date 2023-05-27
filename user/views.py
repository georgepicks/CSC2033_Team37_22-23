from flask import Blueprint, render_template, flash, redirect, url_for, session, Markup, request
from models import Orders, Producer, Consumer
from app import db
from user.forms import LoginForm
import bcrypt
from flask_login import login_user, current_user, logout_user, login_required, UserMixin
from datetime import datetime
import logging
from flask_mail import Message, Mail
from consumer.view import find_producers

users_blueprint = Blueprint('users', __name__, template_folder='templates')

# defining a login function
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # create login form object
    form = LoginForm()
    # if request method is POST or form is valid
    if form.validate_on_submit():
        # session implemented to limit the number of logins if user fails to login
        if not session.get('authentication_attempts'):
            session['authentication_attempts'] = 0
        # checks if the user mail logged in is a producer mail
        if Producer.query.filter_by(email=form.email.data).first():
            user = Producer.query.filter_by(email=form.email.data).first()
            # if condition checking if the encrypted password is similar to database, if the user exists and the
            # verification key entered is false
            if not user or not bcrypt.checkpw(form.password.data.encode('utf-8'), user.password.encode('utf-8')):
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
                    return redirect(url_for('users.ProducerRegister.html'))

                flash('Please check your login details and try again,{} login attempts remaining'.format(
                    5 - session.get('authentication_attempts')))
            else:
                # user login is initiated
                login_user(user)
                # current login user is matched to the last login user
                # user.last_login = user.current_login
                # user.current_login = datetime.now()
                db.session.add(user)
                db.session.commit()
                # Data is recorded in lottery.log each time login action takes place
                return render_template('producer/supplier_dash.html', id=current_user.id)

        # checks if the user mail logged in is a consumer mail
        elif Consumer.query.filter_by(email=form.email.data).first():
            user = Consumer.query.filter_by(email=form.email.data).first()
            # if condition checking if the encrypted password is similar to database, if the user exists and the
            # verification key entered is false
            if not user :
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
                    return redirect(url_for('users.ConsumerRegister.html'))

                flash('Please check your login details and try again,{} login attempts remaining'.format(
                    5 - session.get('authentication_attempts')))
            else:
                # user login is initiated
                login_user(user)
                # # current login user is matched to the last login user
                feed = find_producers(1000)
                db.session.add(user)
                db.session.commit()
                # Data is recorded in lottery.log each time login action takes place
                logging.warning('SECURITY - Log in [%s, %s]', current_user.id, current_user.email)
                return render_template('consumer/feed.html', suppliers=feed)

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
    logout_user()
    #the user is redirected to index page after logout
    return redirect(url_for('index'))


# Function to send mails to producers while an order is made
def send_email(subject, recipients, body):
    msg = Message(subject=subject, recipients=recipients)
    msg.body = body
    Mail.send(msg)


# Message for the producer that is sent through email
def send_mail_notification_producer(consumer_id, order_id):
    subject = 'New Order Notification'
    recipients = get_producer_email(consumer_id)
    body = f"You have received a new order from a consumer. Order ID: {order_id}"
    send_email(subject, recipients, body)
    return 'Email sent successfully!'


# Function to retrieve relevant producer mail for the message to be sent
def get_producer_email(consumer_id):
    # order is retrieved in reference to the customer_id
    order = Orders.query.filter_by(consumer_id=consumer_id).first()
    if order:
        producer = Producer.query.get(order.producer_id)
        return [producer.email]
    return []

# Message for the consumer that is sent through email
def send_mail_notification_consumer( order_id):
    subject = 'New Order Notification'
    recipients = get_consumer_mail(order_id)
    body = f"Your order have been received, Order ID: {order_id}"
    send_email(subject, recipients, body)
    return 'Email sent successfully!'

#Function to retrieve relevant consumer mail for the message to be sent
def get_consumer_mail(order_id):
    order = Orders.query.filter_by(order_id=order_id).first()
    if order:
        consumer = Consumer.query.get(order.consumer_id)
        return [consumer.email]
    return []

def cancel_mail(consumer_id, order_id):
    subject = 'New Order Notification'
    recipients = get_producer_email(consumer_id)
    body = f"The order,  Order ID: {order_id} is cancelled"
    send_email(subject, recipients, body)
    return 'Email sent successfully!'


