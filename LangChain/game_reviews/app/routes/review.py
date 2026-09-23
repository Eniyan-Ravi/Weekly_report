from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schema import ReviewRequest
from app.services import review_service

router = APIRouter(prefix="/reviews",tags=["Reviews"])


@router.post("/")
def create_review(review_request: ReviewRequest,db: Session = Depends(get_db)):
    return review_service.create_review(db, review_request)


@router.get("/")
def get_reviews(db: Session = Depends(get_db)):
    return review_service.get_reviews(db)


@router.get("/{review_id}")
def get_review(review_id: int,db: Session = Depends(get_db)):
    return review_service.get_review(db, review_id)


@router.put("/{review_id}")
def update_review(review_id: int,review_request: ReviewRequest,db: Session = Depends(get_db)):
    return review_service.update_review(db,review_id,review_request)


@router.delete("/{review_id}")
def delete_review(review_id: int,db: Session = Depends(get_db)):
    return review_service.delete_review(db, review_id)