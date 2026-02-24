
# Bibliotheque API

A modern RESTful API for library management, built with **FastAPI** and **PostgreSQL**.

## Overview

Bibliotheque API is a robust backend application for managing books, users, and associated tags. It provides a complete API interface for CRUD (Create, Read, Update, Delete) operations on the main resources of a library.

### Main Features

- Book management
- User management
- Tag/category system
- PostgreSQL database
- Data validation with Pydantic
- Automatic API documentation with Swagger UI

---

## Prerequisites

Before you start, make sure you have installed:

- **Python** ≥ 3.11.9
- **PostgreSQL** ≥ 12
- **uv** for dependency management
- **Git**

### Install uv

**Windows** (with winget):
```powershell
winget install astral-sh.uv
```
**macOS / Linux**:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Installation

### 1. Clone the project

```bash
git clone <repository-url>
cd bibliotheque-api
```
### 2. Install dependencies

```bash
uv sync
```

This command will automatically create a virtual environment (`.venv`) and install all dependencies.

### 3. Configure environment variables

See the provided `.env.example` file and create a `.env` file at the root of the project:

```env
SUPABASE_DB_URL=postgresql+psycopg://postgres:<password>@db.<project>.supabase.co:5432/postgres
secret_key = "<your_secret_key>"
algorithm = "HS256"
access_token_expire_minutes = 70
ADMIN_EMAIL = "<admin@email.com>"
ADMIN_PASSWORD = "<admin_password>"
Admin_Username = "admin"
OpenLibrary_URL = "https://openlibrary.org"
GoogleBooks_URL = "https://www.googleapis.com/books/v1/volumes?q=isbn:"
```
Replace the values with those from your Supabase project and your secrets.

### 4. Initialize the database

```bash
python -m app.main
```
---
## Project structure
```
├── app
│   ├── core
│   │   ├── auth.py
│   │   └── security.py
│   ├── models
│   │   ├── Books.py
│   │   ├── tags.py
│   │   └── users.py
│   ├── routers
│   │   ├── auth.py
│   │   ├── books.py
│   │   ├── tags.py
│   │   └── users.py
│   ├── schemas
│   │   ├── Books.py
│   │   ├── tags.py
│   │   └── users.py
│   ├── database.py
│   └── main.py
├── .env.example
├── .gitignore
├── README.md
├── pyproject.toml
└── uv.lock
```
---

## API Endpoints

### Books (`/books`)
- `GET /books/` - Retrieve all books

### Users (`/users`)
- `GET /users/` - Retrieve all users

### Tags (`/tags`)
- `GET /tags/` - Retrieve all tags

### Root
- `GET /` - Welcome message

---

## Running the application


### Start the development server

```bash
uv run python -m uvicorn app.main:app --reload
```

The application will be available at: `http://localhost:8000`

### Access the API documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Dependencies

| Package        | Version    | Purpose                        |
|---------------|------------|--------------------------------|
| fastapi       | ≥0.128.0   | Asynchronous web framework     |
| sqlalchemy    | ≥2.0.46    | ORM for database interactions  |
| psycopg[binary]| ≥3.3.2    | PostgreSQL driver              |
| pydantic      | ≥2.12.5    | Data validation                |
| uvicorn       | ≥0.40.0    | ASGI server                    |
| python-dotenv | ≥1.2.1     | Environment variable management|
| python-jose   | ≥3.5.0     | JWT management                 |
| pytest        | ≥9.0.2     | Testing framework              |
| passlib       | ≥1.7.4     | Password hashing               |
| bcrypt        | =4.0.1     | Password hashing (backend)     |
| requests      | ≥2.32.5    | HTTP requests                  |
| ruff (dev)    | ≥0.15.1    | Linter/formatter (dev only)    |
---

## Architecture

The application follows a **layered modular architecture**:

1. **Routers**: HTTP entry points
2. **Models**: Database schemas (SQLAlchemy)
3. **Database**: Connection and session configuration
4. **Main**: FastAPI initialization and global configuration
---

## Support

For any questions or issues, please open an issue in the repository.