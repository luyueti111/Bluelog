from faker import Faker
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_login import LoginManager

bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
ckeditor = CKEditor()
mail = Mail()
login_manager = LoginManager()
fake = Faker(locale='zh_CN')


@login_manager.user_loader
def load_user(user_id):
    from bluelog.models import User
    user = User.query.get(int(user_id))
    return user
