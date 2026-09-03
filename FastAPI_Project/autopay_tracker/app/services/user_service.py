from sqlalchemy.orm import Session
from app.models import User
from app.schema import UserCreate, UserUpdate
from app.utility import require_exists
from app.crud import user_crud
from fastapi import HTTPException, status
from sqlalchemy import select
from app.security import hash_password, verify_password, create_access_token

def login_user(db: Session, email: str, password: str):
    stmt = select(User).where(User.email == email)
    user = db.execute(stmt).scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    token = create_access_token({"user_id": user.id})
    return {"access_token": token, "token_type": "bearer"}


def create_user(db: Session, request: UserCreate):
    user_data = request.model_dump()
    plain_password = user_data.pop("password")
    user_data["hashed_password"] = hash_password(plain_password)
    user = User(**user_data)
    return user_crud.create(db, user)

def get_user(db: Session, user_id: int):
    return require_exists(db, User, user_id, "User")

def list_users(db: Session):
    return user_crud.get_all(db)

def update_user(db: Session, user_id: int, request: UserUpdate):
    user = require_exists(db, User, user_id, "User")
    user.name = request.name
    user.email = request.email
    user.phone = request.phone
    return user_crud.update(db, user)

def delete_user(db: Session, user_id: int):
    user = require_exists(db, User, user_id, "User")
    user_crud.delete(db, user)