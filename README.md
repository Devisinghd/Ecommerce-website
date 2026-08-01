# Ecommerce Website

## Project Summary
This is a production-ready Django e-commerce backend with PostgreSQL, secure JWT APIs, seller product management, shopping cart and checkout workflows, address handling, order history, and interactive API documentation.

## Why this project matters
This repository demonstrates a real-world backend implementation for a modern e-commerce application. It combines clean Django architecture, REST API design, security best practices, and deployment-ready configuration for container-based platforms such as Render, Railway, AWS, and others.

## ✅ What has been implemented

- Full product catalog and seller product CRUD
- Customer-facing product browsing and search
- Shopping cart operations and checkout flow
- Address management for shipping and checkout
- Order creation, order items, and order history tracking
- JWT authentication with access and refresh tokens
- API documentation with Swagger UI and ReDoc
- Dockerized production build using Gunicorn
- PostgreSQL-ready deployment configuration

## 🧱 Project Structure

- `myapp/` — storefront views, product APIs, and frontend templates
- `cart/` — shopping cart logic and cart context injection
- `orders/` — order, order item, and address models and workflows
- `users/` — authentication, user registration, and token handling
- `seller/` — seller dashboard and product management
- `mysite/` — Django settings, URL routing, and WSGI configuration
- `media/` — persisted uploaded product images
- `requirements.txt` — Python dependencies
- `Dockerfile` — containerized production build
- `docker-compose.yml` — local Docker stack with PostgreSQL

## 💻 Tech Stack

- Python 3.11+
- Django 5.2.12
- Django REST Framework
- PostgreSQL
- REST authentication via `djangorestframework-simplejwt`
- OpenAPI docs via `drf-spectacular`
- `gunicorn` for production WSGI serving
- Docker for containerization

## 🚀 Local setup

1. Clone the repository

```bash
git clone https://github.com/devisinghd/Ecommerce-website.git
cd Ecommerce-website
```

2. Copy the environment example

```bash
copy .env.example .env
```

3. Update `.env`

- Set a real `DJANGO_SECRET_KEY`
- Set `DEBUG=False` for production or `DEBUG=True` for local development
- Configure PostgreSQL database credentials
- Configure email settings if needed

4. Create and activate a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

5. Install dependencies

```bash
pip install -r requirements.txt
```

6. Run migrations

```bash
python manage.py migrate
```

7. Run the development server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in the browser.

## 📚 API documentation

- Swagger UI: `http://localhost:8000/api/swagger-ui/`
- ReDoc: `http://localhost:8000/api/redoc/`
- OpenAPI schema: `http://localhost:8000/api/schema/`

## 🌐 Deployment readiness

This app is ready to deploy on any container-capable service, including:

- Render
- Railway
- AWS ECS / Fargate
- AWS Elastic Beanstalk
- Google Cloud Run
- Azure App Service

### What makes it ready

- Environment-based configuration for secrets and database
- PostgreSQL support via `DATABASE_URL`
- Production WSGI server (`gunicorn`)
- Static collection configured with `STATIC_ROOT`
- Secure cookie and SSL proxy settings are enabled when `DEBUG=False`
- API docs and clean endpoint structure

### Recommended production commands

- Build dependencies:

```bash
pip install -r requirements.txt
```

- Run migrations:

```bash
python manage.py migrate
```

- Collect static assets:

```bash
python manage.py collectstatic --noinput
```

- Start the server:

```bash
gunicorn mysite.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

## ☁️ Cloud deployment notes

### Render

- Use Docker or the Python service mode.
- Set env vars: `DJANGO_SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `DATABASE_URL`, and email settings.

### Railway

- Use the Dockerfile or Python service.
- Railway provides a PostgreSQL add-on; wire it using `DATABASE_URL`.

### AWS ECS / Fargate

- Build a Docker image and push to ECR.
- Use a managed RDS PostgreSQL instance or AWS Postgres service.
- Set environment variables in your task definition.

## 👩‍💼 Shopfusion summary

This project is built as a complete backend service for an e-commerce application. It demonstrates:

- scalable Django architecture with separated app responsibilities
- REST API design and documentation
- secure authentication and user session handling
- production-grade configuration and Docker deployment
- order and checkout workflows with shipping address support

It is ready for production deployment and designed for easy extension with payment, search, analytics, and marketplace features.

## 👤 Author

Developed by Dev Dangi

