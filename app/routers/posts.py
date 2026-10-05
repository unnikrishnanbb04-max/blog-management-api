from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Post
from app.schemas import PostCreate, PostUpdate, PostResponse
from app.auth import get_current_user


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get(
    "/",
    response_model=list[PostResponse]
)
def get_posts(
    db: Session = Depends(get_db)
):
    return db.query(Post).all()


@router.get(
    "/mine",
    response_model=list[PostResponse]
)
def get_my_posts(
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Post).filter(
        Post.author_id == current_user.id
    ).all()


@router.get(
    "/{post_id}",
    response_model=PostResponse
)
def get_post(
    post_id: int,
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    return post


@router.post(
    "/",
    response_model=PostResponse
)
def create_post(
    post_data: PostCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = Post(
        title=post_data.title,
        content=post_data.content,
        author_id=current_user.id
    )

    db.add(post)
    db.commit()
    db.refresh(post)

    return post


@router.put(
    "/{post_id}",
    response_model=PostResponse
)
def update_post(
    post_id: int,
    post_data: PostUpdate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only update your own posts"
        )

    post.title = post_data.title
    post.content = post_data.content

    db.commit()
    db.refresh(post)

    return post


@router.delete(
    "/{post_id}"
)
def delete_post(
    post_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = db.query(Post).filter(
        Post.id == post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )

    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own posts"
        )

    db.delete(post)
    db.commit()

    return {
        "message": "Post deleted successfully"
    }