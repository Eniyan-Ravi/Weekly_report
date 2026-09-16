from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import User
from app.schema import EMICreate, EMIOut, EMIUpdate
from app.services import emi_service
from app.security import get_current_user

router = APIRouter(prefix="/emis", tags=["EMI"])

@router.post("/", response_model=EMIOut)
def create_emi(emi_request: EMICreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return emi_service.create_emi(db, emi_request, current_user)

@router.get("/", response_model=List[EMIOut])
def get_emis(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return emi_service.list_emis(db, current_user)

@router.get("/{emi_id}", response_model=EMIOut)
def get_emi(emi_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return emi_service.get_emi(db, emi_id, current_user)

@router.put("/{emi_id}", response_model=EMIOut)
def update_emi(emi_id: int, emi_request: EMIUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return emi_service.update_emi(db, emi_id, emi_request, current_user)

@router.delete("/{emi_id}")
def delete_emi(emi_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    emi_service.delete_emi(db, emi_id, current_user)
    return {"message": "EMI has been Deleted successfully"}