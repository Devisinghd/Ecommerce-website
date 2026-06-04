# ShopFusion — Django E-Commerce Website

ShopMate is a Django-based e-commerce application built to demonstrate a complete shopping experience. The project includes product browsing, user authentication, cart management, checkout flows, email verification, and order handling.

## ✅ Features

- User registration, login, logout, and profile management
- Product listing and detail pages with image handling
- Shopping cart operations with AJAX-powered add-to-cart
- Order checkout flow with shipping address collection
- Email verification and password reset support
- Modular Django app structure for maintainability
- Admin dashboard for product and user management

## 🧱 Project Structure

- `myapp/` — core storefront and product pages
- `cart/` — shopping cart logic and templates
- `orders/` — checkout, address, and order workflows
- `users/` — authentication, registration, verification, and profile views
- `mysite/` — Django project settings and URL configuration
- `media/` — uploaded product images
- `db.sqlite3` — local development database

## 💻 Tech Stack

- Python 3.11+
- Django 5.0.3
- SQLite for development
- Tailwind CSS via CDN for styling
- jQuery for cart interaction and basic AJAX

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/devisinghd/Ecommerce-website.git
cd Ecommerce-website
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Run the development server

```bash
python manage.py runserver
```

Open your browser at `http://127.0.0.1:8000/`.

## 🔧 Admin Access

Create a Django superuser to manage products, users, and orders:

```bash
python manage.py createsuperuser
```

Then visit:

```text
http://127.0.0.1:8000/admin/
```

## 📌 Notes

- This project currently uses SQLite for development. For production, switch to PostgreSQL, MySQL, or another supported database.
- Tailwind is loaded through CDN in templates, making setup simple for prototype development.
- The project structure is designed to be extensible, so adding payments, search, and marketplace features is straightforward.

## 🚧 Potential Enhancements

- Add payment gateway integration (Stripe, Razorpay, PayPal)
- Improve product search and filtering
- Add order history and customer dashboards
- Implement responsive mobile navigation and cart animation
- Deploy to a managed cloud platform

## 🤝 Contributing

Contributions, bug reports, and enhancements are welcome. Please fork the repository and submit a pull request.

## 👤 Author

Developed by Dev Dangi

---

