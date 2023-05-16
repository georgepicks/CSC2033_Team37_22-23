from app import db

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
    consumer_orders = db.relationship('Orders', foreign_keys='Orders.consumer_id')
    producer_orders = db.relationship('Orders', foreign_keys='Orders.producer_id')
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
    item = db.Column(db.String(100), nullable=False, primary_key=True)

    producer_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    producer = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    dietary = db.Column(db.String(100), nullable=False, default="None")


    def __init__(self, item, quantity, dietary):
        self.item = item
        self.quantity = quantity
        self.dietary = dietary


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

    item = db.Column(db.String(100), nullable=False, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey(Orders.order_id))

    def __init__(self, order_id, item, quantity):
        self.item = item
        self.quantity = quantity


#def init_db():
#    to use this function, "from app import app"
#    with app.app_context():
        #db.drop_all()
        #db.create_all()
        #user1 = User("a@m.com", "Alex", "MacMillan", "secretPassword1", "NE1 4SH", '07538152684', 'admin')
        #user2 = User("s@k.com", "Sree", 'Kalathil', 'secretPassword2', 'NE1 2YX', '012345678910', 'producer')
        #user3 = User('b@g.com', 'Broden', 'Gates', 'secretPassword3', 'NE3 4TT', '0987654321', 'consumer')
        #db.session.add(user1)
        #db.session.add(user2)
        #db.session.add(user3)
        #db.session.commit()


# init_db()
