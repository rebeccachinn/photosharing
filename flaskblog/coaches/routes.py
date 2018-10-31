from flask import render_template, request, Blueprint, flash, redirect, url_for
from flaskblog.models import User, Message, Image
from flaskblog.coaches.forms import RateImageForm
from flask_login import current_user, login_required
from flaskblog import db
from sqlalchemy import or_, and_


coaches = Blueprint('coaches', __name__)

@coaches.route("/clients")
@login_required
def view_clients():
	clients=User.query.filter_by(coach=current_user)
	return render_template('clients.html', clients=clients)

@coaches.route('/feed', methods=['GET', 'POST'])
@login_required
def feed():
	clients=User.query.filter_by(coach=current_user)
	images=db.session.query(Image).filter(or_(Image.rating==None, Image.rating==0))

	#hacky way to do query, only getting relevant clients in feed
	n=[]
	for image in images:
		if image.client in clients:
			form = RateImageForm()
			if form.validate_on_submit():
				comment = form.comment.data
				rating = form.rating.data
				image.comment=comment
				image.rating=rating
				db.session.commit()
				# flash('photo has updated!', 'success')
				return redirect(url_for('coaches.feed'))
			t={}
			t['form']=form
			t['image']=image
			n.append(t)

	return render_template('feed.html',tuples=n)