# database.py
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import datetime

Base = declarative_base()
engine = create_engine("sqlite:///skillswap.db")
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

class UserDB(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String, default="learner")
    skills = relationship("SkillDB", back_populates="mentor")

class SkillDB(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    mentor_id = Column(Integer, ForeignKey("users.id"))
    mentor = relationship("UserDB", back_populates="skills")

class BookingDB(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    mentor_id = Column(Integer, ForeignKey("users.id"))
    learner_id = Column(Integer, ForeignKey("users.id"))
    time_slot = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="pending")

class PaymentDB(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("bookings.id"))
    amount = Column(Float, default=10.0)
    platform_fee = Column(Float, default=1.0)
    status = Column(String, default="unpaid")

Base.metadata.create_all(bind=engine)
