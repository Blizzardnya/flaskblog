from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required

from flaskblog.models import Post
from flaskblog.posts.forms import PostForm
from flaskblog.posts.services import create_post_service, update_post_service, delete_post_service

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        create_post_service(form.title.data, form.content.data, current_user)
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))

    return render_template('post/create_post.html', title='Create new post',
                           form=form, legend='New Post')


@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post/post.html', title=post.title, post=post)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    form = PostForm()

    if form.validate_on_submit():
        update_post_service(post, form.title.data, form.content.data)
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('post/create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    delete_post_service(post)
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
