from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Literal
import re
import phonenumbers
from app.posts.schemas import PostResponseSchema

class UserSchema(BaseModel):
    username : str = Field(max_length=10)
    password: str
    email: EmailStr | None
    phone: str
    age: int = Field(ge=14, le=120)
    gender: Literal["male", "female", "other"]
    #I understand если user send "MALE" будет ошибка. Чтобы этого не было front сделает просто кнопки через <select name="gender">

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

class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: EmailStr | None
    phone: str
    age: int
    gender: str
    coin: float
    followers: int
    following: int
    favorite: int
    posts: list[PostResponseSchema] = []

class UserLoginSchema(BaseModel):
    username: str
    password: str

class LoginResponseSchema(BaseModel):
    token: str

class UserItemResponseSchema(BaseModel):
    id: int
    title: str
    user_id: int
    item_id: int
    quantity: int

class UserUpdateSchema(BaseModel):
    username : str = Field(max_length=10)
    password: str
    email: EmailStr | None
    phone: str
    age: int = Field(ge=14, le=120)
    gender: Literal["male", "female", "other"]
    is_admin: bool

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