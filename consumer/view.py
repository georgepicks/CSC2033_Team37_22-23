from flask import Blueprint, render_template,request,session, redirect, url_for
from flask_login import login_required
from models import User, InventoryItems
from app import app, db


consumer_blueprint = Blueprint('consumer', __name__, template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
@login_required
def search():

    if request.method == 'POST':
      query = request.form.get('query')  # Retrieve the search query from the form

      # Perform the search in the database using SQLAlchemy
      results = InventoryItems.item.query.filter(InventoryItems.item.name.ilike(f'%{query}%')).all()

      if not results:
        message = "No items found matching your search query."
      else:
        message = None

      return render_template('search_results.html', results=results, message=message)

    return render_template('search.html')


@app.route('/filter search', methods=['GET', 'POST'])
def filter_search():
    if request.method == 'POST':
        query = request.form['query']
        # Perform search based on the query
        results = search(query)
        return render_template('search_results.html', results=results)
    else:
        session['selected_products'] = []
        return render_template('search.html')


def get_product_by_id(product_id):
  # Find a product with the given ID
  for product in InventoryItems.item:
    if product['id'] == product_id:
      return product
  return None


@app.route('/add_to_order/<int:product_id>', methods=['GET'])
def add_to_order(product_id):
  # Retrieve the product based on the product_id
  product = get_product_by_id(product_id)
  if product:
    selected_products = session.get('selected_products', [])
    selected_products.append(product)
    session['selected_products'] = selected_products
  return redirect(url_for('order'))


@app.route('/search_results/<query>')
@login_required
def search_results(query):
  results = User.query.whoosh_search(query).all()
  return render_template('search_results.html', query=query, results=results)


@app.route('/order/edit/<int:order_id>', methods=['GET', 'POST'])
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
        return redirect(url_for('Order', order_id=order_id))
    else:
        # Retrieve the order from the database
        select_query = "SELECT * FROM Order WHERE order_id=%s"
        cursor.execute(select_query, (order_id,))
        order = cursor.fetchone()

        if order:
          return (render_template('edit_order.html', order=order))

        else:
          return 'Order not found'

    cursor.close()


@app.route('/order/<int:order_id>')
def order_details(order_id):
  cursor = db.cursor()
  select_query = "SELECT * FROM Order WHERE order_id=%s"
  cursor.execute(select_query, (order_id,))
  order = cursor.fetchone()

  if order:
    return render_template('order_details.html', order=order)

