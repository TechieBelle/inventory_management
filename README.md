# 📦 Inventory Management API  

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.x-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.x-red.svg)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13%2B-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)](LICENSE)
[![Heroku](https://img.shields.io/badge/Deploy-Heroku-purple.svg)](https://heroku.com)

An API built with **Django** and **Django REST Framework (DRF)** to manage products, categories, stock levels, and transactions for a retail or mini-mart system.  
This project is part of my **capstone project at ALX Africa**.  

---

Features

✅ User Authentication (JWT login/refresh)

✅ CRUD for Inventory Items (Create, Read, Update, Delete)

✅ Automatic Change Logging for quantity & price updates

✅ Audit Trail: See full history of changes per item

✅ Categories Management (add, update, delete categories)

✅ Filtering, Searching, Ordering, Pagination

✅ Low Stock Endpoint (/items/low_stock/)

 Stretch Goals: low stock alerts, supplier management, reports, barcode scanning, multi-store suppo

## 🛠️ Tech Stack  
| Technology        | Purpose                          |
|-------------------|----------------------------------|
| Django            | Backend framework                |
| Django REST Framework | Build RESTful APIs          |
| PostgreSQL        | Relational database              |
| python-decouple / python-dotenv | Environment variables |
| Gunicorn          | WSGI server for deployment       |
| Heroku            | Cloud deployment   


           
## ⚙️ Setup & Installation  

### 📁 1. Clone the repository  
```bash
git clone https://github.com/<your-username>/inventory_management.git
cd inventory_management
```

### 🧪 2. Create and activate a virtual environment  
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 📦 3. Install dependencies  
```bash
pip install -r requirements.txt
```

### 🔑 4. Create a `.env` file in the root directory  
```ini
# .env
SECRET_KEY=your_django_secret_key
DEBUG=True
DATABASE_URL=postgres://postgres:yourpassword@localhost:5432/inventory_db
```

### 🛠 5. Run migrations  
```bash
python manage.py makemigrations
python manage.py migrate
```

### 👩‍💻 6. Create a superuser  
```bash
python manage.py createsuperuser
```

### ▶️ 7. Run the development server  
```bash
python manage.py runserver
```

---

API Endpoints
🔹 Inventory Items

GET /api/inventory/items/ → List items

POST /api/inventory/items/ → Create item

GET /api/inventory/items/{id}/ → Retrieve item

PUT /api/inventory/items/{id}/ → Update item

DELETE /api/inventory/items/{id}/ → Delete item

GET /api/inventory/items/{id}/history/ → View change history for one item

GET /api/inventory/items/{id}/audit/ → View audit trail (price + stock changes)

GET /api/inventory/items/low_stock/?threshold=5 → List items below stock threshold

---

## 📦 Project Structure  

```
inventory_management/
├── inventory_management/     # Main project settings
├── api/                      # Your API app (models, serializers, views)
├── requirements.txt
├── .env                      # Environment variables
├── .gitignore
├── README.md
└── manage.py

/api/inventory/items/?price__gte=100&price__lte=500

/api/inventory/items/?quantity__lte=5

/api/inventory/items/?category=2

/api/inventory/items/?date_added__gte=2025-08-01

/api/inventory/items/?ordering=-price

/api/inventory/items/?search=laptop

## 🧑‍💻 Author  

**Folashade Bello**  
- 💼 GitHub: https://github.com/TechieBelle/FolashadeBello
- 🔗 LinkedIn: https://www.linkedin.com/in/folashadebello/

---

## 📜 License  
This project is licensed under the MIT License.  

---

 _This project is actively being developed. Stay tuned for more updates and endpoints!_
