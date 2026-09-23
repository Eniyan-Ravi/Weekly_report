from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.model import Customer

from app.schema import (
    CustomerRequest,
    CustomerUpdate,
    CustomerResponse,
    LoginRequest
)


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.post(
    "/",
    response_model=CustomerResponse
)
def create_customer(
    customer_request: CustomerRequest,
    db: Session = Depends(get_db)
):

    stmt = select(Customer).where(
        Customer.email == customer_request.email
    )

    existing = db.execute(
        stmt
    ).scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    customer = Customer(
        **customer_request.model_dump()
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


@router.get(
    "/",
    response_model=list[CustomerResponse]
)
def get_customers(
    db: Session = Depends(get_db)
):

    stmt = select(Customer)

    result = db.execute(stmt)

    return result.scalars().all()


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):

    stmt = select(Customer).where(
        Customer.id == customer_id
    )

    customer = db.execute(
        stmt
    ).scalar_one_or_none()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


@router.put(
    "/{customer_id}",
    response_model=CustomerResponse
)
def update_customer(
    customer_id: int,
    customer_request: CustomerUpdate,
    db: Session = Depends(get_db)
):

    stmt = select(Customer).where(
        Customer.id == customer_id
    )

    customer = db.execute(
        stmt
    ).scalar_one_or_none()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    customer.name = customer_request.name
    customer.email = customer_request.email
    customer.age = customer_request.age

    db.commit()
    db.refresh(customer)

    return customer


@router.put(
    "/{customer_id}/status",
    response_model=CustomerResponse
)
def update_customer_status(
    customer_id: int,
    is_active: bool,
    db: Session = Depends(get_db)
):

    stmt = select(Customer).where(
        Customer.id == customer_id
    )

    customer = db.execute(
        stmt
    ).scalar_one_or_none()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    customer.is_active = is_active

    db.commit()
    db.refresh(customer)

    return customer


@router.post("/login")
def login(
    login_request: LoginRequest,
    db: Session = Depends(get_db)
):

    stmt = select(Customer).where(
        Customer.email == login_request.email
    )

    customer = db.execute(
        stmt
    ).scalar_one_or_none()

    if customer is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Temporary only.
    # Hashing will be added later.

    if customer.password != login_request.password:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not customer.is_active:
        raise HTTPException(
            status_code=403,
            detail="Customer account is inactive"
        )

    return {
        "message": "Login successful",
        "customer_id": customer.id,
        "role": customer.role
    }


@router.delete("/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):

    stmt = select(Customer).where(
        Customer.id == customer_id
    )

    customer = db.execute(
        stmt
    ).scalar_one_or_none()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    db.delete(customer)
    db.commit()

    return {
        "message": "Customer deleted successfully"
    }