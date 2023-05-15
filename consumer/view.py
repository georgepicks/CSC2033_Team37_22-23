
from flask_login import login_required, current_user
import pgeocode
from _curses import flash
from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from flask_login import login_required
from models import User, InventoryItems
from app import app, db
from datetime import datetime, timedelta



consumer_blueprint = Blueprint('consumer', __name__, template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def generate_dashboard():
    # need to change to allow consumers to select a max distance
    placeholder = 1000
    # get list of producers within user-specified range alongside their distance from consumer
    producers = find_producers(placeholder)


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


@app.route('/food/<food_type>')
def filter_by_dietary(food_type):
    # Retrieve the items based on the food type
    items = InventoryItems.query.filter(InventoryItems.dietary.ilike(food_type)).all()

    if not items:
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


def get_product_by_id(product_id):

    # Find a product with the given ID
  for product in InventoryItems.item:
    if product['id'] == product_id:
      return product
  return None


@app.route('/add_to_order/<int:product_id>', methods=['GET'])
def order_item(product_id):
    # Retrieve the product based on the product_id
  product = get_product_by_id(product_id)
  if product:
    selected_products = session.get('selected_products', [])
    selected_products.append(product)
    session['selected_products'] = selected_products
#setting the time for cancelling the order to be 5 minutes
    cancellation_deadline = datetime.now() + timedelta(minutes=5)
    session['cancellation_deadline'] = cancellation_deadline

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
          return render_template('edit_order.html', order=order)

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

# Cancel order endpoint
  @app.route('/cancel-order', methods=['POST'])
  def cancel_order():
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
    producers = User.query.filter_by(role="producer").all()
    for i in producers:
        # calculate distance between all producers and current user
        distance = geodistance.query_postal_code(current_user.postcode, i.postcode)
        if distance < distance_range:
            # key = producer, value = distance
            nearby_producers.update({i:distance})
    # sorts producers by distance from low to high
    sorted_producers = dict(sorted(nearby_producers.items(), key=lambda x: x[1]))
    return sorted_producers

      

