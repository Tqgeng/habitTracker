# маршруты для регистрации, входа (jwt)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .auth_jwt import validate_auth_user, get_current_active_auth_user, get_current_token_payload, get_db
from app.db.database import SessionLocal
from app.db.shemas import UserCreate, TokenInfo, UserShema
from app.db import crud
from app.core import utils as auth_utils

router = APIRouter(prefix='/jwt', tags=['JWT'])

@router.post('/register', response_model=UserCreate)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    ex_user = crud.get_user_by_email(db, user_data.email)
    if ex_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='email already taken'
        )
    
    hashed_password = auth_utils.hash_password(user_data.password)

    new_user = crud.create_user(db, user_data.email, hashed_password)

    return UserCreate(
        email=new_user.email,
        password='hidden'
    )

@router.put('/register/status', response_model=UserCreate)
def update_stats_user(user_data: UserCreate, db: Session = Depends(get_db)):
    ex_user = crud.get_user_by_email(db, user_data.email)
    if not ex_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='email not found'
        )
    
    hashed_password = auth_utils.hash_password(user_data.password)

    new_user = crud.update_text_user(db, hashed_password, user_data.email)

    return UserCreate(
        email=new_user.email,
        password='hidden'
    )

@router.post('/login', response_model=TokenInfo)
def auth_user_issue_jwt(
    user: UserShema = Depends(validate_auth_user)
):
    jwt_payload = {
        'email': user.email
    }

    access_token = auth_utils.encode_jwt(jwt_payload)
    
    return TokenInfo(
        access_token=access_token,
        token_type='Bearer'
    )

@router.get('/users/me')
def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserShema = Depends(get_current_active_auth_user)
):
    iat = payload.get('iat')
    return {
        'email' : user.email,
        'iat' : iat
    }

