from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User
from app.schema import SubscriptionCreate, SubscriptionOut, SubscriptionUpdate
from app.services import subscription_service
from app.security import get_current_user

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

@router.post("/", response_model=SubscriptionOut)
def create_subscription(sub_request: SubscriptionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return subscription_service.create_subscription(db, sub_request, current_user)

@router.get("/", response_model=List[SubscriptionOut])
def get_subscriptions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return subscription_service.list_subscriptions(db, current_user)

@router.get("/{sub_id}", response_model=SubscriptionOut)
def get_subscription(sub_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return subscription_service.get_subscription(db, sub_id, current_user)

@router.put("/{sub_id}", response_model=SubscriptionOut)
def update_subscription(sub_id: int, sub_request: SubscriptionUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return subscription_service.update_subscription(db, sub_id, sub_request, current_user)

@router.delete("/{sub_id}")
def delete_subscription(sub_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    subscription_service.delete_subscription(db, sub_id, current_user)
    return {"message": "Subscription has been deleted"}