from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user
from sqlalchemy import and_

from bluelog import User, db
from bluelog.models import Post, Comment, UnreadMessage

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/test')
def login():
    return "this is admin's test"


@admin_bp.route('/index')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    else:
        recentPosts = Post.query.filter(Post.user_id == current_user.id).order_by(Post.postTime.desc()).limit(5)
        recentComments = Comment.query.filter(Comment.user_id == current_user.id) \
            .order_by(Comment.timestamp.desc()).limit(5)
        return render_template('admin/index.html', posts=recentPosts, comments=recentComments)


@admin_bp.route('/posts')
def managePosts():
    if not current_user.is_authenticated:
        return redirect(url_for('blog.index'))
    else:
        allPosts = Post.query.filter(Post.user_id == current_user.id).order_by(Post.postTime.desc()).all()
        return render_template('admin/managePosts.html', posts=allPosts)


@admin_bp.route('/comments')
def manageComments():
    if not current_user.is_authenticated:
        return redirect(url_for('blog.index'))
    else:
        allComments = Comment.query.filter(Comment.user_id == current_user.id).order_by(Comment.timestamp.desc()).all()
        return render_template('admin/manageComments.html', comments=allComments)


@admin_bp.route('/deletePost/<int:post_id>')
def deletePost(post_id):
    post = Post.query.get(post_id)
    if post:
        posterId = post.user_id
        if current_user.is_authenticated and current_user.id == posterId:
            for comment in post.comments:
                unreadMessages = UnreadMessage.query.filter(UnreadMessage.comment_id == comment.id).all()
                for unreadMessage in unreadMessages:
                    db.session.delete(unreadMessage)
                db.session.delete(comment)
            db.session.delete(post)
            db.session.commit()
            return redirect(url_for('admin.managePosts'))
        else:
            return redirect(url_for('blog.index'))
    else:
        return redirect(url_for('blog.index'))


@admin_bp.route('/deleteComment/<int:comment_id>')
def deleteComment(comment_id):
    comment = Comment.query.get(comment_id)
    if comment:
        commenterId = comment.user_id
        if current_user.is_authenticated and current_user.id == commenterId:
            unreadMessages = UnreadMessage.query.filter(UnreadMessage.comment_id == comment.id).all()
            for unreadMessage in unreadMessages:
                db.session.delete(unreadMessage)
            db.session.delete(comment)
            db.session.commit()
            return redirect(url_for('admin.manageComments'))
    return redirect(url_for('blog.index'))


@admin_bp.route('/unreadMessages')
def manageUnreadMessages():
    if not current_user.is_authenticated:
        return redirect(url_for('blog.index'))
    else:
        unreadMessages = UnreadMessage.query.filter(and_(UnreadMessage.user_id == current_user.id,
                                                         UnreadMessage.haveRead == 0)).all()
        readMessages = UnreadMessage.query.filter(and_(UnreadMessage.user_id == current_user.id,
                                                       UnreadMessage.haveRead == 1)).all()
        unreadMessages = Comment.query.filter(Comment.id.in_([unreadMessage.comment_id for unreadMessage in unreadMessages])).order_by(Comment.timestamp.desc()).all()
        readMessages = Comment.query.filter(Comment.id.in_([readMessage.comment_id for readMessage in readMessages])).order_by(Comment.timestamp.desc()).all()
        return render_template('admin/manageUnreadMessage.html', comments=unreadMessages, readComments=readMessages)


@admin_bp.route('/readAll')
def readAll():
    if not current_user.is_authenticated:
        return redirect(url_for('blog.index'))
    else:
        unreadMessages = UnreadMessage.query.filter(and_(UnreadMessage.user_id == current_user.id,
                                                         UnreadMessage.haveRead == 0)).all()
        for unreadMessage in unreadMessages:
            unreadMessage.haveRead = True
        db.session.commit()
        return redirect(url_for('admin.manageUnreadMessages'))


