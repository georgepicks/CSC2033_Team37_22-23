import pgeocode
from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify, flash
from flask_login import login_required, current_user
from models import Consumer, InventoryItems, OrderItems, Orders, Producer
from app import app, db
from datetime import datetime
from user.forms import ConsumerRegisterForm

consumer_blueprint = Blueprint('consumer', __name__, template_folder='templates')


@consumer_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    # create signup form object
    form = ConsumerRegisterForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        user = Consumer.query.filter_by(email=form.email.data).first()
        # if this returns a user, then the email already exists in database

        # if email already exists redirect user back to signup page with error message so user can try again
        if user:
            flash('Email address already exists')
            return render_template('users/ConsumerRegister.html', form=form)

        # create a new user with the form data according to a consumer
        new_user = Consumer(email=form.email.data,
                            firstname=form.firstname.data,
                            lastname=form.lastname.data,
                            phone=form.phone.data,
                            password=form.password.data,
                            postcode=form.postcode.data)

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # sends user to login page
        return redirect(url_for('users.login'))
    # if request method is GET or form not valid re-render signup page
    return render_template('users/ConsumerRegister.html', form=form)


@consumer_blueprint.route('/feed', methods=['GET', 'POST'])
@login_required
def feed():
    suppliers = []  # Create an empty list to store supplier information

    # Retrieve all producers from the database
    producers = Producer.query.all()

    # Iterate over each supplier and extract the required information
    for producer in producers:
        producer_data = {
            'id': producer.id,
            'name': producer.producer_name,
            'address1': producer.address_1,
            'address2': producer.address_2,
            'address3': producer.address_3,
            'postcode': producer.postcode
        }
        suppliers.append(producer_data)

    return render_template('consumer/feed.html', suppliers=suppliers)


@app.route('/order', methods=['GET', 'POST'])
@login_required
def order_generate():
    supplier_id = request.args.get('supplier_id')

    supplier = Producer.query.filter_by(id=supplier_id).first()

    name = supplier.producer_name
    address1 = supplier.address_1
    address2 = supplier.address_2
    address3 = supplier.address_3
    postcode = supplier.postcode

    items = []

    item_list = InventoryItems.query.filter_by(producer=supplier_id).all()

    for item in item_list:
        item_data = {
            'id': item.id,
            'item': item.item,
            'quantity': item.quantity,
            'producer': item.producer,
            'dietary': item.dietary
        }

        items.append(item_data)

        print(items)

    return render_template('consumer/order.html', items=items, supplier_name=name, supplier_address1=address1,
                           supplier_address2=address2,supplier_address3=address3, supplier_postcode=postcode)


# Function to search for an item in the inventory
@app.route('/feed', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        query = request.form.get('query')  # Retrieve the search query from the form

        # Searching using SQLALCHEMY
        results = InventoryItems.item.query.filter(InventoryItems.item.name.ilike(f'%{query}%')).all()

        if not results:
            message = "No items found matching your search query."

        return render_template('consumer/feed.html', results=results, message=message)

    return render_template('consumer/feed.html')


# Function that allows to show items by a dietary filter
@app.route('/food/<food_type>')
@login_required
def filter_by_dietary(food_type):
    # Retrieve the items based on the food type
    items = InventoryItems.query.filter(InventoryItems.dietary.ilike(food_type)).all()

    if not items:
        # Returns error if no item is found
        return jsonify({
            'success': False,
            'error': 'No items found for the specified food type.'
        }), 404

    results = [item.format() for item in items]

    return jsonify({
        'success': True,
        'results': results,
        'count': len(results)
    })


# The Function returning a list of all the relevant items from the search
@app.route('/search_results/<query>')
@login_required
def search_results(query):
    results = Consumer.query.whoosh_search(query).all()
    return render_template('search_results.html', query=query, results=results)


# Function that allows the user to edit or make changes to the order before confirmation
@app.route('/order/edit/<int:order_id>', methods=['GET', 'POST'])
@login_required
def edit_order(order_id):
    order = OrderItems.query.get_or_404(order_id)
    if request.method == 'POST':
        order.item = request.form['item']
        order.quantity = request.form['quantity']
        db.session.commit()
        return redirect(url_for(''))
    else:
        return render_template('', order=order)


# Function to place an order
# Function to place an order
@app.route('/place_order', methods=['GET', 'POST'])
@login_required
def place_order():
    producer_id = request.form.get('supplier_id')
    consumer_id = current_user.id
    order_time = datetime.now()

    # Creates an instance of the Orders model
    order = Orders(producer_id=producer_id, consumer_id=consumer_id, order_time=order_time)
    db.session.add(order)
    db.session.commit()
    # Retrieves the order_id for the newly created order
    order_id = order.id
    items = request.form.getlist('item[]')
    quantities = request.form.getlist('quantity[]')

    # Creates instances of OrderItems for each item in the order
    for item, quantity in zip(items, quantities):
        order_item = OrderItems(item=item, quantity=quantity, order_id=order_id)
        db.session.add(order_item)

        # Subtract the quantity from the inventory
        inventory_item = InventoryItems.query.filter_by(producer=producer_id, item=item).first()
        if inventory_item:
            inventory_item.quantity -= int(quantity)

            if inventory_item.quantity <= 0:
                db.session.delete(inventory_item)
            else:
                db.session.add(inventory_item)
    db.session.commit()
    #views.send_mail_notification(consumer_id, order_id)
    return render_template("consumer/order_confirm.html", order_id=order_id)


# Function to cancel an order made within a timeframe
# Function to place an order
@app.route('/place_order-order', methods=['GET', 'POST'])
@login_required
def order_details():
    consumer_id = current_user.id
    orders = Orders.query.filter_by(consumer_id=consumer_id).all()
    order_ids = [order.id for order in orders]
    order_list = []

    order_info = OrderItems.query.filter(OrderItems.order_id.in_(order_ids)).all()

    for order in order_info:
        order_dict = {
            'id': order.id,
            'item': order.item,
            'quantity': order.quantity,
            'order_id': order.order_id
        }
        order_list.append(order_dict)

    db.session.commit()

    return render_template('consumer/consumer_orders.html', orders_list=order_list)


@app.route('/')
def find_producers(distance_range):
    # if user has not yet specified a distance
    if distance_range == 0:
        producers = Producer.query.all()
        return producers
    else:
        geodistance = pgeocode.GeoDistance('gb')
        nearby_producers = {}
        # query all producers
        producers = Producer.query.all()
        # ------------ need to add distance functionality in later ----------------
        for i in producers:
            # calculate distance between all producers and current user
            distance = geodistance.query_postal_code(current_user.postcode, i.postcode)
            if distance < distance_range:
                # key = producer, value = distance
                nearby_producers.update({i: distance})
        # sorts producers by distance from low to high
        sorted_producers = dict(sorted(nearby_producers.items(), key=lambda x: x[1]))
        return sorted_producers


@consumer_blueprint.route('/consumer_account/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_consumer_account(id):
    consumer = Consumer.query.get_or_404(id)
    if request.method == 'POST':
        consumer.email = request.form['email']
        consumer.firstname = request.form['firstname']
        consumer.lastname = request.form['lastname']
        consumer.phone = request.form['phone']
        consumer.postcode = request.form['postcode']
        db.session.commit()
        return redirect(url_for('users.account'))
    else:
        return render_template('users/edit_account.html', consumer=consumer)


