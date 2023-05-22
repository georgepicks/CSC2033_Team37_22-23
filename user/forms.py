from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, RadioField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp
import re



# define character check forms
def character_check(form,field):
    excluded_chars = "^[A-Z0-9+_.-]+@[A-Z0-9.-]+$"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(f"Character {char} is not allowed.")

# define password validator functions
def validate_password(self, data_field):
    p = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-])')
    if not p.match(data_field.data):
        raise ValidationError(
            "Password should contain 1 uppercase letter, lowercase letters, one digit and should be atleast 6 charscters with one special character")


# Define phone validate function
def validate_phone(self,data_field):
    i = re.compile(r'(?=\d\d\d\d-\d\d\d-\d\d\d\d)')
    if not i.match(data_field.data):
        raise ValidationError("Phone number must be of the format XXXX-XXX-XXX")

def validate_postcode(self, data_field):
    c = re.compile(r'^[A-Za-z]{1,2}[0-9][0-9A-Za-z]?\s?[0-9][A-Za-z]{2}$')
    if not c.match(data_field.data):
        raise ValidationError("Invalid Postcode")

#Initialising register form validators
class RegisterForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()],render_kw={"size": 50, "maxlength": 70})
    firstname = StringField(validators=[DataRequired(), character_check],render_kw={"size": 50, "maxlength": 70})
    lastname = StringField(validators=[DataRequired(), character_check],render_kw={"size": 50, "maxlength": 70})
    phone = StringField(validators=[DataRequired(), validate_phone],render_kw={"size": 50, "maxlength": 70})
    password = PasswordField('password',
                            validators=[DataRequired(), Length(min=6, max=15), validate_password],render_kw={"size": 50, "maxlength": 70})
    confirm_password = PasswordField('confirm_password', validators=[
        EqualTo('password', message='Both password fields must be equal!')],render_kw={"size": 50, "maxlength": 70})
    postcode = StringField('Postcode', validators=[
        DataRequired(), validate_postcode()],render_kw={"size": 50, "maxlength": 70})
    role = RadioField('Are you registering as a producer or consumer?',
                      choices=[('producer', 'Producer'), ('consumer', 'Consumer')], validators=[DataRequired()],render_kw={"size": 50, "maxlength": 70})
    submit = SubmitField(validators=[DataRequired()],render_kw={"size": 50, "maxlength": 50})

class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()],render_kw={"size": 50, "maxlength": 70})
    password = PasswordField('password',
                             validators=[DataRequired()],render_kw={"size": 50, "maxlength": 70})
    submit = SubmitField(validators=[DataRequired()],render_kw={"size": 50, "maxlength": 50})



