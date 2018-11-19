from flask import render_template, request, Blueprint, jsonify
from flaskblog.models import User, Message
from flask_login import current_user, login_required
from flaskblog import socketio, db
from flask_socketio import send, join_room, leave_room

from sqlalchemy import or_
import json 
import sys

messages = Blueprint('messages', __name__)

user_sessions ={}

@messages.route("/chat/<string:client_room_id>")
@login_required
def chat(client_room_id):
	msgs=Message.query.filter_by(client_room_id=client_room_id).all()

	if current_user.is_client:
		return render_template('chat.html', title='Chat', messages=msgs, client_room_id=client_room_id)
	else:
		return render_template('chat_coach_view.html', title='Chat', messages=msgs, client_room_id=client_room_id)


@socketio.on('message')
def handleMessage(msg, client_room_id):
	message = Message(messageContent = msg, author=current_user, client_room_id=client_room_id)
	db.session.add(message)
	db.session.commit()
	print('Message: ' + msg)

	json_data = {
	    "messageContent": message.messageContent,
	    "author": current_user.username,
	    "date": message.date_posted.strftime('%m/%d, %I:%M%p'),
	}
	send(json_data, broadcast=True)




# @socketio.on('join room')
# def on_join(client_room_id):
#     username = current_user.username
#     room = client_room_id
#     join_room("new room")
#     print(username + ' has entered the room.')

#     json_data = {
# 	    "messageContent": "hi",
# 	    "author": "there",
# 	    "date": "bloop",
# 	}
#     send(json_data, room=room)

# @socketio.on('leave')
# def on_leave(client_room_id):
#     username = current_user.username
#     room = client_room_id
#     leave_room(room)

#     print(username + ' has left the room.')
#     send(username + ' has left the room.', room=room)


@messages.route('/get_latest_message')
def get_latest_message():
    client_room_id=request.args.get('client_room_id')
    message =db.session.query(Message).order_by(Message.id.desc()).first()
    results={'message': message.messageContent}
    return jsonify(results)

@messages.route('/saveQA', methods=['POST', 'GET'])
def saveQA():
    if request.method=='POST':
    	print(request.form['client_room_id'])
    return "this is a return variable"