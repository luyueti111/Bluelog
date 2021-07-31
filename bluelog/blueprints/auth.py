import string

from flask import Blueprint, render_template, url_for, redirect, session
from flask_login import current_user, login_user, login_required, logout_user

from bluelog.models import User
from bluelog.forms import LoginForm, SendEmailForm, RegisterForm, ConfirmForm

from bluelog.extensions import mail, db
from bluelog.functions import redirect_back

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/testCurrent')
def testCurrent():
    return render_template('auth/testCurrent.html')


@auth_bp.route('login', methods=['GET', 'POST'])
def login():
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

    return render_template('auth/login.html', form=loginForm)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect_back()


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    registerForm = RegisterForm()
    confirmForm = ConfirmForm()

    if registerForm.validate_on_submit():
        email = registerForm.emailAddress.data
        user = User(email=email, password=registerForm.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('auth/testRegister.html', registerForm=registerForm, confirmForm=confirmForm)


