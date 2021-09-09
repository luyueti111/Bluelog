import os

import click
from flask_login import current_user
from sqlalchemy.sql.elements import and_

from bluelog.forms import SearchForm
from bluelog.models import User, UnreadMessage
from bluelog.settings import config
from flask import Flask, render_template
from bluelog.extensions import bootstrap, db, moment, ckeditor, mail, login_manager
from bluelog.blueprints.auth import auth_bp
from bluelog.blueprints.admin import admin_bp
from bluelog.blueprints.blog import blog_bp


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('bluelog')
    app.config.from_object(config[config_name])

    register_logging(app)  # 注册日志处理器
    register_extensions(app)  # 注册扩展(拓展初始化)
    register_blueprints(app)  # 注册蓝本
    register_commands(app)  # 注册自定义shell命令
    register_errors(app)  # 注册错误处理函数
    register_shell_context(app)  # 注册shell上下文处理函数
    register_template_context(app)  # 注册模版上下文处理函数

    return app


def register_logging(app):
    pass


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_template_context(app):
    @app.context_processor
    def injectSearchForm():
        searchForm = SearchForm()
        return dict(searchForm=searchForm)

    @app.context_processor
    def injectUnreadMessage():
        if current_user.is_authenticated:
            user = User.query.get(current_user.id)
            unreadMessageNum = UnreadMessage.query.filter(and_(UnreadMessage.user_id == user.id,
                                                               UnreadMessage.haveRead == 0)).count()
            return dict(unreadMessageNum=unreadMessageNum)
        else:
            return dict(unreadMessageNum=0)


def register_errors(app):
    pass


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        admin0 = User(email='769163832@qq.com', password='luyueti1', isAdmin=True)
        admin1 = User(email='123456@qq.com', password='luyueti1', isAdmin=True)
        db.session.add(admin0)
        db.session.add(admin1)
        db.session.commit()
        click.echo('Done!')
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--email', prompt=True, help='The username used to login')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login')
    def addAdmin(email, password):
        click.echo('Initializing the database...')
        click.echo('Creating the temporary administrator account...')
        admin = User(email=email, password=password, isAdmin=True)
        db.session.add(admin)
        db.session.commit()
        click.echo('Done!')
