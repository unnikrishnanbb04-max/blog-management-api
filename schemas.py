from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


# =========================
# USER
# =========================

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================
# AUTH
# =========================

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# =========================
# POST
# =========================

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    image: str | None = None
    author_id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class PostListResponse(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int
    posts: list[PostResponse]


# =========================
# COMMENT
# =========================

class CommentCreate(BaseModel):
    text: str


class CommentResponse(BaseModel):
    id: int
    post_id: int
    user_id: int
    text: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# =========================
# LIKE
# =========================

class LikeResponse(BaseModel):
    message: str