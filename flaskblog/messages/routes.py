from flask import render_template, request, Blueprint
from flaskblog.models import User, Message
from flask_login import current_user, login_required
from flaskblog import socketio, db
from flask_socketio import send
from sqlalchemy import or_

messages = Blueprint('messages', __name__)


@messages.route("/chat")
@login_required
def chat():
	# coach = current_user.coach
	# msgs=db.session.query(Message).filter(or_(Message.author==current_user, Message.author==coach))
	msgs=Message.query.all()
	msgs.reverse()
	return render_template('chat.html', title='Chat', messages=msgs)

@socketio.on('message')
def handleMessage(msg) :
	message = Message(messageContent = msg, author=current_user)
	db.session.add(message)
	db.session.commit()
	print('Message: ' + msg)
	send(msg, broadcast=True)
