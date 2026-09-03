from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User
from app.schema import UserCreate, UserOut, UserUpdate, LoginRequest
from app.services import user_service
from app.security import get_current_user

router = APIRouter(prefix="/user", tags=["Users"])


@router.post("/login")
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    return user_service.login_user(db, login_request.email, login_request.password)


@router.post("/", response_model=UserOut)
def create_user(user_request: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user_request)


@router.get("/", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db)):
    return user_service.list_users(db)


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return user_service.get_user(db, user_id)


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_request: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return user_service.update_user(db, user_id, user_request)


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_service.delete_user(db, user_id)
    return {"message": "User has been deleted"}