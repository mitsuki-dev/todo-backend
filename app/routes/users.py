# app/routes/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, crud

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    exists = crud.get_user_by_email(db, user_in.email)
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user_in)

@router.get("/{user_id}", response_model=schemas.UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
