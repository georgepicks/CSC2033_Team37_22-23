from app import db, app
import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    postcode = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False, default='consumer')
    orders = db.relationship('Order')
    # only for producers:
    inventory = db.relationship('Inventory')
    # verification to be added for producers too

    def __init__(self, email, firstname, lastname, password, postcode, phone, role):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.postcode = postcode
        self.phone = phone
        self.role = role


class Inventory(db.Model):
    __tablename__ = 'inventory items'
    producer_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    item = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, producer_id, item, quantity):
        self.producer_id = producer_id
        self.item = item
        self.quantity = quantity

class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    producer_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    consumer_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    items = db.Column(db.List, nullable=False)
    order_time = db.Column(db.DateTime, nullable=False)

    def __init(self, producer_id, consumer_id, items, order_time):
        self.producer_id = producer_id
        self.consumer_id = consumer_id
        self.producer_id = producer_id
        self.items = items
        self.datetime = datetime

# DO NOT RUN init_db YET, DATABASE IS NOT READY
def init_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

init_db()
