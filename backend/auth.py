from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from argon2 import PasswordHasher
from pydantic import BaseModel
from database import get_db
from models import Users
from schemas import UserCreate

auth_router = APIRouter()
ph = PasswordHasher()

class LoginRequest(BaseModel):
    email: str
    password: str

@auth_router.post("/auth/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(Users).filter(Users.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = ph.hash(user.password)
    new_user = Users(
        username=user.username,
        email=user.email,
        password=hashed_pw,
        department=user.department
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

@auth_router.post("/auth/login")
def login_user(login: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.email == login.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    try:
        ph.verify(user.password, login.password)
        return {"message": "Login successful", "username": user.username}
    except:
        raise HTTPException(status_code=401, detail="Invalid credentials")
