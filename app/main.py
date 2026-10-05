from fastapi import FastAPI

from app.database import Base, engine
from app.routers import auth
from app.routers import posts
from app.routers import comments
from app.routers import likes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blog Management API",
    description="Mini blogging system using FastAPI, SQLite and JWT",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(likes.router)


@app.get("/")
def root():
    return {
        "message": "Blog Management API is running"
    }