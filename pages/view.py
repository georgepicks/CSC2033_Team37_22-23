from flask import Blueprint, render_template


pages_blueprint = Blueprint('pages', __name__, template_folder='templates')


@pages_blueprint.route('/index')
def home():
    return render_template('main/index.html')



@pages_blueprint.route('/feed')
def feed():
    # Sample data for demonstration, will take data from D
    nearby_suppliers = [
        {'name': 'Test', 'address': 'Newcastle', 'allergens': 'Allergens: Nuts', 'image': 'https://picsum.photos/200/300'},
        {'name': 'Test', 'address': 'York', 'allergens': 'Allergens: Dairy', 'image': 'https://picsum.photos/200/300'},
        {'name': 'Test', 'address': 'Newcastle', 'allergens': 'Allergens: Gluten', 'image': 'https://picsum.photos/200/300'},
        {'name': 'Test', 'address': 'Sheffield', 'allergens': 'Allergens: Soy', 'image': 'https://picsum.photos/200/300'},
        {'name': 'Test', 'address': 'London', 'allergens': 'Allergens: Nuts', 'image': 'https://picsum.photos/200/300'},
        {'name': 'Test', 'address': 'Newcastle', 'allergens': 'Allergens: Soy', 'image': 'https://picsum.photos/200/300'},
        {'name': 'Test', 'address': 'London', 'allergens': 'Allergens: Gluten', 'image': 'https://picsum.photos/200/300'},
        {'name': 'Test', 'address': 'Leeds', 'allergens': 'Allergens: Nuts', 'image': 'https://picsum.photos/200/300'},
        {'name': 'Test', 'address': 'Sheffield', 'allergens': 'Allergens: Dairy', 'image': 'https://picsum.photos/200/300'},
        {'name': 'Test', 'address': 'Newcastle', 'allergens': 'Allergens: Nuts', 'image': 'https://picsum.photos/200/300'}
    ]
    return render_template('consumer/feed.html', suppliers=nearby_suppliers)

@pages_blueprint.route('/order')
def order():
    # Sample data for demonstration, will take data from DB
    supplier = {
        'inventory': [
            {'item': 'Item 1', 'quantity': 10},
            {'item': 'Item 2', 'quantity': 5},
            {'item': 'Item 3', 'quantity': 2},
            {'item': 'Item 3', 'quantity': 2},
            {'item': 'Item 3', 'quantity': 2},
            {'item': 'Item 3', 'quantity': 2},
            {'item': 'Item 3', 'quantity': 2},
            {'item': 'Item 3', 'quantity': 2},
            {'item': 'Item 3', 'quantity': 2}
        ]
    }
    return render_template('consumer/order.html', supplier=supplier)

@pages_blueprint.route('/about_us')
def about_us():
    return render_template('main/about_us.html')


@pages_blueprint.route('/contact')
def contact_us():
    return render_template('main/contact.html')
