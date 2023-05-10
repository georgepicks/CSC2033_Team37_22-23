from wtforms import Form, StringField, SelectField


class Search_Item(Form):
    choices = [('Vegeterain', 'Vegan'),
               ('Pescatarian', 'Non-veg'),
               ('Diary', 'Drinks')]
    select = SelectField('Search item:', choices=choices)
    search = StringField('')

