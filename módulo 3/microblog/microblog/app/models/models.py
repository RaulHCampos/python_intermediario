from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    foto = db.Column(db.String(256))
    bio = db.Column(db.String(500))

    # relacionamento com Post: user.posts retorna todos os posts do usuário
    posts = db.relationship('Post', back_populates='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(280), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # relacionamento com User: post.author retorna o usuário autor do post
    author = db.relationship('User', back_populates='posts')

    def __repr__(self):
        return f'<Post {self.body[:20]}>'


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
