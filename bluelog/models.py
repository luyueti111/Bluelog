from bluelog.extensions import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(128))
    isAdmin = db.Column(db.Boolean, default=False)
    posts = db.relationship('Post', back_populates='user')
    comments = db.relationship('Comment', back_populates='user')


# class Category(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(30), unique=True)
#     posts = db.relationship('Post', back_populates='category')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    name = db.Column(db.String(60))
    clickNum = db.Column(db.Integer, default=0)
    commentNum = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    # category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    # category = db.relationship('Category', back_populates='posts')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', cascade='all,delete-orphan')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    body = db.Column(db.Text)
    replyTo = db.Column(db.String(30))
    from_admin = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates='comments')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='comments')


class FakeName(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    name = db.Column(db.String)
