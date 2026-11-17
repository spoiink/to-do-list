from pydantic import BaseModel, Field, field_validator, ConfigDict
from pydantic_core.core_schema import FieldValidationInfo
import re


def check_username(value: str) -> str:
    # Только латиница, цифры и _
    if not re.match(r"^[a-zA-Z0-9_]+$", value):
        raise ValueError("Имя пользователя может содержать только буквы, цифры и _")
    # И хотя бы одна буква или цифра, чтобы нельзя было взять "___"
    if not re.search(r"[a-zA-Z0-9]", value):
        raise ValueError("Имя пользователя должно содержать хотя бы одну букву или цифру")
    return value


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
        return check_username(value)

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



class ProfileUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=20)
    bio: str | None = Field(default=None, max_length=255)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str | None) -> str:
        if value is None:
            raise ValueError("username нельзя удалить")
        return check_username(value)

    @field_validator("bio")
    @classmethod
    def normalize_bio(cls, value: str | None) -> str | None:
        # "" и "   " считаем пустым bio, то есть null
        if value is None:
            return None
        value = value.strip()
        return value or None


# Примеры для выпадающего списка в Swagger у PATCH /profile/me.
# Без них Swagger подставляет ВСЕ поля со значением "string".
PROFILE_UPDATE_EXAMPLES = {
    "bio": {
        "summary": "Только bio",
        "value": {"bio": "Пару слов о себе"},
    },
    "username": {
        "summary": "Только username",
        "value": {"username": "new_name"},
    },
    "both": {
        "summary": "username и bio",
        "value": {"username": "new_name", "bio": "Пару слов о себе"},
    },
    "clear_bio": {
        "summary": "Очистить bio",
        "value": {"bio": None},
    },
}