from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from bluelog import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 100), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class RegisterForm(FlaskForm):
    emailAddress = StringField('Email', validators=[DataRequired(), Length(1, 100), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 100), EqualTo('password2')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    # verificationCode = StringField('verificationCode', validators=[DataRequired(), Length(1, 100)])
    submit = SubmitField('Register')

    def validate_emailAddress(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('The email is already in use')


class PostForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired(), Length(1, 20)])
    body = TextAreaField('Message', validators=[DataRequired(), Length(1, 200)])
    submit = SubmitField()


class ReplyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    body = TextAreaField('Message', validators=[DataRequired(), Length(1, 200)])
    submit = SubmitField()
