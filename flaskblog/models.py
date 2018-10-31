from flaskblog import db, login_manager, app
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer 
from flask_login import UserMixin

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

	
	coach_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	clients = db.relationship("User", backref=db.backref('coach', remote_side=[id]))

	is_client=db.Column(db.Boolean, default=False)
	images=db.relationship('Image', backref='client',lazy=True)


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