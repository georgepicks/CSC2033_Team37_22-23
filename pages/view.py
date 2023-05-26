from flask import Blueprint, render_template

pages_blueprint = Blueprint('pages', __name__, template_folder='templates')


@pages_blueprint.route('/order')
def order():
    # Sample data for demonstration, will take data from DB
    supplier = {
        'inventory': [
            {'item': 'Item 1', 'quantity': 10},
            {'item': 'Item 2', 'quantity': 5},
            {'item': 'Item 3', 'quantity': 20},
            {'item': 'Item 4', 'quantity': 18},
            {'item': 'Item 4', 'quantity': 18},
            {'item': 'Item 4', 'quantity': 20},
            {'item': 'Item 4', 'quantity': 18}
        ]
    }
    return render_template('consumer/order.html', supplier=supplier)
