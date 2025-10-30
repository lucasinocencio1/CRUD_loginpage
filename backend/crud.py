from sqlalchemy.orm import Session
from datetime import datetime
from argon2 import PasswordHasher #add to create the hash of the password
from models import Users
from schemas import UserCreate, UserUpdate

ph = PasswordHasher()

def get_users_by_id(db: Session,user_id: int):
    """
    Get a user by their ID
    Args:
        db: Session
        user_id: int
    Returns:
        User: User object
    """

    return db.query(Users).filter(Users.id == user_id).first()

def get_users_by_email(db: Session,email: str):
    """
    Get a user by their email
    Args:
        db: Session
        email: str
    Returns:
        User: User object
    """

    return db.query(Users).filter(Users.email == email).first()

def get_all_users(db: Session):
    """
    Get all users
    Args:
        db: Session
    Returns:
        List[User]: List of User objects
    """
    return db.query(Users).all()

def create_user(db: Session,user: UserCreate):
    """
    Create a new user
    Args:
        db: Session
        user: UserCreate
    Returns:
        User: User object
    """
    db_user = Users(**user.model_dump()) #convert the UserCreate object to a dictionary
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user_by_email(db: Session,user_email: str):
    """
    Delete a user by their ID
    Args:
        db: Session
        user_id: int
    Returns:
        User: User object
    """
    db_user = db.query(Users).filter(Users.email == user_email).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


# def update_user_by_email(db: Session, user_email: str, user: UserUpdate):
#     """
#     Update a user by their email (case-insensitive)
#     Args:
#         db: Session
#         user_email: str
#         user: UserUpdate
#     Returns:
#         User: Updated User object or None if not found
#     """

#     # Normalize the email (lowercase and no spaces)
#     user_email = user_email.strip().lower()

#     # Search for the user
#     db_user = db.query(Users).filter(Users.email.ilike(user_email)).first()

#     if db_user is None:
#         return None
#     if user.username is not None:
#         db_user.username = user.username
#     if user.email is not None:
#         db_user.email = user.email.strip().lower()
#     if user.department is not None:
#         db_user.department = user.department
#     if user.is_active is not None:
#         db_user.is_active = user.is_active
#     if user.password is not None:
#         db_user.password = ph.hash(user.password)
    
#     db_user.updated_at = datetime.now()

    
#     db.commit()
#     db.refresh(db_user)

#     return db_user
from argon2 import PasswordHasher

ph = PasswordHasher()

def update_user_by_email(db: Session, user_email: str, user: UserUpdate):
    db_user = db.query(Users).filter(Users.email == user_email).first()
    
    if not db_user:
        return None
    
    update_data = user.dict(exclude_unset=True)
    
    # Se está atualizando senha, hashear!
    if "password" in update_data and update_data["password"]:
        update_data["password"] = ph.hash(update_data["password"])
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user
