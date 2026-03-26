# FastAPI — Core Concepts & Learning Project

A hands-on project built while learning the **core concepts of FastAPI**, progressing from in-memory storage to a real PostgreSQL database with SQLAlchemy ORM, full JWT authentication, and voting system.
---

## Phase 1 — In-Memory CRUD (Starting Point)
- Simulated a database using a Python list `my_posts`
- Full CRUD using helper functions `find_post()` and `find_index_post()`
- Learned: FastAPI setup, decorators, Pydantic models, path params, status codes, HTTPException

## Phase 2 — PostgreSQL with psycopg2
- Connected to a real **PostgreSQL** database using `psycopg2`
- Used `RealDictCursor` to return rows as dictionaries
- Executed raw SQL: `SELECT`, `INSERT`, `UPDATE`, `DELETE` with `RETURNING *`
- Added a retry loop for DB connection on startup
- Learned: raw SQL queries, `conn.commit()`, parameterized queries with `%s`

## Phase 3 — SQLAlchemy ORM
- Configured `database.py` with `create_engine`, `sessionmaker`, `declarative_base`
- Defined `Post` ORM model in `models.py` mapped to the `posts` table
- Auto-creates tables on startup with `models.Base.metadata.create_all(bind=engine)`
- Replaced all raw SQL with ORM calls: `db.query()`, `db.add()`, `db.commit()`, `db.refresh()`
- Learned: ORM, Dependency Injection with `Depends(get_db)`, `synchronize_session=False`

## Phase 4 — Routers, Users & Password Hashing
- Split routes into `routers/post.py` and `routers/user.py` using `APIRouter`
- Registered routers in `main.py` with `app.include_router()`
- Added `User` ORM model with `email` (unique), `name`, `password`, `created_at`
- Added `UserCreate` and `UserResponse` Pydantic schemas with `EmailStr` validation
- Password hashing with `pwdlib` — plain text password never stored in DB
- Utility functions `Hash()` and `Verify()` in `utils/hash_password.py`
- Duplicate email check returns `409 Conflict` before attempting DB insert
- Learned: `APIRouter`, `include_router()`, password hashing, `EmailStr`, `409 Conflict`

## Phase 5 — JWT Authentication
- Added `routers/auth.py` with `POST /auth/login` endpoint using `OAuth2PasswordRequestForm`
- Implemented JWT token creation and verification in `oauth2.py` using `python-jose`
- `create_access_token()` encodes `user_id` with expiry into a signed JWT
- `verify_access_token()` decodes and validates the token, raises `401 Unauthorized` on failure
- `get_current_user()` dependency resolves the token to a live DB user — injected into protected routes
- All post routes (`GET`, `POST`, `PUT`, `DELETE`) are now protected with `Depends(oauth2.get_current_user)`
- `PUT` and `DELETE` enforce ownership — only the post owner can modify or delete (`403 Forbidden`)
- `Post` model has `owner_id` (FK → users) and `owner` relationship for nested response
- `Post` schema returns full `owner` object via `UserResponse`
- Added `Token` and `TokenData` Pydantic schemas for JWT response and payload
- `SECRET_KEY` and token config loaded from `.env` via `os.getenv()`
- Learned: JWT, `OAuth2PasswordBearer`, `OAuth2PasswordRequestForm`, ownership checks, `403 Forbidden`

## Phase 6 — Votes, Alembic & Query Params (Current)
- Added `Vote` ORM model with composite PK `(user_id, post_id)` — prevents duplicate votes at DB level
- Vote endpoint `POST /vote` — `dir=1` adds vote, `dir=0` removes it
- Posts now return vote counts via LEFT JOIN + `func.count()` + `GROUP BY`
- `GET /posts` supports `limit`, `skip`, `search` query params for pagination and filtering
- Set up **Alembic** for versioned DB migrations — 6 migration files with full upgrade/downgrade chain
- Switched from `os.getenv()` to `pydantic-settings` (`BaseSettings`) for typed, validated env config
- Added `CORSMiddleware` to allow browser frontends to call the API
- Learned: composite PK, LEFT JOIN aggregates, Alembic migrations, `pydantic-settings`, CORS

