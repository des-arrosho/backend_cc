from sqlalchemy.orm import Session
from models.usersModel import User
from schemas.userSchemas import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_id(db: Session, id: int):
    return db.query(User).filter(User.id == id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_username_or_email(db: Session, username: str, email: str):
    return db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
    username=user.username,
    email=user.email,
    password=hashed_password,
    status=user.status,
    profile_picture=user.profile_picture
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not pwd_context.verify(password, user.password):
        return None
    return user

def get_active_users(db: Session):
    return db.query(User).filter(User.status == "Active").all()
