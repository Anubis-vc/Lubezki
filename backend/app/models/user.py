from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime


# Main database model representing complete user record
class User(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    username: str
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime
    updated_at: datetime
    last_login: datetime | None = None


# Request models - what clients send to the API
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None


class UserPasswordUpdate(BaseModel):
    current_password: str
    new_password: str


class UserDelete(BaseModel):
    # Require password confirmation for deletion
    password: str


# Response models - what clients receive from the API
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login: datetime | None = None


# model for login response with token
class UserLoginResponse(BaseModel):
    user: UserResponse
    access_token: str
    token_type: str = "bearer"


# detailed user response ideas
class UserProfileResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login: datetime | None = None
