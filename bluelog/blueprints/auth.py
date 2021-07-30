from flask import Blueprint, render_template, url_for, redirect
from flask_login import current_user, login_user

from bluelog.models import User
from bluelog.forms import LoginForm, SendEmailForm

from bluelog.extensions import mail
from flask_mail import Mail, Message

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/test')
def login():
    return "this is auth's test"


@auth_bp.route('/testCurrent')
def testCurrent():
    return render_template('auth/testCurrent.html')


@auth_bp.route('testLogin', methods=['GET', 'POST'])
def testLogin():
    if current_user.is_authenticated:
        return redirect(url_for('auth.testCurrent'))

    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        email = loginForm.email.data
        password = loginForm.password.data
        remember = loginForm.remember.data
        user = User.query.filter(email == email).first()
        if user:
            if email == user.email and password == user.password:
                login_user(user, remember)
                return render_template('auth/testCurrent.html')

    return render_template('auth/testLogin.html', form=loginForm)


def send_mail(subject, to, body):
    message = Message(subject, recipients=[to], body=body)
    mail.send(message)


@auth_bp.route('/test_email', methods=['GET', 'POST'])
def test_send():
    form = SendEmailForm()
    if form.validate_on_submit():
        email = form.emailAddress.data
        send_mail('test1', email, 'test2')
        return redirect(url_for('auth.testLogin'))
    return render_template('auth/testSend.html', form=form)

