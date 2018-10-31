from flaskblog import db
from flaskblog.models import User, Message, Image

# db.create_all()

cl =User.query.filter_by(username="colin")
msg = Message.query.filter_by(author=cl)
# # user_2 = User(username="rebs2", email="colin.duo.cook@gmail.com", password="password")

# db.session.add(image1)
# db.session.add(user_2)

# post_1 = Post(title="blog1", content="first post content!", user_id=1)
# post_2 = Post(title="blog2", content="first post content!", user_id=1)
# db.session.add(post_1)
# db.session.add(post_2)

# db.session.commit()

# ms = Message.query.all()
# for m in ms:
# 	db.session.delete(m)

# db.session.commit()


# user = User.query.filter_by(username='rebs').first()
# user.image_file="default.jpg"
# db.session.add(user)
# db.session.commit()


# from flask_bcrypt import Bcrypt
# bcrypt = Bcrypt()

# hashed_pw = bcrypt.generate_password_hash('testing')
# print(bcrypt.check_password_hash(hashed_pw,'testing'))
# print(bcrypt.check_password_hash(hashed_pw,'blah'))