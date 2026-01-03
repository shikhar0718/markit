# models.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from database import Base
from datetime import datetime, timezone


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)

    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(15), nullable=False)

    role = Column(String(20), nullable=False)   # seller / customer 
    is_active = Column(Boolean, default=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda:datetime.now(timezone.utc)
        )


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)          # price in paise

    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    is_active = Column(Boolean, default=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda:datetime.now(timezone.utc)
        )
    
class Category(Base):
    __tablename__="categories"

    id=Column(Integer,primary_key=True)
    admin_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    name=Column(String(100),nullable=False)

    is_active=Column(Boolean,default=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
    
