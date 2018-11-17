from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

#socket
from flask_socketio import SocketIO
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail
import os 

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

#socket
socketio=SocketIO(app)

#passes in function name of the route to login
login_manager.login_view='users.login'
login_manager.login_message_category='info'

app.config['MAIL_SERVER']= 'smtp.googlemail.com'
app.config['MAIL_PORT']= 587
app.config['MAIL_USE_TLS']=True
# app.config['MAIL_USERNAME']=os.environ.get('email_user')
app.config['MAIL_USERNAME']='rc3003@barnard.edu'
app.config['MAIL_PASSWORD']='fixyourP0STURE*'

mail=Mail(app)

from flaskblog.users.routes import users
from flaskblog.main.routes import main
from flaskblog.messages.routes import messages
from flaskblog.coaches.routes import coaches
from flaskblog.clients.routes import clients
from flaskblog.errors.handlers import errors

app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(messages)
app.register_blueprint(coaches)
app.register_blueprint(clients)
app.register_blueprint(errors)

#

from flaskblog.models import User, Message, Image

admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Message, db.session))
admin.add_view(ModelView(Image, db.session))

