from fastapi import FastAPI, HTTPException
from database import engine, Base, SessionLocal
from model import User, Product, Category
from schema import (
    UserCreate, UserUpdate,
    ProductCreate, ProductUpdate
)

app = FastAPI()
Base.metadata.create_all(bind=engine)

# USER

@app.post("/users")
def create_user(data: UserCreate):
    db = SessionLocal()
    try:
        # business validations
        if db.query(User).filter(User.email == data.email).first():
            raise HTTPException(status_code=400, detail="Email already exists")

        if data.role not in ["seller", "customer", "admin"]:
            raise HTTPException(status_code=400, detail="Invalid role")

        if data.role == "admin":
            raise HTTPException(status_code=403, detail="Admin cannot be self-created")

        user = User(
            first_name=data.first_name.strip(),
            last_name=data.last_name.strip(),
            email=data.email.lower(),
            phone=data.phone.strip(),
            role=data.role
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return {"msg": "user added", "user_id": user.id}

    finally:
        db.close()


@app.get("/users")
def get_all_users():
    db = SessionLocal()
    try:
        return db.query(User).all()
    finally:
        db.close()


@app.patch("/users/{id}")
def update_user(id: int, data: UserUpdate, curr_user_id: int):
    db = SessionLocal()
    try:
        curr_user = db.query(User).filter(User.id == curr_user_id).first()
        if not curr_user:
            raise HTTPException(status_code=404, detail="Current user not found")

        user = db.query(User).filter(User.id == id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # only self-update
        if curr_user.id != user.id:
            raise HTTPException(status_code=403, detail="Not allowed")

        if not any(data.model_dump(exclude_unset=True).values()):
            raise HTTPException(status_code=400, detail="No data provided")

        if data.first_name is not None:
            user.first_name = data.first_name.strip()

        if data.last_name is not None:
            user.last_name = data.last_name.strip()

        if data.phone is not None:
            user.phone = data.phone.strip()

        if data.email is not None:
            existing = db.query(User).filter(
                User.email == data.email,
                User.id != user.id
            ).first()
            if existing:
                raise HTTPException(status_code=400, detail="Email already exists")

            user.email = data.email.lower()

        db.commit()
        return {"msg": "user updated", "user_id": user.id}

    finally:
        db.close()


@app.patch("/users/{id}/disable")
def disable_user(id: int, curr_user_id: int):
    db = SessionLocal()
    try:
        curr_user = db.query(User).filter(User.id == curr_user_id).first()
        user = db.query(User).filter(User.id == id).first()

        if not curr_user or not user:
            raise HTTPException(status_code=404, detail="User not found")

        if curr_user.role != "admin" and curr_user.id != user.id:
            raise HTTPException(status_code=403, detail="Not allowed")

        if user.role == "admin":
            raise HTTPException(status_code=403, detail="Admin cannot be disabled")

        if not user.is_active:
            raise HTTPException(status_code=409, detail="Already disabled")

        user.is_active = False
        db.commit()
        return {"msg": "user disabled", "user_id": user.id}

    finally:
        db.close()


@app.patch("/users/{id}/enable")
def enable_user(id: int, admin_id: int):
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.id == admin_id).first()
        user = db.query(User).filter(User.id == id).first()

        if not admin or admin.role != "admin":
            raise HTTPException(status_code=403, detail="Only admin allowed")

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.is_active:
            raise HTTPException(status_code=409, detail="Already active")

        user.is_active = True
        db.commit()
        return {"msg": "user enabled", "user_id": user.id}

    finally:
        db.close()

# PRODUCT

@app.post("/products")
def add_product(data: ProductCreate, seller_id: int):
    db = SessionLocal()
    try:
        seller = db.query(User).filter(User.id == seller_id).first()
        if not seller or seller.role != "seller":
            raise HTTPException(status_code=403, detail="Only seller can add product")

        category = db.query(Category).filter(
            Category.id == data.category_id,
            Category.is_active == True
        ).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found or inactive")

        product = Product(
            name=data.name.strip(),
            price=data.price,
            seller_id=seller_id,
            category_id=data.category_id
        )

        db.add(product)
        db.commit()
        db.refresh(product)

        return {"msg": "product created", "product_id": product.id}

    finally:
        db.close()


@app.get("/products")
def get_products():
    db = SessionLocal()
    try:
        return db.query(Product).filter(Product.is_active == True).all()
    finally:
        db.close()


@app.patch("/products/{id}")
def update_product(id: int, data: ProductUpdate, user_id: int):
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == id).first()
        user = db.query(User).filter(User.id == user_id).first()

        if not product or not user:
            raise HTTPException(status_code=404, detail="Not found")

        if product.seller_id != user.id and user.role != "admin":
            raise HTTPException(status_code=403, detail="Not allowed")

        if not any(data.model_dump(exclude_unset=True).values()):
            raise HTTPException(status_code=400, detail="No data provided")

        if data.name is not None:
            product.name = data.name.strip()

        if data.price is not None:
            product.price = data.price

        if data.category_id is not None:
            category = db.query(Category).filter(
                Category.id == data.category_id,
                Category.is_active == True
            ).first()
            if not category:
                raise HTTPException(status_code=404, detail="Category not found or inactive")

            product.category_id = data.category_id

        db.commit()
        return {"msg": "product updated", "product_id": product.id}

    finally:
        db.close()


