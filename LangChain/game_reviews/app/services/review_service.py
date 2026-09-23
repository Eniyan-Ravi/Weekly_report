from sqlalchemy import (
    select,
    func,
    or_
)

from sqlalchemy.orm import Session

from app.model import GameReview


# =========================================================
# BASIC
# =========================================================

def get_review(
    db: Session,
    review_id: int
):

    stmt = select(GameReview).where(
        GameReview.id == review_id
    )

    return db.execute(
        stmt
    ).scalar_one_or_none()


def get_reviews(db: Session):

    stmt = select(GameReview)

    result = db.execute(stmt)

    return result.scalars().all()


# =========================================================
# BY GAME
# =========================================================

def get_reviews_by_game(
    db: Session,
    game_name: str
):

    stmt = select(GameReview).where(
        GameReview.game_name.ilike(game_name)
    )

    result = db.execute(stmt)

    return result.scalars().all()


# =========================================================
# BY CUSTOMER
# =========================================================

def get_reviews_by_customer(
    db: Session,
    customer_id: int
):

    stmt = select(GameReview).where(
        GameReview.customer_id == customer_id
    )

    result = db.execute(stmt)

    return result.scalars().all()


# =========================================================
# SEARCH
# =========================================================

def search_reviews(
    db: Session,
    query: str
):

    pattern = f"%{query}%"

    stmt = select(GameReview).where(
        or_(
            GameReview.game_name.ilike(pattern),
            GameReview.review.ilike(pattern)
        )
    )

    result = db.execute(stmt)

    return result.scalars().all()


# =========================================================
# BY RATING
# =========================================================

def get_reviews_by_rating(
    db: Session,
    rating: int
):

    stmt = (
        select(GameReview)
        .where(GameReview.rating == rating)
        .order_by(GameReview.id.desc())
    )

    result = db.execute(stmt)

    return result.scalars().all()


# =========================================================
# TOP RATED
# =========================================================

def get_top_rated_reviews(
    db: Session,
    limit: int = 5
):

    stmt = (
        select(GameReview)
        .order_by(
            GameReview.rating.desc(),
            GameReview.id.desc()
        )
        .limit(limit)
    )

    result = db.execute(stmt)

    return result.scalars().all()


# =========================================================
# LOW RATED
# =========================================================

def get_low_rated_reviews(
    db: Session,
    limit: int = 5
):

    stmt = (
        select(GameReview)
        .order_by(
            GameReview.rating.asc(),
            GameReview.id.desc()
        )
        .limit(limit)
    )

    result = db.execute(stmt)

    return result.scalars().all()


# =========================================================
# LATEST REVIEWS
# =========================================================

def get_latest_reviews(
    db: Session,
    limit: int = 5
):

    stmt = (
        select(GameReview)
        .order_by(GameReview.id.desc())
        .limit(limit)
    )

    result = db.execute(stmt)

    return result.scalars().all()


# =========================================================
# GAME SUMMARY
# =========================================================

def get_game_summary(
    db: Session,
    game_name: str
):

    stmt = select(
        func.count(GameReview.id),
        func.avg(GameReview.rating),
        func.min(GameReview.rating),
        func.max(GameReview.rating),
        func.avg(GameReview.price)
    ).where(
        GameReview.game_name.ilike(game_name)
    )

    result = db.execute(stmt).one()

    return {
        "game_name": game_name,
        "review_count": result[0],
        "average_rating": (
            round(float(result[1]), 2)
            if result[1] is not None
            else 0
        ),
        "minimum_rating": result[2],
        "maximum_rating": result[3],
        "average_price": (
            round(float(result[4]), 2)
            if result[4] is not None
            else 0
        )
    }


# =========================================================
# GAME NAMES
# =========================================================

def get_games(
    db: Session
):

    stmt = select(
        GameReview.game_name
    ).distinct().order_by(
        GameReview.game_name
    )

    result = db.execute(stmt)

    return result.scalars().all()


# =========================================================
# GAME COUNT
# =========================================================

def get_game_count(
    db: Session
):

    stmt = select(
        func.count(
            func.distinct(GameReview.game_name)
        )
    )

    return db.execute(stmt).scalar()


# =========================================================
# RATING DISTRIBUTION
# =========================================================

def get_rating_distribution(
    db: Session,
    game_name: str
):

    stmt = (
        select(
            GameReview.rating,
            func.count(GameReview.id)
        )
        .where(
            GameReview.game_name.ilike(game_name)
        )
        .group_by(GameReview.rating)
        .order_by(GameReview.rating)
    )

    result = db.execute(stmt).all()

    return {
        rating: count
        for rating, count in result
    }


# =========================================================
# PRICE RANGE
# =========================================================

def get_games_by_price_range(
    db: Session,
    min_price: float,
    max_price: float
):

    stmt = (
        select(GameReview)
        .where(
            GameReview.price >= min_price,
            GameReview.price <= max_price
        )
        .order_by(GameReview.price)
    )

    result = db.execute(stmt)

    return result.scalars().all()