🔑 Authentication
Method	URL	Description
POST	/api/token/	Get access + refresh tokens (login).
POST	/api/token/refresh/	Refresh access token using refresh token.

📂 Categories
Method	URL	Description
GET	/api/inventory/categories/	List categories.
POST	/api/inventory/categories/	Create category.
GET	/api/inventory/categories/{id}/	Retrieve one category.
PUT	/api/inventory/categories/{id}/	Update category.
DELETE	/api/inventory/categories/{id}/	Delete category.

📦 Items
Method	URL	Description
GET	/api/inventory/items/	List items (supports filters/search/order). |h
POST	/api/inventory/items/	Create item.
GET	/api/inventory/items/{id}/	Retrieve item.
PUT	/api/inventory/items/{id}/	Update item (triggers logs).
DELETE	/api/inventory/items/{id}/	Delete item.

🔎 Special Item Endpoints
Method	URL	Description
GET	/api/inventory/items/{id}/history/	Item’s change history.
GET	/api/inventory/items/{id}/audit/	Item’s audit trail (quantity + price).
GET	/api/inventory/items/low_stock/?threshold=5	All items below stock threshold.

📊 Filtering Examples

/api/inventory/items/?search=laptop → search by name.

/api/inventory/items/?category=1 → filter by category ID.

/api/inventory/items/?price__gte=1000&price__lte=2000 → filter by price range.

/api/inventory/items/?quantity__lte=5 → low stock items.

/api/inventory/items/?ordering=-price → sort by descending price.

📜 Change Logs
Method	URL	Description
GET	/api/inventory/changes/	List logs for your items only.
GET	/api/inventory/changes/{id}/	Retrieve one log entry.
GET	/api/inventory/changes/?field_changed=price	Filter logs by field.
GET	/api/inventory/changes/?change_type=restock	Filter logs by type.
GET	/api/inventory/changes/?search=laptop	Search logs by item name.
GET	/api/inventory/changes/?ordering=-timestamp	Sort logs (latest first).


✅ Checklist to Test in Postman

POST /api/token/ → Login (get tokens).

POST /api/token/refresh/ → Refresh token.

POST /api/inventory/categories/ → Create a category.

GET /api/inventory/categories/ → List categories.

POST /api/inventory/items/ → Create an item.

GET /api/inventory/items/ → List items.

PUT /api/inventory/items/{id}/ → Update item (logs created).

GET /api/inventory/changes/ → View logs.

GET /api/inventory/items/audit/ → Audit trail for one item.

GET /api/inventory/items/low_stock/?threshold=5 → Check low stock.

Test filters/search/sorting on /items/ and /changes/.