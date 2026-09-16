from fastapi import HTTPException, status
from app.models import Subscription, User, Category, PaymentMethod
from app.schema import SubscriptionCreate, SubscriptionUpdate
from app.utility import require_exists
from app.crud import subscription_crud


def create_subscription(db, request: SubscriptionCreate, current_user: User):
    require_exists(db, Category, request.category_id, "Category")
    category = require_exists(db, Category, request.category_id, "Category")
    require_exists(db, PaymentMethod, request.payment_method_id, "Payment Method")

    if category.type != "subscription":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This category is not valid for subscriptions")

    data = request.model_dump()
    data["user_id"] = current_user.id   # ← ignore whatever the client sent, use the authenticated user
    subscription = Subscription(**data)
    return subscription_crud.create(db, subscription)


def get_subscription(db, sub_id: int, current_user: User):
    subscription = require_exists(db, Subscription, sub_id, "Subscription")
    if subscription.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this subscription")
    return subscription


def list_subscriptions(db, current_user: User):
    all_subs = subscription_crud.get_all(db)
    return [s for s in all_subs if s.user_id == current_user.id]


def update_subscription(db, sub_id: int, request: SubscriptionUpdate, current_user: User):
    subscription = get_subscription(db, sub_id, current_user)   # reuses the ownership check above
    subscription.name = request.name
    subscription.amount = request.amount
    subscription.billing_cycle = request.billing_cycle
    subscription.start_date = request.start_date
    subscription.next_due_date = request.next_due_date
    subscription.status = request.status
    subscription.auto_renew = request.auto_renew
    return subscription_crud.update(db, subscription)


def delete_subscription(db, sub_id: int, current_user: User):
    subscription = get_subscription(db, sub_id, current_user)
    subscription_crud.delete(db, subscription)