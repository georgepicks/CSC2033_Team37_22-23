"""
Models.py:
Authors: Alexander MacMillan
Description: This file creates classes which initialise tables in the database, this enables interaction with the database through
the classes.
"""
from app import db, app
from flask_login import UserMixin
import bcrypt


class Consumer(db.Model, UserMixin):
    __tablename__ = 'consumers'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    postcode = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    orders = db.relationship('Orders', foreign_keys='Orders.consumer_id')

    def __init__(self, email, firstname, lastname, password, postcode, phone):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.postcode = postcode
        self.phone = phone


class Producer(db.Model, UserMixin):
    __tablename__ = 'producers'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    producer_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    postcode = db.Column(db.String(100), nullable=False)
    address_1 = db.Column(db.String(100), nullable=False)
    address_2 = db.Column(db.String(100), nullable=False)
    address_3 = db.Column(db.String(100), nullable=False)
    inventory = db.relationship('InventoryItems')
    orders = db.relationship('Orders')

    def __init__(self, email, producer_name, password, phone, postcode, address_1, address_2, address_3):
        self.email = email
        self.producer_name = producer_name
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.phone = phone
        self.postcode = postcode
        self.address_1 = address_1
        self.address_2 = address_2
        self. address_3 = address_3


class InventoryItems(db.Model):
    __tablename__ = 'inventory_items'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    producer = db.Column(db.Integer, db.ForeignKey(Producer.id), nullable=False)
    dietary = db.Column(db.String(100), nullable=False, default="None")

    def __init__(self, item, quantity, producer, dietary):
        self.item = item
        self.quantity = quantity
        self.producer = producer
        self.dietary = dietary


class Orders(db.Model):
    __tablename__ = 'orders'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    producer_id = db.Column(db.Integer, db.ForeignKey(Producer.id), nullable=False)
    consumer_id = db.Column(db.Integer, db.ForeignKey(Consumer.id), nullable=False)
    order_time = db.Column(db.DateTime, nullable=False)
    items = db.Relationship('OrderItems')

    def __init__(self, producer_id, consumer_id, order_time):
        self.consumer_id = consumer_id
        self.producer_id = producer_id
        self.order_time = order_time


class OrderItems(db.Model):
    __tablename__ = 'order_items'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey(Orders.id))

    def __init__(self, item, quantity, order_id):
        self.item = item
        self.quantity = quantity
        self.order_id = order_id

#def init_db():
#    with app.app_context():
#        db.drop_all()
#        db.session.commit()
#       db.create_all()
#        new_producer = Producer("jd@jdwetherspoons.com", "The Keel Row", "secretPassword1", '07538152684', "NE1 4SH",
#                                'The Gate', 'Newgate St, Newcastle upon Tyne', 'Tyne and Wear')
#        new_consumer = Consumer("s@k.com", "Sree", 'Kalathil', 'secretPassword2', 'NE1 2YX', '012345678910')
#        db.session.add(new_producer)
#        db.session.add(new_consumer)
#        db.session.commit()


#init_db()
