from fastapi import HTTPException
from sqlalchemy import select

from app.model import GameReview


def create_review(db, review_request):
    review = GameReview(
        game_name=review_request.game_name,
        customer_id=review_request.customer_id,
        rating=review_request.rating,
        review=review_request.review,
        price=review_request.price
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    return review


def get_reviews(db):
    stmt = select(GameReview)
    return db.execute(stmt).scalars().all()


def get_review(db, review_id):
    stmt = select(GameReview).where(GameReview.id == review_id)
    review = db.execute(stmt).scalar_one_or_none()

    if review is None:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    return review