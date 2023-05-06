from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class LoginForm():
    username = StringField(render_kw={"size": 50, "maxlength": 70})
    password = PasswordField(render_kw={"size": 50, "maxlength": 70})
    submit = SubmitField(render_kw={"size": 50, "maxlength": 70})


class RegisterForm():
    username = StringField(render_kw={"size": 50, "maxlength": 70})
    password = PasswordField(render_kw={"size": 50, "maxlength": 70})
    confirm_password = PasswordField(render_kw={"size": 50, "maxlength": 70})
    phone = StringField(render_kw={"size": 50, "maxlength": 70})
    submit = SubmitField(render_kw={"size": 50, "maxlength": 70})
