from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import PaymentHistory, PaymentMethod, Subscription, EMI, User
from app.schema import PaymentHistoryCreate
from app.utility import require_exists
from app.crud import payment_history_crud


def create_payment_history(db: Session, request: PaymentHistoryCreate, current_user: User):
    payment_method = require_exists(db, PaymentMethod, request.payment_method_id, "Payment Method")
    if payment_method.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to use this payment method")

    if (request.subscription_id is None) == (request.emi_id is None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Exactly one of subscription_id or emi_id must be provided"
        )

    if request.subscription_id is not None:
        subscription = require_exists(db, Subscription, request.subscription_id, "Subscription")
        if subscription.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to use this subscription")

    if request.emi_id is not None:
        emi = require_exists(db, EMI, request.emi_id, "EMI")
        if emi.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to use this EMI")

    data = request.model_dump()
    data["user_id"] = current_user.id
    payhistory = PaymentHistory(**data)
    return payment_history_crud.create(db, payhistory)


def get_payment_history(db: Session, payhistory_id: int, current_user: User):
    payhistory = require_exists(db, PaymentHistory, payhistory_id, "Payment History")
    if payhistory.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this payment history")
    return payhistory


def list_payment_histories(db: Session, current_user: User):
    all_history = payment_history_crud.get_all(db)
    return [h for h in all_history if h.user_id == current_user.id]