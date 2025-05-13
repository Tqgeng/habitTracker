# crud для привычек

from datetime import date
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db import models, shemas, crud
from .auth_jwt import  get_db, get_current_active_auth_user

router = APIRouter(prefix='/habits', tags=['Habits'])


@router.get('/', response_model=List[shemas.HabitOut], summary='Получить все привычки')
def get_user_habits(current_user: shemas.UserShema = Depends(get_current_active_auth_user),
                    db: Session = Depends(get_db)):
    return crud.get_habits_by_user(db, user_id = current_user.id)


@router.get('/{id}', response_model=shemas.HabitOut, summary='Получить конкретную привычку')
def get_user_habit(id: int, db: Session = Depends(get_db), current_user: shemas.UserShema = Depends(get_current_active_auth_user)):
    habit = crud.get_habit_by_id(db, id)
    if not habit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='not found habit'
        )
    if habit.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='not have permission'
        )
    return habit

@router.post('/', response_model=shemas.HabitOut)
def create_habit(habit: shemas.HabitCreate,
                 current_user: shemas.UserShema = Depends(get_current_active_auth_user),
                 db: Session = Depends(get_db)):
    return crud.create_habits(db, habit, user_id=current_user.id)

@router.put('/{id}', response_model=shemas.HabitOut)
def update_user_habit(
    id: int,
    habit_data: shemas.HabitUpdate,
    db: Session = Depends(get_db),
    current_user: shemas.UserShema = Depends(get_current_active_auth_user)
):
    updated = crud.update_habits(db, habit_data, id, current_user.id)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='habits not found'
        )
    return updated
    
@router.delete('/{id}')
def delete_user_habit(
    id: int,
    current_user: shemas.UserShema = Depends(get_current_active_auth_user),
    db: Session = Depends(get_db)
):
    deleted = crud.delete_habit(db, id, current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='habits not found'
        )
    return {'message': 'habit deleted'}

@router.post('/{id}/checkin', response_model=shemas.HbitCheckinOut)
def chekin_habit(
    id: int,
    current_user: shemas.UserShema = Depends(get_current_active_auth_user),
    db: Session = Depends(get_db)
):
    checkin = crud.chekin_today(db, id, current_user.id)
    if not checkin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='habits not found'
        )
    return checkin
    