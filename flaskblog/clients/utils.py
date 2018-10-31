import os, stat
import secrets
from PIL import Image
from flask import url_for
from flask_login import current_user
from flask_mail import Message
from flaskblog import app, mail

def save_image(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    folder = os.path.join(app.root_path,  'static', current_user.username)
    picture_path = os.path.join(folder, picture_fn)
    if not os.path.exists(folder):
        os.makedirs(folder)
    output_size = (300,300)
    i=Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
