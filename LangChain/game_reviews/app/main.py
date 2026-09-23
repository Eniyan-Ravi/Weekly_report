from fastapi import FastAPI

from app.database import engine, Base

from app.routes.customer import router as customer_router
from app.routes.review import router as review_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Online Game Review API",
    description="API for customers and game reviews")


app.include_router(customer_router)
app.include_router(review_router)


@app.get("/")
def root():
    return {"message": "Online Game Review API is running"}

