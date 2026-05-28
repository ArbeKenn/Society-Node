from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator
import re
import phonenumbers
from app.posts.schemas import PostResponseSchema

class UserSchema(BaseModel):
    username : str
    password: str
    email: EmailStr | None
    phone: str
    age: int
    gender: str

    @field_validator('password')
    def validate_password(cls, v):
        errors = []
        if len(v) < 8:
            errors.append('minimum password length is 8'
            )
        if not re.search(r'[A-Z]', v):
            errors.append('A capital letter is needed'
            )
        if not re.search(r'[0-9]', v):
            errors.append('Need a number'
            )
        if errors:
            raise HTTPException(
                status_code=422,
                detail=errors
            )
        return v

    @field_validator('phone')
    def validate_phone(cls, v):
        try:
            phone = phonenumbers.parse(v)
            if not phonenumbers.is_valid_number(phone):
                raise ValueError('wrong number')
        except Exception:
            raise ValueError('wrong format number')
        return v


class UserLoginSchema(BaseModel):
    username: str
    password: str

class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: str | None
    phone: str
    age: int
    gender: str
    coin: float
    followers: int
    following: int
    posts: list[PostResponseSchema] = []

class UserUpdateSchema(BaseModel):
    username: str
    password: int
    email: str | None
    phone: str
    age: int
    gender: str

    @field_validator('password')
    def validate_password(cls, v):
        errors = []

        if len(v) < 8:
            errors.append('minimum password length is 8')
        if not re.search(r'[A-Z]', v):
            errors.append('A capital letter is needed')
        if not re.search(r'[0-9]', v):
            errors.append('Need a number')

        if errors:
            raise HTTPException(
                status_code=422,
                detail=errors
            )
        return v

    @field_validator('phone')
    def validate_phone(cls, v):
        try:
            phone = phonenumbers.parse(v)
            if not phonenumbers.is_valid_number(phone):
                raise ValueError('wrong number')
        except Exception:
            raise ValueError('wrong format number')
        return v

    class Config:
        from_attributes = True


class FollowResponse(BaseModel):
    status: str

class FollowerUserSchema(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class FollowersListSchema(BaseModel):
    followers: list[FollowerUserSchema]
    following: list[FollowerUserSchema]
    followers_count: int
    following_count: int