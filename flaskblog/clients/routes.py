from flask import render_template, request, Blueprint, url_for, flash, redirect, jsonify
from flaskblog.models import User, Message, Image
from flask_login import current_user, login_required
from flaskblog import db
# from flask_socketio import send
from flaskblog.clients.utils import save_image
from flaskblog.clients.forms import UploadImageForm
from sqlalchemy import or_



clients = Blueprint('clients', __name__)


@clients.route("/user/<string:username>")
def client_progress(username):
    user = User.query.filter_by(username=username).first_or_404()
    imgs=Image.query.filter_by(client=user)
    
    #gets avgs of image ratings

    s=0
    n=0
    for img in imgs:
    	if img.rating:
    		s+=img.rating
    	n+=1

    if n==0:
    	avg=0
    else:
    	avg = float(s)/float(n)


    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    return render_template('client_progress.html', title='User', image_file=image_file, user=user, avg=avg)

@clients.route('/get_progress_data')
def get_progress_data():
    username=request.args.get('userID')
    user = User.query.filter_by(id=username).first_or_404()
    imgs=Image.query.filter_by(client=user)
    results={'dates':[], 'ratings':[] }
    for image in imgs:
        if image.rating:
            results['dates'].append(image.date_posted.strftime('%m/%d'))
            results['ratings'].append(image.rating)


    return jsonify(results)

@clients.route("/user/log/<string:username>")
def client_log(username):
    client = User.query.filter_by(username=username).first_or_404()
    imgs=Image.query.filter_by(client=client)
    return render_template('client_log.html', title='Client Log', images=imgs, client=client)

@clients.route("/user/image/<string:username>/<string:image_file>")
def image(username, image_file):
	client=User.query.filter_by(username=username).first_or_404()
	image=Image.query.filter_by(image_file=image_file).first_or_404()
	return render_template('image.html', image=image, client=client)

@clients.route('/new_photo',  methods=['GET', 'POST'])
def new_photo():
    form = UploadImageForm()
    if form.validate_on_submit():
        picture_file = save_image(form.picture.data)
        image = Image(client=current_user, image_file=picture_file)
        db.session.add(image)
        db.session.commit()
        flash('photo has been added!', 'success')
        return redirect(url_for('clients.client_progress', username=current_user.username))
    return render_template('new_photo.html', form=form)