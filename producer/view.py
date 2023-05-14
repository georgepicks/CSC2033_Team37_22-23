from flask import render_template, redirect, url_for, request,Blueprint
from flask_login import login_required
from models import InventoryItems
from app import app, db

producer_blueprint = Blueprint('producer', __name__, template_folder='templates')


@app.route('/admin/inventory')
@login_required
def inventory():
    items = InventoryItems.query.all()
    return render_template('', items=items)


@app.route('/', methods=['GET', 'POST'])
@login_required
def edit_item(id):
    item = InventoryItems.query.get_or_404(id)
    if request.method == 'POST':
        item.name = request.form['name']
        item.quantity = request.form['quantity']
        db.session.commit()
        return redirect(url_for('inventory'))
    else:
        return render_template('edit_item.hyml', item=item)


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

@app.route('/orders')
def orders():
    cursor = db.cursor()

    # Retrieve all orders from the database
    select_query = "SELECT * FROM Orders"
    cursor.execute(select_query)
    orders = cursor.fetchall()

    # Pass the orders to the template for rendering
    return render_template('orders.html', orders=orders)


def accept_order(order_id, inventory):
    for item in inventory:
        if item['id'] == order_id:
            inventory.remove(item)
            return True
    return False


def remove_item(item_id):
    item = InventoryItems.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return True
    else:
        return False

@app.route('/inventory/remove/<int:item_id>', methods=['POST'])
def remove_item_route(item_id):
    if remove_item(item_id):
        return redirect(url_for('inventory'))
    else:
        return "Item not found"
