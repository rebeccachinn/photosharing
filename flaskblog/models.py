from flaskblog import db, login_manager, app
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 
from flask_login import UserMixin
import json

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin, Base):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file=db.Column(db.String(20), nullable=False, default='default.jpg')
	password = db.Column(db.String(60), nullable=False)
	messages=db.relationship('Message',backref='author',lazy=True)


	is_client=db.Column(db.Boolean, default=False)

	#is coach
	clients = db.relationship("User", backref=db.backref('coach', remote_side=[id]))
	answers=db.relationship('Answer',backref='coach',lazy=True)


	#is client 
	coach_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	images=db.relationship('Image', backref='client',lazy=True)
	questions=db.relationship('Question',backref='client',lazy=True)


	def get_reset_token(self, expires_sec=1800):
		#1800 seconds = 30 mins
		s = Serializer(app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def verify_reset_token(token):
		s= Serializer(app.config['SECRET_KEY'])
		try:
			user_id= s.loads(token)['user_id']
		except:
			return None 
		return User.query.get(user_id)

	def __repr__(self):
		return f"User('{self.username}','{self.email}','{self.image_file}')"

class Message(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	messageContent=db.Column(db.String(500), nullable=False)
	user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	#client room id is equivalent to id of client recipient. works because each client will
	#only ever have one room --> chatting with coach
	client_room_id=db.Column(db.Integer, nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	image_file=db.Column(db.String(20), nullable=False, default='default.jpg')

	def __repr__(self):
		return f"Message('{self.messageContent}','{self.date_posted}')"

class Image(db.Model): 
	id = db.Column(db.Integer, primary_key=True)
	client_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	image_file=db.Column(db.String(20), nullable=False, default='default.jpg')

	#filled in by coach
	comment=db.Column(db.String(500), nullable=True)
	rating=db.Column(db.Integer, nullable=True)

	def __repr__(self):
		return f"Image('{self.client_id}','{self.date_posted}')"

class Question(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text=db.Column(db.String(500), nullable=False)

	client_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	answer = db.relationship("Answer", uselist=False, back_populates="question")
	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	def __repr__(self):
		return f"Message('{self.question_text}','{self.date_created}')"

class Answer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	text=db.Column(db.String(500), nullable=False)

	coach_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
	question = db.relationship("Question", back_populates="answer")

	date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

	def __repr__(self):
		return f"Message('{self.question_text}','{self.date_created}')"