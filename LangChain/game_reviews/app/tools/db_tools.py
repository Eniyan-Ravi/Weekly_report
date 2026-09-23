from sqlalchemy import select

from app.database import SessionLocal
from app.model import Customer, GameReview


def get_customers():
    db = SessionLocal()

    try:
        stmt = select(Customer)
        customers = db.execute(stmt).scalars().all()

        return {
            "status": "ok",
            "data": [
                {
                    "id": customer.id,
                    "name": customer.name,
                    "email": customer.email,
                    "age": customer.age,
                    "role": customer.role,
                    "is_active": customer.is_active
                }
                for customer in customers
            ]
        }

    finally:
        db.close()


def get_customer(customer_id: int):
    db = SessionLocal()

    try:
        stmt = select(Customer).where(Customer.id == customer_id)
        customer = db.execute(stmt).scalar_one_or_none()

        if customer is None:
            return {
                "status": "error",
                "message": "Customer not found"
            }

        return {
            "status": "ok",
            "data": {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email,
                "age": customer.age,
                "role": customer.role,
                "is_active": customer.is_active
            }
        }

    finally:
        db.close()


def get_reviews():
    db = SessionLocal()

    try:
        stmt = select(GameReview)
        reviews = db.execute(stmt).scalars().all()

        return {
            "status": "ok",
            "data": [
                {
                    "id": review.id,
                    "game_name": review.game_name,
                    "customer_id": review.customer_id,
                    "rating": review.rating,
                    "review": review.review,
                    "price": review.price
                }
                for review in reviews
            ]
        }

    finally:
        db.close()


def get_review(review_id: int):
    db = SessionLocal()

    try:
        stmt = select(GameReview).where(GameReview.id == review_id)
        review = db.execute(stmt).scalar_one_or_none()

        if review is None:
            return {
                "status": "error",
                "message": "Review not found"
            }

        return {
            "status": "ok",
            "data": {
                "id": review.id,
                "game_name": review.game_name,
                "customer_id": review.customer_id,
                "rating": review.rating,
                "review": review.review,
                "price": review.price
            }
        }

    finally:
        db.close()


tool_function_map = {
    "get_customers": get_customers,
    "get_customer": get_customer,
    "get_reviews": get_reviews,
    "get_review": get_review
}