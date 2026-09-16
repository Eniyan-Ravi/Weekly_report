from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User
from app.schema import PaymentMethodCreate, PaymentMethodOut, PaymentMethodUpdate
from app.services import payment_method_service
from app.security import get_current_user

router = APIRouter(prefix="/payment_methods", tags=["Payment Methods"])

@router.post("/", response_model=PaymentMethodOut)
def create_payment_method(payment_request: PaymentMethodCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return payment_method_service.create_payment_method(db, payment_request, current_user)

@router.get("/", response_model=List[PaymentMethodOut])
def get_payment_methods(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return payment_method_service.list_payment_methods(db, current_user)

@router.get("/{pay_method_id}", response_model=PaymentMethodOut)
def get_payment_method(pay_method_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return payment_method_service.get_payment_method(db, pay_method_id, current_user)

@router.put("/{pay_method_id}", response_model=PaymentMethodOut)
def update_payment_method(pay_method_id: int, payment_request: PaymentMethodUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return payment_method_service.update_payment_method(db, pay_method_id, payment_request, current_user)

@router.delete("/{pay_method_id}")
def delete_payment_method(pay_method_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    payment_method_service.delete_payment_method(db, pay_method_id, current_user)
    return {"message": "Payment Method has been deleted"}