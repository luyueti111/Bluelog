from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from bluelog import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 100), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class SendEmailForm(FlaskForm):
    emailAddress = StringField('Email', validators=[DataRequired(), Length(1, 100)])
    submit = SubmitField()


class RegisterForm(FlaskForm):
    emailAddress = StringField('Email', validators=[DataRequired(), Length(1, 100), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 100), EqualTo('password2')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    verificationCode = StringField('verificationCode', validators=[DataRequired(), Length(1, 100)])
    submit = SubmitField('Register')


    def validate_emailAddress(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('The email is already in use')


class ConfirmForm(FlaskForm):
    submit = SubmitField('Send')
