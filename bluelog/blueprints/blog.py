from datetime import datetime

from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user
from sqlalchemy import and_, or_
from jieba import lcut_for_search


from bluelog import db
from bluelog.extensions import fake
from bluelog.forms import PostForm, ReplyForm, SearchForm
from bluelog.models import Post, Comment, User, FakeName

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/', methods=['GET', 'POST'])
def hello():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))
    return render_template('blog/hello.html')


@blog_bp.route('/index', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            name = form.name.data
            title = form.title.data
            body = form.body.data
            post = Post(body=body, title=title, name=name)
            db.session.add(post)
            user = User.query.filter_by(id=current_user.id).first()
            post.user = user
            fakeName = FakeName(post_id=post.id, user_id=user.id, name=name)
            db.session.add(fakeName)
            db.session.commit()
            return redirect(url_for('blog.index'))
        else:
            flash('Please Login to Post Message')

    form.name.data = fake.name()
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('blog/index.html',
                           form=form,
                           posts=posts)


@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def replyPage(post_id):
    replyForm = ReplyForm()
    fakesNames = FakeName.query.filter_by(post_id=post_id).all()
    replyForm.toName.choices = [(fakeName.name, fakeName.name) for fakeName in fakesNames]
    post = Post.query.get(post_id)
    post.clickNum += 1
    comments = post.comments
    db.session.commit()
    if replyForm.validate_on_submit():
        if current_user.is_authenticated:
            name = replyForm.name.data
            body = replyForm.body.data
            toName = replyForm.toName.data
            if toName == post.name:
                toName = None
            comment = Comment(body=body, name=name, replyTo=toName, commentFloor=post.commentNum + 1)
            user = User.query.get(current_user.id)
            post.timestamp = datetime.now()
            comment.user = user
            comment.post = post
            fakeName = FakeName.query.filter(and_(FakeName.post_id == post_id, FakeName.user_id == user.id)).first()
            post.commentNum += 1
            if not fakeName:
                fn = FakeName(post_id=post.id, user_id=user.id, name=name)
                db.session.add(fn)
            db.session.commit()
            return redirect(url_for('blog.replyPage', post_id=post_id))
        else:
            flash('Please Login to Reply Post')
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        fakeName = FakeName.query.filter(and_(FakeName.post_id == post_id, FakeName.user_id == user.id)).first()
        if fakeName:
            replyForm.name.data = fakeName.name
        else:
            replyForm.name.data = fake.name()
    else:
        replyForm.name.data = fake.name()
    return render_template('blog/reply.html',
                           comments=comments,
                           form=replyForm,
                           post=post)


@blog_bp.route('/search', methods=['GET', 'POST'])
def searchMessage():
    searchForm = SearchForm()
    if searchForm.validate_on_submit():
        searchRule = searchForm.body.data
        searchList = lcut_for_search(searchRule)
        rules = ""
        for rule in searchList:
            rules += rule + "|"
        rules = rules.rstrip("|")
        searchedPost = Post.query.filter(or_(Post.body.op('regexp')(rules),
                                             Post.title.op('regexp')(rules)))
        searchComment = Comment.query.filter(Comment.body.op('regexp')(rules))


        return render_template('blog/search.html',
                               searchPostNumber=searchedPost.count(),
                               searchCommentNumber=searchComment.count(),
                               posts=searchedPost,
                               comments=searchComment)
