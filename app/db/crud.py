#  функции для работы с бд

from datetime import date
from sqlalchemy.orm import Session
from .shemas import HabitCreate, HabitUpdate
from .models import User, Habit, HabitCheckin

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, hashed_password: str):
    user = User(
        email = email, 
        password = hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_text_user(db: Session, hashed_password: str, email: str = None):
    db_user = db.query(User).filter(User.email == email).first()
    db_user.email = email

    db_user.password = hashed_password

    db.commit()
    db.refresh(db_user)

    return db_user

def get_habits_by_user(db: Session, user_id: int):
    return db.query(Habit).filter(Habit.owner_id == user_id).all()

def get_habit_by_id(db: Session, habit_id: int):
    return db.query(Habit).filter(Habit.id == habit_id).first()

def create_habits(db: Session, habit: HabitCreate, user_id: int):
    db_habit = Habit(
        title = habit.title,
        description = habit.description,
        frequency = habit.frequency,
        owner_id = user_id)
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit

def update_habits(
        db: Session,
        habit: HabitUpdate,
        habit_id: int,
        user_id: int
):
    db_habit = db.query(Habit).filter(Habit.id == habit_id, Habit.owner_id == user_id).first()
    if not db_habit:
        return None
    
    db_habit.title = habit.title
    db_habit.description = habit.description
    db_habit.frequency = habit.frequency

    db.commit()
    db.refresh(db_habit)
    return db_habit

def delete_habit(
        db: Session,
        habit_id: int,
        user_id: int
):
    db_habit = db.query(Habit).filter(Habit.id == habit_id, Habit.owner_id == user_id).first()
    if not db_habit:
        return False
    
    db.delete(db_habit)
    db.commit()
    return db_habit

def chekin_today(
        db: Session, 
        habit_id: int,
        user_id: int
):
    db_habit = db.query(Habit).filter(Habit.id == habit_id, Habit.owner_id == user_id).first()
    if not db_habit:
        return False
    
    existing = db.query(HabitCheckin).filter_by(habit_id=habit_id, checkin_date=date.today()).first()
    if existing:
        return existing
    
    checkin = HabitCheckin(habit_id=habit_id)
    db.add(checkin)
    db.commit()
    db.refresh(checkin)
    return checkin