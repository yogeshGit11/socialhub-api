# 🌐 Social Hub — FastAPI Backend

A **FastAPI-powered social media backend** that enables users to create accounts, publish posts, comment, and engage in real-time conversations.  
It supports **JWT authentication**, **background tasks** (via Celery + Redis), **database migrations** (via Alembic), and **WebSocket-based live updates** — all built with a clean, scalable architecture.

---

## 📋 Project Overview

**Social Hub** is a backend API for a social media platform that offers:
- Secure **user authentication** and profile management  
- **Post creation**, likes, and comment features  
- **Real-time notifications and updates** via WebSockets  
- **Email service** for account notifications and async communication  
- Built-in **rate limiting** and **request logging middleware**  
- **Redis integration** for Celery tasks and rate limit storage  

---

## ⚙️ Tech Stack

| Component | Technology |
|------------|-------------|
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) |
| **ORM** | [SQLAlchemy](https://www.sqlalchemy.org/) |
| **Migrations** | [Alembic](https://alembic.sqlalchemy.org/) |
| **Background Tasks** | [Celery](https://docs.celeryq.dev/) + Redis |
| **Real-time Communication** | WebSockets |
| **Database** | SQLite (default) / MySQL (configurable) |
| **Authentication** | JWT (JSON Web Tokens) |
| **Rate Limiting** | Redis-based throttling |
| **Email** | SMTP via Celery tasks |

---

## 🧩 Project Structure

```
.
├── alembic.ini                 # Alembic migration config
├── app/
│   ├── celery/                 # Celery configuration & background tasks
│   ├── core/                   # Core settings (config, security, etc.)
│   ├── db/                     # Database models, sessions, and sync utilities
│   ├── dependencies/           # FastAPI dependencies (e.g., rate limiters)
│   ├── email/                  # Email service integration
│   ├── middleware/             # Custom middlewares (e.g., request logger)
│   ├── routers/                # Route handlers for all API modules
│   ├── schemas/                # Pydantic models for validation and response
│   ├── services/               # Business logic layer for each module
│   ├── static_media/           # User-uploaded media files
│   └── websocket/              # WebSocket endpoints and connection manager
├── migrations/                 # Alembic migration scripts
├── socialhub.db                # SQLite database (for local dev)
└── README.md
```

---

## 🔐 Features

✅ **User Authentication & Authorization** — JWT-based login/signup  
✅ **Post & Comment System** — User posts and comments  
✅ **Email Notifications** — Sent asynchronously using Celery + Redis  
✅ **WebSocket Notifications** — Real-time updates for events like comments/likes  
✅ **Rate Limiting** — Redis-backed request throttling  
✅ **Request Logging Middleware** — Track incoming requests for debugging  
✅ **Database Migrations** — Managed cleanly using Alembic  

---

## 🔄 Celery Integration

Celery is used to handle **background tasks** (like sending emails) asynchronously, improving API performance.  
Redis is used as the **message broker** for reliable queue management.


Run the Celery worker:

```bash
celery -A app.celery.celery_app.celery worker --loglevel=info
```

---

## 🧠 Database Migrations (Alembic)

Alembic is used to manage schema versions seamlessly.

```bash
# Create a new migration
alembic revision --autogenerate -m "Added new feature table"

# Apply migrations
alembic upgrade head

# Rollback to previous version
alembic downgrade -1
```

Migration scripts are stored in the `migrations/versions` folder.

---

## 💬 API Endpoints Summary

| Endpoint | Description |
|----------|-------------|
| `/auth` | Register, login, and refresh JWT tokens |
| `/users` | User profiles |
| `/posts` | Add, view posts |
| `/likes` | Add likes on posts |
| `/comments` | Add comments on posts |
| `/download_profile_report` | Export user activity reports |

---

## 🧪 Testing & API Docs

FastAPI provides an automatic interactive API documentation via Swagger UI.

- 👉 [http://localhost:8000/docs](http://localhost:8000/docs) — Swagger UI  
- 👉 [http://localhost:8000/redoc](http://localhost:8000/redoc) — ReDoc view  

You can also test endpoints using tools like **Postman** or **cURL**.

---

## 🏗️ Future Enhancements

- ✨ Docker Support — Full Docker Compose setup for API, Redis, and Celery  
- ✨ OAuth2 Login — Support Google/GitHub single sign-on  
- ✨ Redis Caching — Cache API responses and user sessions  
- ✨ Unit Testing Suite — Integrate pytest and coverage reports  
- ✨ CI/CD Pipeline — GitHub Actions for automated deployment  

---

## 💻 Author & License

**Author**: Yogesh Chaudhari  

