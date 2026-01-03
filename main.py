from fastapi import FastAPI,HTTPException
import re
from database import engine 
from model import User,Product,Category
from database import Base
from database import SessionLocal


app= FastAPI()

Base.metadata.create_all(bind=engine)



#  USER


@app.post("/users")
def create_user(
    first_name: str,
    last_name: str,
    email: str,
    phone: str,
    role: str
):
    db=SessionLocal()

    # Name validation
    if len(first_name.strip()) < 2 or len(last_name.strip()) < 2:
        raise HTTPException(status_code=400, detail="Name too short")

    # Email format validation
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_regex, email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    # Check duplicate email
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    # role validation
    allowed_roles=["seller", "customer","admin"]

    if role not in allowed_roles:
        raise HTTPException(status_code=400, detail="Invalid role")

    if role == "admin":
        raise HTTPException(status_code=403, detail="Admin cannot be self-created")

    
    user = User(
        first_name=first_name.strip(),
        last_name=last_name.strip(),
        email=email.lower(),
        phone=phone,
        role=role
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"msg":"user added",
            "user_id": user.id}


@app.get("/users")
def get_all_user():
    db=SessionLocal()
    users=db.query(User).all()
    return users


#  PRODUCT

@app.post("/products")
def add_product(
    name: str,
    price: int,
    seller_id: int,
    category_id: int,
):
    db = SessionLocal()

    # Product name validation
    if len(name.strip()) < 3:
        raise HTTPException(status_code=400, detail="Product name too short")

    # Price validation
    if price <= 0:
        raise HTTPException(status_code=400, detail="Price must be greater than 0")

    # Seller existence check
    seller = db.query(User).filter(User.id == seller_id).first()
    if seller is None:
        raise HTTPException(status_code=404, detail="Seller not found")

    # Seller role check
    if seller.role != "seller":
        raise HTTPException(status_code=403, detail="Only seller can add product")
    
    # category check
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.is_active == True
    ).first()

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found or inactive")



    product = Product(
        name=name.strip(),
        price=price,
        seller_id=seller_id,
        category_id=category_id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return {
        "msg": "product created successfully",
        "product_id": product.id
    }


@app.get("/products")
def get_all_product():
    db=SessionLocal()

    product=db.query(Product).all()
    return product

#  CATEGORIES

@app.post("/categories")
def add_category(name:str,
                 admin_id:int):
    db=SessionLocal()

    if len(name.strip()) < 3:
        raise HTTPException(status_code=400, detail="Category name too short")
    
    admin = db.query(User).filter(User.id == admin_id).first()

    if admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")

    if admin.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create category")

    # duplicate category check (VERY IMPORTANT)
    existing = db.query(Category).filter(Category.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")

    
    category=Category(name=name.strip())

    db.add(category)
    db.commit()
    db.refresh(category)

    return {
        "msg": "category created successfully",
        "category_id": category.id
    }

@app.get("/categories")
def view_all_categories():
    db=SessionLocal()

    category=db.query(Category).all()
    return category

