import random
from sqlalchemy.orm import Session

from database import SessionLocal
from model import User, Category, Product


# ---------- NAME POOLS ----------
SELLER_NAMES = [
    ("Ramesh", "Gupta"), ("Suresh", "Agarwal"), ("Mahesh", "Jain"),
    ("Prakash", "Verma"), ("Anil", "Sharma"), ("Vijay", "Bansal"),
    ("Ashok", "Mittal"), ("Rajesh", "Goyal"), ("Sunil", "Khanna"),
    ("Deepak", "Singhal"), ("Manoj", "Tiwari"), ("Naresh", "Patel"),
    ("Dinesh", "Mehta"), ("Harish", "Chopra"), ("Alok", "Srivastava"),
]

CUSTOMER_NAMES = [
    ("Aarav", "Singh"), ("Vihaan", "Sharma"), ("Riya", "Verma"),
    ("Ananya", "Gupta"), ("Aditya", "Mishra"), ("Kavya", "Jain"),
    ("Ishaan", "Malhotra"), ("Neha", "Agarwal"), ("Sanya", "Kapoor"),
    ("Rahul", "Yadav"), ("Pooja", "Pandey"), ("Kunal", "Tripathi"),
    ("Sneha", "Chaturvedi"), ("Arjun", "Rawat"), ("Muskan", "Saxena"),
    ("Ayush", "Bhardwaj"), ("Nikhil", "Chauhan"), ("Simran", "Kohli"),
    ("Tanmay", "Rastogi"), ("Aditi", "Shukla"),
]

PRICE_MAP = {
    "Laptop": (4000000, 12000000),
    "Mobile": (1200000, 8000000),
    "Headphones": (80000, 800000),
    "Smart Watch": (200000, 3000000),
    "Keyboard": (70000, 500000),
    "T-Shirt": (49900, 199900),
    "Shoes": (150000, 700000),
    "Backpack": (99900, 399900),
    "Notebook": (9900, 39900),
    "Coffee Mug": (19900, 69900),
}

PRODUCT_CATALOG = {
    "Electronics": ["Laptop", "Mobile", "Headphones", "Smart Watch", "Keyboard"],
    "Fashion": ["T-Shirt", "Shoes", "Backpack"],
    "Books & Stationery": ["Notebook"],
    "Home & Kitchen": ["Coffee Mug"],
    "Accessories": ["Headphones", "Backpack"],
}


def seed_users(db: Session):
    print("🌱 Seeding users...")

    # ADMIN (FIRST)
    admin = User(
        first_name="Admin",
        last_name="Markit",
        email="admin@markit.com",
        phone="9999999999",
        role="admin"
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)

    # SELLERS (12–15)
    sellers = []
    seller_count = random.randint(12, 15)
    seller_names = random.sample(SELLER_NAMES, seller_count)

    for i, (fn, ln) in enumerate(seller_names):
        seller = User(
            first_name=fn,
            last_name=ln,
            email=f"seller{i+1}@markit.com",
            phone=f"98{random.randint(10000000,99999999)}",
            role="seller"
        )
        sellers.append(seller)
        db.add(seller)

    # CUSTOMERS (TOTAL USERS ≥ 50)
    remaining = 50 - seller_count - 1
    customer_names = random.choices(CUSTOMER_NAMES, k=remaining)

    for i, (fn, ln) in enumerate(customer_names):
        customer = User(
            first_name=fn,
            last_name=ln,
            email=f"customer{i+1}@markit.com",
            phone=f"97{random.randint(10000000,99999999)}",
            role="customer"
        )
        db.add(customer)

    db.commit()
    print("✅ Users seeded")
    return admin, sellers


def seed_categories(db: Session, admin):
    print("🌱 Seeding categories...")

    categories = []
    for name in PRODUCT_CATALOG.keys():
        category = Category(
            name=name,
            admin_id=admin.id,
            is_active=True
        )
        categories.append(category)
        db.add(category)

    db.commit()
    return categories


def seed_products(db: Session, sellers, categories):
    print("🌱 Seeding products...")

    total = 0
    for seller in sellers:
        primary_category = random.choice(categories)
        product_types = PRODUCT_CATALOG[primary_category.name]

        chosen = random.sample(product_types, k=min(3, len(product_types)))

        for product_name in chosen:
            min_p, max_p = PRICE_MAP[product_name]

            for _ in range(random.randint(2, 5)):
                product = Product(
                    name=product_name,
                    price=random.randint(min_p, max_p),
                    seller_id=seller.id,
                    category_id=primary_category.id
                )
                db.add(product)
                total += 1

    db.commit()
    print(f"✅ {total} product rows seeded")


def run():
    print("\n🚀 MARKIT DB SEEDING STARTED\n")
    db = SessionLocal()

    try:
        admin, sellers = seed_users(db)
        categories = seed_categories(db, admin)
        seed_products(db, sellers, categories)
        print("\n🎉 MARKIT DATABASE READY (REALISTIC DATA)")
    finally:
        db.close()


if __name__ == "__main__":
    run()
