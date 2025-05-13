#  модели 

from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import date, datetime

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    active = Column(Boolean, default=True)

    habits = relationship('Habit', back_populates='owner')


class Habit(Base):
    __tablename__ = 'habits'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    frequency = Column(String, nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship('User', back_populates='habits')
    chekins = relationship('HabitCheckin', back_populates='habit', cascade='all, delete')

class HabitCheckin(Base):
    __tablename__ = 'habit_checkins'

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey('habits.id'))
    checkin_date = Column(Date, default=date.today)

    habit = relationship('Habit', back_populates='chekins')

