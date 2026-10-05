from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Post, Comment
from app.schemas import CommentCreate, CommentResponse
from app.auth import get_current_user
from app.email_service import send_comment_notification


router = APIRouter(
    prefix="/posts",
    tags=["Comments"]
)


@router.post(
    "/{post_id}/comments",
    response_model=CommentResponse
)
def add_comment(
    post_id: int,
    comment_data: CommentCreate,
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

    comment = Comment(
        post_id=post_id,
        user_id=current_user.id,
        text=comment_data.text
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    send_comment_notification(
        post.author.email,
        current_user.username,
        post.title
    )

    return comment


@router.get(
    "/{post_id}/comments",
    response_model=list[CommentResponse]
)
def get_comments(
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

    return db.query(Comment).filter(
        Comment.post_id == post_id
    ).all()