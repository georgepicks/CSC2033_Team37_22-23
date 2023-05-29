"""
File: consumer/view.py
Authors: Sreejith Sudhir Kalathil, George Pickard, Alexander MacMillan
Description: Provides all the functionality specific to consumer users. This includes their specific register form, as
well as displaying the feed, allowing them to filter or search for producers in the feed, and CREATE, UPDATE and
DELETING orders.
"""
import pgeocode
from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify, flash
from flask_login import login_required, current_user
from models import Consumer, InventoryItems, OrderItems, Orders, Producer
from app import app, db
from datetime import datetime
from user import views
from user.forms import ConsumerRegisterForm

consumer_blueprint = Blueprint('consumer', __name__, template_folder='templates')


@consumer_blueprint.route('/consumer/register', methods=['GET', 'POST'])
def register():
    """
    Called when a user is redirected to consumer/register, calls upon the ConsumerRegisterForm() in forms.py, when user
    submits it creates a new consumer in the consumer table then redirects them to log into their new account.
    """
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
    """
    Called when user redirects to /feed, collects all producers and displays them as buttons which consumer can click on to
    proceed to /order
    """
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
    """
    Called when the consumer selects a producer, displays information about the producer and all of the items they have
    available in their inventory
    """
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


    return render_template('consumer/order.html', items=items, supplier_name=name, supplier_address1=address1,
                           supplier_address2=address2, supplier_address3=address3, supplier_postcode=postcode)


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



@app.route('/feed', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        query = request.form.get('query')  # Retrieve the search query from the form

        # Searching using SQLALCHEMY
        results = InventoryItems.item.query.filter(InventoryItems.item.name.ilike(f'%{query}%')).all()

        if not results:
            message = "No items found matching your search query."

        return render_template('search_results.html', results=results, message=message)

    return render_template('search.html')


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


@app.route('/order/edit/<int:order_id>', methods=['GET', 'POST'])
@login_required
def edit_order(order_id):
    """
    Allows the user to edit or make changes to the order before confirmation
    """
    order = OrderItems.query.get_or_404(order_id)
    if request.method == 'POST':
        order.item = request.form['item']
        order.quantity = request.form['quantity']
        db.session.commit()
        return redirect(url_for(''))
    else:
        return render_template('', order=order)


# Shows the information about the order
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


@app.route('/cancel-order', methods=['POST'])
@login_required
def cancel_order(order_id):
    """
    If the cancellation deadline has not expired, enables the consumer to delete an Order object
    """
    # Retrieve the order with the given order ID from the database
    order = Orders.query.get(order_id)

    if order:
        cancellation_deadline = session.get('cancellation_deadline')
        if cancellation_deadline and datetime.now() < cancellation_deadline:
            # Perform cancellation logic
            db.session.delete(order)  # Delete the order from the database
            db.session.commit()
            session.pop('selected_products', None)
            session.pop('cancellation_deadline', None)
            flash('Order is cancelled')
            views.cancel_mail(order_id)
        else:
            flash('Cancellation period has expired.')
    else:
        flash('Order not found.')

    return redirect(url_for('order'))


@app.route('/')
def find_producers(distance_range):
    """
    Called before loading the feed, by default just displays them all to the consumer, but if they add a maximum distance
    filter, compares the producer's postcodes against that of the user, removes from the display the ones that are too far
    away, and sorts the rest by distance from the consumer.
    """
    # if user has not yet specified a distance
    if distance_range == 0:
        producers = Producer.query.all()
        return producers
    else:
        geodistance = pgeocode.GeoDistance('gb')
        nearby_producers = {}
        # query all producers
        producers = Producer.query.all()
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
    """
    Enables the consumer to edit their personal details
    """
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

