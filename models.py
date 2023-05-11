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
    inventory = db.relationship('InventoryItems')
    # verification to be added for producers too

    def __init__(self, email, firstname, lastname, password, postcode, phone, role):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.postcode = postcode
        self.phone = phone
        self.role = role


class InventoryItems(db.Model):
    __tablename__ = 'inventory items'
    producer_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    item = db.Column(db.String(100), nullable=False, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, producer_id, item, quantity):
        self.producer_id = producer_id
        self.item = item
        self.quantity = quantity


class Orders(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    producer_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    consumer_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    order_time = db.Column(db.DateTime, nullable=False)
    items = db.Relationship('OrderItems')

    def __init(self, producer_id, consumer_id, order_time):
        self.consumer_id = consumer_id
        self.producer_id = producer_id
        self.order_time = order_time


class OrderItems(db.Model):
    __tablename__ = 'order items'
    order_id = db.Column(db.Integer, db.ForeignKey(Orders.order_id), nullable=False)
    item = db.Column(db.String(100), nullable=False, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, order_id, item, quantity):
        self.order_id = order_id
        self.item = item
        self.quantity = quantity


def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()

#init_db()