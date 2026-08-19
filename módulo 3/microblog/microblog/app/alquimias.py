from sqlalchemy import select
from app import db
from app.models.models import User, Post


def get_user_by_username(username):
    return db.session.scalar(select(User).where(User.username == username))


def create_user(username, email, password, foto=None, bio=None):
    user = User(username=username, email=email, foto=foto, bio=bio)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user


def create_post(body, user):
    # note que ao alimentar 'author', o user_id é preenchido automaticamente
    post = Post(body=body, author=user)
    db.session.add(post)
    db.session.commit()
    return post


def get_timeline():
    # os 5 posts mais recentes, ordenados por timestamp desc
    stmt = select(Post).order_by(Post.timestamp.desc()).limit(5)
    return db.session.scalars(stmt).all()
