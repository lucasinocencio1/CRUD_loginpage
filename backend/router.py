from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from argon2 import PasswordHasher
from database import get_db
from schemas import UserCreate, UserUpdate, UserResponse
from models import Users
from crud import (
    get_all_users,
    get_users_by_id,
    get_users_by_email,
    create_user,
    delete_user_by_email,
    update_user_by_email
)

router = APIRouter()
ph = PasswordHasher()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/users", response_model=UserResponse)
def create_user_route(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user
    Args:
        user: UserCreate
        db: Session
    Returns:
        User: User object
    """
    return create_user(db=db, user=user)

@router.get("/users/id/{user_id}", response_model=UserResponse)
def get_user_by_id_route(user_id: int, db: Session = Depends(get_db)):
    """
    Get a user by their ID
    Args:
        user_id: int
        db: Session
    Returns:
        User: User object
    """
    user = get_users_by_id(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/email/{user_email}", response_model=UserResponse)
def get_user_by_email_route(user_email: str, db: Session = Depends(get_db)):
    """
    Get a user by their email
    Args:
        user_email: str
        db: Session
    Returns:
        User: User object
    """
    user = get_users_by_email(db=db, email=user_email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users", response_model=List[UserResponse])
def get_users_route(db: Session = Depends(get_db)):
    """
    Get all users
    Args:
        db: Session
    Returns:
        List[User]: List of User objects
    """
    return get_all_users(db=db)

@router.delete("/users/email/{user_email}", response_model=UserResponse)
def delete_user_route(user_email: str, db: Session = Depends(get_db)):
    """
    Delete a user by their email
    Args:
        user_email: str
        db: Session
    Returns:
        User: User object
    """
    user = delete_user_by_email(db=db, user_email=user_email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/email/{user_email}", response_model=UserResponse)
def update_user_route(user_email: str, user: UserUpdate, db: Session = Depends(get_db)):
    """
    Update a user by their email
    Args:
        user_email: str
        user: UserUpdate
        db: Session
    Returns:
        User: User object
    """
    user = update_user_by_email(db=db, user_email=user_email, user=user)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/auth/register")
def register_user_route(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    Args:
        user: UserCreate
        db: Session
    Returns:
        dict: Message confirming user creation
    """
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

@router.post("/auth/login")
def login_user_route(login: LoginRequest, db: Session = Depends(get_db)):
    """
    Login user
    Args:
        login: LoginRequest
        db: Session
    Returns:
        dict: Message with username on successful login
    """
    user = db.query(Users).filter(Users.email == login.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    try:
        ph.verify(user.password, login.password)
        return {"message": "Login successful", "username": user.username}
    except:
        raise HTTPException(status_code=401, detail="Invalid credentials")
