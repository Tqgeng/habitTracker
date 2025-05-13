#  валидация данных для запросов и ответов

from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class TokenInfo(BaseModel):
    access_token: str
    token_type: str

class UserResponce(BaseModel):
    id: int
    email: EmailStr

class UserShema(BaseModel):
    model_config = ConfigDict(strict=True)

    email: EmailStr
    password: bytes
    active: bool = True

class HabitCreate(BaseModel):
    title: str
    description: Optional[str] = None
    frequency: str


class HabitOut(BaseModel):
    id: int
    title: str
    description: Optional[str] 
    frequency: str
    start_date: datetime
    # checked_today: bool

    class Config:
        orm_mode = True

class HabitUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    frequency: Optional[str] = None

class HbitCheckinOut(BaseModel):
    id: int
    habit_id: int
    checkin_date: date

    class Config:
        orm_mode = True

    

