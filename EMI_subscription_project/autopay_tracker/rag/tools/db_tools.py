import sys
from pathlib import Path
from fastapi import HTTPException

sys.path.append(str(Path(__file__).parent.parent.parent))

from app.services import subscription_service, emi_service, payment_history_service, category_service, payment_method_service


def get_subscriptions(db, current_user):
    subscriptions = subscription_service.list_subscriptions(db, current_user)

    if not subscriptions:
        return {"status": "empty", "message": "No subscriptions found for this user."}

    data = [
        {
            "id": s.id,
            "name": s.name,
            "amount": s.amount,
            "billing_cycle": s.billing_cycle,
            "next_due_date": str(s.next_due_date),
            "status": s.status,
            "auto_renew": s.auto_renew,
        }
        for s in subscriptions
    ]
    return {"status": "ok", "data": data}


def get_subscription_by_id(db, current_user, subscription_id: int):
    try:
        subscription = subscription_service.get_subscription(db, subscription_id, current_user)
    except HTTPException as e:
        return {"status": "error", "message": e.detail}

    data = {
        "id": subscription.id,
        "name": subscription.name,
        "amount": subscription.amount,
        "billing_cycle": subscription.billing_cycle,
        "next_due_date": str(subscription.next_due_date),
        "status": subscription.status,
        "auto_renew": subscription.auto_renew,
    }
    return {"status": "ok", "data": data}


def get_emis(db, current_user):
    emis = emi_service.list_emis(db, current_user)

    if not emis:
        return {"status": "empty", "message": "No EMIs found for this user."}

    data = [
        {
            "id": e.id,
            "item_name": e.item_name,
            "total_amount": e.total_amount,
            "monthly_installment": e.monthly_installment,
            "installments_paid": e.installments_paid,
            "installments_remaining": e.installments_remaining,
            "next_due_date": str(e.next_due_date),
            "status": e.status,
        }
        for e in emis
    ]
    return {"status": "ok", "data": data}


def get_emi_by_id(db, current_user, emi_id: int):
    try:
        emi = emi_service.get_emi(db, emi_id, current_user)
    except HTTPException as e:
        return {"status": "error", "message": e.detail}

    data = {
        "id": emi.id,
        "item_name": emi.item_name,
        "total_amount": emi.total_amount,
        "monthly_installment": emi.monthly_installment,
        "installments_paid": emi.installments_paid,
        "installments_remaining": emi.installments_remaining,
        "next_due_date": str(emi.next_due_date),
        "status": emi.status,
    }
    return {"status": "ok", "data": data}


def get_payment_history(db, current_user):
    history = payment_history_service.list_payment_histories(db, current_user)

    if not history:
        return {"status": "empty", "message": "No payment history found for this user."}

    data = [
        {
            "id": h.id,
            "amount_paid": h.amount_paid,
            "paid_on": str(h.paid_on),
            "status": h.status,
            "subscription_id": h.subscription_id,
            "emi_id": h.emi_id,
        }
        for h in history
    ]
    return {"status": "ok", "data": data}


def get_payment_history_by_id(db, current_user, payhistory_id: int):
    try:
        history = payment_history_service.get_payment_history(db, payhistory_id, current_user)
    except HTTPException as e:
        return {"status": "error", "message": e.detail}

    data = {
        "id": history.id,
        "amount_paid": history.amount_paid,
        "paid_on": str(history.paid_on),
        "status": history.status,
        "subscription_id": history.subscription_id,
        "emi_id": history.emi_id,
    }
    return {"status": "ok", "data": data}


def get_categories(db, current_user):
    categories = category_service.list_categories(db)

    if not categories:
        return {"status": "empty", "message": "No categories found."}

    data = [
        {"id": c.id, "name": c.name, "type": c.type}
        for c in categories
    ]
    return {"status": "ok", "data": data}


def get_payment_methods(db, current_user):
    methods = payment_method_service.list_payment_methods(db, current_user)

    if not methods:
        return {"status": "empty", "message": "No payment methods found for this user."}

    data = [
        {
            "id": m.id,
            "type": m.type,
            "provider_name": m.provider_name,
            "is_default": m.is_default,
        }
        for m in methods
    ]
    return {"status": "ok", "data": data}