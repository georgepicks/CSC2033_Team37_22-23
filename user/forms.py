from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField


class LoginForm(FlaskForm):
    email = StringField(render_kw={"size": 50, "maxlength": 70})
    password = PasswordField(render_kw={"size": 50, "maxlength": 70})
    submit = SubmitField(render_kw={"size": 50, "maxlength": 50})


class RegisterForm(FlaskForm):
    email = StringField(render_kw={"size": 50, "maxlength": 70})
    password = PasswordField(render_kw={"size": 50, "maxlength": 70})
    confirm_password = PasswordField(render_kw={"size": 50, "maxlength": 70})
    phone = StringField(render_kw={"size": 50, "maxlength": 70})
    submit = SubmitField(render_kw={"size": 50, "maxlength": 50})
