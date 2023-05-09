from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask import flash, render_template, request, redirect
from models import Inventory
from consumer import view

app = Flask(__name__)

app = Flask(__name__)
# initialise database
engine = create_engine('mariadb:///csc2033_team37:BikeRode4out@cs-db.ncl.ac.uk:3306/csc2033_team37')
# engine = create_engine("jdbc:mariadb://cs-db.ncl.ac.uk:3306/csc2033_team37")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb://csc2033_team37:BikeRode4out@cs-db.ncl.ac.uk/csc2033_team37'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/', methods=['GET', 'POST'])
def index():
    search = view.Search_Item(request.form)
    if request.method == 'POST':
        return search_results(search)
    return render_template('', form=search)

@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']
    if search.data['search'] == '':
        qry = db.session.query(Inventory.item)
        results = qry.all()
    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        return render_template('', results=results)



if __name__ == '__main__':
    app.run()
