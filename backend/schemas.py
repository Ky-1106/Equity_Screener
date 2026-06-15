from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    phone_number: Optional[str] = None
    sms_alerts_enabled: bool = False

    class Config:
        from_attributes = True

class UserUpdateProfile(BaseModel):
    phone_number: Optional[str] = None
    sms_alerts_enabled: bool = False

class UserUpdatePassword(BaseModel):
    current_password: str
    new_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class WatchlistItemCreate(BaseModel):
    ticker: str

class WatchlistItemResponse(BaseModel):
    id: int
    user_id: int
    ticker: str

    class Config:
        from_attributes = True
