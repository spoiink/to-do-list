from pydantic import BaseModel, Field, field_validator, ConfigDict
from pydantic_core.core_schema import FieldValidationInfo
import re


class UserRegister(BaseModel):
    login: str = Field(min_length=3, max_length=127)
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(
        min_length=8,
        description="Пароль (минимум 8 символов, буквы и цифры)"
    )
    password_approve: str = Field(min_length=8)


    @field_validator("username")
    @classmethod
    def validate_username_chars(cls, value: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_]+$", value):
            raise ValueError("Имя пользователя может содержать только буквы и цифры")
        return value

    # Валидатор для пароля: проверка на наличие букв И чисел
    @field_validator("password")
    @classmethod
    def validate_password_complexity(cls, value: str) -> str:
        # Проверяем наличие хотя бы одной буквы
        if not re.search(r"[a-zA-Zа-яА-ЯёЁ]", value):
            raise ValueError("Пароль должен содержать хотя бы одну букву")
        # Проверяем наличие хотя бы одной цифры
        if not re.search(r"\d", value):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
            
        return value

    @field_validator('password_approve')
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Пароль не совпадает')
        return v


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    login: str
    username: str


class LoginRequest(BaseModel):
    login: str = Field(min_length=3, max_length=127)
    password: str = Field(min_length=8)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"   # клиент будет передавать токен в заголовке Authorization: Bearer <токен>


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshSchema(BaseModel):
    refresh_token: str




class UserProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    login: str
    username: str
    bio: str | None = None
    avatar_url: str | None = None