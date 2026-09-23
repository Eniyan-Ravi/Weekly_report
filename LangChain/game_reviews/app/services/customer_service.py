from sqlalchemy import select
from sqlalchemy.orm import Session

from app.model import Customer, GameReview


def get_customer(
    db: Session,
    customer_id: int
):
    stmt = select(Customer).where(
        Customer.id == customer_id
    )

    return db.execute(stmt).scalar_one_or_none()


def get_customers(db: Session):

    stmt = select(Customer)

    result = db.execute(stmt)

    return result.scalars().all()


def get_customer_review_count(
    db: Session,
    customer_id: int
):

    customer = get_customer(
        db,
        customer_id
    )

    if customer is None:
        return None

    stmt = select(GameReview).where(
        GameReview.customer_id == customer_id
    )

    reviews = db.execute(stmt).scalars().all()

    return {
        "customer_id": customer.id,
        "customer_name": customer.name,
        "review_count": len(reviews)
    }


def get_customer_reviews(
    db: Session,
    customer_id: int
):

    stmt = select(GameReview).where(
        GameReview.customer_id == customer_id
    )

    result = db.execute(stmt)

    return result.scalars().all()