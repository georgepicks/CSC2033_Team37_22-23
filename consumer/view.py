from _curses import flash
import pgeocode
from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models import Consumer, InventoryItems, OrderItems, Orders, Producer
from app import app, db
from datetime import datetime
from user import views
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

        # create a new user with the form data
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
        logging.warning('SECURITY - User registration [%s, %s]', form.email.data, request.remote_addr)
        return redirect(url_for('users/login.html'))
    # if request method is GET or form not valid re-render signup page
    return render_template('users/ConsumerRegister.html', form=form)


@app.route('/', methods=['GET', 'POST'])
@login_required
def generate_dashboard():
    # need to change to allow consumers to select a max distance
    placeholder = 1000
    # get list of producers within user-specified range alongside their distance from consumer
    producers = find_producers(placeholder)
    return render_template("")


# Function to search for an item in the inventory
@app.route('/', methods=['GET', 'POST'])
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


# Function that allows the user to edit or make changes to the order before confirmation
@app.route('/order/edit/<int:order_id>', methods=['GET', 'POST'])
@login_required
def edit_order(order_id):
    cursor = db.cursor()

    if request.method == 'POST':
        # Get the updated order information from the form
        new_order_info = {
            'item': request.form['item'],
            'quantity': request.form['quantity'],
        }

        # Update the order in the database
        update_query = "UPDATE OrderItems SET item=%s, quantity=%s WHERE order_id=%s"
        cursor.execute(update_query, (new_order_info['item'], new_order_info['quantity'], order_id))
        db.commit()

        # Redirect to the order details page
        cursor.close()
        return redirect(url_for('Order_detail.html', order_id=order_id))
    else:
        # Retrieve the order from the database
        select_query = "SELECT * FROM OrderItems WHERE order_id=%s"
        cursor.execute(select_query, (order_id,))
        order = cursor.fetchone()

        if order:
            cursor.close()
            return render_template('edit_item.html', order=order)
        else:
            cursor.close()
            return 'Order not found'


# Shows the information about the order
@app.route('/order/<int:order_id>')
@login_required
def order_details(order_id):
    cursor = db.cursor()
    select_query = "SELECT * FROM OrderItems WHERE order_id=%s"
    cursor.execute(select_query, (order_id,))
    order = cursor.fetchone()

    if order:
        return render_template('order_details.html', order=order)


# Function to place an order
@app.route('/place_order-order', methods=['GET', 'POST'])
@login_required
def place_order(consumer_id, producer_id, items):
    order_time = datetime.now()

    # Creates an instance of the Orders model
    order = Orders(producer_id=producer_id, consumer_id=consumer_id, order_time=order_time)
    db.session.add(order)
    db.session.commit()

    # Retrieves the order_id for the newly created order
    order_id = order.order_id

    # Creates instances of OrderItems for each item in the order
    for item, quantity in items.items():
        order_item = OrderItems(item=item, quantity=quantity, order_id=order_id)
        db.session.add(order_item)

    db.session.commit()
    views.send_mail_notification(consumer_id, order_id)

    return order_id


# Function to cancel an order made within a timeframe
@app.route('/cancel-order', methods=['POST'])
@login_required
def cancel_order():
    # calls for cancellation deadline time
    cancellation_deadline = session.get('cancellation_deadline')
    if cancellation_deadline and datetime.now() < cancellation_deadline:
        # Perform cancellation logic
        session.pop('selected_products', None)
        session.pop('cancellation_deadline', None)
        flash('Order is cancelled')
    else:
        flash('Cancellation period has expired.')

    return redirect(url_for('order'))


@app.route('/')
def find_producers(distance_range, filter):
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


# view user account
@consumer_blueprint.route('/account')
@login_required
def account():
    # Shows the account details of the user
    return render_template('users/account.html',
                           id=current_user.id,
                           email=current_user.email,
                           firstname=current_user.firstname,
                           lastname=current_user.lastname,
                           phone=current_user.phone,
                           postcode=current_user.postcode)