@app.patch("/products/{id}/disable")
def disable_product(id: int, user_id: int):
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if product.seller_id != user.id and user.role != "admin":
            raise HTTPException(status_code=403, detail="Not allowed")

        if not product.is_active:
            raise HTTPException(status_code=409, detail="Product already disabled")

        product.is_active = False
        db.commit()

        return {"msg": "product disabled",
                 "product_id": product.id}

    finally:
        db.close()

@app.patch("/products/{id}/enable")
def enable_product(id: int, user_id: int):
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if product.seller_id != user.id and user.role != "admin":
            raise HTTPException(status_code=403, detail="Not allowed")

        if product.is_active:
            raise HTTPException(status_code=409, detail="Product already active")

        product.is_active = True
        db.commit()

        return {"msg": "product enabled", "product_id": product.id}

    finally:
        db.close()


# CATEGORY


@app.post("/categories")
def add_category(name: str, admin_id: int):
    db = SessionLocal()
    try:
        if len(name.strip()) < 3:
            raise HTTPException(status_code=400, detail="Category name too short")

        admin = db.query(User).filter(User.id == admin_id).first()
        if not admin or admin.role != "admin":
            raise HTTPException(status_code=403, detail="Only admin can create category")

        if db.query(Category).filter(Category.name == name).first():
            raise HTTPException(status_code=400, detail="Category already exists")

        category = Category(name=name.strip())
        db.add(category)
        db.commit()
        db.refresh(category)

        return {"msg": "category created", 
                "category_id": category.id}

    finally:
        db.close()


@app.get("/categories")
def get_categories():
    db = SessionLocal()
    try:
        return db.query(Category).filter(Category.is_active == True).all()
    finally:
        db.close()


@app.patch("/categories/{id}/disable")
def disable_category(id: int, admin_id: int):
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.id == admin_id).first()
        if not admin or admin.role != "admin":
            raise HTTPException(status_code=403, detail="Only admin allowed")

        category = db.query(Category).filter(Category.id == id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        if not category.is_active:
            raise HTTPException(status_code=409, detail="Category already disabled")

        category.is_active = False
        db.commit()

        return {"msg": "category disabled", 
                "category_id": category.id}

    finally:
        db.close()

@app.patch("/categories/{id}/enable")
def enable_category(id: int, admin_id: int):
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.id == admin_id).first()
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")

        if admin.role != "admin":
            raise HTTPException(status_code=403, detail="Only admin can enable category")

        category = db.query(Category).filter(Category.id == id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")

        if category.is_active:
            raise HTTPException(status_code=409, detail="Category already active")

        category.is_active = True
        db.commit()

        return {"msg": "category enabled", "category_id": category.id}

    finally:
        db.close()
