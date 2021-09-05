from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user

from bluelog import User, db
from bluelog.models import Post, Comment

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/test')
def login():
    return "this is admin's test"


@admin_bp.route('/index')
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('blog.index'))
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
        allPosts = Post.query.filter(Post.user_id == current_user.id).all()
        return render_template('admin/managePosts.html', posts=allPosts)


@admin_bp.route('/comments')
def manageComments():
    if not current_user.is_authenticated:
        return redirect(url_for('blog.index'))
    else:
        allComments = Comment.query.filter(Comment.user_id == current_user.id)
        return render_template('admin/manageComments.html', comments=allComments)


@admin_bp.route('/deletePost/<int:post_id>')
def deletePost(post_id):
    post = Post.query.get(post_id)
    if post:
        posterId = post.user_id
        if current_user.is_authenticated and current_user.id == posterId:
            db.session.delete(post)
            for comment in post.comments:
                db.session.delete(comment)
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
            db.session.delete(comment)
            db.session.commit()
            return redirect(url_for('admin.manageComments'))

    return redirect(url_for('blog.index'))





