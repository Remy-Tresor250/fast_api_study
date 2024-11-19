from pydantic import BaseModel
from datetime import datetime

class VisitRequestBase(BaseModel):
    visit_date: datetime
    visit_time_from: datetime
    visit_time_to: datetime
    organization_name: str

class VisitRequestCreate(VisitRequestBase):
    pass

class VisitRequest(VisitRequestBase):
    id: int
    status: str

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str
    role: str

class User(UserBase):
    id: int
    role: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str
