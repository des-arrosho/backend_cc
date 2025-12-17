from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import SessionLocal
from controller import commentController
from schemas.commentSchemas import CommentCreate, CommentOut, CommentWithUser
from config.jwt import get_current_user
from schemas.userSchemas import User

comment_router = APIRouter(prefix="/comments", tags=["comments"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@comment_router.post("/create", response_model=CommentOut)
def create_comment(
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment_data = comment.model_dump()
    comment_data["user_id"] = current_user.id
    return commentController.create_comment(db, comment_data)

@comment_router.get("/product/{product_id}", response_model=list[CommentWithUser])
def get_comments_for_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    return commentController.get_comments_by_product(db, product_id)

@comment_router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment = commentController.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    
    commentController.delete_comment(db, comment_id)
    return {"message": "Comment deleted successfully"}

@comment_router.put("/{comment_id}", response_model=CommentOut)
def update_comment(
    comment_id: int,
    comment_update: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment = commentController.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this comment")

    return commentController.update_comment(db, comment_id, comment_update.model_dump())
