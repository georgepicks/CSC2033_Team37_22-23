from flask import Blueprint, render_template


pages_blueprint = Blueprint('pages', __name__, template_folder='templates')


@pages_blueprint.route('/index')
def home():
    return render_template('main/index.html')



@pages_blueprint.route('/feed')
def feed():
    nearby_suppliers = [
        {'name': 'Test', 'address': 'Newcastle', 'allergens': 'Nuts'},
        {'name': 'Test', 'address': 'York', 'allergens': 'Dairy'},
        {'name': 'Test', 'address': 'Newcastle', 'allergens': 'Gluten'},
        {'name': 'Test', 'address': 'Sheffield', 'allergens': 'Soy'},
        {'name': 'Test', 'address': 'London', 'allergens': 'Nuts'},
        {'name': 'Test', 'address': 'Newcastle', 'allergens': 'Soy'},
        {'name': 'Test', 'address': 'London', 'allergens': 'Gluten'},
        {'name': 'Test', 'address': 'Leeds', 'allergens': 'Nuts'},
        {'name': 'Test', 'address': 'Sheffield', 'allergens': 'Dairy'},
        {'name': 'Test', 'address': 'Newcastle', 'allergens': 'Nuts'}
    ]
    return render_template('consumer/feed.html', suppliers=nearby_suppliers)



@pages_blueprint.route('/about_us')
def about_us():
    return render_template('main/about_us.html')


@pages_blueprint.route('/contact')
def contact_us():
    return render_template('main/contact.html')
