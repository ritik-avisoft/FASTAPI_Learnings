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
- Learned: raw SQL queries, `conn.commit()`, parameterized queries with `%s`

## Phase 3 — SQLAlchemy ORM (Current)
- Configured `database.py` with `create_engine`, `sessionmaker`, `declarative_base`
- Defined `Post` ORM model in `models.py` mapped to the `posts` table
- Auto-creates tables on startup with `models.Base.metadata.create_all(bind=engine)`
- Replaced all raw SQL with ORM calls: `db.query()`, `db.add()`, `db.commit()`, `db.refresh()`
- Learned: ORM, Dependency Injection with `Depends(get_db)`, `synchronize_session=False`

## Core Concepts (All Phases)
- **Decorators** — `@app.get()` registers a function as an API route
- **Pydantic** — validates request body, `model_dump()` converts to dict
- **Path Parameters** — `{id}` in URL, auto type-converted by FastAPI
- **Status Codes** — `201 Created`, `204 No Content`, `404 Not Found`
- **HTTPException** — raises an error response immediately
- **Dependency Injection** — `Depends(get_db)` auto-provides a DB session per request
- **Environment Variables** — credentials stored in `.env`, never hardcoded

---

## Progression Summary

| Phase | Storage       | Key Tech                        |
|-------|---------------|---------------------------------|
| 1     | Python List   | In-memory, no persistence       |
| 2     | PostgreSQL    | `psycopg2`, raw SQL             |
| 3     | PostgreSQL    | `SQLAlchemy` ORM, `models.py`   |

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
| Phase 1 | Phase 3 |
|---|---|
| Only `main.py` | `main.py` + `database.py` + `models.py` |
| No DB config | SQLAlchemy engine, session, `Base` |
| Hardcoded data | Credentials in `.env` via `python-dotenv` |

### Dependencies
| Phase 1 | Phase 2 | Phase 3 |
|---|---|---|
| `fastapi`, `uvicorn` | + `psycopg2-binary` | + `sqlalchemy`, `python-dotenv` |

---

## API Endpoints

| Method | Endpoint      | Description             |
|--------|---------------|-------------------------|
| GET    | `/`           | Welcome message         |
| POST   | `/login`      | User login              |
| GET    | `/posts`      | Get all posts           |
| POST   | `/posts`      | Create a new post       |
| GET    | `/posts/{id}` | Get a single post by ID |
| PUT    | `/posts/{id}` | Update a post by ID     |
| DELETE | `/posts/{id}` | Delete a post by ID     |

---

## Project Structure

```
FASTAPI/
├── app/
│   ├── __init__.py
│   ├── main.py        # Routes & app logic
│   ├── database.py    # SQLAlchemy engine & session setup
│   └── models.py      # ORM models
├── .env               # DB credentials (not committed)
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
pip install fastapi uvicorn psycopg2-binary sqlalchemy python-dotenv

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
