import os
import uuid
import math

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form
)

from sqlalchemy import or_

from sqlalchemy.orm import Session

from database import get_db

from models import (
    User,
    Post,
    Comment,
    Like
)

from schemas import (
    PostResponse,
    PostListResponse,
    CommentCreate,
    CommentResponse,
    LikeResponse
)

from auth import get_current_user


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


MEDIA_DIRECTORY = "media/posts"


# ============================================================
# HELPER - SAVE IMAGE
# ============================================================

def save_image(image: UploadFile) -> str:

    os.makedirs(
        MEDIA_DIRECTORY,
        exist_ok=True
    )

    original_name = image.filename or ""

    extension = os.path.splitext(
        original_name
    )[1].lower()


    allowed_extensions = {
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".webp"
    }


    if extension not in allowed_extensions:

        raise HTTPException(
            status_code=400,
            detail="Only JPG, JPEG, PNG, GIF and WEBP images are allowed"
        )


    filename = (
        f"{uuid.uuid4()}"
        f"{extension}"
    )


    file_path = os.path.join(
        MEDIA_DIRECTORY,
        filename
    )


    with open(
        file_path,
        "wb"
    ) as buffer:

        while True:

            chunk = image.file.read(1024 * 1024)

            if not chunk:
                break

            buffer.write(chunk)


    return f"/media/posts/{filename}"


# ============================================================
# CREATE POST
# ============================================================

@router.post(
    "/create",
    response_model=PostResponse
)
def create_post(

    title: str = Form(...),

    content: str = Form(...),

    image: UploadFile | None = File(None),

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)
):

    title = title.strip()

    content = content.strip()


    if not title:

        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )


    if not content:

        raise HTTPException(
            status_code=400,
            detail="Content cannot be empty"
        )


    image_path = None


    if image:

        image_path = save_image(image)


    new_post = Post(

        title=title,

        content=content,

        image=image_path,

        author_id=current_user.id
    )


    db.add(new_post)

    db.commit()

    db.refresh(new_post)


    return new_post


# ============================================================
# GET POSTS - SEARCH + PAGINATION
# ============================================================

@router.get(
    "/",
    response_model=PostListResponse
)
def get_posts(

    page: int = 1,

    limit: int = 10,

    search: str | None = None,

    db: Session = Depends(get_db)
):

    if page < 1:

        raise HTTPException(
            status_code=400,
            detail="Page must be greater than 0"
        )


    if limit < 1:

        raise HTTPException(
            status_code=400,
            detail="Limit must be greater than 0"
        )


    if limit > 100:

        raise HTTPException(
            status_code=400,
            detail="Limit cannot exceed 100"
        )


    query = db.query(Post)


    # SEARCH

    if search:

        search = search.strip()


        if search:

            query = query.filter(

                or_(

                    Post.title.ilike(
                        f"%{search}%"
                    ),

                    Post.content.ilike(
                        f"%{search}%"
                    )

                )

            )


    # TOTAL COUNT

    total = query.count()


    # TOTAL PAGES

    total_pages = math.ceil(
        total / limit
    ) if total > 0 else 0


    # PAGINATION

    offset = (
        page - 1
    ) * limit


    posts = (

        query

        .order_by(
            Post.created_at.desc()
        )

        .offset(offset)

        .limit(limit)

        .all()

    )


    return {

        "page": page,

        "limit": limit,

        "total": total,

        "total_pages": total_pages,

        "posts": posts

    }


# ============================================================
# GET SINGLE POST
# ============================================================

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


# ============================================================
# UPDATE POST
# ============================================================

@router.put(
    "/{post_id}/update",
    response_model=PostResponse
)
def update_post(

    post_id: int,

    title: str = Form(...),

    content: str = Form(...),

    image: UploadFile | None = File(None),

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)
):

    post = db.query(Post).filter(
        Post.id == post_id
    ).first()


    if not post:

        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )


    # OWNERSHIP CHECK

    if post.author_id != current_user.id:

        raise HTTPException(
            status_code=403,
            detail="You can only update your own post"
        )


    title = title.strip()

    content = content.strip()


    if not title:

        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )


    if not content:

        raise HTTPException(
            status_code=400,
            detail="Content cannot be empty"
        )


    post.title = title

    post.content = content


    if image:

        post.image = save_image(image)


    db.commit()

    db.refresh(post)


    return post


# ============================================================
# DELETE POST
# ============================================================

@router.delete(
    "/{post_id}"
)
def delete_post(

    post_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)
):

    post = db.query(Post).filter(
        Post.id == post_id
    ).first()


    if not post:

        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )


    # OWNERSHIP CHECK

    if post.author_id != current_user.id:

        raise HTTPException(
            status_code=403,
            detail="You can only delete your own post"
        )


    db.delete(post)

    db.commit()


    return {
        "message": "Post deleted successfully"
    }


# ============================================================
# MY POSTS
# ============================================================

@router.get(
    "/mine/list",
    response_model=list[PostResponse]
)
def get_my_posts(

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)
):

    posts = db.query(Post).filter(
        Post.author_id == current_user.id
    ).order_by(
        Post.created_at.desc()
    ).all()


    return posts


# ============================================================
# ADD COMMENT
# ============================================================

@router.post(
    "/{post_id}/comments",
    response_model=CommentResponse
)
def add_comment(

    post_id: int,

    comment_data: CommentCreate,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)
):

    post = db.query(Post).filter(
        Post.id == post_id
    ).first()


    if not post:

        raise HTTPException(
            status_code=404,
            detail="Post not found"
        )


    text = comment_data.text.strip()


    if not text:

        raise HTTPException(
            status_code=400,
            detail="Comment cannot be empty"
        )


    comment = Comment(

        post_id=post_id,

        user_id=current_user.id,

        text=text
    )


    db.add(comment)

    db.commit()

    db.refresh(comment)


    # Email notification can be added here.

    return comment


# ============================================================
# GET COMMENTS
# ============================================================

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


    comments = db.query(Comment).filter(
        Comment.post_id == post_id
    ).order_by(
        Comment.created_at.desc()
    ).all()


    return comments


# ============================================================
# LIKE POST
# ============================================================

@router.post(
    "/{post_id}/like",
    response_model=LikeResponse
)
def like_post(

    post_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)
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


    new_like = Like(

        post_id=post_id,

        user_id=current_user.id
    )


    db.add(new_like)

    db.commit()


    # Email notification can be added here.

    return {
        "message": "Post liked successfully"
    }


# ============================================================
# UNLIKE POST
# ============================================================

@router.delete(
    "/{post_id}/like",
    response_model=LikeResponse
)
def unlike_post(

    post_id: int,

    db: Session = Depends(get_db),

    current_user: User = Depends(get_current_user)
):

    like = db.query(Like).filter(

        Like.post_id == post_id,

        Like.user_id == current_user.id

    ).first()


    if not like:

        raise HTTPException(
            status_code=404,
            detail="You have not liked this post"
        )


    db.delete(like)

    db.commit()


    return {
        "message": "Post unliked successfully"
    }