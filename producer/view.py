"""
File: producer/view.py
Authors: Sreejith Sudhir Kalathil, Samuel Robertson
Description: Provides all the functionality specific to producer users. This includes their specific register form, as
well as CREATE, UPDATE and DELETE functions for the producer's inventory, in addition to allowing the producer to
accept newly created orders.
"""
from flask import render_template, redirect, url_for, request, Blueprint, flash
from flask_login import login_required, current_user
from models import InventoryItems, Producer, OrderItems, Orders
from app import app, db
from user.forms import ProducerRegisterForm
from user.views import send_mail_notification_consumer

producer_blueprint = Blueprint('producer', __name__, template_folder='templates')


@producer_blueprint.route('/producer/register', methods=['GET', 'POST'])
def register():
    """
    Called when a user is redirected to producer/register, calls upon the ProducerRegisterForm() in forms.py, when user
    submits it creates a new producer in the producer table then redicts them to log into their new account.
    """
    # create signup form object
    form = ProducerRegisterForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():

        user = Producer.query.filter_by(email=form.email.data).first()
        # if this returns a user, then the email already exists in the database

        # if email already exists redirect user back to signup page with error message so user can try again
        if user:
            flash('Email address already exists')
            return render_template('users/ProducerRegister.html', form=form)

        # create a new user with the form data according to a producer
        new_user = Producer(email=form.email.data,
                            producer_name=form.producer_name.data,
                            phone=form.phone.data,
                            password=form.password.data,
                            address_1=form.address1.data,
                            address_2=form.address2.data,
                            address_3=form.address3.data,
                            postcode=form.postcode.data)

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # sends user to login page
        return redirect(url_for('users.login'))

    # if request method is GET or form not valid re-render signup page
    return render_template('users/ProducerRegister.html', form=form)


@app.route('/supplier_inventory')
@login_required
def inventory():
    """
    Shows a producer the items they have already in their inventory, and renders buttons to edit.
    """
    id = current_user.id
    items = InventoryItems.query.filter(InventoryItems.producer.ilike(id)).all()
    return render_template('producer/supplier_inventory.html', items=items)


@producer_blueprint.route('/edit_item/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_inventory(id):
    """
    Enables producer to edit the items in their inventory
    """
    item = InventoryItems.query.get_or_404(id)
    if request.method == 'POST':
        item.item = request.form.get('name')
        item.quantity = request.form.get('quantity')
        item.dietary = request.form.get('dietary')
        db.session.commit()
        return redirect(url_for('inventory'))
    else:
        return render_template('producer/edit_item.html', item=item)


@app.route('/supplier_additem', methods=['GET', 'POST'])
@login_required
def add_item():
    """
    Adds a new item to the producer's inventory, where item details are based on form input, then returns the producer to
    their inventory page
    """
    if request.method == 'POST':
        # if not isinstance(current_user._get_current_object(), Producer):
        # flash('You need to be a producer to add items')
        # return redirect(url_for('home'))

        try:
            item = request.form['name']
            quantity = int(request.form['quantity'])  # convert to integer
            dietary = request.form['dietary']
            producer = current_user.id  # Assuming the logged in user is the producer
            inventory_item = InventoryItems(item=item, quantity=quantity, producer=producer, dietary=dietary)
            db.session.add(inventory_item)
            db.session.commit()
        except ValueError:  # catch conversion errors
            flash('Invalid quantity. Please enter a number')
            return redirect(url_for('add_item'))

        return redirect(url_for('inventory'))
    else:
        return render_template('producer/supplier_additem.html')



# Function that shows the proper order from the consumer to the producer
@app.route('/supplier_orders')
@login_required
def orders():
    """
    Loads all orders requested from the logged in producer from the database and displays them
    """
    id = current_user.id
    orders = Orders.query.filter(Orders.producer_id.ilike(id)).all()
    return render_template('producer/supplier_orders.html', orders=orders)


@app.route('/')
@login_required
def accept_order(order_id):
    """
    Allows the producer to accept a pending order
    """
    # If an item is accepted as an order, then reduce its quantity in the inventory
    for item in current_user.inventory():
        if item['id'] == order_id:
            if item['quantity'] > 0:
                item['quantity'] -= 1
                flash('Order accepted')
            elif item['quantity'] == OrderItems.quantity:
                inventory.remove(item)
                send_mail_notification_consumer(order_id)
                return True
            else:
                flash('Insufficient quantity')
            return redirect(url_for('dashboard'))
    flash('Order not found')
    return redirect(url_for('dashboard'))


@app.route('/')
@login_required
def remove_item(item_id):
    """
    Enables the producer to manually remove an item from their inventory
    """
    item = InventoryItems.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return True
    else:
        return False


# Function prompts for an error handling part for remove_item(item_id)
@app.route('/inventory/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_item_route(item_id):
    # Checks for any item removed
    if remove_item(item_id):
        return redirect(url_for('inventory'))
    # Case for no item is found
    else:
        return "Item not found"


@login_required
def edit_producer_account(id):
    """
    Allows the producer to change their personal details
    """
    producer = Producer.query.get_or_404(id)
    if request.method == 'POST':
        producer.email = request.form['email']
        producer.producer_name = request.form['producer_name']
        producer.phone = request.form['phone']
        producer.postcode = request.form['postcode']
        producer.address_1 = request.form['address_1']
        producer.address_2 = request.form['address_2']
        producer.address_3 = request.form['address_3']
        db.session.commit()
        return redirect(url_for('users.account'))
    else:
        return render_template('users/edit_account.html', producer=producer)

      
# renders the producer's dashboard
@producer_blueprint.route('/supplier_dash')
@login_required
def supplier_dash():
    return render_template('producer/supplier_dash.html')
