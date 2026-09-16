from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import EMI, Category, PaymentMethod, User
from app.schema import EMICreate, EMIUpdate
from app.utility import require_exists
from app.crud import emi_crud


def create_emi(db: Session, request: EMICreate, current_user: User):
    category = require_exists(db, Category, request.category_id, "Category")
    require_exists(db, PaymentMethod, request.payment_method_id, "Payment Method")

    if category.type != "emi":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This category is not valid for emis")

    emi_data = request.model_dump()
    emi_data["user_id"] = current_user.id
    emi_data["installments_paid"] = 0
    emi_data["installments_remaining"] = request.emi_months

    emi = EMI(**emi_data)
    return emi_crud.create(db, emi)


def get_emi(db: Session, emi_id: int, current_user: User):
    emi = require_exists(db, EMI, emi_id, "EMI")
    if emi.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this EMI")
    return emi


def list_emis(db: Session, current_user: User):
    all_emis = emi_crud.get_all(db)
    return [e for e in all_emis if e.user_id == current_user.id]


def update_emi(db: Session, emi_id: int, request: EMIUpdate, current_user: User):
    emi = get_emi(db, emi_id, current_user)
    emi.item_name = request.item_name
    emi.total_amount = request.total_amount
    emi.emi_months = request.emi_months
    emi.monthly_installment = request.monthly_installment
    emi.start_date = request.start_date
    emi.next_due_date = request.next_due_date
    emi.installments_paid = request.installments_paid
    emi.installments_remaining = request.installments_remaining
    emi.status = request.status
    return emi_crud.update(db, emi)


def delete_emi(db: Session, emi_id: int, current_user: User):
    emi = get_emi(db, emi_id, current_user)
    emi_crud.delete(db, emi)