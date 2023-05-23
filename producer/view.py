from flask import render_template, redirect, url_for, request, Blueprint, flash
from flask_login import login_required, current_user
from models import InventoryItems, Producer
from app import app, db
from user.forms import ProducerRegisterForm
import logging

producer_blueprint = Blueprint('producer', __name__, template_folder='templates')


@producer_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    # create signup form object
    form = ProducerRegisterForm()

    # if request method is POST or form is valid
    if form.validate_on_submit():
        user = Producer.query.filter_by(email=form.email.data).first()
        # if this returns a user, then the email already exists in database

        # if email already exists redirect user back to signup page with error message so user can try again
        if user:
            flash('Email address already exists')
            return render_template('users/register.html', form=form)

        # create a new user with the form data
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
        logging.warning('SECURITY - User registration [%s, %s]', form.email.data, request.remote_addr)
        return redirect(url_for('users/login.html'))
    # if request method is GET or form not valid re-render signup page
    return render_template('users/register.html', form=form)


# Function that shows the inventory to the producer
@app.route('/admin/inventory')
@login_required
def inventory(id):
    items = InventoryItems.query.filter(InventoryItems.producer_id.ilike(id)).all()
    return render_template('', items=items)


# Function to edit inventory table, authentication for relevant producer only
@app.route('/', methods=['GET', 'POST'])
@login_required
def edit_inventory(id):
    item = InventoryItems.query.get_or_404(id)
    if request.method == 'POST':
        item.name = request.form['name']
        item.quantity = request.form['quantity']
        db.session.commit()
        return redirect(url_for('inventory'))
    else:
        return render_template('edit_item.hyml', item=item)


# Function to add an item to the inventory
@app.route('/', methods=['GET', 'POST'])
@login_required
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        item = InventoryItems.item(name=name, quantity=quantity)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('inventory'))
    else:
        return render_template('')


# Function that shows the proper order from the consumer to the produxer
@app.route('/orders')
@login_required
def orders():
    cursor = db.cursor()

    # Retrieve all orders from the database
    select_query = "SELECT * FROM Orders"
    cursor.execute(select_query)
    orders = cursor.fetchall()

    # Pass the orders to the template for rendering
    return render_template('orders.html', orders=orders)


# Function that allows the producer to accept an order by the consumer
@app.route('/orders')
@login_required
def accept_order(order_id, inventory):
    # If an item is accepted as an order, then it is removed from the inventory
    for item in inventory:
        if item['id'] == order_id:
            inventory.remove(item)
            return True
    return False


# Function to remove an item from the inventory by the producer

@app.route('/orders')
@login_required
def remove_item(item_id):
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


# view user account
@producer_blueprint.route('/account')
@login_required
def account():
    # Shows the account details of the user
    return render_template('users/account.html',
                           id=current_user.id,
                           email=current_user.email,
                           producer_name=current_user.producer_name,
                           phone=current_user.phone,
                           postcode=current_user.postcode,
                           address_1=current_user.address_1,
                           address_2=current_user.address_2,
                           address_3=current_user.address_3)
