import string

from flask import Blueprint, render_template, url_for, redirect, session
from flask_login import current_user, login_user

from bluelog.models import User
from bluelog.forms import LoginForm, SendEmailForm, RegisterForm, ConfirmForm

from bluelog.extensions import mail, db
from flask_mail import Mail, Message

import random

auth_bp = Blueprint('auth', __name__)


def geneText():
    return ''.join(random.sample(string.ascii_letters + string.digits, 4))


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


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    registerForm = RegisterForm()
    confirmForm = ConfirmForm()

    if registerForm.validate_on_submit():
        email = registerForm.emailAddress.data
        # print('fuck', session[email])
        # if registerForm.verificationCode.data == session[email]:
        user = User(email=email, password=registerForm.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.testLogin'))

    return render_template('auth/testRegister.html', registerForm=registerForm, confirmForm=confirmForm)

# @auth_bp.route('/sent/<string:email>', methods=['GET', 'POST'])
# def sent(email):
#     confirmForm = ConfirmForm()
#     if confirmForm.validate_on_submit():
#         c = geneText()
#         session[email] = c
#         print('shit', session[email])
#     return redirect(url_for('auth.register'))
