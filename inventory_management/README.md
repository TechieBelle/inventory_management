# 🛒 Inventory Management API (Django + DRF)

A **personal inventory management system** built with **Django Rest Framework (DRF)**.  
Each user can register, login, and manage their own inventory items, while admins can manage categories and audit the system.

---

## 🚀 Features

### ✅ Core Features
- User registration & JWT authentication (login/refresh).
- Users can **CRUD their own inventory items**:
  - Fields: `name`, `description`, `quantity`, `price`, `category`, `date_added`, `last_updated`.
- Automatic **change logging** for:
  - Quantity changes (restock/sale).
  - Price changes (increase/decrease).
  - Item deletions.
- Item history (`/items/{id}/history/`).
- System audit logs (`/items/audit/`).
- Filters, search, ordering, pagination.

### ✅ Admin Features
- Manage categories (CRUD).
- View all users’ inventory & logs.
- Promote/demote users (via Django Admin).

### 🔮 Stretch Goals (Future)
- Low-stock alerts (email/in-app).
- Supplier management.
- Inventory reports (stock valuation, sales).
- Multi-store support.

---

## 🛠️ Tech Stack

- Python 3.12+
- Django 5.x
- Django Rest Framework (DRF)
- PostgreSQL (Heroku) / SQLite (local dev)
- JWT Authentication (`djangorestframework-simplejwt`)
- `dj-database-url` + `whitenoise` (deployment)

---

## 📦 Installation (Local Dev)

1. Clone repo:
   ```bash
   git clone https://github.com/TechieBelle/inventory_management.git
   cd inventory_management

2. Create & activate virtual env:
    python -m venv venv
    source venv/bin/activate   # Linux/Mac
    venv\Scripts\activate      # Windows

3. Install dependencies:
    pip install -r requirements.txt

4. Run migrations:
    python manage.py migrate

5. Create superuser:
    python manage.py createsuperuser

6. Run server:
    python manage.py runserver
    API available at → http://127.0.0.1:8000/api/

| Method | Endpoint                                      | Description                        | Access         |
| ------ | --------------------------------------------- | ---------------------------------- | -------------- |
| POST   | `/api/accounts/register/`                     | Register new user                  | Public         |
| POST   | `/api/accounts/auth/token/`                   | Login (JWT)                        | Public         |
| POST   | `/api/accounts/auth/token/refresh/`           | Refresh token                      | Auth users     |
| GET    | `/api/inventory/categories/`                  | List categories                    | All users      |
| POST   | `/api/inventory/categories/`                  | Create category                    | Admin only     |
| GET    | `/api/inventory/items/`                       | List user’s items (filters/search) | Auth users     |
| POST   | `/api/inventory/items/`                       | Create item                        | Auth users     |
| PUT    | `/api/inventory/items/{id}/`                  | Update item                        | Owner/Admin    |
| DELETE | `/api/inventory/items/{id}/`                  | Delete item                        | Owner/Admin    |
| GET    | `/api/inventory/items/low_stock/?threshold=5` | Low-stock items                    | Auth users     |
| GET    | `/api/inventory/items/{id}/history/`          | Item change history                | Owner/Admin    |
| GET    | `/api/inventory/items/audit/`                 | System-wide audit logs             | Admin sees all |
| GET    | `/api/inventory/logs/`                        | Change logs (filterable)           | Auth users     |


🌐 Deployment - Heroku

Install CLI:

heroku login


Create app:

heroku create inventory-capstone-api


Push code:

git push heroku main


Run migrations:

heroku run python manage.py migrate


Create superuser:

heroku run python manage.py createsuperuser


API live at → https://inventory-capstone-api.herokuapp.com/api/