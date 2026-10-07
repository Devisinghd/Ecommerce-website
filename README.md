# Ecommerce Website

A Django-based e-commerce backend built for real-world online shopping workflows, including catalog management, seller tools, cart logic, checkout, authentication, and API documentation.

## Project Summary

This repository is a production-ready e-commerce backend built with Django and Django REST Framework. It supports online shopping features such as product browsing, seller product management, authentication, cart handling, order creation, address management, and interactive API documentation.

The project is designed to be practical, extensible, and deployment-ready for real-world use on cloud platforms and containerized environments.

## Why this project matters

This project demonstrates a complete backend architecture for an online store, including:

- secure user authentication with JWT
- separate seller and customer workflows
- order and checkout logic
- database-backed inventory and cart handling
- API documentation for faster onboarding
- Docker and deployment-ready configuration for modern hosting providers

## Features

- Product catalog and seller product CRUD
- Customer-facing product browsing and search
- Add-to-cart and cart update flows
- Checkout and order creation workflow
- Shipping address management
- Order history and order item tracking
- JWT authentication with access and refresh tokens
- Interactive API documentation via Swagger and ReDoc
- PostgreSQL-ready configuration
- Docker-based setup and production-friendly deployment patterns

## Tech Stack

- Python 3.11+
- Django 5.2.12
- Django REST Framework
- PostgreSQL
- djangorestframework-simplejwt
- drf-spectacular
- Gunicorn
- Docker

## Project Structure

- `myapp/` — storefront, product views, and templates
- `cart/` — cart logic and cart-related workflows
- `orders/` — order, item, and address management
- `users/` — authentication and user management
- `seller/` — seller dashboard and product management
- `mysite/` — Django settings and core project configuration
- `media/` — uploaded image storage
- `staticfiles/` — generated static assets for deployment
- `requirements.txt` — Python dependencies
- `dockerfile` — production containerization
- `docker-compose.yml` — local Docker orchestration

## Demo

The configured [deployment](https://ecommerce-website-coral-gamma.vercel.app/) returned an HTTP 500 error when checked on October 7, 2026. Use the local setup below until the hosted demo is available again.

## Local Setup

1. Clone the repository

```bash
git clone https://github.com/Devisinghd/Ecommerce-website.git
cd Ecommerce-website
```

2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Copy environment settings

```bash
copy .env.example .env
```

5. Update `.env` with your real configuration values

- `DJANGO_SECRET_KEY`
- `DEBUG`
- PostgreSQL database credentials
- Email configuration if needed

6. Run database migrations

```bash
python manage.py migrate
```

7. Start the development server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## API Documentation

After starting the server, visit:

- Swagger UI: `http://localhost:8000/api/swagger-ui/`
- ReDoc: `http://localhost:8000/api/redoc/`
- OpenAPI schema: `http://localhost:8000/api/schema/`

## Deployment Notes

This project is suitable for deployment on platforms such as:

- Render
- Railway
- AWS ECS / Fargate
- Azure App Service
- Google Cloud Run

Recommended production steps:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn mysite.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

## Contribution Guidelines

Contributions are welcome. Please read [CONTRIBUTING.md](./CONTRIBUTING.md) before submitting changes.

We also provide a set of beginner-friendly task ideas in [GOOD_FIRST_ISSUES.md](./GOOD_FIRST_ISSUES.md).

## Code of Conduct

Please review our community expectations in [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).

## License

This project is licensed under the [MIT License](./LICENSE).

## Resume-Friendly Summary

This project is a Django-based e-commerce backend with secure JWT authentication, product management, cart workflows, checkout and order handling, address tracking, and API documentation. It combines backend architecture, deployment readiness, and real-world business logic in a practical full-stack portfolio project.

## Author

Developed by Devisingh Dangi.
