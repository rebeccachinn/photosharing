from flask import render_template, request, Blueprint, url_for, redirect
from flaskblog.models import User, Message
from flask_login import current_user, login_required
from flaskblog import db




main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
@login_required
def home():
    if current_user.is_client:
    	return redirect(url_for('clients.client_progress', username=current_user.username ))
    else:
    	return redirect(url_for('coaches.feed'))