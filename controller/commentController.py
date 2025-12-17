from sqlalchemy.orm import Session, joinedload
from models.commentModel import Comment
from schemas.commentSchemas import CommentCreate
from models.usersModel import User

def create_comment(db: Session, comment_data: dict):
    db_comment = Comment(**comment_data)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    # Traer también al usuario con joinedload para que Pydantic pueda serializarlo
    db_comment = db.query(Comment).options(joinedload(Comment.user)).filter(Comment.id == db_comment.id).first()
    return db_comment

def get_comments_by_product(db: Session, product_id: int):
    # Trae comentarios con usuario cargado
    return db.query(Comment).options(joinedload(Comment.user))\
             .filter(Comment.product_id == product_id).all()


def get_comment(db: Session, comment_id: int):
    return db.query(Comment).filter(Comment.id == comment_id).first()

def delete_comment(db: Session, comment_id: int):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        db.delete(comment)
        db.commit()
    return comment
