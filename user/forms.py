"""
File: forms.py
Author: Sreejith Sudhir Kalathil, Samuel Robertson
Description: Generates forms for the user to use to submit data to the server. Also includes input validation functions
to prevent invalid or even malicious data into storage.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, RadioField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp
import re


def character_check(form, field):
    """
    Whitelists characters which are allowed to be input
    """
    excluded_chars = "^[A-Z0-9+_.-]+@[A-Z0-9.-]+$"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(f"Character {char} is not allowed.")


def validate_password(self, data_field):
    """
    Ensures password and confirm password fields are identical
    """
    p = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-])')
    if not p.match(data_field.data):
        raise ValidationError(
            "Password should contain 1 uppercase letter, lowercase letters, one digit "
            "and should be at least 6 characters with one special character")


def validate_phone(self, data_field):
    """
    Ensures phone field is a valid phone number
    """
    i = re.compile(r'(?=\d\d\d\d\d\d\d\d\d\d\d)')
    if not i.match(data_field.data):
        raise ValidationError("Phone number must have 11 digits")


def validate_postcode(self, data_field):
    """
    Ensures postcode entry is a valid postcode
    """
    c = re.compile(r'^[A-Za-z]{1,2}[0-9][0-9A-Za-z]?\s?[0-9][A-Za-z]{2}$')
    if not c.match(data_field.data):
        raise ValidationError("Invalid Postcode")


# initialising register form validators
class ConsumerRegisterForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()], render_kw={"size": 50, "maxlength": 70})
    firstname = StringField(validators=[DataRequired(), character_check], render_kw={"size": 50, "maxlength": 70})
    lastname = StringField(validators=[DataRequired(), character_check], render_kw={"size": 50, "maxlength": 70})
    phone = StringField(validators=[DataRequired(), validate_phone], render_kw={"size": 50, "maxlength": 70})
    password = PasswordField('password',
                             validators=[DataRequired(), Length(min=6, max=15), validate_password],
                             render_kw={"size": 50, "maxlength": 70})
    confirm_password = PasswordField('confirm_password',
                                     validators=[EqualTo('password', message='Both password fields must be equal!')],
                                     render_kw={"size": 50, "maxlength": 70})
    postcode = StringField('Postcode', validators=[DataRequired(), validate_postcode],
                           render_kw={"size": 50, "maxlength": 70})
    submit = SubmitField(validators=[DataRequired()], render_kw={"size": 50, "maxlength": 50})


class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()], render_kw={"size": 50, "maxlength": 70})
    password = PasswordField('password',
                             validators=[DataRequired()], render_kw={"size": 50, "maxlength": 70})
    submit = SubmitField(validators=[DataRequired()], render_kw={"size": 50, "maxlength": 50})


class ProducerRegisterForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()], render_kw={"size": 50, "maxlength": 70})
    producer_name = StringField(validators=[DataRequired(), character_check], render_kw={"size": 50, "maxlength": 70})
    phone = StringField(validators=[DataRequired(), validate_phone], render_kw={"size": 50, "maxlength": 70})
    password = PasswordField('password', validators=[DataRequired(), Length(min=6, max=15), validate_password],
                             render_kw={"size": 50, "maxlength": 70})
    confirm_password = PasswordField('confirm_password',
                                     validators=[EqualTo('password', message='Both password fields must be equal!')],
                                     render_kw={"size": 50, "maxlength": 70})

    address1 = StringField('Address 1', validators=[DataRequired()], render_kw={"size": 50, "maxlength": 70})
    address2 = StringField('Address 2', validators=[DataRequired()], render_kw={"size": 50, "maxlength": 70})
    address3 = StringField('Address 2', validators=[DataRequired()], render_kw={"size": 50, "maxlength": 70})
    postcode = StringField('Postcode', validators=[
        DataRequired(), validate_postcode], render_kw={"size": 50, "maxlength": 70})
    submit = SubmitField(validators=[DataRequired()], render_kw={"size": 50, "maxlength": 50})
