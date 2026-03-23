# FastAPI — Core Concepts & Learning Project

A hands-on project built while learning the **core concepts of FastAPI**, progressing from in-memory storage to a real PostgreSQL database with SQLAlchemy ORM.

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
- Learned: raw SQL queries, `conn.commit()`, parameterized queries with `%s`## Phase 3 — - Configured `database.py` with `create_engine`, `sessionmaker`, `declarative_base`
- Defined `Post` ORM model in `models.py` mapped to the `posts` table
- Auto-creates tables on startup with `models.Base.metadata.create_all(bind=engine)`
- Replaced all raw SQL with ORM calls: `db.query()`, `db.add()`, `db.commit()`, `db.refresh()`
- Learned: ORM, Dependency Injection with `Depends(get_db)`, `synchronize_session=False`

## Phase 4 — Routers, Users & Password Hashing (Current ✅)
- Split routes into `routers/post.py` and `routers/user.py` using `APIRouter`
- Registered routers in `main.py` with `app.include_router()`
- Added `User` ORM model with `email` (unique), `name`, `password`, `created_at`
- Added `UserCreate` and `UserResponse` Pydantic schemas with `EmailStr` validation
- Password hashing with `pwdlib` — plain text password never stored in DB
- Utility function `Hash()` in `utils/hash_password.py` keeps hashing logic separate
- Duplicate email check returns `409 Conflict` before attempting DB insert
- Learned: `APIRouter`, `include_router()`, password hashing, `EmailStr`, `409 Conflict`

## Core Concepts (All Phases)
- **Decorators** — `@router.get()` registers a function as an API route
- **Pydantic** — validates request body, `model_dump()` converts to dict, `EmailStr` validates email format
- **Path Parameters** — `{id}` in URL, auto type-converted by FastAPI
- **Status Codes** — `201 Created`, `204 No Content`, `404 Not Found`, `409 Conflict`
- **HTTPException** — raises an error response immediately
- **Dependency Injection** — `Depends(get_db)` auto-provides a DB session per request
- **APIRouter** — splits routes into separate files, registered in `main.py`
- **Password Hashing** — `pwdlib` hashes passwords before storing in DB
- **Environment Variables** — credentials stored in `.env`, never hardcoded

---

## Progression Summary

| Phase | Storage       | Key Tech                                          |
|-------|---------------|---------------------------------------------------|
| 1     | Python List   | In-memory, no persistence                         |
| 2     | PostgreSQL    | `psycopg2`, raw SQL                               |
| 3     | PostgreSQL    | `SQLAlchemy` ORM, `models.py`                     |
| 4     | PostgreSQL    | `APIRouter`, `User` model, `pwdlib` password hash |

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
| Phase 1 | Phase 3 | Phase 4 |
|---|---|---|
| Only `main.py` | `main.py` + `database.py` + `models.py` | + `routers/` + `utils/` + `schemas.py` |
| No DB config | SQLAlchemy engine, session, `Base` | Routes split into `post.py` + `user.py` |
| Hardcoded data | Credentials in `.env` via `python-dotenv` | Password hashing in `utils/hash_password.py` |

### Dependencies
| Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|---|---|---|---|
| `fastapi`, `uvicorn` | + `psycopg2-binary` | + `sqlalchemy`, `python-dotenv` | + `pwdlib`, `email-validator` |

---

## API Endpoints

### Posts
| Method | Endpoint       | Description             |
|--------|----------------|-------------------------|
| GET    | `/`            | Welcome message         |
| GET    | `/posts`       | Get all posts           |
| POST   | `/posts`       | Create a new post       |
| GET    | `/posts/{id}`  | Get a single post by ID |
| PUT    | `/posts/{id}`  | Update a post by ID     |
| DELETE | `/posts/{id}`  | Delete a post by ID     |

### Users
| Method | Endpoint          | Description          |
|--------|-------------------|----------------------|
| POST   | `/createusers`    | Register a new user  |
| GET    | `/users`          | Get all users        |
| GET    | `/users/{id}`     | Get a user by ID     |

---

## Project Structure

```
FASTAPI/
├── app/
│   ├── routers/
│   │   ├── post.py        # Post routes
│   │   └── user.py        # User routes
│   ├── utils/
│   │   └── hash_password.py  # Password hashing utility
│   ├── __init__.py
│   ├── main.py            # App entry point, router registration
│   ├── database.py        # SQLAlchemy engine & session setup
│   ├── models.py          # ORM models (Post, User)
│   └── schemas.py         # Pydantic schemas
├── .env                   # DB credentials (not committed)
├── .gitignore
└── README.md
```

---

## Environment Variables (`.env`)

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_password
```

---

## How to Run

```bash
# Install dependencies
pip install fastapi uvicorn psycopg2-binary sqlalchemy python-dotenv pwdlib email-validator

# Start the server
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive **Swagger UI**.

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
