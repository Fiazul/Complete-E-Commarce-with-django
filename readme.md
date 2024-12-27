# E-Commerce Project

## Overview
This is a scalable and modular e-commerce project built using Django. The project is designed to handle various functionalities such as user authentication, profile management, product catalog, categories, cart, and order processing. It is built with dynamic database capabilities to ensure seamless scalability and future integration of advanced features like machine learning models and APIs.

---

## Features

### 1. AuthenticationApp
- User registration and login.
- Email-based authentication.
- OTP verification for additional security.
- Custom user model (`CustomUser`) with fields for email and verification status.

### 2. ProfileApp
- One-to-one relationship with users.
- Fields for profile details like bio, phone, address, and profile picture.
- Support for seller identification using `is_seller` flag.

### 3. ProductApp
- Dynamic product management.
- Product variations (e.g., size, color) with price adjustments.
- Product image uploads and stock tracking.

### 4. CategoryApp
- Hierarchical category structure for product organization.
- Ability to associate products with multiple categories.
- Support for users to follow categories.

### 5. OrderApp
- Order creation and management.
- Tracks the relationship between users and their orders.
- Supports order status updates (e.g., pending, completed).

### 6. CartApp
- Manages user-specific cart items.
- Tracks product quantities and prices in the cart.
- Allows adding, updating, and removing items.


---

## Installation

### Prerequisites
- Python (>= 3.8)
- Django (>= 4.0)
- PostgreSQL 

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database:
   - Update `DATABASES` in `settings.py` to point to your PostgreSQL database.

5. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```



7. Start the development server:
   ```bash
   python manage.py runserver
   ```

---

## API Endpoints

### Authentication
- **Register User:** `POST /auth/register/`
- **Login User:** `POST /auth/login/`
- **Verify OTP:** `POST /auth/verify/`

### Profile
- **Retrieve Profile:** `GET /profile/`
- **Update Profile:** `PATCH /profile/`

### Products
- **List Products:** `GET /products/`
- **Retrieve Product Details:** `GET /products/<product_id>/`
- **Add Product (Admin):** `POST /products/`
- **Update Product (Admin):** `PATCH /products/<product_id>/`
- **Delete Product (Admin):** `DELETE /products/<product_id>/`

### Categories
- **List Categories:** `GET /categories/`
- **Retrieve Category Details:** `GET /categories/<category_id>/`
- **Add Category (Admin):** `POST /categories/`
- **Update Category (Admin):** `PATCH /categories/<category_id>/`
- **Delete Category (Admin):** `DELETE /categories/<category_id>/`

### Cart
- **Retrieve Cart:** `GET /cart/`
- **Add to Cart:** `POST /cart/`
- **Update Cart Item:** `PATCH /cart/item/<item_id>/`
- **Remove Cart Item:** `DELETE /cart/item/<item_id>/`

### Orders
- **List Orders:** `GET /orders/`
- **Retrieve Order Details:** `GET /orders/<order_id>/`
- **Create Order:** `POST /orders/`

---

## Project Structure
```plaintext
project/
├── AuthenticationApp/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── ProfileApp/
├── ProductApp/
├── CategoryApp/
├── CartApp/
├── OrderApp/
├── templates/
├── static/
├── manage.py
└── requirements.txt
```

---

## Testing

1. Use **Postman** for API testing.
2. Authenticate using the `Authorization: Bearer <access token>` header.

---

## Future Enhancements
- **WishlistApp**: Allow users to save favorite items.
- **ReviewApp**: Support user reviews and ratings for products.
- **NotificationApp**: Notify users about order updates or promotional offers.
- **AnalyticsApp**: Provide sales and user activity insights.
- **ShippingApp**: Manage shipping details and track shipments.
- **Machine Learning Integration**: Use category and product data for advanced recommendation systems.

---



## Contributors
- **Fiazul Haque** 
- **Proshanto Bhakta** 

---


