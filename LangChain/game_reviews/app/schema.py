from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    ConfigDict
)


# =========================================================
# CUSTOMER
# =========================================================

class CustomerRequest(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        min_length=4,
        max_length=255
    )

    age: int = Field(
        ge=13,
        le=100
    )


class CustomerUpdate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr

    age: int = Field(
        ge=13,
        le=100
    )


class CustomerResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    name: str
    email: EmailStr
    age: int
    role: str
    is_active: bool


# =========================================================
# CUSTOMER LOGIN
# =========================================================

class LoginRequest(BaseModel):

    email: EmailStr

    password: str


# =========================================================
# REVIEW
# =========================================================

class ReviewRequest(BaseModel):

    game_name: str = Field(
        min_length=1,
        max_length=100
    )

    customer_id: int = Field(
        gt=0
    )

    rating: int = Field(
        ge=1,
        le=5
    )

    review: str = Field(
        min_length=5,
        max_length=500
    )

    price: float = Field(
        ge=0
    )


class ReviewUpdate(BaseModel):

    game_name: str = Field(
        min_length=1,
        max_length=100
    )

    rating: int = Field(
        ge=1,
        le=5
    )

    review: str = Field(
        min_length=5,
        max_length=500
    )

    price: float = Field(
        ge=0
    )


class ReviewResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    game_name: str
    customer_id: int
    rating: int
    review: str
    price: float