## Core Concepts (All Phases)
- **Decorators** — `@router.get()` registers a function as an API route
- **Pydantic** — validates request body, `model_dump()` converts to dict, `EmailStr` validates email format
- **Path Parameters** — `{id}` in URL, auto type-converted by FastAPI
- **Status Codes** — `201 Created`, `204 No Content`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `409 Conflict`
- **HTTPException** — raises an error response immediately
- **Dependency Injection** — `Depends(get_db)` auto-provides a DB session, `Depends(get_current_user)` protects routes
- **APIRouter** — splits routes into separate files, registered in `main.py`
- **Password Hashing** — `pwdlib` hashes passwords before storing in DB
- **JWT** — `python-jose` signs and verifies access tokens
- **Ownership** — routes check `post.owner_id == current_user.id` before mutating data
- **Environment Variables** — credentials and secrets stored in `.env`, loaded via `pydantic-settings`
- **Alembic** — versioned DB migrations with `upgrade()`/`downgrade()`, chained via `down_revision`
- **Votes** — composite PK `(user_id, post_id)` enforces one vote per user per post
- **LEFT JOIN + func.count()** — aggregate vote counts per post, includes posts with 0 votes
- **Query Params** — `limit`, `skip`, `search` declared in function signature, auto-parsed by FastAPI
- **CORS** — `CORSMiddleware` allows browser cross-origin requests

---

## Progression Summary

| Phase | Storage       | Key Tech                                                      |
|-------|---------------|---------------------------------------------------------------|
| 1     | Python List   | In-memory, no persistence                                     |
| 2     | PostgreSQL    | `psycopg2`, raw SQL                                           |
| 3     | PostgreSQL    | `SQLAlchemy` ORM, `models.py`                                 |
| 4     | PostgreSQL    | `APIRouter`, `User` model, `pwdlib` password hash             |
| 5     | PostgreSQL    | JWT auth, `oauth2.py`, protected routes, ownership checks     |
| 6     | PostgreSQL    | Votes, Alembic migrations, `pydantic-settings`, CORS          |

---

## How It Evolved — Phase by Phase

### Data Storage
| Phase 1 | Phase 2 | Phase 3 |
|---|---|---|
| Python list in memory | PostgreSQL via psycopg2 | PostgreSQL via SQLAlchemy ORM |
| Lost on restart | Persists | Persists |
| No setup | DB connection needed | DB + ORM models needed |

### Data Access (GET one post)
| Phase 1 | Phase 2 | Phase 3 |
|---|---|---|
| `find_post(id)` loop | `cursor.execute("SELECT * FROM posts WHERE id = %s")` | `db.query(models.Post).filter(models.Post.id == id).first()` |

### Data Access (CREATE post)
| Phase 1 | Phase 2 | Phase 3 |
|---|---|---|
| `my_posts.append(post_dict)` | `cursor.execute("INSERT INTO posts ... RETURNING *")` | `db.add(post)` → `db.commit()` → `db.refresh(post)` |

### Data Access (DELETE post)
| Phase 1 | Phase 2 | Phase 3 |
|---|---|---|
| `my_posts.pop(index)` | `cursor.execute("DELETE FROM posts WHERE id=%s RETURNING *")` | `post.delete(synchronize_session=False)` → `db.commit()` |

### Project Files
| Phase 1 | Phase 3 | Phase 4 | Phase 5 | Phase 6 |
|---|---|---|---|---|
| Only `main.py` | `main.py` + `database.py` + `models.py` | + `routers/` + `utils/` + `schemas.py` | + `oauth2.py` + `routers/auth.py` | + `routers/vote.py` + `alembic/` + `config.py` |
| No DB config | SQLAlchemy engine, session, `Base` | Routes split into `post.py` + `user.py` | JWT token logic, protected routes | Alembic migrations, vote system, CORS |

### Dependencies
| Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 |
|---|---|---|---|---|---|
| `fastapi`, `uvicorn` | + `psycopg2-binary` | + `sqlalchemy`, `python-dotenv` | + `pwdlib`, `email-validator` | + `python-jose[cryptography]` | + `alembic`, `pydantic-settings` |

---

## API Endpoints

### Authentication
| Method | Endpoint        | Description                        | Auth Required |
|--------|-----------------|------------------------------------|---------------|
| POST   | `/auth/login`   | Login and receive a JWT token      | No            |

