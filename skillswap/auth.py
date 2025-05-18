# auth.py
from database import session, UserDB

def register_user(name, email, password):
    try:
        user = UserDB(name=name, email=email, password=password, role='learner')
        session.add(user)
        session.commit()
        return user
    except Exception as e:
        session.rollback()
        raise e

def login_user(email, password):
    try:
        user = session.query(UserDB).filter_by(email=email, password=password).first()
        return user
    except Exception as e:
        session.rollback()
        raise e
