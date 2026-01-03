🛒 Markit:

Markit is a backend-focused e-commerce application built using FastAPI and SQLAlchemy, designed with role-based access control and scalable architecture in mind.
The project currently focuses on strong backend fundamentals such as database modeling, CRUD APIs, and business-rule enforcement.
Advanced features will be added incrementally, following real-world backend practices.


🚀 Tech Stack:

1- Backend Framework: FastAPI
2- ORM: SQLAlchemy
3- Database: SQLite (development)
4- Language: Python
5- Version Control: Git


🧩 Core Entities (Current Implementation):
1) 👤 User

Supported roles:
1- admin
2- seller
3- customer

.Admin users are seeded manually (cannot self-register)
.Sellers can create products
.Customers can browse products

2) 📦 Product

Can be created only by sellers
Each product is linked to:
. a seller
. a category

Includes validations for:
. product name
. price
. 🗂 Category
1. Can be created only by admin
2. Supports soft enable/disable using is_active
3. Products can be added only to active categories

🔐 Role-Based Rules (Implemented):
Action	           Admin	Seller	Customer
View Users	        ✅	    ❌	   ❌
Create Category	    ✅	    ❌	   ❌
Add Product	        ❌	    ✅	   ❌
View Products	    ✅	    ✅	   ✅

⚠️ Note:
Authentication is not implemented yet.
Role validation is currently enforced using request parameters and database checks.


📡 API Endpoints (Current):
1) 👤 Users
. POST /users → Create customer or seller
. GET /users → Get all users

2) 🗂 Categories
. POST /categories → Create category (admin only)
. GET /categories → View all categories

3) 📦 Products
. POST /products → Add product (seller only)
. GET /products → View all products


🧪 Data Seeding:

To simulate a real-world e-commerce database, a custom seeding script will populate:
. 1 Admin
. Multiple Sellers
. Multiple Customers
. 10–15 Categories
. 100+ Products


🛣 Roadmap (Upcoming Features)
Planned future enhancements:

 JWT-based authentication
 Admin-protected routes using dependencies
 Product update & delete APIs
 User profile update & delete
 Cart & Order system
 Pagination and filtering
 Environment-based configuration
 Docker support
 Production database (PostgreSQL)

📁 Project Structure:
.
├── main.py        # API routes
├── model.py       # Database models
├── database.py    # DB connection & session
├── readme.md
└── .gitignore


🎯 Project Philosophy:
✅ Clean role-based logic
✅ Incremental feature development
✅ Real-world backend patterns
✅ Interview-ready architecture
✅ Honest documentation


📌 Project Status:
  🟢 Active Development
      Markit is under continuous development.
      New features will be added step by step with proper Git commits and documentation updates.

👤 Author:
    Shikhar
    Backend Developer | Learning FastAPI & System Design