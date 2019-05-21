import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail


def save_picture(form_pictire):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pictire.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    outpup_size = (125, 125)
    i = Image.open(form_pictire)
    i.thumbnail(outpup_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = """
    To reset your password visit the following link:
    {0}

    If you did not make this request ignore it.
    """.format(url_for('users.reset_token', token=token, _external=True))
    mail.send(msg)
