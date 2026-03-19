# FastAPI — Core Concepts & Learning Project

A hands-on project built while learning the **core concepts of FastAPI**, progressing from in-memory storage to a real PostgreSQL database with SQLAlchemy ORM.

---

## What I Learned

### 1. FastAPI App Setup
- Creating a FastAPI instance with `FastAPI()`
- Running the app using **Uvicorn** as the ASGI server

### 2. Path Operations (Routes)
- Defining routes using `@app.get()`, `@app.post()`, `@app.put()`, `@app.delete()`
- Understanding HTTP methods and when to use each

### 3. Request Body & Pydantic Models
- Using `pydantic.BaseModel` to define and validate request schemas
- Auto-parsing incoming JSON into typed Python models

### 4. Path Parameters & Type Validation
- Extracting dynamic values from URLs using `{id}` syntax
- FastAPI auto-validates and converts types (e.g., `id: int`)

### 5. Response & Status Codes
- Setting status codes via `status`, `Response`, and decorator-level `status_code`
- e.g., `201 Created`, `204 No Content`, `404 Not Found`

### 6. HTTPException & Error Handling
- Raising `HTTPException` with status codes and detail messages
- Handling **404 Not Found** when a resource doesn't exist

### 7. In-Memory CRUD (Phase 1)
- Simulated a database using a Python list (`my_posts`)
- Implemented full CRUD with helper functions `find_post()` and `find_index_post()`

### 8. PostgreSQL with psycopg2 (Phase 2)
- Connected to a real **PostgreSQL** database using `psycopg2`
- Used `RealDictCursor` to return rows as dictionaries
- Executed raw SQL queries: `SELECT`, `INSERT`, `UPDATE`, `DELETE`
- Used `RETURNING *` to get the affected row back
- Added a retry loop for database connection on startup

### 9. SQLAlchemy ORM Setup (Phase 3)
- Configured `database.py` with `create_engine`, `sessionmaker`, and `declarative_base`
- Defined a `Post` ORM model in `models.py` mapped to the `posts` table
- Used `models.Base.metadata.create_all(bind=engine)` to auto-create tables
- Set up a `get_db()` dependency function for session management

### 10. Environment Variables
- Used `python-dotenv` to load secrets from a `.env` file
- Stored DB credentials (`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`) securely
- Used `urllib.parse.quote_plus` to safely encode the password in the DB URL

---

## Progression Summary

| Phase | Storage       | Key Tech                        |
|-------|---------------|---------------------------------|
| 1     | Python List   | In-memory, no persistence       |
| 2     | PostgreSQL    | `psycopg2`, raw SQL             |
| 3     | PostgreSQL    | `SQLAlchemy` ORM, `models.py`   |

---

## Before vs Now — What Changed

### Storage
| Before (Phase 1) | Now (Phase 2 & 3) |
|---|---|
| Python list `my_posts` in memory | Real PostgreSQL database |
| Data lost on every restart | Data persists across restarts |
| No setup needed | Requires DB connection + credentials |

### Data Access
| Before | Now |
|---|---|
| `find_post(id)` — manual loop over list | `cursor.execute("SELECT * FROM posts WHERE id = %s")` |
| `my_posts.append(post_dict)` | `INSERT INTO posts ... RETURNING *` |
| `my_posts.pop(index)` | `DELETE FROM posts WHERE id = %s RETURNING *` |
| `my_posts[index] = post_dict` | `UPDATE posts SET ... WHERE id = %s RETURNING *` |

### Project Files
| Before | Now |
|---|---|
| Only `main.py` | Added `database.py` + `models.py` |
| No DB config | SQLAlchemy engine, session, `Base` in `database.py` |
| No ORM models | `Post` ORM model in `models.py` maps to `posts` table |
| Hardcoded data | Credentials loaded from `.env` via `python-dotenv` |

### Dependencies
| Before | Now |
|---|---|
| `fastapi`, `uvicorn` | + `psycopg2-binary`, `sqlalchemy`, `python-dotenv` |

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