### Posts
| Method | Endpoint       | Description             | Auth Required |
|--------|----------------|-------------------------|---------------|
| GET    | `/posts`       | Get all posts (supports `limit`, `skip`, `search`) | Yes |
| POST   | `/posts`       | Create a new post       | Yes           |
| GET    | `/posts/{id}`  | Get a single post by ID | Yes           |
| PUT    | `/posts/{id}`  | Update a post (owner only) | Yes        |
| DELETE | `/posts/{id}`  | Delete a post (owner only) | Yes        |

### Users
| Method | Endpoint               | Description          | Auth Required |
|--------|------------------------|----------------------|---------------|
| POST   | `/users/createusers`   | Register a new user  | No            |
| POST   | `/users/updateprofile` | Update user profile  | Yes           |
| GET    | `/users`               | Get all users        | No            |
| GET    | `/users/{id}`          | Get a user by ID     | No            |

### Votes
| Method | Endpoint  | Description                        | Auth Required |
|--------|-----------|------------------------------------|---------------|
| POST   | `/vote`   | Add (`dir=1`) or remove (`dir=0`) a vote | Yes      |

### Root
| Method | Endpoint | Description     |
|--------|----------|-----------------|
| GET    | `/`      | Welcome message |

---

## Project Structure

```
FASTAPI/
├── app/
│   ├── routers/
│   │   ├── post.py        # Post routes (all protected)
│   │   ├── user.py        # User routes
│   │   └── auth.py        # Login route, JWT token issuance
│   ├── utils/
│   │   └── hash_password.py  # Hash() and Verify() utilities
│   ├── __init__.py
│   ├── main.py            # App entry point, router registration
│   ├── database.py        # SQLAlchemy engine & session setup
│   ├── models.py          # ORM models (Post, User)
│   ├── schemas.py         # Pydantic schemas (Post, User, Token, TokenData)
│   ├── oauth2.py          # JWT creation, verification, get_current_user dependency
│   └── config.py          # pydantic-settings BaseSettings — typed env config
├── alembic/               # DB migration files (versioned schema changes)
│   └── versions/          # 6 migration files chained via down_revision
├── .env                   # DB credentials + SECRET_KEY (not committed)
├── .gitignore
└── README.md
```

---

## Environment Variables (`.env`)

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=<your_db_name>
DB_USER=<your_db_user>
DB_PASSWORD=<your_password>
SECRET_KEY=<your_secret_key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

> Generate a secure `SECRET_KEY` with: `openssl rand -hex 32`

---

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd FASTAPI
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install fastapi uvicorn psycopg2-binary sqlalchemy python-dotenv pwdlib email-validator "python-jose[cryptography]" alembic pydantic-settings
   ```

4. **Set up PostgreSQL database**
   - Create a new PostgreSQL database
   - Note your database credentials

5. **Configure environment variables**
   - Create a `.env` file in the root directory
   - Add your configuration (see Environment Variables section below)

6. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

7. **Start the server**
   ```bash
   uvicorn app.main:app --reload
   ```

8. **Access the API**
   - Swagger UI: `http://127.0.0.1:8000/docs`
   - ReDoc: `http://127.0.0.1:8000/redoc`

---

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic](https://docs.pydantic.dev/)
- [Uvicorn](https://www.uvicorn.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [psycopg2](https://www.psycopg.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [pwdlib](https://pypi.org/project/pwdlib/)
- [email-validator](https://pypi.org/project/email-validator/)
- [python-jose](https://pypi.org/project/python-jose/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)

---

## Features

✅ RESTful API with FastAPI  
✅ PostgreSQL database with SQLAlchemy ORM  
✅ JWT authentication & authorization  
✅ Password hashing with pwdlib  
✅ Database migrations with Alembic  
✅ Voting system with composite primary keys  
✅ Query parameters (pagination, search)  
✅ CORS enabled for frontend integration  
✅ Ownership-based access control  
✅ Email validation  
✅ Interactive API documentation (Swagger UI)

---

## Learning Outcomes

This project demonstrates:
- Building production-ready REST APIs
- Database design and ORM usage
- Authentication and authorization patterns
- API security best practices
- Database migrations and version control
- Dependency injection
- Request validation with Pydantic
- Error handling and HTTP status codes

---

## Contributing

This is a learning project, but suggestions and improvements are welcome!

---

## License

This project is open source and available for educational purposes.

---

## Acknowledgments

Built while following FastAPI best practices and learning modern Python web development.
