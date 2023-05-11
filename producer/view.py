
=======
from flask import render_template, redirect, url_for, request,Blueprint
from flask_login import login_required
from models import Inventory
from app import app, db

producer_blueprint = Blueprint('producer', __name__, template_folder='templates')


@app.route('/admin/inventory')
@login_required
def inventory():
    items = Inventory.query.all()
    return render_template('', items=items)


@app.route('/', methods=['GET', 'POST'])
@login_required
def edit_item(id):
    item = Inventory.query.get_or_404(id)
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
        item = Inventory.item(name=name, quantity=quantity)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('inventory'))
    else:
        return render_template('')


@app.route('/orders')
def orders():
    cursor = db.cursor()

    # Retrieve all orders from the database
    select_query = "SELECT * FROM OrderItems"
    cursor.execute(select_query)
    orders = cursor.fetchall()

    # Pass the orders to the template for rendering
    return render_template('orders.html', orders=orders)
