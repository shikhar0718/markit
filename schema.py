from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import re

# VALIDATION(INTERNAL USE-CASES)

def normalize_indian_phone(value: str) -> str:
    """
    Accepts:
    - 9876543210
    - +91 9876543210
    - 919876543210
    - 09876543210

    Stores:
    - 9876543210
    """
    phone = re.sub(r"\D", "", value)

    if phone.startswith("91") and len(phone) == 12:
        phone = phone[2:]
    elif phone.startswith("0") and len(phone) == 11:
        phone = phone[1:]

    if not re.match(r"^[6-9]\d{9}$", phone):
        raise ValueError("Invalid Indian mobile number")

    return phone


# USER

class UserCreate(BaseModel):
    first_name: str = Field(..., min_length=2)
    last_name: str = Field(..., min_length=2)
    email: EmailStr
    phone: str
    role: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        return normalize_indian_phone(value)


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2)
    last_name: Optional[str] = Field(None, min_length=2)
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

    @field_validator("phone")
    @classmethod
    def validate_phone_optional(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return normalize_indian_phone(value)

# PRODUCT

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=3)
    price: int = Field(..., gt=0)
    category_id: int


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3)
    price: Optional[int] = Field(None, gt=0)
    category_id: Optional[int] = None
