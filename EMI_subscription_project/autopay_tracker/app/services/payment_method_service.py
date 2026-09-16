from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import PaymentMethod, User
from app.schema import PaymentMethodCreate, PaymentMethodUpdate
from app.utility import require_exists
from app.crud import payment_method_crud


def create_payment_method(db: Session, request: PaymentMethodCreate, current_user: User):
    data = request.model_dump()
    data["user_id"] = current_user.id
    payment_method = PaymentMethod(**data)
    return payment_method_crud.create(db, payment_method)


def get_payment_method(db: Session, pay_method_id: int, current_user: User):
    payment_method = require_exists(db, PaymentMethod, pay_method_id, "Payment Method")
    if payment_method.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this payment method")
    return payment_method


def list_payment_methods(db: Session, current_user: User):
    all_methods = payment_method_crud.get_all(db)
    return [pm for pm in all_methods if pm.user_id == current_user.id]


def update_payment_method(db: Session, pay_method_id: int, request: PaymentMethodUpdate, current_user: User):
    payment_method = get_payment_method(db, pay_method_id, current_user)   # reuses the ownership check
    payment_method.type = request.type
    payment_method.provider_name = request.provider_name
    payment_method.is_default = request.is_default
    return payment_method_crud.update(db, payment_method)


def delete_payment_method(db: Session, pay_method_id: int, current_user: User):
    payment_method = get_payment_method(db, pay_method_id, current_user)
    payment_method_crud.delete(db, payment_method)