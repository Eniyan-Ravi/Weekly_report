from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User
from app.schema import PaymentHistoryCreate, PaymentHistoryOut
from app.services import payment_history_service
from app.security import get_current_user

router = APIRouter(prefix="/payment_history", tags=["Payment History"])

@router.post("/", response_model=PaymentHistoryOut)
def create_payment_history(payhistory_request: PaymentHistoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return payment_history_service.create_payment_history(db, payhistory_request, current_user)

@router.get("/", response_model=List[PaymentHistoryOut])
def get_payment_histories(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return payment_history_service.list_payment_histories(db, current_user)

@router.get("/{payhistory_id}", response_model=PaymentHistoryOut)
def get_payment_history(payhistory_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return payment_history_service.get_payment_history(db, payhistory_id, current_user)