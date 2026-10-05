from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import Base, engine

from routers.auth import router as auth_router
from routers.posts import router as posts_router


# Create database tables

Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="Blog Management API",
    description="Blog API with JWT, image upload, comments, likes, search and pagination",
    version="1.0.0"
)


# Static media

app.mount(
    "/media",
    StaticFiles(directory="media"),
    name="media"
)


# Routers

app.include_router(
    auth_router
)

app.include_router(
    posts_router
)


@app.get("/")
def root():

    return {
        "message": "Blog Management API is running"
    }