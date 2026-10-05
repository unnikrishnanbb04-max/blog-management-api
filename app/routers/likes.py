from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Post, Like
from app.auth import get_current_user
from app.email_service import send_like_notification


router = APIRouter(
    prefix="/posts",
    tags=["Likes"]
)


@router.post("/{post_id}/like")
def like_post(
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

    existing_like = db.query(Like).filter(
        Like.post_id == post_id,
        Like.user_id == current_user.id
    ).first()

    if existing_like:
        raise HTTPException(
            status_code=400,
            detail="You already liked this post"
        )

    like = Like(
        post_id=post_id,
        user_id=current_user.id
    )

    db.add(like)
    db.commit()

    send_like_notification(
        post.author.email,
        current_user.username,
        post.title
    )

    return {
        "message": "Post liked successfully"
    }


@router.delete("/{post_id}/like")
def unlike_post(
    post_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    like = db.query(Like).filter(
        Like.post_id == post_id,
        Like.user_id == current_user.id
    ).first()

    if not like:
        raise HTTPException(
            status_code=404,
            detail="Like not found"
        )

    db.delete(like)
    db.commit()

    return {
        "message": "Post unliked successfully"
    }