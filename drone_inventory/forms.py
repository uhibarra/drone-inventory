# Third Party Library Imports
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

# Project Files
from wtforms.validators import InputRequired, Email, EqualTo


class UserLoginForm(FlaskForm):
    # email, password, confirm, submit_button
    email = StringField('Email', validators= [InputRequired(), Email()])
    password = PasswordField('Password', validators= [InputRequired(), EqualTo('confirm', message='Passwords must MATCH!')])
    confirm = PasswordField('Repeat Password')
    submit_button = SubmitField()