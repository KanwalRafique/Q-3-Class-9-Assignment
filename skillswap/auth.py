# auth.py
from database import session, UserDB

def register_user(name, email, password):
    user = UserDB(name=name, email=email, password=password)
    session.add(user)
    session.commit()
    return user

def login_user(email, password):
    return session.query(UserDB).filter_by(email=email, password=password).first()
