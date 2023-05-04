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
    producer_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True, nullable=False)
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
    order_time = db.Column(db.DateTime, nullable=False)
    items = db.relationship('OrderItems')

    def __init__(self, order_id, consumer_id, producer_id, items, order_time):
        self.order_id = order_id
        self.consumer_id = consumer_id
        self.producer_id = producer_id
        self.items = items
        self.order_time = order_time


class OrderItems(db.Model):
    __tablename__ = 'order items'
    item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey(Order.order_id))
    item = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, item_id, order_id, item, quantity):
        self.item_id = item_id
        self.order_id = order_id
        self.item = item
        self.quantity = quantity


def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()

# init_db()
