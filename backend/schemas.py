from pydantic import BaseModel, PositiveFloat, EmailStr, validator, Field
from enum import Enum
from datetime import datetime
from typing import Optional

class UserDepartment(Enum):
    HR = "HR"
    IT = "IT"
    FINANCE = "FINANCE"
    MARKETING = "MARKETING"
    SALES = "SALES"
    CUSTOMER_SERVICE = "CUSTOMER_SERVICE"
    SUPPORT = "SUPPORT"
    ADMIN = "ADMIN"
    OTHER = "OTHER"
    
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    department: UserDepartment
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
@validator("department")
def validate_department(cls, v):
    if v not in UserDepartment:
        raise ValueError("Invalid department")
    return v

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    department: UserDepartment

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    department: UserDepartment
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[UserDepartment] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None
    updated_at: datetime = Field(default_factory=datetime.now)
