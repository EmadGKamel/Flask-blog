import random
from os import path
from blog import app, mail
from flask_mail import Message
from flask import url_for


def save_picture(form_picture):
    random_name = random.randint(0, 9999999999)
    _, f_ext = path.splitext(form_picture.filename)
    picture_fn = str(random_name) + f_ext
    picture_path = path.join(app.root_path, 'static/images', picture_fn)
    form_picture.save(picture_path)
    return picture_fn


def send_reset_email(user):
    token = user.get_token()
    msg = Message(
        subject='Password Reset Request',
        recipients=[user.email],
        sender='host@domain.com',
        body='''Hello {0},\nYou or someone else has requested a new password for your account.
Are you made this request?
If yes, please follow this link:\n{1}'''.format(user.username, url_for('reset_token', token=token, _external=True))
    )
    mail.send(msg)


def send_confirmation_email(user):
    token = user.get_token()
    msg = Message(
        subject='Password Reset Request',
        recipients=[user.email],
        sender='host@domain.com',
        body='''Hello {0},\nYou or someone else has requested a new password for your account.
Are you made this request?
If yes, please follow this link:\n{1}'''.format(user.username, url_for('reset_token', token=token, _external=True))
    )
    mail.send(msg)
