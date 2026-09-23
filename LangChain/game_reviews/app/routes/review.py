from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)

from sqlalchemy import (
    select,
    func,
    or_
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.model import Customer, GameReview

from app.schema import (
    ReviewRequest,
    ReviewUpdate,
    ReviewResponse
)


router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"]
)


# =========================================================
# CREATE REVIEW
# =========================================================

@router.post(
    "/",
    response_model=ReviewResponse
)
def create_review(
    review_request: ReviewRequest,
    db: Session = Depends(get_db)
):

    customer_stmt = select(Customer).where(
        Customer.id == review_request.customer_id
    )

    customer = db.execute(
        customer_stmt
    ).scalar_one_or_none()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    if not customer.is_active:
        raise HTTPException(
            status_code=403,
            detail="Inactive customer cannot create reviews"
        )

    review = GameReview(
        **review_request.model_dump()
    )

    db.add(review)
    db.commit()
    db.refresh(review)

    return review


# =========================================================
# GET ALL REVIEWS
# =========================================================

@router.get(
    "/",
    response_model=list[ReviewResponse]
)
def get_reviews(
    db: Session = Depends(get_db)
):

    stmt = select(GameReview)

    result = db.execute(stmt)

    return result.scalars().all()


# =========================================================
# GET REVIEW BY ID
# =========================================================

@router.get(
    "/{review_id}",
    response_model=ReviewResponse
)
def get_review(
    review_id: int,
    db: Session = Depends(get_db)
):

    stmt = select(GameReview).where(
        GameReview.id == review_id
    )

    review = db.execute(
        stmt
    ).scalar_one_or_none()

    if review is None:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    return review


# =========================================================
# GET REVIEWS BY GAME
# =========================================================

@router.get(
    "/game/{game_name}",
    response_model=list[ReviewResponse]
)
def get_reviews_by_game(
    game_name: str,
    db: Session = Depends(get_db)
):

    stmt = select(GameReview).where(
        GameReview.game_name.ilike(game_name)
    )

    result = db.execute(stmt)

    return result.scalars().all()


# =========================================================
# GET REVIEWS BY CUSTOMER
# =========================================================

@router.get(
    "/customer/{customer_id}",
    response_model=list[ReviewResponse]
)
def get_reviews_by_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):

    customer_stmt = select(Customer).where(
        Customer.id == customer_id
    )

    customer = db.execute(
        customer_stmt
    ).scalar_one_or_none()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    stmt = select(GameReview).where(
        GameReview.customer_id == customer_id
    )

    result = db.execute(stmt)

    return result.scalars().all()


# =========================================================
# NEW GET 1
# SEARCH REVIEWS
# =========================================================

@router.get(
    "/search",
    response_model=list[ReviewResponse]
)
def search_reviews(
    query: str = Query(
        min_length=2,
        max_length=100
    ),
    db: Session = Depends(get_db)
):

    search_pattern = f"%{query}%"

    stmt = select(GameReview).where(
        or_(
            GameReview.game_name.ilike(search_pattern),
            GameReview.review.ilike(search_pattern)
        )
    )

    result = db.execute(stmt)

    return result.scalars().all()


# =========================================================
# NEW GET 2
# GET TOP RATED REVIEWS
# =========================================================

@router.get(
    "/top-rated",
    response_model=list[ReviewResponse]
)
def get_top_rated_reviews(
    limit: int = Query(
        default=5,
        ge=1,
        le=20
    ),
    db: Session = Depends(get_db)
):

    stmt = (
        select(GameReview)
        .order_by(GameReview.rating.desc())
        .limit(limit)
    )

    result = db.execute(stmt)

    return result.scalars().all()


# =========================================================
# NEW GET 3
# GET REVIEWS BY RATING
# =========================================================

@router.get(
    "/rating/{rating}",
    response_model=list[ReviewResponse]
)
def get_reviews_by_rating(
    rating: int,
    db: Session = Depends(get_db)
):

    if rating < 1 or rating > 5:
        raise HTTPException(
            status_code=400,
            detail="Rating must be between 1 and 5"
        )

    stmt = select(GameReview).where(
        GameReview.rating == rating
    )

    result = db.execute(stmt)

    return result.scalars().all()


# =========================================================
# GAME SUMMARY
# =========================================================

@router.get(
    "/game/{game_name}/summary"
)
def get_game_summary(
    game_name: str,
    db: Session = Depends(get_db)
):

    stmt = select(
        func.count(GameReview.id),
        func.avg(GameReview.rating),
        func.min(GameReview.rating),
        func.max(GameReview.rating)
    ).where(
        GameReview.game_name.ilike(game_name)
    )

    result = db.execute(stmt).one()

    review_count = result[0]
    average_rating = result[1]
    minimum_rating = result[2]
    maximum_rating = result[3]

    if review_count == 0:
        raise HTTPException(
            status_code=404,
            detail="No reviews found for this game"
        )

    return {
        "game_name": game_name,
        "review_count": review_count,
        "average_rating": round(
            float(average_rating),
            2
        ),
        "minimum_rating": minimum_rating,
        "maximum_rating": maximum_rating
    }


# =========================================================
# UPDATE REVIEW
# =========================================================

@router.put(
    "/{review_id}",
    response_model=ReviewResponse
)
def update_review(
    review_id: int,
    review_request: ReviewUpdate,
    db: Session = Depends(get_db)
):

    stmt = select(GameReview).where(
        GameReview.id == review_id
    )

    review = db.execute(
        stmt
    ).scalar_one_or_none()

    if review is None:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    review.game_name = review_request.game_name
    review.rating = review_request.rating
    review.review = review_request.review
    review.price = review_request.price

    db.commit()
    db.refresh(review)

    return review


# =========================================================
# DELETE REVIEW
# =========================================================

@router.delete("/{review_id}")
def delete_review(
    review_id: int,
    db: Session = Depends(get_db)
):

    stmt = select(GameReview).where(
        GameReview.id == review_id
    )

    review = db.execute(
        stmt
    ).scalar_one_or_none()

    if review is None:
        raise HTTPException(
            status_code=404,
            detail="Review not found"
        )

    db.delete(review)
    db.commit()

    return {
        "message": "Review deleted successfully",
        "review_id": review_id
    }