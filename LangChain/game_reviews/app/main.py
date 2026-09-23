from fastapi import FastAPI

from app.database import engine, Base

from app.routes.customer import router as customer_router
from app.routes.review import router as review_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Online Game Review API",
    description=(
        "API for customer management, "
        "game reviews and review analysis"
    ),
    version="1.0.0"
)


app.include_router(customer_router)
app.include_router(review_router)


@app.get("/")
def root():

    return {
        "message": "Online Game Review API is running"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }