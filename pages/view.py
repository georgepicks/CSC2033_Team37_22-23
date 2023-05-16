from flask import Blueprint, render_template


pages_blueprint = Blueprint('pages', __name__, template_folder='templates')


@pages_blueprint.route('/index')
def home():
    return render_template('main/index.html')


@pages_blueprint.route('/feed')
def feed():
    return render_template('consumer/feed.html')


@pages_blueprint.route('/about_us')
def about_us():
    return render_template('main/about_us.html')


@pages_blueprint.route('/contact')
def contact_us():
    return render_template('main/contact.html')
