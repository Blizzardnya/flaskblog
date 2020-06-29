from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email
from flaskblog.users.services import create_user_service, update_user_service, reset_user_password_service

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        create_user_service(form.username.data, form.email.data, form.password.data)
        flash('Your account has been created!', 'success')
        return redirect(url_for('users.login'))

    return render_template('account/register.html', title='Registration', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')

    return render_template('account/login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        picture_file = None

        if form.picture.data:
            picture_file = save_picture(form.picture.data)

        update_user_service(current_user, form.username.data, form.email.data, picture_file)
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account/account.html', title='Account',
                           image_file=image_file, form=form)


@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user) \
        .order_by(Post.date_posted.desc()) \
        .paginate(page=page, per_page=5)

    return render_template('post/user_posts.html', posts=posts, user=user)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instruction to reset your password.')
        return redirect(url_for('users.login'))

    return render_template('account/reset_request.html', title='Reset password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)

    if user is None:
        flash('That is an invalid or expiried token', 'warning')
        return redirect(url_for('users.reset_request'))

    form = ResetPasswordForm()

    if form.validate_on_submit():
        reset_user_password_service(user, form.password.data)
        flash('Your password has been updated!', 'success')
        return redirect(url_for('users.login'))

    return render_template('account/reset_token.html', title='Reset password', form=form)
